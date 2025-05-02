from time import time
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage
from start_queue_processor import process


def run_it():
    start = time()
    print("start")
    text = "El juez ordena arresto domiciliar, ligarlo a proceso y una caución económica de Q10,000."
    translation_task_message = TranslationTaskMessage(key="key", text=text, language_from="Spanish", languages_to=["English"])
    results = process(translation_task_message.model_dump())
    translation_response_message = TranslationResponseMessage(**results)
    print(translation_response_message.model_dump())
    print("time", round(time() - start, 2), "s")


if __name__ == "__main__":
    run_it()
