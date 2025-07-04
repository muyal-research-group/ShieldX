import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from shieldx.server import app
from shieldx.db import connect_to_mongo, get_collection

# ---------- FIXTURES ----------

@pytest_asyncio.fixture(autouse=True)
async def setup_and_clean_mongodb():
    """
    Fixture automática que limpia la colección 'triggers' antes de cada prueba.
    """
    await connect_to_mongo()
    collection = get_collection("triggers")
    assert collection is not None, "❌ La colección 'triggers' no fue inicializada. Revisa connect_to_mongo()."
    await collection.delete_many({})

@pytest_asyncio.fixture
async def client():
    """
    Crea un cliente HTTP asíncrono para enviar solicitudes a la API de FastAPI.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# ---------- DATOS DE PRUEBA ----------

trigger_payload = {
    "name": "TriggerTestNuevo"
}

@pytest_asyncio.fixture
async def existing_trigger(client):
    """
    Crea un trigger de prueba en la base de datos antes de ejecutar el test.
    """
    await client.post("/api/v1/triggers/", json=trigger_payload)

# ---------- TESTS ----------

@pytest.mark.asyncio
async def test_create_trigger(client):
    """
    ✅ Verifica que se pueda crear un trigger correctamente.
    """
    response = await client.post("/api/v1/triggers/", json=trigger_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger_payload["name"]
    assert "_id" in data

@pytest.mark.asyncio
async def test_get_trigger_by_name(client, existing_trigger):
    """
    ✅ Verifica que se pueda obtener un trigger por su nombre.
    """
    response = await client.get(f"/api/v1/triggers/{trigger_payload['name']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == trigger_payload["name"]
    assert "_id" in data

@pytest.mark.asyncio
async def test_get_all_triggers(client, existing_trigger):
    """
    📋 Verifica que se puedan listar todos los triggers registrados.
    """
    response = await client.get("/api/v1/triggers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(t["name"] == trigger_payload["name"] for t in data)

@pytest.mark.asyncio
async def test_update_trigger(client, existing_trigger):
    """
    🔄 Verifica que se pueda actualizar el nombre de un trigger existente.
    """
    updated_payload = {"name": "TriggerTestActualizado"}
    response = await client.put(f"/api/v1/triggers/{trigger_payload['name']}", json=updated_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "TriggerTestActualizado"

@pytest.mark.asyncio
async def test_delete_trigger(client, existing_trigger):
    """
    🗑️ Verifica que se pueda eliminar un trigger existente por su nombre.
    """
    response = await client.delete(f"/api/v1/triggers/{trigger_payload['name']}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_create_duplicate_trigger(client, existing_trigger):
    """
    ❌ Verifica que no se pueda crear un trigger duplicado.
    """
    response = await client.post("/api/v1/triggers/", json=trigger_payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Trigger already exists"

@pytest.mark.asyncio
async def test_get_nonexistent_trigger(client):
    """
    ❌ Verifica que al intentar obtener un trigger inexistente, se retorne 404.
    """
    response = await client.get("/api/v1/triggers/no_existe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"

@pytest.mark.asyncio
async def test_update_nonexistent_trigger(client):
    """
    ❌ Verifica que no se pueda actualizar un trigger que no existe.
    """
    payload = {"name": "no_existe"}
    response = await client.put("/api/v1/triggers/no_existe", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"

@pytest.mark.asyncio
async def test_delete_nonexistent_trigger(client):
    """
    ❌ Verifica que no se pueda eliminar un trigger inexistente.
    """
    response = await client.delete("/api/v1/triggers/no_existe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"
