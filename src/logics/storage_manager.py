from src.core.abstract_manager import abstract_manager
from src.core.validator import validator
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model
from src.models.recipe_model import recipe_model
from src.models.organization_model import organization_model
from src.models.settings_model import settings_model
from src.models.turnover_model import turnover_model
from src.dtos.turnover_type_enum import turnover_type_enum


class storage_manager(abstract_manager):
    """
    Менеджер хранилища (кеш в памяти) для централизованного хранения
    и доступа к доменным сущностям: единицам измерения, группам номенклатуры,
    номенклатуре, складам и технологическим картам (рецептам).

    Реализует паттерн Одиночка (Singleton) и контракт abstract_manager.
    Базовое хранилище отвечает исключительно за сохранение (save/add) и загрузку (load/get).
    Любые операции изменения и удаления состояния инкапсулируются в сервисах.
    """

    __data: dict = {}
    __entity_registry: dict[str, type] = {}

    @classmethod
    def register_entity_type(cls, model_class: type, *keys: str) -> None:
        """
        Регистрирует класс доменной модели в универсальном реестре хранилища.
        """
        if not isinstance(model_class, type):
            return
        name = model_class.__name__.lower()
        cls.__entity_registry[name] = model_class
        clean_name = name.replace("_model", "")
        cls.__entity_registry[clean_name] = model_class
        full_type = f"{model_class.__module__}.{model_class.__qualname__}".lower()
        cls.__entity_registry[full_type] = model_class
        for k in keys:
            if isinstance(k, str) and k.strip():
                cls.__entity_registry[k.strip().lower()] = model_class

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
        if getattr(self, "_initialized", False):
            return

        self.register_entity_type(range_model, "единица_измерения", "range")
        self.register_entity_type(nomenclature_group_model, "группа_номенклатуры", "group", "nomenclature_group")
        self.register_entity_type(nomenclature_model, "номенклатура", "nomenclature")
        self.register_entity_type(storage_model, "склад", "storage")
        self.register_entity_type(recipe_model, "рецепт", "recipe")
        self.register_entity_type(organization_model, "организация", "organization", "company")
        self.register_entity_type(settings_model, "настройки", "settings")
        self.register_entity_type(turnover_model, "оборот", "turnover", "движение")

        self.__data = {}
        self.__data[self.range_key()] = []
        self.__data[self.nomenclature_key()] = []
        self.__data[self.group_key()] = []
        self.__data[self.storage_key()] = []
        self.__data[self.recipe_key()] = []
        self.__data[self.organization_key()] = []
        self.__data[self.settings_key()] = []
        self.__data[self.turnover_key()] = []
        self._initialized = True

        self.convert()

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
        return range_model.__name__

    @staticmethod
    def nomenclature_key() -> str:
        """
        Ключ доступа к коллекции номенклатурных позиций (nomenclature_model).
        """
        return nomenclature_model.__name__

    @staticmethod
    def group_key() -> str:
        """
        Ключ доступа к коллекции групп номенклатуры (nomenclature_group_model).
        """
        return nomenclature_group_model.__name__

    @staticmethod
    def storage_key() -> str:
        """
        Ключ доступа к коллекции складов (storage_model).
        """
        return storage_model.__name__

    @staticmethod
    def recipe_key() -> str:
        """
        Ключ доступа к коллекции технологических карт и рецептов (recipe_model).
        """
        return recipe_model.__name__

    @staticmethod
    def organization_key() -> str:
        """
        Ключ доступа к коллекции организаций (organization_model).
        """
        return organization_model.__name__

    @staticmethod
    def settings_key() -> str:
        """
        Ключ доступа к коллекции настроек (settings_model).
        """
        return settings_model.__name__

    @staticmethod
    def turnover_key() -> str:
        """
        Ключ доступа к коллекции складских движений и оборотов (turnover_model).
        """
        return turnover_model.__name__

    @property
    def data(self) -> dict:
        """
        Полный словарь кешированных коллекций доменных сущностей.
        """
        return self.__data

    def load(self, file_name: str = "") -> None:
        """
        Загружает данные из источника в хранилище согласно контракту abstract_manager.
        При передаче пути к файлу импортирует данные из JSON, иначе выполняет convert().

        :param file_name: Путь к файлу источника данных.
        """
        inner_file = file_name.strip() if file_name and isinstance(file_name, str) else ""
        if inner_file:
            self.import_all_from_json(inner_file)
        else:
            self.convert()

    def collection(self, key: str) -> list:
        """
        Возвращает коллекцию сущностей по ключу из хранилища.

        :param key: Текстовый ключ коллекции (например, storage_manager.range_key()).
        :return: Список объектов соответствующей модели.
        """
        validator.validate(key, str)
        if key not in self.__data:
            self.__data[key] = []
        return self.__data[key]

    def get_by_type(self, entity_type: object) -> list | None:
        """
        Возвращает список сущностей по типу класса или наименованию сущности.
        """
        if entity_type is None:
            return None

        if isinstance(entity_type, type):
            return self.collection(entity_type.__name__)

        if not isinstance(entity_type, str):
            return None

        clean = entity_type.strip().lower()
        if not clean:
            return None

        if clean in self.__data:
            return self.collection(clean)

        model_cls = self.__entity_registry.get(clean)
        if model_cls is not None:
            return self.collection(model_cls.__name__)

        return None

    def get_by_type_and_code(self, entity_type: object, code: str) -> object:
        """
        Поиск сущности в хранилище по ее типу и коду (id или наименованию).
        """
        collection = self.get_by_type(entity_type)
        if collection is None:
            return None

        code_str = str(code).strip()
        return next((item for item in collection if str(getattr(item, "id", "")) == code_str or str(getattr(item, "name", "")).strip() == code_str), None)

    def export_all_to_json(self, file_path: str) -> bool:
        """
        Экспортирует все данные из хранилища в один JSON файл.

        :param file_path: Путь к целевому файлу
        :return: True при успешном экспорте
        """
        from src.logics.json_serializer import json_serializer

        serializer = json_serializer()
        all_data = {
            self.range_key(): self.collection(self.range_key()),
            self.nomenclature_key(): self.collection(self.nomenclature_key()),
            self.group_key(): self.collection(self.group_key()),
            self.storage_key(): self.collection(self.storage_key()),
            self.recipe_key(): self.collection(self.recipe_key()),
        }

        serializer.to_json_file(all_data, file_path)
        return True

    def import_all_from_json(self, file_path: str, clear_existing: bool = False) -> bool:
        """
        Импортирует коллекции доменных объектов из JSON-файла.

        :param file_path: Путь к файлу с данными
        :param clear_existing: Флаг очистки существующих данных перед загрузкой
        :return: True при успешном импорте
        """
        from src.logics.json_deserializer import json_deserializer

        deserializer = json_deserializer()
        imported = deserializer.from_json_file(file_path)

        if not isinstance(imported, dict):
            return False

        if clear_existing:
            for collection in self.data.values():
                if isinstance(collection, list):
                    collection.clear()

        for key, items in imported.items():
            if isinstance(items, list):
                for item in items:
                    self.save(key, item)

        return True

    def save(self, key: str, item: object) -> bool:
        """
        Сохраняет объект доменной модели в коллекцию хранилища по ключу,
        если он ещё не присутствует (контракт сохранения данных).

        :param key: Текстовый ключ коллекции.
        :param item: Объект доменной модели для сохранения.
        :return: True, если объект сохранен; False, если дубликат или None.
        """
        validator.validate(key, str)
        if item is None:
            return False
        collection = self.collection(key)
        if item in collection:
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
        self._build_settings()
        self._build_turnovers()
        return True

    def _build_turnovers(self) -> None:
        """
        Создаёт демонстрационные складские движения (приход и расход номенклатуры)
        и сохраняет их в коллекцию хранилища.
        """
        storages = self.collection(self.storage_key())
        nomenclatures = self.collection(self.nomenclature_key())
        ranges = self.collection(self.range_key())

        def find_storage(name: str) -> storage_model:
            return next((s for s in storages if s.name == name), None)

        def find_nomenclature(name: str) -> nomenclature_model:
            return next((n for n in nomenclatures if n.name == name), None)

        def find_range(name: str) -> range_model:
            return next((r for r in ranges if r.name == name), None)

        raw_storage = find_storage("Основной склад сырья")
        finished_storage = find_storage("Склад готовой продукции")

        flour = find_nomenclature("Мука пшеничная")
        sugar = find_nomenclature("Сахар")
        pizza = find_nomenclature("Пицца Маргарита")

        kg = find_range("килограмм")
        piece = find_range("штука")

        if raw_storage and flour and kg:
            # 1. Приход муки на склад сырья (100 кг)
            self.save(
                self.turnover_key(),
                turnover_model.create(raw_storage, flour, kg, 100.0, turnover_type_enum.RECEIPT, name="Приход муки на склад сырья"),
            )
            # 2. Расход муки со склада сырья (20 кг)
            self.save(
                self.turnover_key(),
                turnover_model.create(raw_storage, flour, kg, 20.0, turnover_type_enum.EXPENSE, name="Списание муки на производство"),
            )

        if raw_storage and sugar and kg:
            # 3. Приход сахара на склад сырья (50 кг)
            self.save(
                self.turnover_key(),
                turnover_model.create(raw_storage, sugar, kg, 50.0, turnover_type_enum.RECEIPT, name="Поступление сахара"),
            )
            # 4. Расход сахара со склада сырья (10 кг)
            self.save(
                self.turnover_key(),
                turnover_model.create(raw_storage, sugar, kg, 10.0, turnover_type_enum.EXPENSE, name="Расход сахара на сироп"),
            )

        if finished_storage and pizza and piece:
            # 5. Приход готовой пиццы (15 шт)
            self.save(
                self.turnover_key(),
                turnover_model.create(finished_storage, pizza, piece, 15.0, turnover_type_enum.RECEIPT, name="Выпуск пиццы Маргарита"),
            )
            # 6. Расход пиццы на доставку (5 шт)
            self.save(
                self.turnover_key(),
                turnover_model.create(finished_storage, pizza, piece, 5.0, turnover_type_enum.EXPENSE, name="Отгрузка пиццы курьеру"),
            )

    def _build_settings(self) -> None:
        """
        Загружает настройки и организацию из settings_manager в коллекции хранилища.
        """
        from src.logics.settings_manager import settings_manager
        settings_mgr = settings_manager()
        if not settings_mgr.is_loaded:
            settings_mgr.load()
        if settings_mgr.settings:
            self.save(self.settings_key(), settings_mgr.settings)
            if settings_mgr.settings.company:
                self.save(self.organization_key(), settings_mgr.settings.company)

    def _build_ranges(self) -> None:
        """
        Создаёт базовые единицы измерения через фабричные методы range_model
        и наполняет ими коллекцию.
        """
        kilogram = range_model.create_kilogram()
        gram = kilogram.base_range
        milliliter = range_model.create_milliliter()
        liter = range_model.create_liter(milliliter)
        piece = range_model.create_piece()

        for unit in (gram, kilogram, milliliter, liter, piece):
            self.save(self.range_key(), unit)

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
            self.save(self.group_key(), group)

    def _build_nomenclature(self) -> None:
        """
        Создаёт базовые номенклатурные позиции через фабричный метод nomenclature_model.create
        и наполняет ими коллекцию.
        """
        ranges = self.collection(self.range_key())
        groups = self.collection(self.group_key())

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
            nomenclature_model.create("Вода", "Вода питьевая очищенная", raw_group, liter if liter else milliliter),
            nomenclature_model.create("Дрожжи сухие", "Дрожжи хлебопекарные сухие, 100 г", raw_group, gram if gram else kilogram),
            nomenclature_model.create("Томатная паста", "Томатная паста концентрированная, 1 кг банка", raw_group, kilogram),
            nomenclature_model.create("Сыр Моцарелла", "Сыр Моцарелла для пиццы, 1 кг брусок", raw_group, kilogram),
            nomenclature_model.create("Тесто дрожжевое", "Тесто дрожжевое для основы пиццы", semi_group, kilogram),
            nomenclature_model.create("Соус томатный фирменный", "Соус томатный для основы пиццы", semi_group, kilogram),
            nomenclature_model.create("Коробка для пиццы", "Коробка картонная 30х30 см", pack_group, piece),
            nomenclature_model.create("Пицца Маргарита", "Пицца Маргарита 30 см готовая к употреблению", finished_group, piece),
        ]
        for item in items:
            self.save(self.nomenclature_key(), item)

    def _build_storages(self) -> None:
        """
        Создаёт базовые склады через фабричный метод storage_model.create
        и наполняет ими коллекцию.
        """
        storages = [
            storage_model.create("Основной склад сырья", "г. Москва, ул. Складская, д. 1"),
            storage_model.create("Склад готовой продукции", "г. Москва, ул. Складская, д. 2"),
            storage_model.create("Цеховой склад полуфабрикатов", "г. Москва, Производственный цех №1"),
        ]
        for st in storages:
            self.save(self.storage_key(), st)

    def _build_recipes(self) -> None:
        """
        Создаёт технологические карты (рецепты) через фабричные методы recipe_model.
        Формирует рецепт с полуфабрикатами, а также рецепт с упаковкой.
        """
        ranges = self.collection(self.range_key())
        groups = self.collection(self.group_key())
        nomenclatures = self.collection(self.nomenclature_key())

        recipe_margarita = recipe_model.create_pizza_margarita(
            ranges=ranges, groups=groups, nomenclatures=nomenclatures
        )
        if recipe_margarita:
            self.save(self.recipe_key(), recipe_margarita)

        recipe_packaged = recipe_model.create_pizza_with_packaging(
            ranges=ranges, groups=groups, nomenclatures=nomenclatures
        )
        if recipe_packaged:
            self.save(self.recipe_key(), recipe_packaged)
