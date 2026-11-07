from datetime import datetime, date, time
from enum import Enum
from src.core.abstract_deserializer import abstract_deserializer
from src.core.abstract_deserializer_factory import abstract_deserializer_factory
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.logics.basic_deserializer import basic_deserializer
from src.logics.datetime_deserializer import datetime_deserializer
from src.logics.deserialization_context import deserialization_context
from src.logics.model_deserializer import model_deserializer
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model
from src.models.settings_model import settings_model
from src.models.storage_model import storage_model


class deserializer_factory(abstract_deserializer_factory):
    """
    Фабрика десериализаторов данных в доменные модели и базовые типы.
    Осуществляет диспетчеризацию по словарю типов и строковых ключей.
    """

    def __init__(self, context: deserialization_context = None):
        """
        Инициализирует фабрику с регистрацией десериализаторов и сопоставлений типов.

        :param context: Контекст реестра идентичности
        """
        self.__context = context if context is not None else deserialization_context()
        self.__basic_deserializer = basic_deserializer()
        self.__datetime_deserializer = datetime_deserializer()
        self.__model_deserializer = model_deserializer(self, self.__context)

        self.__type_mapping: dict[type, abstract_deserializer] = {
            int: self.__basic_deserializer,
            float: self.__basic_deserializer,
            str: self.__basic_deserializer,
            bool: self.__basic_deserializer,
            datetime: self.__datetime_deserializer,
            date: self.__datetime_deserializer,
            time: self.__datetime_deserializer,
        }

        self.__key_mapping: dict[str, type] = {
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
            "recipe_step_model": recipe_step_model,
            "organization_model": organization_model,
            "organization": organization_model,
            "settings_model": settings_model,
            "settings": settings_model,
        }

    @property
    def context(self) -> deserialization_context:
        """
        Контекст десериализации (реестр идентичности).
        """
        return self.__context

    @property
    def basic_deserializer(self) -> basic_deserializer:
        """
        Десериализатор простых типов.
        """
        return self.__basic_deserializer

    @property
    def datetime_deserializer(self) -> datetime_deserializer:
        """
        Десериализатор дат и времени.
        """
        return self.__datetime_deserializer

    @property
    def model_deserializer(self) -> model_deserializer:
        """
        Десериализатор доменных моделей.
        """
        return self.__model_deserializer

    def get_deserializer(self, target_type_or_key: object) -> abstract_deserializer:
        """
        Возвращает подходящий десериализатор по типу данных или строковому ключу.

        :param target_type_or_key: Тип данных или имя сущности
        :return: Экземпляр десериализатора
        """
        if isinstance(target_type_or_key, str):
            resolved_cls = self.__key_mapping.get(target_type_or_key.strip().lower())
            if resolved_cls is not None:
                return self.__model_deserializer
            return self.__basic_deserializer

        if isinstance(target_type_or_key, type):
            direct = self.__type_mapping.get(target_type_or_key)
            if direct is not None:
                return direct

            if issubclass(target_type_or_key, abstract_model):
                return self.__model_deserializer

            for registered_type, handler in self.__type_mapping.items():
                if issubclass(target_type_or_key, registered_type):
                    return handler

        return self.__model_deserializer

    def deserialize_value(self, data: object, target_type: object = None) -> object:
        """
        Рекурсивно преобразует сырые структуры в объекты целевого типа.

        :param data: Исходные данные
        :param target_type: Целевой класс или строковое имя сущности
        :return: Восстановленный объект
        """
        if data is None:
            return None

        actual_target_type = target_type
        if isinstance(target_type, str):
            actual_target_type = self.__key_mapping.get(target_type.strip().lower())

        if isinstance(data, list):
            element_type = None
            if isinstance(actual_target_type, tuple) and len(actual_target_type) == 2:
                element_type = actual_target_type[1]
            elif isinstance(actual_target_type, type) and issubclass(actual_target_type, abstract_model):
                element_type = actual_target_type

            return [self.deserialize_value(item, element_type) for item in data]

        if isinstance(data, dict):
            if isinstance(actual_target_type, type) and issubclass(actual_target_type, abstract_model):
                return self.__model_deserializer.deserialize(data, actual_target_type)

            if actual_target_type is None or actual_target_type is dict:
                is_collections_snapshot = len(data) > 0 and all(k in self.__key_mapping for k in data.keys())
                if is_collections_snapshot:
                    return {
                        k: self.deserialize_value(v, self.__key_mapping[k])
                        for k, v in data.items()
                    }

                detected_model = self.__model_deserializer._resolve_target_type(data)
                if detected_model is not None:
                    return self.__model_deserializer.deserialize(data, detected_model)

                return {k: self.deserialize_value(v) for k, v in data.items()}

        if isinstance(actual_target_type, type):
            deserializer = self.get_deserializer(actual_target_type)
            return deserializer.deserialize(data, actual_target_type)

        return data
