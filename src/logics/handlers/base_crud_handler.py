from src.core.event_type import event_type
from src.core.exception import arguments_exception, operation_exception
from src.dtos.log_entry_dto import log_entry_dto
from src.logics.observer import observer
from src.logics.storage_manager import storage_manager
from src.logics.dependency_validator import entity_dependency_validator
from src.logics.deserializer_factory import deserializer_factory
from src.logics.handlers.base_read_handler import base_read_handler


class base_crud_handler(base_read_handler):
    """
    Базовый класс для полных CRUD-операций над доменными сущностями.
    """

    def __init__(
        self,
        storage: storage_manager,
        validator: entity_dependency_validator = None,
        deserializer: deserializer_factory = None,
    ) -> None:
        super().__init__(storage)
        self._validator = validator or entity_dependency_validator()
        self._deserializer = deserializer or deserializer_factory()

    def _after_save(self, item: object) -> None:
        """Хук после успешного сохранения сущности в хранилище."""
        pass

    def create(self, data: dict):
        """Создать новую доменную сущность из словаря через десериализатор."""
        try:
            from src.logics.deserialization_context import deserialization_context
            isolated_factory = deserializer_factory(context=deserialization_context(isolated=True))
            item = isolated_factory.deserialize_value(data, self._model_class)
        except (arguments_exception, operation_exception) as ex:
            return {"error": str(ex)}, 400

        added = self._storage.save(self._storage_key, item)
        if not added:
            return {"error": f"Объект с идентификатором {item.id} уже существует"}, 409
        self._after_save(item)
        observer.create(
            event_type.crud_create(),
            log_entry_dto(
                entity_type=self._model_class.__name__,
                entity_id=str(getattr(item, "id", "")),
                message=f"Создана сущность '{getattr(item, 'name', '')}'",
            ),
        )
        return self._to_dict(item), 201

    def update(self, entity_id: str, data: dict):
        """Обновить существующую доменную сущность в коллекции хранилища."""
        collection = self._storage.collection(self._storage_key)
        target_id = str(entity_id).strip()
        existing_index = next(
            (i for i, item in enumerate(collection) if str(getattr(item, "id", "")).strip() == target_id),
            None,
        )
        if existing_index is None:
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
            from src.logics.deserialization_context import deserialization_context
            isolated_factory = deserializer_factory(context=deserialization_context(isolated=True))
            updated = isolated_factory.deserialize_value(data_copy, self._model_class)
        except (arguments_exception, operation_exception) as ex:
            return {"error": str(ex)}, 400

        collection[existing_index] = updated
        self._after_save(updated)
        observer.create(
            event_type.crud_update(),
            log_entry_dto(
                entity_type=self._model_class.__name__,
                entity_id=str(getattr(updated, "id", target_id)),
                message=f"Обновлена сущность '{getattr(updated, 'name', '')}'",
            ),
        )
        return self._to_dict(updated), 200

    def delete(self, entity_id: str):
        """Удалить сущность по идентификатору из коллекции хранилища."""
        deps = self._validator.validate_delete(entity_id, self._storage)
        if deps:
            return {"error": "Невозможно удалить: есть зависимые объекты", "dependencies": deps}, 409

        collection = self._storage.collection(self._storage_key)
        target_id = str(entity_id).strip()
        existing_index = next(
            (i for i, item in enumerate(collection) if str(getattr(item, "id", "")).strip() == target_id),
            None,
        )
        if existing_index is None:
            return {"error": f"{self._model_class.__name__} с id={entity_id} не найден"}, 404

        collection.pop(existing_index)
        observer.create(
            event_type.crud_delete(),
            log_entry_dto(
                entity_type=self._model_class.__name__,
                entity_id=target_id,
                message="Удалена сущность",
            ),
        )
        return "", 204
