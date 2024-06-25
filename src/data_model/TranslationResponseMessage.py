from src.data_model.Translation import Translation
from src.data_model.TranslationTaskMessage import TranslationTaskMessage


class TranslationResponseMessage(TranslationTaskMessage):
    translations: list[Translation]
