from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.logics.dependency_validator import entity_dependency_validator
from src.models.settings_model import settings_model


class settings_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для настроек приложения (settings_model).
    """

    def __init__(
        self,
        storage: storage_manager,
        validator: entity_dependency_validator = None,
    ) -> None:
        super().__init__(storage, validator)
        self._ensure_initial_data()

    def _ensure_initial_data(self) -> None:
        items = self._storage.get(self._storage_key)
        if not items:
            from src.logics.settings_manager import settings_manager
            s_mgr = settings_manager()
            if not s_mgr.is_loaded:
                s_mgr.load()
            if s_mgr.settings:
                self._storage.add(self._storage_key, s_mgr.settings)

    def _after_save(self, item: object) -> None:
        from src.logics.settings_manager import settings_manager
        s_mgr = settings_manager()
        if s_mgr.settings and s_mgr.settings.id == getattr(item, "id", None):
            s_mgr.settings = item

    @property
    def _storage_key(self) -> str:
        return storage_manager.settings_key()

    @property
    def _model_class(self) -> type:
        return settings_model
