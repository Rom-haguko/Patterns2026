from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.range_model import range_model


class range_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для единиц измерения (range_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.range_key()

    @property
    def _model_class(self) -> type:
        return range_model
