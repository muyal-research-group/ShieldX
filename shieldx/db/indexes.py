from shieldx.db import get_database

async def create_indexes():
    """
    Crea índices en la colección 'events' para mejorar la eficiencia de las consultas.
    """
    db = get_database()
    if db is None:
        raise RuntimeError("🚨 Error: La base de datos no está inicializada antes de crear índices.")
    
    await db["events"].create_index("service_id")
    await db["events"].create_index("microservice_id")
    await db["events"].create_index("function_id")
    print("✅ Índices creados correctamente")
