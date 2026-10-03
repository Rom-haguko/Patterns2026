from src.core.abstract_model import abstract_model
from src.models.organization_model import organization_model


class settings_model(abstract_model):
    """
    Модель настроек приложения.
    Хранит информацию о компании (организации), руководителе и главном бухгалтере.
    """

    def __init__(self, name: str = None) -> None:
        """
        Инициализирует модель настроек.
        """
        super().__init__(name=name)
        self.__company: organization_model = None
        self.__boss_name: str = ""
        self.__account_name: str = ""

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