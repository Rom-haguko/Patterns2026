from src.core.abstract_model import name_id
from src.core.exception import arguments_exception


class organization_model(name_id):
    """
    Сущность компании / юридического лица.
    Хранит ключевые учетные реквизиты: ИНН, БИК, номер расчетного счета и форму собственности.
    """

    def __init__(
        self, 
        name: str = "", 
        inn: str = "", 
        bik: str = "", 
        account: str = "", 
        ownership_form: str = ""
    ):
        """
        Инициализирует данные компании.

        :param name: Название контрагента (до 50 символов)
        :param inn: ИНН (строка из 10 или 12 цифр)
        :param bik: Банковский идентификационный код (9 цифр)
        :param account: Номер р/с (20 цифр)
        :param ownership_form: ОПФ / форма собственности (например, "ООО", "ИП", до 5 символов)
        """
        super().__init__()
        self.name = name
        self.inn = inn
        self.bik = bik
        self.account = account
        self.ownership_form = ownership_form

    @property
    def inn(self) -> str:
        """
        Возвращает ИНН компании.
        """
        return self.__inn

    @inn.setter
    def inn(self, value):
        """
        Устанавливает ИНН. Валидирует формат: строка из 10 или 12 цифровых символов.
        """
        if not isinstance(value, str):
            raise arguments_exception("inn", "ИНН должен передаваться строкой")

        value = value.strip()

        if not value.isdigit():
            raise arguments_exception("inn", "ИНН может состоять только из цифр")

        if len(value) not in (10, 12):
            raise arguments_exception("inn", "ИНН должен содержать ровно 10 или 12 цифр")

        self.__inn = value

    @property
    def bik(self) -> str:
        """
        Возвращает БИК организации.
        """
        return self.__bik

    @bik.setter
    def bik(self, value):
        """
        Устанавливает БИК. Проверяет наличие ровно 9 цифр.
        """
        if not isinstance(value, str):
            raise arguments_exception("bik", "БИК должен быть строкой")

        value = value.strip()

        if not value.isdigit():
            raise arguments_exception("bik", "БИК должен состоять исключительно из цифр")

        if len(value) != 9:
            raise arguments_exception("bik", "Длина БИК должна составлять 9 цифр")

        self.__bik = value

    @property
    def account(self) -> str:
        """
        Возвращает расчетный счет.
        """
        return self.__account

    @account.setter
    def account(self, value):
        """
        Устанавливает расчетный счет (строка из 20 цифр).
        """
        if not isinstance(value, str):
            raise arguments_exception("account", "Расчетный счет должен быть строковым значением")

        value = value.strip()

        if not value.isdigit():
            raise arguments_exception("account", "Расчетный счет должен состоять только из цифр")

        if len(value) != 20:
            raise arguments_exception("account", "Расчетный счет должен состоять ровно из 20 цифр")

        self.__account = value

    @property
    def ownership_form(self) -> str:
        """
        Возвращает форму собственности.
        """
        return self.__ownership_form

    @ownership_form.setter
    def ownership_form(self, value):
        """
        Устанавливает форму собственности (непустая строка длиной до 5 символов).
        """
        if not isinstance(value, str):
            raise arguments_exception("ownership_form", "Форма собственности должна быть строковым значением")

        value = value.strip()

        if value == "":
            raise arguments_exception("ownership_form", "Форма собственности не может быть пустой")

        if len(value) > 5:
            raise arguments_exception("ownership_form", "Длина формы собственности не может превышать 5 символов")

        self.__ownership_form = value