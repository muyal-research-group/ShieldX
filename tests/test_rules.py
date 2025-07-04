import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from shieldx.server import app
from shieldx.db import connect_to_mongo, get_collection

# ---------- FIXTURES ----------

@pytest_asyncio.fixture(autouse=True)
async def clean_rules_collection():
    """
    Conecta a la base de datos y limpia la colección 'rules' antes de cada test.
    """
    await connect_to_mongo()
    collection = get_collection("rules")
    assert collection is not None
    await collection.delete_many({})

@pytest_asyncio.fixture
async def client():
    """
    Proporciona un cliente HTTP asíncrono para las pruebas utilizando la app FastAPI.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# ---------- PAYLOAD BASE ----------

# Regla válida para el target conocido 'mictlanx.get'
valid_rule_payload = {
    "target": "mictlanx.get",
    "parameters": {
        "bucket_id": {"type": "string", "description": "ID del bucket"},
        "key": {"type": "string", "description": "Llave de acceso"},
        "sink_path": {"type": "string", "description": "Ruta de destino"}
    }
}

# ---------- TESTS ----------

@pytest.mark.asyncio
async def test_create_rule(client):
    """
    ✅ Verifica que se pueda crear una regla válida.
    """
    response = await client.post("/api/v1/rules", json=valid_rule_payload)
    assert response.status_code == 201
    assert isinstance(response.text, str)

@pytest.mark.asyncio
async def test_create_rule_missing_param(client):
    """
    ❌ Verifica que no se pueda crear una regla si faltan parámetros requeridos.
    """
    incomplete_payload = {
        "target": "mictlanx.get",
        "parameters": {
            "bucket_id": {"type": "string", "description": "ID del bucket"},
            # faltan 'key' y 'sink_path'
        }
    }
    response = await client.post("/api/v1/rules", json=incomplete_payload)
    assert response.status_code == 422 or response.status_code == 400

@pytest.mark.asyncio
async def test_create_rule_invalid_type(client):
    """
    ❌ Verifica que no se pueda crear una regla si un parámetro tiene un tipo no válido.
    """
    invalid_payload = {
        "target": "mictlanx.get",
        "parameters": {
            "bucket_id": {"type": "dragon", "description": "No válido"},
            "key": {"type": "string", "description": "Llave"},
            "sink_path": {"type": "string", "description": "Destino"}
        }
    }
    response = await client.post("/api/v1/rules", json=invalid_payload)
    assert response.status_code == 422 or response.status_code == 400

@pytest_asyncio.fixture
async def created_rule_id(client):
    """
    Crea una regla válida y devuelve su ID.
    """
    response = await client.post("/api/v1/rules", json=valid_rule_payload)
    return response.text.strip('"')

@pytest.mark.asyncio
async def test_get_rule_by_id(client, created_rule_id):
    """
    ✅ Verifica que se pueda obtener una regla existente por su ID.
    """
    response = await client.get(f"/api/v1/rules/{created_rule_id}")
    assert response.status_code == 200
    assert response.json()["target"] == valid_rule_payload["target"]

@pytest.mark.asyncio
async def test_get_rule_not_found(client):
    """
    ❌ Verifica que obtener una regla con ID inexistente retorne 404.
    """
    response = await client.get("/api/v1/rules/000000000000000000000000")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_rule(client, created_rule_id):
    """
    🔄 Verifica que se pueda actualizar correctamente una regla existente.
    """
    updated_payload = {
        "target": "mictlanx.get",
        "parameters": {
            "bucket_id": {  "type": "string", "description": "Modificado"},
            "key": {    "type": "string", "description": "Clave"},
            "sink_path": {  "type": "string", "description": "Ruta nueva"}
        }
    }
    response = await client.put(f"/api/v1/rules/{created_rule_id}", json=updated_payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Rule updated"

@pytest.mark.asyncio
async def test_update_rule_not_found(client):
    """
    ❌ Verifica que intentar actualizar una regla inexistente retorne 404.
    """
    payload = valid_rule_payload.copy()
    response = await client.put("/api/v1/rules/000000000000000000000000", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Rule not found"

@pytest.mark.asyncio
async def test_list_rules(client, created_rule_id):
    """
    📋 Verifica que se puedan listar todas las reglas registradas.
    """
    response = await client.get("/api/v1/rules")
    assert response.status_code == 200
    rules = response.json()
    assert isinstance(rules, list)
    assert any(rule["_id"] == created_rule_id for rule in rules)

@pytest.mark.asyncio
async def test_delete_rule(client, created_rule_id):
    """
    🗑️ Verifica que se pueda eliminar correctamente una regla existente.
    """
    response = await client.delete(f"/api/v1/rules/{created_rule_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_rule_not_found(client):
    """
    ❌ Verifica que intentar eliminar una regla inexistente retorne 404.
    """
    response = await client.delete("/api/v1/rules/000000000000000000000000")
    assert response.status_code == 404
