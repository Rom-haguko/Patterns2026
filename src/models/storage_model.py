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

    @classmethod
    def create_from_dict(cls, data: dict) -> "storage_model":
        """
        Фабричный метод создания склада из словаря.

        :param data: Словарь с данными склада
        :return: Экземпляр storage_model
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Для создания storage_model требуется словарь")

        from src.logics.deserialization_context import deserialization_context

        context = deserialization_context()
        entity_id = str(data.get("id", "")).strip()
        if entity_id:
            cached = context.get(entity_id)
            if cached is not None:
                return cached

        name = data.get("name", "")
        address = data.get("address", "")
        instance = cls(name=name, address=address)
        if entity_id:
            instance.id = entity_id
            context.register(instance)

        return instance