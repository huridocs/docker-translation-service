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
from configuration import cejil_1_page, cejil_2_page, cejil_3_page


# MODELS = ["llama3", "tinyllama", "GLM-4"]
LANGUAGES_PAIRS = ["en-ru"]

# MODELS = ["llama3"]
MODELS = ["aya"]
# LANGUAGES_PAIRS = ["en-fr"]


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
    for i, row in tqdm(df.iterrows()):
        texts_translations.append((row['translation'][lang1], row['translation'][lang2]))
        if limit and i == limit:
            break

    return texts_translations


def get_bleu_scores(correct_text: str, prediction: str):
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


def benchmark():
    for model in MODELS:
        for pair in LANGUAGES_PAIRS:
            average_performance = 0
            print(f"Model: {model}, Pair: {pair}")
            samples = read_samples(pair)
            total_time = 0
            for from_text, human_translation in tqdm(samples):
                language_from = LANGUAGES[LANGUAGES_SHORT.index(pair.split('-')[0])]
                language_to = LANGUAGES[LANGUAGES_SHORT.index(pair.split('-')[1])]
                start_time = time()
                prediction = get_prediction(model, from_text, language_from, language_to)
                total_time += time() - start_time
                average_performance += get_bleu_scores(human_translation, prediction)

            print(f"Average performance: {100 * average_performance/len(samples)}")
            print(f"Total time: {total_time} || Average time: {total_time/len(samples)}")


def predict_long_text():
    translation_task = TranslationTask(text=cejil_3_page, language_from="", language_to="English")
    content = get_content(translation_task)
    start_time = time()
    response = client.chat(model="aya:35b", messages=[{"role": "user", "content": content}])
    response_time = time() - start_time
    print(response["message"]["content"])
    print(f"\nResponse time: {round(response_time)} seconds.")


if __name__ == '__main__':
    # download_data()
    # read_samples("en-es")
    # get_bleu_scores()
    # benchmark()
    predict_long_text()
