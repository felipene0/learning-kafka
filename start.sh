if [ -f ".env" ]; then
    echo ".env file found."
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found."
    exit 1
fi

if [ -z "$KAFKA_PATH" ]; then
    echo "KAFKA_PATH is not set in .env file"
    exit 1
fi

echo "Starting Zookeeper..."
nohup $KAFKA_PATH/zookeeper-server-start.sh $KAFKA_PATH/config/zookeeper.properties > zookeeper.log 2>&1 &

sleep 20

echo "Starting Kafka..."
nohup $KAFKA_PATH/kafka-server-start.sh $KAFKA_PATH/config/server.properties > starting_kafka.log 2>&1 &