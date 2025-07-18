import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from shieldx.server import app
from shieldx.db import connect_to_mongo, get_collection

# ---------- FIXTURES ----------

@pytest_asyncio.fixture(autouse=True)
async def clean_collections():
    """
    Fixture automática que se ejecuta antes de cada prueba.
    Limpia las colecciones 'rules', 'triggers' y 'rules_triggers'.
    """
    await connect_to_mongo()
    for name in ["rules", "triggers", "rules_triggers"]:
        collection = get_collection(name)
        assert collection is not None
        await collection.delete_many({})

@pytest_asyncio.fixture
async def client():
    """
    Proporciona un cliente HTTP asíncrono configurado con la aplicación FastAPI.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def setup_rule_and_trigger(client):
    """
    Crea un trigger y una regla válida. Devuelve sus IDs junto con el payload de la regla.
    """
    # Crear trigger
    trigger_resp = await client.post("/api/v1/triggers/", json={"name": "TriggerRulesTest"})
    assert trigger_resp.status_code == 201
    trigger_id = trigger_resp.json()["_id"]

    # Crear regla válida
    rule_payload = {
        "target": "mictlanx.get",
        "parameters": {
            "bucket_id": {"type": "string", "description": "ID del bucket"},
            "key": {"type": "string", "description": "Llave"},
            "sink_path": {"type": "string", "description": "Destino"}
        }
    }
    rule_resp = await client.post("/api/v1/rules", json=rule_payload)
    assert rule_resp.status_code == 201
    rule_id = rule_resp.text.strip('"')

    return trigger_id, rule_id, rule_payload

# ---------- TESTS ----------

@pytest.mark.asyncio
async def test_link_rule(client, setup_rule_and_trigger):
    """
    ✅ Verifica que se pueda vincular una regla existente a un trigger.
    """
    trigger_id, rule_id, _ = setup_rule_and_trigger
    response = await client.post(f"/api/v1/triggers/{trigger_id}/rules/{rule_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_list_rules_for_trigger(client, setup_rule_and_trigger):
    """
    📋 Verifica que se pueda obtener la lista de reglas vinculadas a un trigger específico.
    """
    trigger_id, rule_id, _ = setup_rule_and_trigger

    # Vincula la regla al trigger
    await client.post(f"/api/v1/triggers/{trigger_id}/rules/{rule_id}")

    response = await client.get(f"/api/v1/triggers/{trigger_id}/rules")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(r["rule_id"] == rule_id for r in data)

@pytest.mark.asyncio
async def test_create_and_link_rule(client, setup_rule_and_trigger):
    """
    🆕 Verifica que se pueda crear una nueva regla y vincularla a un trigger en un solo paso.
    """
    trigger_id, _, rule_data = setup_rule_and_trigger

    response = await client.post(f"/api/v1/triggers/{trigger_id}/rules", json=rule_data)
    assert response.status_code == 201
    

    # Confirmar que la nueva regla está vinculada
    response = await client.get(f"/api/v1/triggers/{trigger_id}/rules")
    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_unlink_rule(client, setup_rule_and_trigger):
    """
    ❌ Verifica que se pueda desvincular correctamente una regla de un trigger.
    """
    trigger_id, rule_id, _ = setup_rule_and_trigger

    # Vincula la regla antes de intentar desvincularla
    await client.post(f"/api/v1/triggers/{trigger_id}/rules/{rule_id}")

    # Eliminar la relación
    response = await client.delete(f"/api/v1/triggers/{trigger_id}/rules/{rule_id}")
    assert response.status_code == 204

    # Confirmar que ya no esté en la lista de reglas vinculadas
    response = await client.get(f"/api/v1/triggers/{trigger_id}/rules")
    assert all(r["rule_id"] != rule_id for r in response.json())
