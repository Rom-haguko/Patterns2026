from src.core.abstract_model import name_id
from src.core.exception import arguments_exception


class organization_model(name_id):
    """
    Сущность компании / юридического лица.
    Хранит ключевые учетные реквизиты: ИНН, БИК, номер расчетного счета и форму собственности.
    """

    def __init__(
        self,
        name: str = None,
        inn: str = "",
        bik: str = "",
        account: str = "",
        ownership_form: str = "",
        corr_account: str = ""
    ):
        """
        Инициализирует данные компании.

        :param name: Название контрагента (до 50 символов). Необязательный параметр.
        :param inn: ИНН (строка из 10 или 12 цифр). Пустая строка — не заполнен.
        :param bik: Банковский идентификационный код (9 цифр). Пустая строка — не заполнен.
        :param account: Номер р/с (20 цифр). Пустая строка — не заполнен.
        :param ownership_form: ОПФ / форма собственности (например, "ООО", "ИП", до 5 символов). Пустая строка — не заполнена.
        :param corr_account: Корреспондентский счет. Пустая строка — не заполнен.
        """
        super().__init__(name=name)
        # Устанавливаем только непустые значения — пустые оставляем без валидации
        self.__inn = ""
        self.__bik = ""
        self.__account = ""
        self.__ownership_form = ""
        self.__corr_account = ""

        if inn:
            self.inn = inn
        if bik:
            self.bik = bik
        if account:
            self.account = account
        if ownership_form:
            self.ownership_form = ownership_form
        if corr_account:
            self.corr_account = corr_account

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
    def bic(self) -> str:
        """
        Псевдоним (алиас) для свойства bik. Используется для обратной совместимости.
        """
        return self.__bik

    @bic.setter
    def bic(self, value):
        """
        Сеттер-алиас для bik.
        """
        self.bik = value

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

    @property
    def ownership(self) -> str:
        """
        Псевдоним (алиас) для свойства ownership_form. Используется для обратной совместимости.
        """
        return self.__ownership_form

    @ownership.setter
    def ownership(self, value):
        """
        Сеттер-алиас для ownership_form.
        """
        self.ownership_form = value

    @property
    def corr_account(self) -> str:
        """
        Возвращает корреспондентский счет.
        """
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value):
        """
        Устанавливает корреспондентский счет. Допускается пустое значение.
        """
        if value is None:
            self.__corr_account = ""
            return
        if not isinstance(value, (str, int)):
            raise arguments_exception("corr_account", "Корр. счет должен быть строкой или числом")
        val_str = str(value).strip()
        if val_str and not val_str.isdigit():
            raise arguments_exception("corr_account", "Корр. счет может содержать только цифры")
        self.__corr_account = val_str

    @staticmethod
    def create(
        name: str = None,
        inn: str = "",
        bik: str = "",
        account: str = "",
        ownership_form: str = "",
        corr_account: str = ""
    ) -> 'organization_model':
        """
        Фабричный метод создания объекта организации.

        :param name: Название контрагента
        :param inn: ИНН (10 или 12 цифр)
        :param bik: БИК (9 цифр)
        :param account: Номер расчетного счета (20 цифр)
        :param ownership_form: Форма собственности (до 5 символов)
        :param corr_account: Корреспондентский счет
        :return: Экземпляр organization_model
        """
        return organization_model(
            name=name,
            inn=inn,
            bik=bik,
            account=account,
            ownership_form=ownership_form,
            corr_account=corr_account
        )