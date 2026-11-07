from enum import Enum
import inspect
from src.core.abstract_deserializer import abstract_deserializer
from src.core.abstract_deserializer_factory import abstract_deserializer_factory
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.dtos.report_type_enum import report_type_enum
from src.logics.deserialization_context import deserialization_context
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model
from src.models.settings_model import settings_model
from src.models.storage_model import storage_model


class model_deserializer(abstract_deserializer):
    """
    Десериализатор доменных сущностей и моделей данных.
    Преобразует словари в типизированные объекты с рекурсивным разбором
    вложенных связей и сохранением исходных идентификаторов.
    """

    MODEL_FIELD_TYPES = {
        range_model: {
            "base_range": range_model,
        },
        nomenclature_model: {
            "group": nomenclature_group_model,
            "range": range_model,
            "recipe": recipe_model,
        },
        recipe_row_model: {
            "nomenclature": nomenclature_model,
            "range": range_model,
        },
        recipe_model: {
            "rows": (list, recipe_row_model),
            "steps": (list, recipe_step_model),
            "target_nomenclature": nomenclature_model,
        },
        settings_model: {
            "company": organization_model,
            "response_format": report_type_enum,
        },
    }

    MODEL_SIGNATURES = [
        (frozenset(["inn", "bik"]), organization_model),
        (frozenset(["company", "boss_name"]), settings_model),
        (frozenset(["step_number", "time_minutes"]), recipe_step_model),
        (frozenset(["brutto", "netto"]), recipe_row_model),
        (frozenset(["rows", "steps"]), recipe_model),
        (frozenset(["full_name", "group"]), nomenclature_model),
        (frozenset(["conversion_factor"]), range_model),
        (frozenset(["address"]), storage_model),
        (frozenset(["name"]), nomenclature_group_model),
    ]

    CLASS_NAME_MAPPING = {
        "range_model": range_model,
        "range": range_model,
        "nomenclature_model": nomenclature_model,
        "nomenclature": nomenclature_model,
        "nomenclature_group_model": nomenclature_group_model,
        "nomenclature_group": nomenclature_group_model,
        "storage_model": storage_model,
        "storage": storage_model,
        "recipe_model": recipe_model,
        "recipe": recipe_model,
        "recipe_row_model": recipe_row_model,
        "recipe_row": recipe_row_model,
        "recipe_step_model": recipe_step_model,
        "recipe_step": recipe_step_model,
        "organization_model": organization_model,
        "organization": organization_model,
        "settings_model": settings_model,
        "settings": settings_model,
    }

    def __init__(
        self,
        factory: abstract_deserializer_factory = None,
        context: deserialization_context = None,
    ):
        """
        Инициализирует десериализатор моделей.

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
        Десериализует словарь в экземпляр доменной модели.

        :param data: Исходные данные (словарь)
        :param target_type: Ожидаемый класс доменной модели
        :return: Экземпляр доменной модели
        """
        if data is None:
            return None

        if not isinstance(data, dict):
            raise arguments_exception("data", f"Ожидается словарь данных для десериализации модели, получено: {type(data)}")

        model_cls = self._resolve_target_type(data, target_type)
        if model_cls is None:
            raise arguments_exception("target_type", "Не удалось определить целевой класс для десериализации словаря")

        entity_id = self._extract_id(data)
        if entity_id:
            cached_instance = self.__context.get(entity_id)
            if cached_instance is not None:
                return cached_instance

        if set(data.keys()) == {"id"} and entity_id:
            return self.__context.get(entity_id)

        init_kwargs = self._build_init_kwargs(model_cls, data)
        instance = model_cls(**init_kwargs)

        if entity_id:
            instance.id = entity_id
            self.__context.register(instance)

        self._populate_remaining_properties(instance, model_cls, data, set(init_kwargs.keys()))

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
        Определяет целевой класс модели по явному типу, полю 'type' в словаре или сигнатуре полей.
        """
        if target_type is not None and isinstance(target_type, type):
            return target_type

        if isinstance(target_type, str):
            clean_name = target_type.split(".")[-1].strip().lower()
            mapped = self.CLASS_NAME_MAPPING.get(clean_name)
            if mapped is not None:
                return mapped

        type_indicator = data.get("type")
        if type_indicator and isinstance(type_indicator, str):
            clean_indicator = type_indicator.split(".")[-1].strip().lower()
            mapped = self.CLASS_NAME_MAPPING.get(clean_indicator)
            if mapped is not None:
                return mapped

        keys = set(data.keys())
        for required_keys, cls in self.MODEL_SIGNATURES:
            if required_keys.issubset(keys):
                return cls

        return None

    def _build_init_kwargs(self, model_cls: type, data: dict) -> dict:
        """
        Формирует словарь аргументов конструктора модели.
        """
        parameters = inspect.signature(model_cls.__init__).parameters
        kwargs = {}

        for param_name, param in parameters.items():
            if param_name in ("self", "args", "kwargs"):
                continue

            if param_name in data:
                kwargs[param_name] = self._resolve_field(param_name, data[param_name], model_cls)

        return kwargs

    def _populate_remaining_properties(
        self,
        instance: object,
        model_cls: type,
        data: dict,
        handled_keys: set,
    ) -> None:
        """
        Заполняет свойства модели, не вошедшие в конструктор, пропуская вычисляемые поля.
        """
        for prop_name, prop_value in data.items():
            if prop_name in handled_keys or prop_name in ("id", "type"):
                continue

            class_prop = getattr(model_cls, prop_name, None)
            if not isinstance(class_prop, property) or class_prop.fset is None:
                continue

            resolved_val = self._resolve_field(prop_name, prop_value, model_cls)
            try:
                setattr(instance, prop_name, resolved_val)
            except AttributeError:
                continue

    def _resolve_field(self, prop_name: str, prop_value: object, model_cls: type) -> object:
        """
        Рекурсивно преобразует значение поля с учетом метаданных типов модели.
        """
        if prop_value is None:
            return None

        field_meta = self.MODEL_FIELD_TYPES.get(model_cls, {}).get(prop_name)

        if isinstance(field_meta, tuple) and len(field_meta) == 2:
            container_type, element_type = field_meta
            if isinstance(prop_value, (list, tuple)):
                items = [self._resolve_value_by_type(item, element_type) for item in prop_value]
                return container_type(items)

        if isinstance(field_meta, type):
            return self._resolve_value_by_type(prop_value, field_meta)

        if self.__factory is not None:
            return self.__factory.deserialize_value(prop_value)

        return prop_value

    def _resolve_value_by_type(self, value: object, target_type: type) -> object:
        """
        Преобразует единичное значение в целевой тип.
        """
        if value is None:
            return None

        if isinstance(value, target_type):
            return value

        if issubclass(target_type, Enum):
            if isinstance(value, int):
                return target_type(value)
            if isinstance(value, str):
                from_str = getattr(target_type, "from_string", None)
                if callable(from_str):
                    return from_str(value)
                return target_type[value]

        if issubclass(target_type, abstract_model):
            return self.deserialize(value, target_type)

        if self.__factory is not None:
            return self.__factory.deserialize_value(value, target_type)

        return value
