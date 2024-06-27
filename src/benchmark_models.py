import json
import os
from pathlib import Path
from time import sleep, time

import pandas as pd
from shutil import rmtree
from os.path import join

from tqdm import tqdm
from huggingface_hub import hf_hub_download

from data_model.TranslationTask import TranslationTask
from src.configuration import ROOT_PATH, LANGUAGES_SHORT, LANGUAGES
from fast_bleu import BLEU
from translate import get_content, client
from configuration import cejil_3_page


# MODELS = ["llama3", "tinyllama", "GLM-4"]
LANGUAGES_PAIRS = ["en-ru"]

MODELS = ["aya:35b"]


def download_data():
    repo_id = "Helsinki-NLP/opus-100"
    train_file_name = "test-00000-of-00001.parquet"
    for pair in LANGUAGES_PAIRS:
        file_name = join(pair, train_file_name)
        hf_hub_download(repo_id=repo_id, filename=file_name, local_dir=join(f"{ROOT_PATH}/data"), repo_type="dataset")
    rmtree(join(ROOT_PATH, "data", ".huggingface"))


def read_samples(language_pair: str, limit: int = 0) -> list[tuple[str, str]]:
    df = pd.read_parquet(join(ROOT_PATH, "data", language_pair), engine='pyarrow')
    lang1, lang2 = df.iloc[0]['translation'].keys()
    texts_translations = list()
    for i, row in df.iterrows():
        texts_translations.append((row['translation'][lang1], row['translation'][lang2]))
        if limit and i == limit:
            break

    return texts_translations


def get_bleu_score(correct_text: str, prediction: str):
    list_of_references = [correct_text.split()]
    hypotheses = [prediction.split()]
    weights = {'bigram': (1/2., 1/2.), 'trigram': (1/3., 1/3., 1/3.)}
    bleu = BLEU(list_of_references, weights)
    average = (bleu.get_score(hypotheses)['bigram'][0] + bleu.get_score(hypotheses)['trigram'][0]) / 2.0
    return average


def get_prediction(model: str, text: str, language_from: str,  language_to: str):
    translation_task = TranslationTask(text=text, language_from=language_from, language_to=language_to)
    content = get_content(translation_task)
    response = client.chat(model=model, messages=[{"role": "user", "content": content}])
    return response["message"]["content"]


def benchmark(model: str, language_pair: str):
    root_path = Path(join(ROOT_PATH, "data", "predictions", model, language_pair))

    if not root_path.exists():
        os.makedirs(root_path)

    print(f"Model: {model}, Pair: {language_pair}")
    samples = read_samples(language_pair)
    translations = list()
    for i, (from_text, human_translation) in tqdm(enumerate(samples)):
        batch = i // 50
        path = Path(join(root_path, str(batch) + ".json"))
        if path.exists():
            print('skipping batch', batch, '...')
            continue

        language_from = language_pair.split('-')[0]
        language_to = language_pair.split('-')[1]

        prediction = get_prediction(model, from_text, language_from, language_to)
        translations.append(prediction)

        if (i + 1) % 50 == 0:
            path.write_text(json.dumps(translations, indent=4))
            translations = list()

    get_performance(samples, root_path)


def get_performance(samples: list[tuple[str, str]], path: Path):
    predictions = list()
    for file in sorted(os.listdir(path), key=lambda x: int(x.split('.')[0])):
        predictions += json.loads(Path(join(path, file)).read_text())
    average_performance = 0
    for i, (text_from, text_to) in tqdm(enumerate(samples)):
        prediction = predictions[i]
        average_performance += get_bleu_score(text_to, prediction)

    print(f"Average performance: {100 * average_performance / len(samples)}")


def predict_long_text():
    translation_task = TranslationTask(text=cejil_3_page, language_from="", language_to="English")
    content = get_content(translation_task)
    start_time = time()
    response = client.chat(model="aya:35b", messages=[{"role": "user", "content": content}])
    response_time = time() - start_time
    print(response["message"]["content"])
    print(f"\nResponse time: {round(response_time)} seconds.")


def get_characters_to_translate():
    size = 0
    for language in ["ar-en", "en-fr", "en-ru"]:
        samples = read_samples(language)

        for text, _ in samples:
            size += len(text)

    print(size)


if __name__ == '__main__':
    # download_data()
    benchmark("aya:35b", "en-ru")
    # predict_long_text()
    # get_characters_to_translate()
