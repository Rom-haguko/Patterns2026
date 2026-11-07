import json
from src.core.exception import arguments_exception
from src.logics.deserializer_factory import deserializer_factory


class json_deserializer:
    """
    Десериализатор объектов из формата JSON в доменные модели и структуры данных.
    Делегирует разбор и восстановление фабрике десериализаторов.
    """

    def __init__(self, factory: deserializer_factory = None):
        """
        Инициализирует десериализатор с фабрикой десериализации.

        :param factory: Фабрика десериализаторов (опционально)
        """
        self.__factory = factory if factory is not None else deserializer_factory()

    @property
    def factory(self) -> deserializer_factory:
        """
        Используемая фабрика десериализаторов.
        """
        return self.__factory

    def from_dict(self, data: object, target_type: object = None) -> object:
        """
        Преобразует структуру Python (словарь или список) в доменный объект или коллекцию.

        :param data: Исходные данные (словарь, список или примитив)
        :param target_type: Целевой класс или строковое имя типа (опционально)
        :return: Восстановленный объект или структура
        """
        if data is None:
            return None

        return self.__factory.deserialize_value(data, target_type)

    def from_json(self, json_string: str, target_type: object = None) -> object:
        """
        Преобразует строку JSON в доменный объект или структуру.

        :param json_string: Строка формата JSON
        :param target_type: Целевой класс или строковое имя типа (опционально)
        :return: Восстановленный объект или структура
        """
        if not isinstance(json_string, str) or not json_string.strip():
            raise arguments_exception("json_string", "Строка JSON не может быть пустой")

        try:
            parsed = json.loads(json_string)
        except Exception as exc:
            raise arguments_exception("json_string", f"Ошибка синтаксиса JSON: {exc}")

        return self.from_dict(parsed, target_type)

    def from_json_file(self, file_path: str, target_type: object = None) -> object:
        """
        Считывает JSON из файла и преобразует его в доменный объект или коллекцию.

        :param file_path: Путь к файлу JSON
        :param target_type: Целевой класс или строковое имя типа (опционально)
        :return: Восстановленный объект или структура
        """
        if not isinstance(file_path, str) or not file_path.strip():
            raise arguments_exception("file_path", "Путь к файлу не может быть пустым")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return self.from_json(content, target_type)
