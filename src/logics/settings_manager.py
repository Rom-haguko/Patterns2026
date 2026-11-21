import json
from src.core.abstract_manager import abstract_manager
from src.core.exception import operation_exception
from src.core.file_resolver import file_path_resolver
from src.core.validator import validator
from src.models.settings_model import settings_model
from src.logics.deserializer_factory import deserializer_factory


class settings_manager(abstract_manager):
    """
    Менеджер для работы с настройками приложения.
    Реализует паттерн Одиночка (Singleton) для централизованного доступа к конфигурации.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
            cls.instance._initialized = False
        return cls.instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.__default_file_name: str = "settings.json"
        self.__settings: settings_model = settings_model()
        self.__data: dict = {}
        self.__is_loaded: bool = False
        self._initialized = True

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства экземпляров менеджера настроек.
        """
        return isinstance(other, settings_manager)

    @property
    def settings(self) -> settings_model:
        """
        Загруженные настройки приложения.
        """
        return self.__settings

    @settings.setter
    def settings(self, value: settings_model) -> None:
        """
        Устанавливает актуальные настройки приложения.
        """
        self.__settings = value

    @property
    def is_loaded(self) -> bool:
        """
        Флаг завершения загрузки.
        """
        return self.__is_loaded

    @property
    def data(self) -> dict:
        """
        Сырые данные настроек.
        """
        return self.__data

    def convert(self) -> bool:
        """
        Обработка загруженных сырых данных JSON и преобразование в модель settings_model
        с использованием фабрики-десериализатора deserializer_factory.
        """
        if not isinstance(self.__data, dict):
            return False

        factory = deserializer_factory()
        self.__settings = factory.deserialize_value(self.__data, settings_model)
        return True

    def load(self, file_name: str = "") -> None:
        """
        Загрузка данных из конфигурационного файла согласно контракту abstract_manager.

        :param file_name: Путь к файлу конфигурации (по умолчанию settings.json).
        :raises operation_exception: При ошибке загрузки или валидации данных.
        """
        inner_file_name = file_name.strip() if file_name and file_name.strip() != "" else self.__default_file_name
        validator.validate(inner_file_name, str)

        resolved_file = file_path_resolver.resolve(inner_file_name, __file__)

        try:
            with open(resolved_file, "r", encoding="utf-8") as file:
                self.__data = json.load(file)
                self.__is_loaded = self.convert()
        except Exception as ex:
            raise operation_exception(f"Ошибка при загрузке и обработке данных: {ex}")
