import requests
import logging
import json
import subprocess
import os
from dotenv import load_dotenv
from confluent_kafka import Producer, KafkaException

load_dotenv()

KAFKA_SERVER = os.getenv('KAFKA_SERVER')
REDPANDA_USER = os.getenv('REDPANDA_USER')
REDPANDA_PWD = os.getenv('REDPANDA_PWD')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

conf = {
    'bootstrap.servers': KAFKA_SERVER,
    'client.id': 'weather-producer',
    'session.timeout.ms': 6000,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': REDPANDA_USER,
    'sasl.password': REDPANDA_PWD,
}

API_URL = 'https://api.open-meteo.com/v1/forecast'
params = {
    "latitude": -23.54,
    "longitude": -46.63,
    "current": "temperature_2m",
}

logging.basicConfig(level=logging.INFO)

def fetch_weather_data():
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching the data: {e}")
        return None

def send_to_kafka(data):
    producer = Producer(conf)
    try:
        message = json.dumps(data)
        producer.produce(KAFKA_TOPIC, value=message)
        producer.flush()
        logging.info("Message sent to Kafka sucessfully")
    except KafkaException as e:
        logging.error(f"Kafka error: {e}")
        
def main():
    while True:
        weather_data = fetch_weather_data()
        if weather_data:
            send_to_kafka(weather_data)
        
if __name__ == "__main__":
    main()
    
    # sh = './start.sh'
    # process = subprocess.run(["bash", sh], check=True)
    
    # if process.returncode == 0:
    #     logging.info("Zookeeper and Kafka started successfully.")
    #     main()
    # else:
    #     logging.error("Error starting services.")