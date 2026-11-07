from datetime import datetime, date, time
import importlib
from src.core.abstract_deserializer import abstract_deserializer
from src.core.abstract_deserializer_factory import abstract_deserializer_factory
from src.core.abstract_model import abstract_model
from src.logics.basic_deserializer import basic_deserializer
from src.logics.datetime_deserializer import datetime_deserializer
from src.logics.deserialization_context import deserialization_context
from src.logics.model_deserializer import model_deserializer


class deserializer_factory(abstract_deserializer_factory):
    """
    Фабрика десериализаторов данных в доменные модели и базовые типы.
    Осуществляет диспетчеризацию по типам и динамическое разрешение классов моделей.
    """

    def __init__(self, context: deserialization_context = None):
        """
        Инициализирует фабрику с регистрацией десериализаторов.

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

    def _resolve_model_type(self, target_type_or_key: object) -> type | None:
        """
        Динамически разрешает тип доменной модели по объекту, типу или строковому ключу.

        :param target_type_or_key: Тип данных или строковый идентификатор класса
        :return: Класс доменной модели или None
        """
        if isinstance(target_type_or_key, type):
            if issubclass(target_type_or_key, abstract_model):
                return target_type_or_key
            return None

        if not isinstance(target_type_or_key, str) or not target_type_or_key.strip():
            return None

        clean_name = target_type_or_key.strip()

        if "." in clean_name:
            try:
                module_name, class_name = clean_name.rsplit(".", 1)
                module = importlib.import_module(module_name)
                candidate = getattr(module, class_name, None)
                if candidate is not None and isinstance(candidate, type) and issubclass(candidate, abstract_model):
                    return candidate
            except (ImportError, AttributeError):
                pass

        try:
            module = importlib.import_module(f"src.models.{clean_name}")
            candidate = getattr(module, clean_name, None)
            if candidate is not None and isinstance(candidate, type) and issubclass(candidate, abstract_model):
                return candidate
        except (ImportError, AttributeError):
            pass

        return None

    def get_deserializer(self, target_type_or_key: object) -> abstract_deserializer:
        """
        Возвращает подходящий десериализатор по типу данных или строковому ключу.

        :param target_type_or_key: Тип данных или имя сущности
        :return: Экземпляр десериализатора
        """
        if isinstance(target_type_or_key, type):
            direct = self.__type_mapping.get(target_type_or_key)
            if direct is not None:
                return direct

            if issubclass(target_type_or_key, abstract_model):
                return self.__model_deserializer

            for registered_type, handler in self.__type_mapping.items():
                if issubclass(target_type_or_key, registered_type):
                    return handler

        if isinstance(target_type_or_key, str):
            resolved_cls = self._resolve_model_type(target_type_or_key)
            if resolved_cls is not None:
                return self.__model_deserializer
            return self.__basic_deserializer

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
            resolved = self._resolve_model_type(target_type)
            if resolved is not None:
                actual_target_type = resolved

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

            if "type" in data:
                return self.__model_deserializer.deserialize(data)

            if actual_target_type is None or actual_target_type is dict:
                result = {}
                for k, v in data.items():
                    k_type = self._resolve_model_type(k)
                    result[k] = self.deserialize_value(v, k_type)
                return result

        if isinstance(actual_target_type, type):
            deserializer = self.get_deserializer(actual_target_type)
            return deserializer.deserialize(data, actual_target_type)

        return data
