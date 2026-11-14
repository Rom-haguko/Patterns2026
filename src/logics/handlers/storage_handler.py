from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.storage_model import storage_model


class storage_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для складов (storage_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.storage_key()

    @property
    def _model_class(self) -> type:
        return storage_model
