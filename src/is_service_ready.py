from time import sleep

from rsmq import cmd

from test_end_to_end import QUEUE


def is_service_ready():
    for i in range(10):
        try:
            QUEUE.sendMessage().message('{"message_to_ignore":"is_service_ready?"}').execute()
        except cmd.exceptions.QueueDoesNotExist:
            print("Waiting for service to be ready...")
            sleep(5)

        print("Service is ready")
        break


if __name__ == "__main__":
    is_service_ready()
