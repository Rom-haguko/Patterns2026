import json
import os
from src.core.abstract_manager import abstract_manager
from src.core.validator import validator, operation_exception
from src.models.settings_model import settings_model
from src.models.organization_model import organization_model
from src.core.file_resolver import FilePathResolver


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

    def _get_first_valid(self, data_dict: dict, keys: list) -> str:
        """
        Ищет в словаре первое непустое значение по списку ключей.
        Удобно для обработки опечаток и альтернативных названий полей в JSON.
        """
        for key in keys:
            if key in data_dict and data_dict[key]:
                return str(data_dict[key]).strip()
        return ""

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
            
            # Безопасное присвоение (только если значение не пустое)
            name_val = self._get_first_valid(comp_dict, ["name"])
            if name_val: company.name = name_val
            
            inn_val = self._get_first_valid(comp_dict, ["inn"])
            if not inn_val and "inn_kpp" in comp_dict and comp_dict["inn_kpp"]:
                inn_part = str(comp_dict["inn_kpp"]).split("/")[0].strip()
                if len(inn_part) in (10, 12) and inn_part.isdigit():
                    inn_val = inn_part
            if inn_val: company.inn = inn_val

            bik_val = self._get_first_valid(comp_dict, ["bik", "bic"])
            if bik_val: company.bik = bik_val

            account_val = self._get_first_valid(comp_dict, ["account"])
            if account_val: company.account = account_val

            ownership_val = self._get_first_valid(comp_dict, ["ownership_form", "ownership"])
            if ownership_val: company.ownership_form = ownership_val

            self.__settings.company = company

        # Маппинг полей руководителя и бухгалтера
        boss_val = self._get_first_valid(self.__data, ["boss_name"])
        if not boss_val and "company" in self.__data and isinstance(self.__data["company"], dict):
            boss_val = self._get_first_valid(self.__data["company"], ["ceo"])
        if boss_val:
            self.__settings.boss_name = boss_val
            
        acc_name_val = self._get_first_valid(self.__data, ["account_name"])
        if acc_name_val:
            self.__settings.account_name = acc_name_val

        return True
    

    def load(self, file_name: str = "") -> bool:
        # ... (валидация и определение inner_file_name остаются)
        inner_file_name = file_name.strip() if file_name and file_name.strip() != "" else self.__default_file_name
        validator.validate(inner_file_name, str)

        # Делегируем поиск файла отдельному резолверу
        resolved_file = FilePathResolver.resolve(inner_file_name, __file__)

        try:
            with open(resolved_file, "r", encoding="utf-8") as file:
                self.__data = json.load(file)
                self.__is_loaded = self.convert()
                return self.__is_loaded
        except Exception as ex:
            raise operation_exception(f"Ошибка при загрузке и обработке данных: {ex}")