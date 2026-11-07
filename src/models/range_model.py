from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception


class range_model(abstract_model):
    """
    Модель единицы измерения.
    Хранит информацию о базовой единице измерения и коэффициенте пересчёта относительно неё.
    """

    def __init__(
        self, 
        name: str = "", 
        conversion_factor: float = 1, 
        base_range=None
    ):
        """
        Инициализирует объект единицы измерения.

        :param name: Наименование единицы (например, "грамм", "кг")
        :param conversion_factor: Множитель для пересчёта к базовой единице
        :param base_range: Ссылка на базовую единицу (экземпляр range_model) или None
        """
        super().__init__()
        self.name = name
        self.conversion_factor = conversion_factor
        self.base_range = base_range

    @property
    def conversion_factor(self):
        """
        Возвращает значение коэффициента пересчёта относительно базовой единицы.
        """
        return self.__conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value):
        """
        Устанавливает коэффициент пересчёта. Ожидает строго положительное число.
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("conversion_factor", "Коэффициент пересчёта должен являться числом")

        if value <= 0:
            raise arguments_exception("conversion_factor", "Значение коэффициента пересчёта должно быть больше нуля")

        self.__conversion_factor = value

    @property
    def base_range(self):
        """
        Возвращает ссылку на базовую единицу измерения (или None).
        """
        return self.__base_range

    @base_range.setter
    def base_range(self, value):
        """
        Устанавливает базовую единицу измерения.
        Ожидает экземпляр range_model или None.
        """
        if value is not None and not isinstance(value, range_model):
            raise arguments_exception("base_range", "Базовая единица должна являться объектом range_model")

        self.__base_range = value

    @property
    def total_conversion_factor(self) -> float:
        """
        Полный коэффициент пересчёта до корневой базовой единицы измерения.
        """
        factor = float(self.conversion_factor)
        current = self.base_range
        while current is not None:
            factor *= float(current.conversion_factor)
            current = current.base_range
        return factor

    def to_base(self, value: float) -> float:
        """
        Пересчёт количества в базовую единицу измерения.

        :param value: Исходное количество в текущих единицах
        :return: Количество в базовых единицах измерения
        """
        return float(value) * self.total_conversion_factor

    @staticmethod
    def create(name: str = "", conversion_factor: float = 1, base_range=None) -> 'range_model':
        """
        Универсальный фабричный метод для создания единицы измерения.

        :param name: Наименование единицы
        :param conversion_factor: Коэффициент пересчёта относительно базовой
        :param base_range: Базовая единица измерения
        :return: Экземпляр range_model
        """
        return range_model(name=name, conversion_factor=conversion_factor, base_range=base_range)

    @staticmethod
    def create_gram() -> 'range_model':
        """
        Фабричный метод создания единицы измерения 'грамм'.
        """
        return range_model(name="грамм", conversion_factor=1)

    @staticmethod
    def create_kilogram() -> 'range_model':
        """
        Фабричный метод для создания связки 'грамм -> килограмм'.
        """
        gram = range_model.create_gram()
        return range_model(name="килограмм", conversion_factor=1000, base_range=gram)

    @staticmethod
    def create_milliliter() -> 'range_model':
        """
        Фабричный метод создания единицы измерения 'миллилитр'.
        """
        return range_model(name="миллилитр", conversion_factor=1)

    @staticmethod
    def create_liter(base_range=None) -> 'range_model':
        """
        Фабричный метод создания связки 'миллилитр -> литр'.
        """
        base = base_range if base_range is not None else range_model.create_milliliter()
        return range_model(name="литр", conversion_factor=1000, base_range=base)

    @staticmethod
    def create_piece() -> 'range_model':
        """
        Фабричный метод создания единицы измерения 'штука'.
        """
        return range_model(name="штука", conversion_factor=1)

    @classmethod
    def create_from_dict(cls, data: dict) -> "range_model":
        """
        Фабричный метод создания единицы измерения из словаря.

        :param data: Словарь с данными модели
        :return: Экземпляр range_model
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Для создания range_model требуется словарь")

        from src.logics.deserialization_context import deserialization_context

        context = deserialization_context()
        entity_id = str(data.get("id", "")).strip()
        if entity_id:
            cached = context.get(entity_id)
            if cached is not None:
                return cached

        name = data.get("name", "")
        conversion_factor = data.get("conversion_factor", 1)
        base_data = data.get("base_range")
        base_range = None
        if isinstance(base_data, dict):
            base_range = cls.create_from_dict(base_data)
        elif isinstance(base_data, range_model):
            base_range = base_data

        instance = cls(name=name, conversion_factor=conversion_factor, base_range=base_range)
        if entity_id:
            instance.id = entity_id
            context.register(instance)

        return instance
