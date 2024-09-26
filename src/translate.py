from ml_cloud_connector.MlCloudConnector import MlCloudConnector
from ollama import Client

from data_model.Translation import Translation
from data_model.TranslationTask import TranslationTask
from configuration import MODEL, LANGUAGES_SHORT, LANGUAGES, service_logger, TRANSLATIONS_PORT


def get_content(translation_task: TranslationTask):
    language_to_name = "English"
    languages_to = [x for x in LANGUAGES_SHORT if translation_task.language_to.lower()[:2] == x]

    if languages_to:
        language_to_name = LANGUAGES[LANGUAGES_SHORT.index(languages_to[0])]

    content = f"""Please translate the following text into {language_to_name}. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.

Here is the text to be translated:
"""
    content += "\n\n" + translation_task.text
    return content


def get_translation(translation_task: TranslationTask) -> Translation:
    ip_address = MlCloudConnector("translation").get_ip()
    client = Client(host=f"http://{ip_address}:{TRANSLATIONS_PORT}")

    service_logger.info(f"Using translation model {MODEL} on ip {ip_address}")
    content = get_content(translation_task)
    models_list = client.list()
    if "models" not in models_list or MODEL not in [model["model"] for model in models_list["models"]]:
        client.pull(model=MODEL)

    response = client.chat(model=MODEL, messages=[{"role": "user", "content": content}])

    return Translation(
        text=response["message"]["content"],
        language=translation_task.language_to,
        success=True,
        error_message="",
    )
