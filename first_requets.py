import requests
import logging
import json
import subprocess
from confluent_kafka import Consumer, Producer, KafkaException, KafkaError

KAKFA_SERVER = 'localhost:9092'
KAKFA_TOPIC = 'testing_forecast'
conf = {
    'bootstrap.servers': KAKFA_SERVER,
    'session.timeout.ms': 6000,
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
        producer.produce(KAKFA_TOPIC, value=message)
        producer.flush()
        logging.info("Message sent to Kafka sucessfully")
    except KafkaException as e:
        logging.error(f"Kafka error: {e}")
        
def main():
    weather_data = fetch_weather_data()
    if weather_data:
        send_to_kafka(weather_data)
        
if __name__ == "__main__":
    sh = './start.sh'
    process = subprocess.run(["bash", sh], check=True)
    
    if process.returncode == 0:
        logging.info("Zookeeper and Kafka started successfully.")
        main()
    else:
        logging.error("Error starting services.")