from time import time

from data_model.TranslationTask import TranslationTask
from translate import get_translation

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
    translation = get_translation(translation_task)
    print(translation)
    print(type(translation))
    print("time", round(time() - start, 2), "s")