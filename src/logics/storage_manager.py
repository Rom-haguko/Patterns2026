from src.core.abstract_manager import abstract_manager
from src.core.validator import validator
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


class storage_manager(abstract_manager):
    """
    Менеджер хранилища (кеш в памяти) для централизованного хранения
    и доступа к доменным сущностям: единицам измерения, группам номенклатуры,
    номенклатуре и складам.

    Реализует паттерн Одиночка (Singleton) и контракт abstract_manager.
    При первом создании экземпляра автоматически формирует первичные данные (convert).
    """

    # Внутренний словарь-хранилище кешированных списков доменных сущностей
    __data: dict = {}

    def __new__(cls, *args, **kwargs):
        """
        Конструктор Singleton: гарантирует единственный экземпляр класса в памяти.
        """
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
            cls.instance._initialized = False 
        return cls.instance

    def __init__(self):
        """
        Инициализация состояния менеджера и первичных данных.
        Благодаря флагу _initialized реальная настройка происходит только при первом запуске.
        """
        # Если уже инициализирован, просто выходим (защита от повторного сброса данных)
        if getattr(self, "_initialized", False):
            return

        self.__data = {}
        # Инициализация пустых списков под каждую доменную сущность
        self.__data[self.range_key()] = []
        self.__data[self.nomenclature_key()] = []
        self.__data[self.group_key()] = []
        self.__data[self.storage_key()] = []
        
        # Первый старт: заполнение первичными данными
        self.convert()
        self._initialized = True

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства экземпляров менеджера хранилища.
        Два экземпляра равны, если оба являются storage_manager (Singleton).
        """
        return isinstance(other, storage_manager)



    @staticmethod
    def range_key() -> str:
        """
        Ключ доступа к коллекции единиц измерения (range_model).
        """
        return "range_model"

    @staticmethod
    def nomenclature_key() -> str:
        """
        Ключ доступа к коллекции номенклатурных позиций (nomenclature_model).
        """
        return "nomenclature_model"

    @staticmethod
    def group_key() -> str:
        """
        Ключ доступа к коллекции групп номенклатуры (nomenclature_group_model).
        """
        return "nomenclature_group_model"

    @staticmethod
    def storage_key() -> str:
        """
        Ключ доступа к коллекции складов (storage_model).
        """
        return "storage_model"

    # ──────────────────────────────── Свойства ─────────────────────────────────────

    @property
    def data(self) -> dict:
        """
        Полный словарь кешированных коллекций доменных сущностей.
        """
        return self.__data

    # ──────────────────────────────── Методы ───────────────────────────────────────

    def get(self, key: str) -> list:
        """
        Возвращает список объектов из кеша по ключу типа сущности.

        :param key: Текстовый ключ коллекции (например, storage_manager.range_key()).
        :return: Список объектов соответствующей модели.
        """
        validator.validate(key, str)
        if key not in self.__data:
            self.__data[key] = []
        return self.__data[key]

    def add(self, key: str, item: object) -> bool:
        """
        Добавляет объект в коллекцию по ключу, если он ещё не присутствует.
        Уникальность определяется через __eq__ доменной модели (сравнение по id).

        :param key: Текстовый ключ коллекции.
        :param item: Объект доменной модели для добавления.
        :return: True, если объект добавлен; False, если дубликат.
        """
        validator.validate(key, str)
        if item is None:
            return False
        collection = self.get(key)
        if item in collection:
            # Объект уже присутствует — дубликат не добавляем
            return False
        collection.append(item)
        return True

    def convert(self) -> bool:
        """
        Формирует первичные данные при первом старте приложения.
        Создаёт базовые единицы измерения, группы номенклатуры,
        номенклатурные позиции и склады.

        :return: True после успешного формирования первичных данных.
        """
        self._build_ranges()
        self._build_groups()
        self._build_nomenclature()
        self._build_storages()
        return True

    # ──────────────────────── Вспомогательные методы первого старта ───────────────

    def _build_ranges(self) -> None:
        """
        Создаёт базовые единицы измерения и наполняет ими коллекцию.
        Формируется минимальный необходимый справочник: граммы, килограммы,
        миллилитры, литры, штуки.
        """
        kilogram = range_model.create_kilogramm()
        gram = kilogram.base  
        milliliter = range_model("миллилитр", 1)
        liter = range_model("литр", 1000, milliliter)
        piece = range_model("штука", 1)

        for unit in (gram, kilogram, milliliter, liter, piece):
            self.add(self.range_key(), unit)

    def _build_groups(self) -> None:
        """
        Создаёт базовые группы номенклатуры и наполняет ими коллекцию.
        Группы соответствуют основным категориям продуктов ресторана «Ромашка».
        """
        group_names = [
            "Сырьё",
            "Полуфабрикаты",
            "Готовая продукция",
            "Упаковка",
        ]
        for name in group_names:
            self.add(self.group_key(), nomenclature_group_model(name))

    def _build_nomenclature(self) -> None:
        """
        Создаёт базовые номенклатурные позиции и наполняет ими коллекцию.
        Для каждой позиции устанавливаются группа и единица измерения
        из уже сформированных справочников.
        """
        ranges = self.get(self.range_key())
        groups = self.get(self.group_key())

        # Вспомогательные функции поиска по имени
        def find_range(name: str) -> range_model:
            return next((r for r in ranges if r.name == name), None)

        def find_group(name: str) -> nomenclature_group_model:
            return next((g for g in groups if g.name == name), None)

        raw_group = find_group("Сырьё")
        semi_group = find_group("Полуфабрикаты")
        pack_group = find_group("Упаковка")
        gram = find_range("грамм")
        kilogram = find_range("килограмм")
        milliliter = find_range("миллилитр")
        liter = find_range("литр")
        piece = find_range("штука")

        items = [
            nomenclature_model("Мука пшеничная", "Мука пшеничная высший сорт, 50 кг мешок", raw_group, kilogram),
            nomenclature_model("Соль", "Соль пищевая поваренная, 1 кг пачка", raw_group, kilogram),
            nomenclature_model("Сахар", "Сахар-песок белый кристаллический, 50 кг мешок", raw_group, kilogram),
            nomenclature_model("Масло подсолнечное", "Масло подсолнечное рафинированное, 5 л", raw_group, liter if liter else milliliter),
            nomenclature_model("Тесто дрожжевое", "Тесто дрожжевое слоёное, полуфабрикат 1 кг", semi_group, kilogram),
            nomenclature_model("Соус томатный", "Соус томатный базовый, полуфабрикат 200 г", semi_group, gram),
            nomenclature_model("Коробка под пиццу 30 см", "Картонная коробка 300х300х40 мм", pack_group, piece),
            nomenclature_model("Пакет бумажный", "Пакет бумажный крафт 20х30 см", pack_group, piece),
        ]

        for item in items:
            self.add(self.nomenclature_key(), item)

    def _build_storages(self) -> None:
        """
        Создаёт базовые склады и наполняет ими коллекцию.
        Соответствуют реальной топологии компании «Ромашка»: производственный цех
        и склады при каждом ресторане.
        """
        storages_data = [
            ("Производственный цех", "г. Москва, ул. Цветочная, д. 10"),
            ("Склад Ресторан №1 (Центральный)", "г. Москва, ул. Центральная, д. 1"),
            ("Склад Ресторан №2 (Север)", "г. Москва, ул. Северная, д. 2"),
            ("Склад Ресторан №3 (Юг)", "г. Москва, ул. Южная, д. 3"),
            ("Склад Ресторан №4 (Доставка 1)", "г. Москва, ул. Доставочная, д. 4"),
            ("Склад Ресторан №5 (Доставка 2)", "г. Москва, ул. Доставочная, д. 5"),
        ]
        for name, address in storages_data:
            self.add(self.storage_key(), storage_model(name, address))