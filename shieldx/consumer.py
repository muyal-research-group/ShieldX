import os
from shieldx.broker import AsyncRabbitMQService
from shieldx.db import connect_to_mongo,close_mongo_connection
import asyncio
import time as T

async def main():
    await connect_to_mongo()
    queues_to_subscribe = os.environ.get("QUEUES", "s_security").split(",")
    service = AsyncRabbitMQService(queues=queues_to_subscribe)
    await service.connect()
    # Start consuming messages
    try:
        await service.start_consuming()
    except KeyboardInterrupt:
        await service.close()
if __name__ == "__main__":
    asyncio.run(main=main())