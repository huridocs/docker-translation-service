import requests

from data_model.TranslationTask import TranslationTask
from translate import get_content


def get_glm_prediction(from_text, language_from, language_to):
    prompt = get_content(TranslationTask(text=from_text, language_from=language_from, language_to=language_to))

    headers = {
        "Content-Type": "application/json",
    }

    json_data = {
        "prompt": prompt,
        "n_predict": 120,
    }

    response = requests.post("http://localhost:8080/completion", headers=headers, json=json_data)
    return response.json()["content"]
