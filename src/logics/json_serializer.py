import json
from src.logics.convert_factory import convert_factory


class json_serializer:
    """
    Сериализатор объектов в формат JSON.
    Делегирует конвертацию фабрике конверторов.
    """

    def __init__(self, factory: convert_factory = None):
        """
        Инициализирует сериализатор с фабрикой конверторов.

        :param factory: Фабрика конверторов (опционально)
        """
        self.__factory = factory if factory is not None else convert_factory()

    # ─────────── Методы сериализации ───────────

    def convert(self, source: object) -> object:
        """
        Преобразует объект через фабрику конверторов.
        Вся логика подбора конвертора инкапсулирована в фабрике.

        :param source: Исходный объект любого типа
        :return: Преобразованная структура данных
        """
        return self.__factory.convert_value(source)

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