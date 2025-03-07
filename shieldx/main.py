import pika
import json
import os
from shieldx.models import EncryptStart
from typing import Dict,Any
import threading
import time as T

# RabbitMQ Config
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
EXCHANGE_NAME = "microservices_exchange"
DEFAULT_QUEUES = ["queue_service_a", "queue_service_b"]  # Default queues to listen

class RabbitMQService:
    def __init__(self, queues=None):
        self.queues = queues if queues else DEFAULT_QUEUES
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establishes a connection with RabbitMQ and declares the exchange."""
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
                )
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

                # Declare and bind queues dynamically
                for queue in self.queues:
                    self.channel.queue_declare(queue=queue, durable=True)
                    self.channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue, routing_key=queue)
                    print(f"[✔] Subscribed to queue: {queue}")

                print("[✔] Connection established with RabbitMQ.")
                return
            except pika.exceptions.AMQPConnectionError:
                print("[❌] Connection error. Retrying in 5 seconds...")
                T.sleep(5)

    def publish(self, queue:str, message:Dict[str,Any]):
        """Publishes a message to a specific queue."""
        if not self.channel:
            print("[❌] No active connection to RabbitMQ.")
            return

        self.channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Message persistence
            ),
        )
        print(f"[📤] Message sent to {queue}: {message}")

    def subscribe(self, queue):
        """Each consumer gets its own connection to avoid StreamLostError."""
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)  # Ensure queue exists

            def callback(ch, method, properties, body):
                message = json.loads(body)
                print(f"[📥] Message received in {queue}: {message}")
                ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

            channel.basic_consume(queue=queue, on_message_callback=callback)
            print(f"[🔄] Listening for messages in queue: {queue}")

            channel.start_consuming()

        except pika.exceptions.StreamLostError:
            print(f"[❌] Connection lost in {queue}, reconnecting...")
            self.subscribe(queue)  # Auto-reconnect if the connection is lost

    def start_consuming(self):
        """Starts consuming messages from all subscribed queues in separate threads."""
        print("[🚀] Starting message consumption...")
        threads = []
        for queue in self.queues:
            t = threading.Thread(target=self.subscribe, args=(queue,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def close(self):
        """Closes the RabbitMQ connection."""
        if self.connection:
            self.connection.close()
            print("[❌] RabbitMQ connection closed.")

# Initialize the service dynamically
if __name__ == "__main__":
    # queues_to_subscribe = os.getenv("QUEUES", "s_security").split(",")
    # service = RabbitMQService(queues=queues_to_subscribe)

    service = RabbitMQService(queues=[])


    # Example: Publish a message
    queue_id = "s_security"
    for i in range(10):
        service.publish(queue_id,  EncryptStart(function_id="encrypt_data", source="/mictlanx/local", sink="/mictlanx/remote").model_dump())
        T.sleep(1)
    
    # Start consuming messages
    try:
        service.start_consuming()
    except KeyboardInterrupt:
        service.close()
