import importlib
from src.core.abstract_deserializer import abstract_deserializer
from src.core.abstract_deserializer_factory import abstract_deserializer_factory
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.logics.deserialization_context import deserialization_context


class model_deserializer(abstract_deserializer):
    """
    Десериализатор доменных сущностей.
    Координирует восстановление объектов, разрешая тип модели по строковому ключу
    или явному типу и делегируя создание фабричному методу модели.
    """

    def __init__(
        self,
        factory: abstract_deserializer_factory = None,
        context: deserialization_context = None,
    ):
        """
        Инициализирует координатор десериализации моделей.

        :param factory: Фабрика десериализаторов для рекурсивной обработки
        :param context: Контекст реестра идентичности
        """
        self.__factory = factory
        self.__context = context if context is not None else deserialization_context()

    @property
    def context(self) -> deserialization_context:
        """
        Текущий контекст идентичности.
        """
        return self.__context

    def deserialize(self, data: object, target_type: type = None) -> object:
        """
        Десериализует словарь в экземпляр доменной модели через фабричный метод модели.

        :param data: Исходные данные (словарь)
        :param target_type: Ожидаемый класс доменной модели
        :return: Экземпляр доменной модели
        """
        if data is None:
            return None

        if not isinstance(data, dict):
            raise arguments_exception(
                "data",
                f"Ожидается словарь данных для десериализации модели, получено: {type(data)}"
            )

        model_cls = self._resolve_target_type(data, target_type)
        if model_cls is None:
            raise arguments_exception(
                "target_type",
                "Не удалось определить целевой класс для десериализации словаря"
            )

        entity_id = self._extract_id(data)
        if entity_id:
            cached_instance = self.__context.get(entity_id)
            if cached_instance is not None:
                return cached_instance

        if set(data.keys()) == {"id"} and entity_id:
            return self.__context.get(entity_id)

        if hasattr(model_cls, "create_from_dict"):
            instance = model_cls.create_from_dict(data)
        else:
            instance = model_cls()
            if entity_id:
                instance.id = entity_id

        if entity_id and hasattr(instance, "id"):
            instance.id = entity_id
            self.__context.register(instance)

        return instance

    def _extract_id(self, data: dict) -> str:
        """
        Извлекает строковый идентификатор из словаря.
        """
        raw_id = data.get("id")
        if raw_id is not None and str(raw_id).strip():
            return str(raw_id).strip()
        return ""

    def _resolve_target_type(self, data: dict, target_type: type = None) -> type:
        """
        Определяет целевой класс модели динамически по полю 'type' или переданному типу.
        """
        if target_type is not None and isinstance(target_type, type):
            return target_type

        if isinstance(target_type, str):
            resolved = self._resolve_class_from_string(target_type)
            if resolved is not None:
                return resolved

        type_indicator = data.get("type")
        if type_indicator and isinstance(type_indicator, str):
            resolved = self._resolve_class_from_string(type_indicator)
            if resolved is not None:
                return resolved

        return None

    @staticmethod
    def _resolve_class_from_string(name: str) -> type | None:
        """
        Динамически импортирует и возвращает класс по его полному имени или краткому названию.
        """
        clean_name = name.strip()
        if not clean_name:
            return None

        if "." in clean_name:
            try:
                module_name, class_name = clean_name.rsplit(".", 1)
                module = importlib.import_module(module_name)
                return getattr(module, class_name, None)
            except (ImportError, AttributeError):
                pass

        try:
            module = importlib.import_module(f"src.models.{clean_name}")
            return getattr(module, clean_name, None)
        except (ImportError, AttributeError):
            pass

        return None
