from fastapi import FastAPI
import shieldx.controllers as Controllers
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


app = FastAPI(
    title="ShieldX API",
    lifespan=lifespan, 
    description="API para registrar y consultar eventos generados por microservicios.",
    contact={
        "name": "Equipo ShieldX",
        "email": "soporte@shieldx.io",
    })


# Include API routes from the service controller under /api/v1
# Rutas para la gestión de eventos generados por servicios
app.include_router(Controllers.events_router, prefix="/api/v1",tags=["Eventos"],)
# Rutas para la gestión de triggers del sistema
app.include_router(Controllers.trigger_router, prefix="/api/v1", tags=["Triggers"])
# Rutas para la gestión de tipos de eventos
app.include_router(Controllers.event_types_router, prefix="/api/v1", tags=["Tipos de Evento"])
# Rutas para administrar la relación EventType <-> Trigger
app.include_router(Controllers.events_triggers_router, prefix="/api/v1", tags=["Event-Triggers"])
# Rutas para manejar la relación jerárquica entre triggers (parent-child)
app.include_router(Controllers.triggers_triggers_router, prefix="/api/v1", tags=["Triggers-Triggers"])
# Rutas para administrar la relación Trigger <-> Rule
app.include_router(Controllers.rules_trigger_router, prefix="/api/v1", tags=["Trigger - Rule"])
# Rutas para CRUD de reglas
app.include_router(Controllers.rules_router, prefix="/api/v1",  tags=["Rules"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=20000)
