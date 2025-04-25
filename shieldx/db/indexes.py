from shieldx.db import get_database
from shieldx.log import Log
from logging import LogRecord,INFO,ERROR,DEBUG,WARNING
import os
import time as T

DEBUG = bool(int(os.environ.get("SHIELDX_DEBUG","1")))

def console_handler_filter(lr:LogRecord):
    if DEBUG:
        return DEBUG
    
    return lr.levelno == INFO or lr.levelno == ERROR or lr.levelno == WARNING
        

L = Log(
    name=__name__,
    console_handler_filter= console_handler_filter
)
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
