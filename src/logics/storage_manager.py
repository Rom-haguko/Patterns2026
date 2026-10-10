from src.core.abstract_manager import abstract_manager
from src.core.validator import validator
from src.core.file_resolver import FilePathResolver
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model
from src.models.recipe_model import recipe_model


class storage_manager(abstract_manager):
    """
    Менеджер хранилища (кеш в памяти) для централизованного хранения
    и доступа к доменным сущностям: единицам измерения, группам номенклатуры,
    номенклатуре, складам и технологическим картам (рецептам).

    Реализует паттерн Одиночка (Singleton) и контракт abstract_manager.
    При первом создании экземпляра автоматически формирует первичные данные (convert)
    с использованием фабричных методов доменных моделей.
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
        self.__data[self.recipe_key()] = []
        
        # Первый старт: заполнение первичными данными через фабричные методы
        self.convert()
        self._initialized = True

    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства экземпляров менеджера хранилища.
        Два экземпляра равны, если оба являются storage_manager (Singleton).
        """
        return isinstance(other, storage_manager)

    # ──────────────────────────────── Ключи коллекций ──────────────────────────────

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

    @staticmethod
    def recipe_key() -> str:
        """
        Ключ доступа к коллекции технологических карт и рецептов (recipe_model).
        """
        return "recipe_model"

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
        Формирует первичные данные при первом старте приложения с использованием
        фабричных методов доменных моделей.
        Создаёт базовые единицы измерения, группы номенклатуры,
        номенклатурные позиции, склады и технологические карты (рецепты).

        :return: True после успешного формирования первичных данных.
        """
        self._build_ranges()
        self._build_groups()
        self._build_nomenclature()
        self._build_storages()
        self._build_recipes()
        return True

    # ──────────────────────── Вспомогательные методы первого старта ───────────────

    def _build_ranges(self) -> None:
        """
        Создаёт базовые единицы измерения через фабричные методы range_model
        и наполняет ими коллекцию.
        """
        kilogram = range_model.create_kilogramm()
        gram = kilogram.base
        milliliter = range_model.create_milliliter()
        liter = range_model.create_liter(milliliter)
        piece = range_model.create_piece()

        for unit in (gram, kilogram, milliliter, liter, piece):
            self.add(self.range_key(), unit)

    def _build_groups(self) -> None:
        """
        Создаёт базовые группы номенклатуры через фабричные методы nomenclature_group_model
        и наполняет ими коллекцию.
        """
        groups = [
            nomenclature_group_model.create_raw(),
            nomenclature_group_model.create_semi_finished(),
            nomenclature_group_model.create_finished(),
            nomenclature_group_model.create_packaging(),
        ]
        for group in groups:
            self.add(self.group_key(), group)

    def _build_nomenclature(self) -> None:
        """
        Создаёт базовые номенклатурные позиции через фабричный метод nomenclature_model.create
        и наполняет ими коллекцию.
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
        finished_group = find_group("Готовая продукция")
        pack_group = find_group("Упаковка")

        gram = find_range("грамм")
        kilogram = find_range("килограмм")
        milliliter = find_range("миллилитр")
        liter = find_range("литр")
        piece = find_range("штука")

        items = [
            nomenclature_model.create("Мука пшеничная", "Мука пшеничная высший сорт, 50 кг мешок", raw_group, kilogram),
            nomenclature_model.create("Соль", "Соль пищевая поваренная, 1 кг пачка", raw_group, kilogram),
            nomenclature_model.create("Сахар", "Сахар-песок белый кристаллический, 50 кг мешок", raw_group, kilogram),
            nomenclature_model.create("Масло подсолнечное", "Масло подсолнечное рафинированное, 5 л", raw_group, liter if liter else milliliter),
            nomenclature_model.create("Тесто дрожжевое", "Тесто дрожжевое слоёное, полуфабрикат 1 кг", semi_group, kilogram),
            nomenclature_model.create("Соус томатный", "Соус томатный базовый, полуфабрикат 200 г", semi_group, gram),
            nomenclature_model.create("Коробка под пиццу 30 см", "Картонная коробка 300х300х40 мм", pack_group, piece),
            nomenclature_model.create("Пакет бумажный", "Пакет бумажный крафт 20х30 см", pack_group, piece),
            # Позиции, необходимые для рецепта Пицца Маргарита
            nomenclature_model.create("Сыр Моцарелла", "Сыр Моцарелла классический для пиццы", raw_group, gram),
            nomenclature_model.create("Масло оливковое", "Масло оливковое Extra Virgin", raw_group, milliliter),
            nomenclature_model.create("Базилик свежий", "Базилик свежий зелёный листья", raw_group, gram),
            nomenclature_model.create("Соль пищевая", "Соль пищевая мелкого помола", raw_group, gram),
            nomenclature_model.create("Пицца Маргарита", "Пицца Маргарита классическая 30 см", finished_group, piece),
        ]

        for item in items:
            self.add(self.nomenclature_key(), item)

    def _build_storages(self) -> None:
        """
        Создаёт базовые склады через фабричный метод storage_model.create
        и наполняет ими коллекцию.
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
            self.add(self.storage_key(), storage_model.create(name, address))

    def _build_recipes(self) -> None:
        """
        Создаёт технологические карты (рецепты) через фабричные методы recipe_model
        согласно собственной спецификации (Docs/Recipe.md) и наполняет ими коллекцию.
        Формирует рецепт, содержащий полуфабрикаты, а также рецепт с упаковкой.
        """
        ranges = self.get(self.range_key())
        groups = self.get(self.group_key())
        nomenclatures = self.get(self.nomenclature_key())

        # Попытка инициализировать рецепт напрямую из Markdown файла Recipe.md
        recipe_margarita = None
        try:
            recipe_file = FilePathResolver.resolve("Docs/Recipe.md", __file__)
            recipe_margarita = recipe_model.from_file(
                recipe_file,
                ranges=ranges,
                groups=groups,
                nomenclatures=nomenclatures
            )
        except Exception:
            # Резервный вызов фабричного метода при отсутствии файла
            recipe_margarita = recipe_model.create_pizza_margarita(
                ranges=ranges,
                groups=groups,
                nomenclatures=nomenclatures
            )

        if recipe_margarita is not None:
            self.add(self.recipe_key(), recipe_margarita)

        # Рецепт с упаковкой (для курьерской доставки)
        recipe_packaged = recipe_model.create_pizza_with_packaging(
            ranges=ranges,
            groups=groups,
            nomenclatures=nomenclatures
        )
        self.add(self.recipe_key(), recipe_packaged)