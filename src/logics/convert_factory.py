import json
from enum import Enum
from datetime import datetime, date, time
from src.core.abstract_covertor import abstract_covertor
from src.logics.basic_convertor import basic_convertor
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor


class convert_factory:
    """
    Фабрика конвертации объектов в словари.
    Подбирает конверторы по типу и собирает итоговую структуру.
    """

    def __init__(self):
        """
        Инициализирует конверторы простых, временных и ссылочных типов.
        """
        self.__basic_convertor = basic_convertor()
        self.__datetime_convertor = datetime_convertor()
        self.__reference_convertor = reference_convertor(self)

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

        :param value_or_type: Тип данных или экземпляр объекта
        :return: Экземпляр абстрактного конвертора
        """
        if value_or_type is None:
            return self.__reference_convertor

        if isinstance(value_or_type, type):
            if issubclass(value_or_type, (int, float, str, bool)):
                return self.__basic_convertor
            if issubclass(value_or_type, (datetime, date, time)):
                return self.__datetime_convertor
            return self.__reference_convertor

        if isinstance(value_or_type, (int, float, str, bool)):
            return self.__basic_convertor

        if isinstance(value_or_type, (datetime, date, time)):
            return self.__datetime_convertor

        return self.__reference_convertor

    # ─────────── Методы сериализации ───────────

    def convert(self, source: object) -> object:
        """
        Преобразует объект любого типа в структуру словарей.

        :param source: Исходный объект любого типа
        :return: Преобразованная структура данных
        """
        if source is None:
            return None

        if isinstance(source, (int, float, str, bool)):
            return source

        if isinstance(source, (datetime, date, time)):
            return self.__datetime_convertor.convert("value", source)["value"]

        if isinstance(source, Enum):
            return source.value

        if isinstance(source, (list, tuple, set)):
            return [self.convert(item) for item in source]

        if isinstance(source, dict):
            return {str(k): self.convert(v) for k, v in source.items()}

        return self.__reference_convertor.convert(source)

    def serialize(self, source: object) -> object:
        """
        Преобразует объект в структуру словарей.
        """
        return self.convert(source)

    def to_json(self, source: object, indent: int = 2) -> str:
        """
        Преобразует объект любого типа в строку JSON.

        :param source: Исходный объект
        :param indent: Величина отступа
        :return: Строка JSON
        """
        data = self.convert(source)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    def to_json_file(self, source: object, file_path: str, indent: int = 2) -> None:
        """
        Сохраняет сериализованный объект в файл JSON.

        :param source: Исходный объект
        :param file_path: Путь к целевому файлу
        :param indent: Величина отступа
        """
        content = self.to_json(source, indent=indent)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
