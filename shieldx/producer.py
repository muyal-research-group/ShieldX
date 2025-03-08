import asyncio
from shieldx.broker import AsyncRabbitMQService
from shieldx.models import EventModel
import time as T
async def main():

    service = AsyncRabbitMQService(queues=["s_security"])
    await service.connect()
    N_events= 100
    # Example: Publish a message
    queue_id = "s_security"
    for i in range(N_events):
        await service.publish(queue_id,  
            EventModel(
                service_id=f"service-{i}",
                microservice_id=f"micro-{i}",
                function_id=f"func-{i}", 
                event_type="EncryptStart",
                timestamp=T.time(),
                payload={}
            ).model_dump()
        )
        T.sleep(1)
    
    service.close()
if __name__ == "__main__":
    asyncio.run(main())