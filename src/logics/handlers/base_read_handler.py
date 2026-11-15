from abc import ABC, abstractmethod
from src.logics.storage_manager import storage_manager
from src.logics.convert_factory import convert_factory


class base_read_handler(ABC):
    """
    Базовый класс для операций чтения доменных сущностей.
    """

    def __init__(self, storage: storage_manager) -> None:
        self._storage = storage
        self._factory = convert_factory()

    @property
    @abstractmethod
    def _storage_key(self) -> str:
        """Ключ коллекции в хранилище."""
        ...

    @property
    @abstractmethod
    def _model_class(self) -> type:
        """Класс доменной модели."""
        ...

    def _to_dict(self, obj) -> dict:
        """Преобразует доменную модель в словарь."""
        return self._factory.convert_value(obj)

    def _find_by_id(self, entity_id: str):
        """Поиск сущности в хранилище по строковому идентификатору."""
        items = self._storage.collection(self._storage_key)
        target_id = str(entity_id).strip()
        return next((item for item in items if str(getattr(item, "id", "")).strip() == target_id), None)

    def get_all(self):
        """Получить список всех сущностей."""
        items = self._storage.collection(self._storage_key)
        return [self._to_dict(item) for item in items], 200

    def get_by_id(self, entity_id: str):
        """Получить сущность по идентификатору."""
        found = self._find_by_id(entity_id)
        if found is None:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404
        return self._to_dict(found), 200
