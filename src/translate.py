from time import time

from ollama import Client
from data_model.Translation import Translation
from data_model.TranslationTask import TranslationTask
from configuration import MODEL, TRANSLATIONS_PORT

client = Client(host=f"http://localhost:{TRANSLATIONS_PORT}")


def get_content(translation_task: TranslationTask):
    context_for_source_language = ""
    if translation_task.language_from:
        context_for_source_language += f"from {translation_task.language_from}"
    content = (
        f"Translate the below text {context_for_source_language} to {translation_task.language_to}, "
        f"keep the layout, do not skip any text, do not output anything else besides translation:"
    )
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
