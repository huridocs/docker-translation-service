from time import sleep

import redis
from pydantic_core._pydantic_core import ValidationError
from rsmq.consumer import RedisSMQConsumer
from rsmq import RedisSMQ, cmd

from configuration import TASK_QUEUE_NAME, RESULTS_QUEUE_NAME, service_logger
from data_model.TranslationResponseMessage import TranslationResponseMessage
from data_model.TranslationTaskMessage import TranslationTaskMessage
from translate import get_translation


class QueueProcessor:
    def __init__(self):
        self.task_queue = RedisSMQ(
            host="127.0.0.1",
            port=6379,
            qname=TASK_QUEUE_NAME,
        )

        self.results_queue = RedisSMQ(
            host="127.0.0.1",
            port=6379,
            qname=RESULTS_QUEUE_NAME,
        )

    def process(self, id, message, rc, ts):
        try:
            task_message = TranslationTaskMessage(**message)
            service_logger.info(f"New task {task_message.model_dump()}")
        except ValidationError:
            service_logger.error(f"Not a valid Redis message: {message}")
            return True

        translations = [get_translation(translation_task) for translation_task in task_message.get_tasks()]

        response = TranslationResponseMessage(
            **task_message.dict(),
            translations=translations,
        )

        self.results_queue.sendMessage(delay=5).message(response.dict()).execute()
        return True

    def subscribe_to_tasks_queue(self):
        print("Translation queue processor started")
        while True:
            try:
                self.task_queue.getQueueAttributes().exec_command()
                self.results_queue.getQueueAttributes().exec_command()

                redis_smq_consumer = RedisSMQConsumer(
                    qname=TASK_QUEUE_NAME,
                    processor=self.process,
                    host="127.0.0.1",
                    port=6379,
                )
                redis_smq_consumer.run()
            except redis.exceptions.ConnectionError:
                sleep(20)
            except cmd.exceptions.QueueDoesNotExist:
                self.task_queue.createQueue().exceptions(False).execute()
                self.results_queue.createQueue().exceptions(False).execute()


if __name__ == "__main__":
    queue_processor = QueueProcessor()
    queue_processor.subscribe_to_tasks_queue()
