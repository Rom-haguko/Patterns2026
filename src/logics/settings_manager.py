import json
import os
from src.core.abstract_manager import abstract_manager
from src.core.validator import validator, operation_exception
from src.models.settings_model import settings_model
from src.models.organization_model import organization_model


class settings_manager(abstract_manager):
    """
    Менеджер для работы с настройками приложения.
    Реализует паттерн Одиночка (Singleton) для централизованного доступа к конфигурации.
    """
    __default_file_name: str = "settings.json"

    # Singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
            cls.instance.__default_file_name = "settings.json"
            cls.instance.__settings = settings_model()
            cls.instance.__data = {}
            cls.instance.__is_loaded = False
        return cls.instance

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

    @property
    def setting(self) -> settings_model:
        """
        Псевдоним (алиас) для свойства settings.
        """
        return self.__settings

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
        Обработка загруженных сырых данных JSON и преобразование в модель settings_model.
        """
        if not isinstance(self.__data, dict):
            return False

        self.__settings = settings_model()

        if "company" in self.__data and isinstance(self.__data["company"], dict):
            comp_dict = self.__data["company"]
            company = organization_model()
            if "name" in comp_dict and comp_dict["name"]:
                company.name = comp_dict["name"]
            if "inn" in comp_dict and comp_dict["inn"]:
                company.inn = str(comp_dict["inn"])
            elif "inn_kpp" in comp_dict and comp_dict["inn_kpp"]:
                inn_part = str(comp_dict["inn_kpp"]).split("/")[0].strip()
                if len(inn_part) in (10, 12) and inn_part.isdigit():
                    company.inn = inn_part
            if "bik" in comp_dict and comp_dict["bik"]:
                company.bik = str(comp_dict["bik"])
            elif "bic" in comp_dict and comp_dict["bic"]:
                company.bik = str(comp_dict["bic"])
            if "account" in comp_dict and comp_dict["account"]:
                company.account = str(comp_dict["account"])
            if "ownership_form" in comp_dict and comp_dict["ownership_form"]:
                company.ownership_form = str(comp_dict["ownership_form"])
            elif "ownership" in comp_dict and comp_dict["ownership"]:
                company.ownership_form = str(comp_dict["ownership"])

            self.__settings.company = company

        if "boss_name" in self.__data:
            self.__settings.boss_name = self.__data["boss_name"]
        elif "company" in self.__data and isinstance(self.__data["company"], dict) and "ceo" in self.__data["company"]:
            self.__settings.boss_name = self.__data["company"]["ceo"]

        if "account_name" in self.__data:
            self.__settings.account_name = self.__data["account_name"]

        return True

    def load(self, file_name: str = "") -> bool:
        """
        Загрузка данных из конфигурационного файла.
        
        :param file_name: Путь к файлу конфигурации (по умолчанию settings.json).
        :return: True при успешной загрузке.
        :raises operation_exception: При ошибке загрузки или валидации данных.
        """
        inner_file_name = file_name.strip() if file_name and file_name.strip() != "" else self.__default_file_name
        validator.validate(inner_file_name, str)

        resolved_file = inner_file_name
        if not os.path.isabs(resolved_file) and not os.path.exists(resolved_file):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            candidate = os.path.join(base_dir, inner_file_name)
            if os.path.exists(candidate):
                resolved_file = candidate
            elif inner_file_name in ("settings.json", "seetings.json"):
                for alt in ("settings.json", "seetings.json"):
                    alt_path = os.path.join(base_dir, alt) if not os.path.exists(alt) else alt
                    if os.path.exists(alt_path):
                        resolved_file = alt_path
                        break

        try:
            with open(resolved_file, "r", encoding="utf-8") as file:
                self.__data = json.load(file)
                self.__is_loaded = self.convert()
                return self.__is_loaded
        except Exception as ex:
            raise operation_exception(f"Ошибка при загрузке и обработке данных: {ex}")