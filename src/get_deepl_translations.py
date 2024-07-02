import json
from os import listdir
from os.path import join
from pathlib import Path

import deepl
from tqdm import tqdm

from benchmark_models import read_samples, get_bleu_score
from configuration import ROOT_PATH

# from data.deepl_api_key import DEEPL_API

deepl_languages = ["ar-en", "en-fr", "en-ru"]


def get_deepl_translations(language: str):
    samples = read_samples(language)
    translations = list()

    for i, (text_from, _) in tqdm(enumerate(samples)):
        batch = i // 50
        print("batch", batch, "...")
        path = Path(join(ROOT_PATH, "deepl_results", language, str(batch) + ".json"))

        if path.exists():
            print("skipping batch", batch, "...")
            continue

        translator = deepl.Translator(DEEPL_API)

        source_lang = language.split("-")[0]

        target_lang = language.split("-")[1]
        target_lang = target_lang if target_lang != "en" else "en-US"

        result = translator.translate_text(text_from, source_lang=source_lang, target_lang=target_lang)
        translations.append(result.text)

        if (i + 1) % 50 == 0:
            path.write_text(json.dumps(translations, indent=4))
            translations = list()


def get_deepl_bleu_score(language: str):
    samples = read_samples(language)
    samples = samples[:100]

    predictions = list()
    path = join(ROOT_PATH, "deepl_results", language)
    for file in sorted(listdir(path), key=lambda x: int(x.split(".")[0])):
        predictions += json.loads(Path(join(path, file)).read_text())

    print(len(predictions))

    average_performance = 0
    for i, (text_from, text_to) in tqdm(enumerate(samples)):
        prediction = predictions[i]
        average_performance += get_bleu_score(text_to, prediction)

    print(f"Average performance: {100 * average_performance / len(samples)}")


if __name__ == "__main__":
    # get_deepl_translations("en-fr")
    get_deepl_bleu_score("ar-en")
    get_deepl_bleu_score("en-fr")
    get_deepl_bleu_score("en-ru")
