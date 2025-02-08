import logging
import json
from confluent_kafka import Consumer, KafkaException, KafkaError

logging.basicConfig(level=logging.INFO)

KAFKA_SERVER = 'localhost:9092'
KAFKA_TOPIC = 'testing_forecast'

conf = {
    'bootstrap.servers': KAFKA_SERVER,
    'group.id': 'reader',
    'enable.auto.offset.store': False, # Must me set to False in order to use store_offset()
    # 'auto.offset.reset': 'latest',
}

def read_from_kafka():
    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC])
    
    try:
        while True:
            msg = consumer.poll(1)
            
            if msg is None:
                logging.info('Waiting for messages...')
                continue  # Skip to the next poll
            
            if msg.error() is not None:
                logging.error(f"Kafka error: {msg.error()}")
                continue

            key = msg.key().decode('utf8') if msg.key() is not None else None
            value = json.loads(msg.value())
            offset = msg.offset()
            
            print(f'Offset: {offset}, Key: {key}, Value: {value}')
            consumer.store_offsets(msg) # Store the last offset consumed
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        consumer.close()

if __name__ == '__main__':
    try:
        read_from_kafka()
    except KeyboardInterrupt: 
        pass
