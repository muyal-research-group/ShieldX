from fastapi import HTTPException
from shieldx.models.trigger_models import TriggerModel
from shieldx.repositories import TriggersRepository


class TriggerService:
    """
    Servicio encargado de gestionar la lógica relacionada con los triggers,
    incluyendo su creación, consulta, actualización y eliminación.
    """

    def __init__(self, repository: TriggersRepository):
        """Inicializa el repositorio para acceder a los datos de triggers."""
        self.repository = repository

    async def create_trigger(self, trigger: TriggerModel):
        """Crea un nuevo trigger si no existe uno con el mismo nombre."""
        if await self.repository.get_trigger_by_name(trigger.name):
            raise HTTPException(status_code=400, detail="Trigger already exists")
        return await self.repository.create_trigger(trigger)

    async def get_all_triggers(self):
        """Devuelve la lista de todos los triggers almacenados."""
        return await self.repository.get_all_triggers()

    async def get_trigger(self, name: str):
        """Obtiene un trigger específico por su nombre."""
        trigger = await self.repository.get_trigger_by_name(name)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        return trigger

    async def update_trigger(self, name: str, updated: TriggerModel):
        """Actualiza un trigger existente con nuevos datos."""
        if not await self.repository.get_trigger_by_name(name):
            raise HTTPException(status_code=404, detail="Trigger not found")
        update_data = updated.model_dump(by_alias=True, exclude_unset=True)
        return await self.repository.update_trigger(name, update_data)

    async def delete_trigger(self, name: str):
        """Elimina un trigger por su nombre."""
        if not await self.repository.get_trigger_by_name(name):
            raise HTTPException(status_code=404, detail="Trigger not found")
        await self.repository.delete_trigger(name)
        return {"detail": f"Trigger '{name}' deleted"}