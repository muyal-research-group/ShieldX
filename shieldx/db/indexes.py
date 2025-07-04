from shieldx.db import get_database
from shieldx.log import Log
from shieldx.log.logger_config import get_logger
import time as T


L = get_logger(__name__)


async def create_indexes():
    """
    Crea índices en la colección 'events' para mejorar la eficiencia de las consultas.
    """
    t1 = T.time()
    db = get_database()
    if db is None:
        raise RuntimeError("🚨 Error: La base de datos no está inicializada antes de crear índices.")
    
    await db["events"].create_index("service_id")
    await db["events"].create_index("microservice_id")
    await db["events"].create_index("function_id")
    L.debug({
        "event":"CREATED.INDEXES",
        "time":T.time() - t1
    })
    # print("✅ Índices creados correctamente")   
