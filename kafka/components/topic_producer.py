from kafka import KafkaAdminClient

if __name__ == "__main__":
    admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])
    topics = admin_client.list_topics()
    print(topics)