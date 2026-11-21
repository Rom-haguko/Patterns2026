from src.logics.handlers.base_crud_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_model import nomenclature_model


class nomenclature_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для номенклатурных позиций (nomenclature_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.nomenclature_key()

    @property
    def _model_class(self) -> type:
        return nomenclature_model
