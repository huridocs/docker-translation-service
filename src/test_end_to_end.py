import json
import time
from unittest import TestCase

from rsmq import RedisSMQ

from data_model.Translation import Translation
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"

QUEUE = RedisSMQ(
    host=REDIS_HOST,
    port=REDIS_PORT,
    qname="translation_tasks",
    quiet=False,
)


class TestEndToEnd(TestCase):
    def test_redis_message_to_ignore(self):
        QUEUE.sendMessage().message('{"message_to_ignore":"to_be_written_in_log_file"}').execute()

    def test_translations(self):
        task = TranslationTaskMessage(namespace="namespace",
                                      key=["key", "1"],
                                      text="Hola",
                                      language_from="es",
                                      languages_to=["en", "fr"])

        QUEUE.sendMessage(delay=0).message(task.model_dump_json()).execute()

        results_message = self.get_results_message()

        self.assertEqual("namespace", results_message.namespace)
        self.assertEqual(["key", "1"], results_message.key)
        self.assertEqual("Hola", results_message.text)
        self.assertEqual("es", results_message.language_from)
        self.assertEqual(["en", "fr"], results_message.languages_to)
        self.assertEqual(2, len(results_message.translations))

        en_translation = [translation for translation in results_message.translations if translation.language == "en"][0]
        self.assertEqual(True, en_translation.success)
        self.assertEqual("", en_translation.error_message)
        self.assertNotEqual("", en_translation.text)

        fr_translation = [translation for translation in results_message.translations if translation.language == "fr"][0]
        self.assertEqual(True, fr_translation.success)
        self.assertEqual("", fr_translation.error_message)
        self.assertNotEqual("", fr_translation.text)

    @staticmethod
    def get_results_message() -> TranslationResponseMessage:
        for i in range(20):
            time.sleep(3)
            queue = RedisSMQ(
                host=REDIS_HOST,
                port=REDIS_PORT,
                qname="translation_results",
                quiet=False,
            )
            message = queue.receiveMessage().exceptions(False).execute()
            if message:
                queue.deleteMessage(id=message["id"]).execute()
                return TranslationResponseMessage(**json.loads(message["message"]))
