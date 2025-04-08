from fastapi import FastAPI
from shieldx.controllers import events_router, trigger_router
from shieldx.db import connect_to_mongo,close_mongo_connection, get_database
import uvicorn
import asyncio
from contextlib import asynccontextmanager
from shieldx.db.indexes import create_indexes



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
        
    # Esperar hasta que la base de datos esté disponible
    for _ in range(5):  # Intentos máximos
        try:
            db = get_database()
            if db is not None:
                await create_indexes()
                break  # Salir del bucle si la base de datos está lista
        except RuntimeError:
            print("⏳ Esperando a que MongoDB esté listo...")
            await asyncio.sleep(1)  # Esperar un segundo antes de intentar nuevamente
    
    yield 
    await close_mongo_connection()


app = FastAPI(title="ShieldX API",lifespan=lifespan, description="API para registrar y consultar eventos generados por microservicios.",
    contact={
        "name": "Equipo ShieldX",
        "email": "soporte@shieldx.io",
    })

# Include API routes from the service controller under /api/v1
# Rutas de eventos
app.include_router(events_router, prefix="/api/v1",tags=["Eventos"],)
# Rutas de triggers
app.include_router(trigger_router, prefix="/api/v1", tags=["Triggers"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=20000)
