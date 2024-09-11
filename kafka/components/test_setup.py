import os
import logging

from kafka import KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
from kafka.errors import TopicAlreadyExistsError


logger = logging.getLogger()


def startup_test_topic():
    client = KafkaAdminClient(bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"])
    topics = [
        NewTopic(
            name=os.environ["KAFKA_TOPIC"],
        ),
    ]
    for topic in topics:
        try:
            client.create_topics([topic])
        except TopicAlreadyExistsError:
            logger.warning("Topic already exists")

    cfg_resource_update = ConfigResource(
        ConfigResourceType.TOPIC,
        configs={'retention.ms': "500000"}
    )

    client.alter_configs([cfg_resource_update])

    client.close()


if __name__ == "__main__":
    startup_test_topic()