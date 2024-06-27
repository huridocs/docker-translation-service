from ollama import Client
from data_model.Translation import Translation
from data_model.TranslationTask import TranslationTask
from configuration import MODEL, TRANSLATIONS_PORT

client = Client(host=f"http://localhost:{TRANSLATIONS_PORT}")


def get_content(translation_task: TranslationTask):
    content = f"""Please translate the following text into {translation_task.language_to}. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.

Here is the text to be translated:
"""
    content += "\n\n" + translation_task.text
    return content


def get_translation(translation_task: TranslationTask) -> Translation:
    translation_task = TranslationTask(text="hola", language_from="es", language_to="fr")
    content = get_content(translation_task)
    response = client.chat(model=MODEL, messages=[{"role": "user", "content": content}])
    return Translation(
        text=response["message"]["content"],
        language=translation_task.language_to,
        success=True,
        error_message="",
    )
