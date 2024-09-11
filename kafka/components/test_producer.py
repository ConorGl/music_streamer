import os
import logging
import random
import uuid
import json

from datetime import datetime
from time import sleep
from typing import Dict

from dotenv import load_dotenv
from kafka.producer import KafkaProducer


events_list = ['dummy_event', 'foo_event', 'bar_event']
page_list = ['new song','repeat song','bad song']

logger = logging.getLogger()
load_dotenv(verbose=True)


def make_producer():
    return KafkaProducer(
        bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

def generate_data():
    return {
        'user_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': random.choice(events_list),
        'details': {
                'page': random.choice(page_list),
                'duration': random.randint(1, 180)
            }
    }

class SuccessHandler:
    def __init__(self, message: Dict):
        self.message = message

    def __call__(self, rec_metadata):
        logger.info(f"Successfully Produced message {self.message} "
                    f"to topic {rec_metadata.topic}"
                    f"to partition {rec_metadata.partition}"
                    f"at offset {rec_metadata.offset}"
                    )


class ErrorHandler:
    def __init__(self, message: Dict):
        self.message = message

    def __call__(self, ex):
        logger.error(f"Failed producing message", exc_info=ex)

def main():
    producer = make_producer()
    try:
        while True:
            # Generate message
            message = generate_data()

            # Send the message to the Producer
            future = producer.send(os.environ["KAFKA_TOPIC"], message).add_callback(SuccessHandler(message)).add_errback(ErrorHandler(message))

            # Get the status to make events 'Synchronous'
            result = future.get(timeout=20)

            print(f"Sent message: {message}")
            print(f"Topic: {result.topic}")
            print(f"Partition: {result.partition}")
            print(f"Offset: {result.offset}")
            print("--------------------")

            sleep(1)
    except KeyboardInterrupt:
        print("Stopping test...")


if __name__ == "__main__":
    main()
