import json

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, Producer

TOPIC = "warehouse"


class TopicCreator:
    def __init__(self, topic: str = TOPIC):
        self._admin_client = AdminClient({'bootstrap.servers': 'localhost:19092'})
        self.create_topic(topic)

    def create_topic(self, topic=TOPIC):
        kafka_topic = NewTopic(topic, num_partitions=3, replication_factor=1)
        self._admin_client.create_topics([kafka_topic])


class ConsumerHandler:
    def __init__(self, host: str, client_id: str):
        self.consumer = Consumer({'bootstrap.servers': host,
                                  'group.id': 'python-consumers',
                                  'client.id': client_id,
                                  'auto.offset.reset': 'latest'})
        self.consumer.subscribe([TOPIC])

    def receive_data(self) -> int:
        # This next make receive only 1 message each time and return
        return json.loads(next(self.consumer.poll(2).decode('utf-8'))['id'])


class ProducerHandler:

    def __init__(self, host: str):
        self.producer = Producer({'bootstrap.servers': host})

    def send(self, send_msg: dict):
        self.producer.produce(TOPIC, json.dumps(send_msg).encode('utf-8'),
                              callback=self.callback_handler)
        self.producer.flush()

    @staticmethod
    def callback_handler(err, msg):
        if err:
            print(err)
        print(f"##########\nMessage delivered to topic: {msg.topic()}\nOn partition: {msg.partition()}\n##########")


if __name__ == '__main__':
    producer = ProducerHandler("localhost:19092")
    producer.send({"id": 12})
