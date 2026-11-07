from src.core.abstract_model import abstract_model
from src.models.organization_model import organization_model
from src.dtos.report_type_enum import report_type_enum
from src.core.exception import arguments_exception


class settings_model(abstract_model):
    """
    Модель настроек приложения.
    Хранит информацию о компании (организации), руководителе, главном бухгалтере
    и формате ответа по умолчанию.
    """

    def __init__(self, name: str = None) -> None:
        """
        Инициализирует модель настроек.
        """
        super().__init__(name=name)
        self.__company: organization_model = None
        self.__boss_name: str = ""
        self.__account_name: str = ""
        self.__response_format: report_type_enum = report_type_enum.TXT

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства моделей настроек.
        """
        if not isinstance(other, settings_model):
            return False
        return (
            self.company == other.company
            and self.boss_name == other.boss_name
            and self.account_name == other.account_name
            and self.response_format == other.response_format
        )

    @property
    def company(self) -> organization_model:
        """
        Карточка организации (компании).
        """
        return self.__company

    @company.setter
    def company(self, value: organization_model) -> None:
        """
        Устанавливает организацию (компанию).
        """
        self.__company = value

    @property
    def boss_name(self) -> str:
        """
        ФИО руководителя компании.
        """
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value: str) -> None:
        """
        Устанавливает ФИО руководителя.
        """
        self.__boss_name = str(value).strip() if value is not None else ""

    @property
    def account_name(self) -> str:
        """
        ФИО главного бухгалтера.
        """
        return self.__account_name
    @account_name.setter
    def account_name(self, value: str) -> None:
        """
        Устанавливает ФИО главного бухгалтера.
        """
        self.__account_name = str(value).strip() if value is not None else ""

    @property
    def response_format(self) -> report_type_enum:
        """
        Формат ответа по умолчанию.
        """
        return self.__response_format

    @response_format.setter
    def response_format(self, value: report_type_enum | str) -> None:
        """
        Устанавливает формат ответа по умолчанию.
        """
        if isinstance(value, report_type_enum):
            self.__response_format = value
            return

        if isinstance(value, str):
            self.__response_format = report_type_enum.from_string(value)
            return

        raise arguments_exception(field="response_format", message=f"Некорректный тип для формата ответа: {type(value)}")

    @classmethod
    def create_from_dict(cls, data: dict) -> "settings_model":
        """
        Фабричный метод создания модели настроек из словаря.

        :param data: Словарь с данными настроек
        :return: Экземпляр settings_model
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Для создания settings_model требуется словарь")

        from src.logics.deserialization_context import deserialization_context

        context = deserialization_context()
        entity_id = str(data.get("id", "")).strip()
        if entity_id:
            cached = context.get(entity_id)
            if cached is not None:
                return cached

        name = data.get("name")
        instance = cls(name=name)
        if entity_id:
            instance.id = entity_id
            context.register(instance)

        instance.boss_name = data.get("boss_name", "")
        instance.account_name = data.get("account_name", "")

        company_data = data.get("company")
        if isinstance(company_data, dict):
            instance.company = organization_model.create_from_dict(company_data)
        elif isinstance(company_data, organization_model):
            instance.company = company_data

        resp_format = data.get("response_format")
        if resp_format is not None:
            if isinstance(resp_format, int):
                instance.response_format = report_type_enum(resp_format)
            else:
                instance.response_format = resp_format

        return instance