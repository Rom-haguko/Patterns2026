from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model


class group_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для групп номенклатуры (nomenclature_group_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.group_key()

    @property
    def _model_class(self) -> type:
        return nomenclature_group_model
