import json
import logging
import os

from dotenv import load_dotenv
from kafka import TopicPartition, OffsetAndMetadata
from kafka.consumer import KafkaConsumer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

load_dotenv(verbose=True)


def main():
    logger.info(f"""
    Started Python Consumer
    for topic {os.environ['KAFKA_TOPIC']}
    """)

    consumer = KafkaConsumer(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        group_id="test_group",
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False,
        auto_offset_reset='earliest',
    )

    consumer.subscribe([os.environ['KAFKA_TOPIC']])
    for record in consumer:
        logger.info(f"""
          Consumed person {record.value}
          with key '{record.key}'
          from partition {record.partition}
          at offset {record.offset}
        """)

        topic_partition = TopicPartition(record.topic, record.partition)
        offset = OffsetAndMetadata(record.offset + 1, record.timestamp)
        consumer.commit({
          topic_partition: offset
        })


if __name__ == '__main__':
  main()

