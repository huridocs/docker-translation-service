import pandas as pd
from shutil import rmtree
from os.path import join
from huggingface_hub import hf_hub_download

from data_model.TranslationTask import TranslationTask
from src.configuration import ROOT_PATH
from fast_bleu import BLEU

from translate import get_content, client

# MODELS = ["llama3", "tinyllama", "GLM-4"]
# LANGUAGES_PAIRS = ["ar-en", "en-es", "en-fr", "en-ru"]

MODELS = ["tinyllama"]
LANGUAGES_PAIRS = ["ar-en"]


def download_data():
    repo_id = "Helsinki-NLP/opus-100"
    train_file_name = "test-00000-of-00001.parquet"
    for pair in LANGUAGES_PAIRS:
        file_name = join(pair, train_file_name)
        hf_hub_download(repo_id=repo_id, filename=file_name, local_dir=join(f"{ROOT_PATH}/data"), repo_type="dataset")
    rmtree(join(ROOT_PATH, "data", ".huggingface"))


def read_samples(language_pair: str):
    df = pd.read_parquet(join(ROOT_PATH, "data", language_pair), engine='pyarrow')
    lang1, lang2 = df.iloc[0]['translation'].keys()
    for i, row in df.iterrows():
        yield row['translation'][lang1], row['translation'][lang2]


def get_bleu_scores(correct_text: str, prediction: str):
    list_of_references = [correct_text.split()]
    hypotheses = [prediction.split()]
    weights = {'bigram': (1/2., 1/2.), 'trigram': (1/3., 1/3., 1/3.)}
    bleu = BLEU(list_of_references, weights)
    average = (bleu.get_score(hypotheses)['bigram'][0] + bleu.get_score(hypotheses)['trigram'][0]) / 2.0
    return average


def get_prediction(model:str, text: str, language_from: str,  language_to: str):
    translation_task = TranslationTask(text=text, language_from=language_from, language_to=language_to)
    content = get_content(translation_task)

    response = client.chat(model=model, messages=[{"role": "user", "content": content}])
    return response["message"]["content"]


def benchmark():
    for model in MODELS:
        for pair in LANGUAGES_PAIRS:
            average_performance = 0
            samples = 0
            print(f"Model: {model}, Pair: {pair}")
            for correct_text, prediction in read_samples(pair):
                language_from = pair.split('-')[0]
                language_to = pair.split('-')[1]
                prediction = get_prediction(model, correct_text, language_from, language_to)
                average_performance += get_bleu_scores(correct_text, prediction)
                samples += 1

            print(f"Average performance: {100 * average_performance/samples}")


if __name__ == '__main__':
    # download_data()
    # read_samples("en-es")
    # get_bleu_scores()
    benchmark()
