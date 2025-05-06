#!/bin/bash

while !nc z $RABBITMQ_HOST $RABBITMQ_PORT; do
    echo "Waiting for RabbitMQ at $RABBITMQ_HOST:$RABBITMQ_PORT..."
  sleep 1
done

echo "RabbitMQ is ready! Starting Celery..."

# RUN Worker
python bot/services/background_tasks/run_worker.py

