import aio_pika
import json
import os
from typing import Dict,Any
import threading
import time as T
from shieldx.models import EventModel
from shieldx.services import EventsService
from shieldx.repositories import EventsRepository
from shieldx.db import get_collection
import asyncio


# RabbitMQ Config
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_HOST", 5672))

EXCHANGE_NAME = "default_exchange"
DEFAULT_QUEUES = ["queue_service_a", "queue_service_b"]  # Default queues to listen

class AsyncRabbitMQService:
    def __init__(self, queues=None):
        self.queues = queues if queues else DEFAULT_QUEUES
        self.connection = None
        self.channel = None
        self.events_service = EventsService(
            repository=EventsRepository(
                collection=get_collection("events")
            )
        )

    async def connect(self):
        """Establish an async connection with RabbitMQ and declare the exchange."""
        while True:
            try:
                self.connection = await aio_pika.connect_robust(host= RABBITMQ_HOST, port= RABBITMQ_PORT)
                self.channel = await self.connection.channel()
                exchange = await self.channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT)

                # Declare and bind queues dynamically
                for queue in self.queues:
                    queue_obj = await self.channel.declare_queue(queue, durable=True)
                    await queue_obj.bind(exchange, routing_key=queue)
                    print(f"[✔] Subscribed to queue: {queue}")

                print("[✔] Connection established with RabbitMQ.")
                return
            except Exception as e:
                print(f"[❌] Connection error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def publish(self, queue: str, message: Dict[str, Any]):
        """Publishes a message to a specific queue asynchronously."""
        if not self.channel:
            print("[❌] No active connection to RabbitMQ.")
            return

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue,
        )
        print(f"[📤] Message sent to {queue}: {message}")

    async def subscribe(self, queue: str):
        """Consumes messages asynchronously, ensuring each queue gets its own consumer."""
        async with self.connection:
            channel = await self.connection.channel()
            queue_obj = await channel.declare_queue(queue, durable=True)

            async for message in queue_obj:
                async with message.process():
                    data = json.loads(message.body.decode())
                    print(f"[📥] Message received in {queue}: {data}")
                    await self.events_service.create_event(EventModel.model_validate(data))

    async def start_consuming(self):
        """Starts consuming messages from all subscribed queues asynchronously."""
        print("[🚀] Starting message consumption...")
        tasks = [asyncio.create_task(self.subscribe(queue)) for queue in self.queues]
        await asyncio.gather(*tasks)

    async def close(self):
        """Closes the RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            print("[❌] RabbitMQ connection closed.")