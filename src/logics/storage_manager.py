from src.core.abstract_manager import abstract_manager
from src.core.validator import validator


class storage_manager(abstract_manager):
    """
    Менеджер хранилища (кеш в памяти) для централизованного хранения 
    и доступа к доменным сущностям (единицам измерения, номенклатуре, группам и складам).
    Реализует паттерн Одиночка (Singleton).
    """

    # Внутренний словарь-хранилище кешированных данных
    __data: dict = {}

    def __new__(cls, *args, **kwargs):
        """
        Конструктор Singleton для гарантирования единственного экземпляра класса в памяти.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(storage_manager, cls).__new__(cls)
            cls.instance.__data = {}
            # Инициализация пустых списков под каждую доменную сущность
            cls.instance.__data[cls.range_key()] = []
            cls.instance.__data[cls.nomenclature_key()] = []
            cls.instance.__data[cls.group_key()] = []
            cls.instance.__data[cls.storage_key()] = []
        return cls.instance

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства экземпляров менеджера хранилища.
        """
        return isinstance(other, storage_manager)

    @staticmethod
    def range_key() -> str:
        """
        Ключ доступа к категории единиц измерения (range_model).
        """
        return "range_model"

    @staticmethod
    def nomenclature_key() -> str:
        """
        Ключ доступа к категории номенклатуры (nomenclature_model).
        """
        return "nomenclature_model"

    @staticmethod
    def group_key() -> str:
        """
        Ключ доступа к категории групп номенклатуры (nomenclature_group_model).
        """
        return "nomenclature_group_model"

    @staticmethod
    def storage_key() -> str:
        """
        Ключ доступа к категории складов (storage_model).
        """
        return "storage_model"

    @property
    def data(self) -> dict:
        """
        Свойство для получения полного словаря кешированных данных.
        """
        return self.__data

    def get(self, key: str) -> list:
        """
        Получить список объектов из кеша по ключу типа сущности.

        :param key: Текстовый ключ категории (например, storage_manager.range_key()).
        :return: Список объектов соответствующей модели.
        """
        validator.validate(key, str)
        if key not in self.__data:
            self.__data[key] = []
        return self.__data[key]