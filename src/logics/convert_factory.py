from datetime import datetime, date, time
from enum import Enum
from src.core.abstract_covertor import abstract_covertor
from src.core.abstract_convertor_factory import abstract_convertor_factory
from src.core.validator import argument_exception
from src.logics.basic_convertor import basic_convertor
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor


class convert_factory(abstract_convertor_factory):
    """
    Фабрика конвертации объектов в словари.
    Реализует паттерн Фабрика через словарь маппинга типов.
    """

    __mapping: dict[type, abstract_covertor]

    def __init__(self):
        """
        Инициализирует фабрику с регистрацией конверторов в словаре.
        """
        self.__basic_convertor = basic_convertor()
        self.__datetime_convertor = datetime_convertor()
        self.__reference_convertor = reference_convertor(self)

        # Словарь маппинга типов на конверторы (как в report_factory)
        self.__mapping = {}
        self.__mapping[int] = self.__basic_convertor
        self.__mapping[float] = self.__basic_convertor
        self.__mapping[str] = self.__basic_convertor
        self.__mapping[bool] = self.__basic_convertor
        self.__mapping[datetime] = self.__datetime_convertor
        self.__mapping[date] = self.__datetime_convertor
        self.__mapping[time] = self.__datetime_convertor

    # ─────────── Свойства конверторов ───────────

    @property
    def basic_convertor(self) -> basic_convertor:
        """
        Конвертор простых типов.
        """
        return self.__basic_convertor

    @property
    def datetime_convertor(self) -> datetime_convertor:
        """
        Конвертор даты и времени.
        """
        return self.__datetime_convertor

    @property
    def reference_convertor(self) -> reference_convertor:
        """
        Конвертор ссылочных типов.
        """
        return self.__reference_convertor

    # ─────────── Выбор конвертора ───────────

    def get_convertor(self, value_or_type: object) -> abstract_covertor:
        """
        Возвращает подходящий конвертор по типу данных или значению.
        Использует словарь маппинга для подбора.

        :param value_or_type: Тип данных или экземпляр объекта
        :return: Экземпляр абстрактного конвертора
        """
        if value_or_type is None:
            return self.__reference_convertor

        # Если передан тип (класс)
        if isinstance(value_or_type, type):
            for key_type, convertor in self.__mapping.items():
                if issubclass(value_or_type, key_type):
                    return convertor
            return self.__reference_convertor

        # Если передан экземпляр
        for key_type, convertor in self.__mapping.items():
            if isinstance(value_or_type, key_type):
                return convertor

        return self.__reference_convertor

    def convert_value(self, source: object) -> object:
        """
        Конвертирует значение в примитивный тип для сериализации.
        Использует полиморфизм через конверторы.

        :param source: Исходное значение
        :return: Примитивное значение (str, int, float, bool, dict, list)
        """
        if source is None:
            return None

        # Перечисления сохраняем как их значение, если оно примитивное
        if isinstance(source, Enum):
            enum_value = source.value
            if isinstance(enum_value, (str, int, float, bool)) or enum_value is None:
                return enum_value
            return source.name

        # Обработка словарей
        if isinstance(source, dict):
            return {str(k): self.convert_value(v) for k, v in source.items()}

        # Обработка списков, кортежей, множеств
        if isinstance(source, (list, tuple, set)):
            return [self.convert_value(item) for item in source]

        # Подбираем конвертор по типу значения
        convertor = self.get_convertor(source)

        # Делегируем конвертацию конвертору
        result = convertor.convert("value", source)
        converted = result["value"]

        if converted == {}:
            raise argument_exception(f"Неподдерживаемый тип для сериализации: {type(source)}")

        return converted