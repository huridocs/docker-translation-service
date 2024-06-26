from time import time

from ollama import Client
from data_model.Translation import Translation
from data_model.TranslationTask import TranslationTask
from configuration import MODEL, TRANSLATIONS_PORT

client = Client(host=f"http://localhost:{TRANSLATIONS_PORT}")


def get_content(translation_task: TranslationTask):
    # context_for_source_language = ""
    # if translation_task.language_from:
    #     context_for_source_language += f"from {translation_task.language_from}"
    content = f"""Please translate the following text into {translation_task.language_to}. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.

Here is the text to be translated:
"""
    content += "\n\n" + translation_task.text
    return content


def get_translations(translation_task: TranslationTask) -> Translation:
    content = get_content(translation_task)

    response = client.chat(model=MODEL, messages=[{"role": "user", "content": content}])
    return response["message"]["content"]


if __name__ == "__main__":
    start = time()
    print("start")

    text = (
        "While there exists a rich body of work on video prediction using generative models, "
        "the design of methods for evaluating the quality of the videos has received much less attention."
    )
    language_from = "English"
    language_to = "Turkish"
    translation_task = TranslationTask(text=text, language_from=language_from, language_to=language_to)
    translation = get_translations(translation_task)
    print(translation)
    print("time", round(time() - start, 2), "s")
