import pytest
from httpx import AsyncClient, ASGITransport
from shieldx.server import app
from shieldx.db import connect_to_mongo


@pytest.fixture(autouse=True)
async def setup_mongodb():
    await connect_to_mongo()



@pytest.fixture
async def client():
    transport = ASGITransport(app=app)  # Usa app FastAPI directamente
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# 🔸 CREATE EVENT
@pytest.mark.asyncio
async def test_create_event(client):
    response = await client.post("/api/v1/events", json={
        "service_id": "service_test",
        "microservice_id": "micro_test",
        "function_id": "func_test",
        "event_type": "TestEvent",
        "payload": {"key": "value"}
    })
    assert response.status_code == 200
    assert "event_id" in response.json()


# 🔸 GET ALL EVENTS
@pytest.mark.asyncio
async def test_get_all_events(client):
    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 🔸 GET BY SERVICE ID (Query param)
@pytest.mark.asyncio
async def test_filter_events_by_service(client):
    response = await client.get("/api/v1/events?service_id=service_test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(e["service_id"] == "service_test" for e in data)


# 🔸 GET BY SERVICE ID (Path param)
@pytest.mark.asyncio
async def test_get_events_by_service_path(client):
    await client.post("/api/v1/events", json={
        "service_id": "service_test_path",
        "microservice_id": "micro_test",
        "function_id": "func_test",
        "event_type": "PathEvent",
        "payload": {}
    })

    response = await client.get("/api/v1/events/service/service_test_path")
    assert response.status_code == 200
    assert all(e["service_id"] == "service_test_path" for e in response.json())


# 🔸 GET BY MICROSERVICE ID
@pytest.mark.asyncio
async def test_get_events_by_microservice(client):
    response = await client.get("/api/v1/events/microservice/micro_test")
    assert response.status_code == 200
    assert all(e["microservice_id"] == "micro_test" for e in response.json())


# 🔸 GET BY FUNCTION ID
@pytest.mark.asyncio
async def test_get_events_by_function(client):
    response = await client.get("/api/v1/events/function/func_test")
    assert response.status_code == 200
    assert all(e["function_id"] == "func_test" for e in response.json())


# 🔸 UPDATE EVENT
@pytest.mark.asyncio
async def test_update_event(client):
    create_response = await client.post("/api/v1/events", json={
        "service_id": "original_service",
        "microservice_id": "original_micro",
        "function_id": "original_func",
        "event_type": "OriginalEvent",
        "payload": {}
    })
    event_id = create_response.json()["event_id"]

    update_response = await client.put(f"/api/v1/events/{event_id}", json={
        "service_id": "updated_service"
    })

    assert update_response.status_code == 200
    assert update_response.json()["service_id"] == "updated_service"


# 🔸 DELETE EVENT
@pytest.mark.asyncio
async def test_delete_event(client):
    create_response = await client.post("/api/v1/events", json={
        "service_id": "to_delete",
        "microservice_id": "micro_test",
        "function_id": "func_test",
        "event_type": "DeleteEvent",
        "payload": {}
    })
    event_id = create_response.json()["event_id"]

    delete_response = await client.delete(f"/api/v1/events/{event_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Evento eliminado"
