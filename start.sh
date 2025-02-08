#!/bin/bash

cd "$(dirname "$0")"

# Load the .env file
if [ -f ".env" ]; then
    echo ".env file found."
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found."
    exit 1
fi

echo "KAFKA_PATH is set to: $KAFKA_PATH"

if [ -z "$KAFKA_PATH" ]; then
    echo "KAFKA_PATH is not set in .env file."
    exit 1
fi

check_service() {
    local host=$1
    local port=$2
    local service_name=$3
    local timeout_seconds=30

    echo "Checking $service_name availability on $host:$port..."
    while [ $timeout_seconds -gt 0 ]; do
        if nc -z "$host" "$port" 2>/dev/null; then
            echo "$service_name is running on $host:$port."
            return 0
        fi
        sleep 1
        timeout_seconds=$((timeout_seconds - 1))
    done

    echo "Error: $service_name did not start on $host:$port within the expected time."
    return 1
}

# Start Zookeeper
echo "Starting Zookeeper using command:"
echo "nohup $KAFKA_PATH/bin/zookeeper-server-start.sh $KAFKA_PATH/config/zookeeper.properties > zookeeper.log 2>&1 &"
nohup "$KAFKA_PATH/bin/zookeeper-server-start.sh" "$KAFKA_PATH/config/zookeeper.properties" > zookeeper.log 2>&1 &
sleep 10 

check_service "localhost" 2181 "Zookeeper"
if [ $? -ne 0 ]; then
    echo "Zookeeper failed to start. Check zookeeper.log for details."
    exit 1
fi

# Start Kafka
echo "Starting Kafka using command:"
echo "nohup $KAFKA_PATH/bin/kafka-server-start.sh $KAFKA_PATH/config/server.properties > starting_kafka.log 2>&1 &"
nohup "$KAFKA_PATH/bin/kafka-server-start.sh" "$KAFKA_PATH/config/server.properties" > starting_kafka.log 2>&1 &
sleep 10 

check_service "localhost" 9092 "Kafka"
if [ $? -ne 0 ]; then
    echo "Kafka failed to start. Check starting_kafka.log for details."
    exit 1
fi

echo "Both Zookeeper and Kafka started successfully."