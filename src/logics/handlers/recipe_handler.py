from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.recipe_model import recipe_model


class recipe_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для технологических карт (recipe_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.recipe_key()

    @property
    def _model_class(self) -> type:
        return recipe_model
