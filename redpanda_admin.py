from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import os
from dotenv import load_dotenv

load_dotenv()

REDPANDA_USER = os.getenv('REDPANDA_USER')
REDPANDA_PWD = os.getenv('REDPANDA_PWD')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
REDPANDA_SERVER = os.getenv('REDPANDA_SERVER')

admin = KafkaAdminClient(
  bootstrap_servers=REDPANDA_SERVER,
  security_protocol="SASL_SSL",
  sasl_mechanism="SCRAM-SHA-256",
  sasl_plain_username=REDPANDA_USER,
  sasl_plain_password=REDPANDA_PWD,
)

try:
  topic = NewTopic(name=KAFKA_TOPIC, num_partitions=1, replication_factor=-1, replica_assignments=[])
  admin.create_topics(new_topics=[topic])
  print("Created topic")
except TopicAlreadyExistsError as e:
  print("Topic already exists")
finally:
  admin.close()