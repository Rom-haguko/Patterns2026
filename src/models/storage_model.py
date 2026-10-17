from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception


class storage_model(abstract_model):
    """
    Модель склада или места хранения.
    Используется для учета помещений, где хранятся сырье, готовая продукция или материалы.
    """

    def __init__(self, name: str = "", address: str = ""):
        """
        Инициализирует объект склада.

        :param name: Название склада (ограничение до 50 символов)
        :param address: Физический адрес или расположение объекта
        """
        super().__init__()
        self.name = name
        self.address = address

    @property
    def address(self) -> str:
        """
        Возвращает адрес склада.
        """
        return self.__address

    @address.setter
    def address(self, value):
        """
        Устанавливает адрес места хранения. Ожидает строковое значение.
        """
        if not isinstance(value, str):
            raise arguments_exception("address", "Адрес должен быть строковым значением")

        self.__address = value.strip()

    @staticmethod
    def create(name: str = "", address: str = "") -> 'storage_model':
        """
        Фабричный метод создания объекта склада.

        :param name: Название склада (до 50 символов)
        :param address: Физический адрес
        :return: Экземпляр storage_model
        """
        return storage_model(name=name, address=address)

    def to_report_data(self) -> tuple[str, list[str], list[list]]:
        """
        Формирует табличное представление склада для отчетов.
        """
        title = self.name
        headers = ["Код", "Наименование", "Адрес"]
        rows = [[self.id, self.name, self.address]]
        return title, headers, rows