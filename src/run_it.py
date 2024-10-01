from time import time
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage
from start_queue_processor import process


def run_it():
    start = time()
    print("start")
    text = "While there exists a rich body of work on video prediction using generative models, "
    text += "the design of methods for evaluating the quality of the videos has received much less attention."
    translation_task_message = TranslationTaskMessage(key="key", text=text, language_from="English", languages_to=["French"])
    results = process(translation_task_message.model_dump())
    translation_response_message = TranslationResponseMessage(**results)
    print(translation_response_message.model_dump())
    print("time", round(time() - start, 2), "s")


if __name__ == "__main__":
    run_it()
