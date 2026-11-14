from abc import ABC, abstractmethod
from src.core.exception import arguments_exception, operation_exception
from src.logics.storage_manager import storage_manager
from src.logics.convert_factory import convert_factory
from src.logics.dependency_validator import entity_dependency_validator


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
        items = self._storage.get(self._storage_key)
        target_id = str(entity_id).strip()
        return next((item for item in items if str(getattr(item, "id", "")).strip() == target_id), None)

    def get_all(self):
        """Получить список всех сущностей."""
        items = self._storage.get(self._storage_key)
        return [self._to_dict(item) for item in items], 200

    def get_by_id(self, entity_id: str):
        """Получить сущность по идентификатору."""
        found = self._find_by_id(entity_id)
        if found is None:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404
        return self._to_dict(found), 200


class base_crud_handler(base_read_handler):
    """
    Базовый класс для полных CRUD-операций над доменными сущностями.
    """

    def __init__(
        self,
        storage: storage_manager,
        validator: entity_dependency_validator = None,
    ) -> None:
        super().__init__(storage)
        self._validator = validator or entity_dependency_validator()

    def _prepare_data(self, data: dict) -> dict:
        """Подготовка данных перед созданием или обновлением экземпляра модели."""
        return data

    def _create_instance(self, data: dict):
        """Создает экземпляр доменной модели из словаря данных."""
        prepared = self._prepare_data(data)
        return self._model_class.create_from_dict(prepared)

    def _after_save(self, item: object) -> None:
        """Хук после успешного сохранения сущности в хранилище."""
        pass

    def create(self, data: dict):
        """Создать новую доменную сущность."""
        try:
            item = self._create_instance(data)
        except (arguments_exception, operation_exception) as ex:
            return {"error": str(ex)}, 400

        added = self._storage.add(self._storage_key, item)
        if not added:
            return {"error": f"Объект с идентификатором {item.id} уже существует"}, 409
        self._after_save(item)
        return self._to_dict(item), 201

    def update(self, entity_id: str, data: dict):
        """Обновить существующую доменную сущность."""
        existing = self._find_by_id(entity_id)
        if existing is None:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404

        new_id = data.get("id")
        if new_id and str(new_id).strip() != entity_id:
            deps = self._validator.validate_delete(entity_id, self._storage)
            if deps:
                return {
                    "error": "Невозможно изменить код/идентификатор: есть зависимые объекты",
                    "dependencies": deps,
                }, 409
            target_id = str(new_id).strip()
        else:
            target_id = entity_id

        data_copy = dict(data)
        data_copy["id"] = target_id
        try:
            updated = self._create_instance(data_copy)
        except (arguments_exception, operation_exception) as ex:
            return {"error": str(ex)}, 400

        success = self._storage.update(self._storage_key, updated, entity_id)
        if not success:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404
        self._after_save(updated)
        return self._to_dict(updated), 200

    def delete(self, entity_id: str):
        """Удалить сущность по идентификатору."""
        deps = self._validator.validate_delete(entity_id, self._storage)
        if deps:
            return {"error": "Невозможно удалить: есть зависимые объекты", "dependencies": deps}, 409

        deleted = self._storage.delete(self._storage_key, entity_id)
        if not deleted:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404
        return "", 204
