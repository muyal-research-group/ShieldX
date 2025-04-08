
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from shieldx.server import app
from shieldx.db import connect_to_mongo, get_collection


@pytest_asyncio.fixture(autouse=True)
async def setup_and_clean_mongodb():
    await connect_to_mongo()
    collection = get_collection("triggers")
    assert collection is not None, "❌ La colección 'triggers' no fue inicializada. Revisa connect_to_mongo()."
    await collection.delete_many({})


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


trigger_payload = {
    "name": "TriggerTest004",
    "rule": {
        "target": "mictlanx.get",
        "parameters": {
            "bucket_id": {"type": "string", "description": "ID del bucket"},
            "key": {"type": "string", "description": "Clave"},
            "sink_path": {"type": "string", "description": "Ruta destino"}
        }
    }
}


@pytest_asyncio.fixture
async def existing_trigger(client):
    await client.post("/api/v1/triggers/", json=trigger_payload)


@pytest.mark.asyncio
async def test_create_trigger(client):
    response = await client.post("/api/v1/triggers/", json=trigger_payload)
    assert response.status_code == 200
    assert response.json()["name"] == trigger_payload["name"]


@pytest.mark.asyncio
async def test_get_trigger_by_name(client, existing_trigger):
    response = await client.get(f"/api/v1/triggers/{trigger_payload['name']}")
    assert response.status_code == 200
    assert response.json()["name"] == trigger_payload["name"]


@pytest.mark.asyncio
async def test_get_all_triggers(client, existing_trigger):
    response = await client.get("/api/v1/triggers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(t["name"] == trigger_payload["name"] for t in response.json())


@pytest.mark.asyncio
async def test_update_trigger(client, existing_trigger):
    updated_payload = trigger_payload.copy()
    updated_payload["rule"]["parameters"]["sink_path"]["description"] = "Ruta modificada"
    response = await client.put(f"/api/v1/triggers/{trigger_payload['name']}", json=updated_payload)
    assert response.status_code == 200
    assert response.json()["rule"]["parameters"]["sink_path"]["description"] == "Ruta modificada"


@pytest.mark.asyncio
async def test_delete_trigger(client, existing_trigger):
    response = await client.delete(f"/api/v1/triggers/{trigger_payload['name']}")
    assert response.status_code == 200
    assert "deleted" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_duplicate_trigger(client, existing_trigger):
    response = await client.post("/api/v1/triggers/", json=trigger_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Trigger already exists"


@pytest.mark.asyncio
async def test_get_nonexistent_trigger(client):
    response = await client.get("/api/v1/triggers/no_existe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"


@pytest.mark.asyncio
async def test_update_nonexistent_trigger(client):
    payload = trigger_payload.copy()
    payload["name"] = "no_existe"
    response = await client.put("/api/v1/triggers/no_existe", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"


@pytest.mark.asyncio
async def test_delete_nonexistent_trigger(client):
    response = await client.delete("/api/v1/triggers/no_existe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trigger not found"
