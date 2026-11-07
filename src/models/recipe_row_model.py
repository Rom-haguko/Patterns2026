from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model


class recipe_row_model(abstract_model):
    """
    Модель строки технологической карты (ингредиента рецепта).
    Хранит информацию о номенклатуре, единице измерения, весе брутто и весе нетто.
    """

    def __init__(
        self,
        nomenclature: nomenclature_model = None,
        brutto: float = 0.0,
        netto: float = 0.0,
        range: range_model = None,
        name: str = None
    ) -> None:
        """
        Инициализирует строку рецепта (ингредиент).

        :param nomenclature: Номенклатурная позиция ингредиента (nomenclature_model)
        :param brutto: Вес брутто ингредиента (неотрицательное число)
        :param netto: Вес нетто ингредиента (неотрицательное число)
        :param range: Единица измерения (range_model), по умолчанию из номенклатуры
        :param name: Пользовательское наименование строки (по умолчанию имя номенклатуры)
        """
        if nomenclature is not None and not isinstance(nomenclature, nomenclature_model):
            raise arguments_exception("nomenclature", "Параметр nomenclature должен быть экземпляром nomenclature_model")

        initial_name = name
        if initial_name is None and nomenclature is not None:
            initial_name = nomenclature.name[:50]
        elif initial_name is None:
            initial_name = "Строка рецепта"

        super().__init__(name=initial_name)

        self.__nomenclature: nomenclature_model = None
        self.__brutto: float = 0.0
        self.__netto: float = 0.0
        self.__range: range_model = None

        if nomenclature is not None:
            self.nomenclature = nomenclature
        self.brutto = brutto
        self.netto = netto

        if range is not None:
            self.range = range
        elif nomenclature is not None and getattr(nomenclature, "range", None) is not None:
            self.range = nomenclature.range

    @property
    def nomenclature(self) -> nomenclature_model:
        """
        Возвращает номенклатурную позицию ингредиента.
        """
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model) -> None:
        """
        Устанавливает номенклатурную позицию. Ожидает экземпляр nomenclature_model.
        """
        if value is not None and not isinstance(value, nomenclature_model):
            raise arguments_exception("nomenclature", "Параметр nomenclature должен быть экземпляром nomenclature_model")

        self.__nomenclature = value

    @property
    def brutto(self) -> float:
        """
        Возвращает вес брутто ингредиента.
        """
        return self.__brutto

    @brutto.setter
    def brutto(self, value: float) -> None:
        """
        Устанавливает вес брутто. Ожидает неотрицательное число (int или float).
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("brutto", "Вес брутто должен быть числом")

        if value < 0:
            raise arguments_exception("brutto", "Вес брутто не может быть отрицательным")

        self.__brutto = float(value)

    @property
    def netto(self) -> float:
        """
        Возвращает вес нетто ингредиента.
        """
        return self.__netto

    @netto.setter
    def netto(self, value: float) -> None:
        """
        Устанавливает вес нетто. Ожидает неотрицательное число (int или float).
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("netto", "Вес нетто должен быть числом")

        if value < 0:
            raise arguments_exception("netto", "Вес нетто не может быть отрицательным")

        self.__netto = float(value)

    @property
    def range(self) -> range_model:
        """
        Возвращает единицу измерения строки рецепта.
        """
        return self.__range

    @range.setter
    def range(self, value: range_model) -> None:
        """
        Устанавливает единицу измерения. Ожидает объект range_model или None.
        """
        if value is not None and not isinstance(value, range_model):
            raise arguments_exception("range", "Единица измерения должна быть объектом range_model")

        self.__range = value

    @staticmethod
    def create(
        nomenclature: nomenclature_model,
        brutto: float,
        netto: float,
        range: range_model = None,
        name: str = None
    ) -> 'recipe_row_model':
        """
        Фабричный метод создания строки технологической карты (ингредиента).

        :param nomenclature: Номенклатурная позиция
        :param brutto: Вес брутто
        :param netto: Вес нетто
        :param range: Единица измерения (опционально)
        :param name: Наименование строки (опционально)
        :return: Экземпляр recipe_row_model
        """
        return recipe_row_model(
            nomenclature=nomenclature,
            brutto=brutto,
            netto=netto,
            range=range,
            name=name
        )

    @classmethod
    def create_from_dict(cls, data: dict) -> "recipe_row_model":
        """
        Фабричный метод создания строки технологической карты из словаря.

        :param data: Словарь с данными строки
        :return: Экземпляр recipe_row_model
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Для создания recipe_row_model требуется словарь")

        from src.logics.deserialization_context import deserialization_context

        context = deserialization_context()
        entity_id = str(data.get("id", "")).strip()
        if entity_id:
            cached = context.get(entity_id)
            if cached is not None:
                return cached

        nom_data = data.get("nomenclature")
        nomenclature = None
        if isinstance(nom_data, dict):
            nomenclature = nomenclature_model.create_from_dict(nom_data)
        elif isinstance(nom_data, nomenclature_model):
            nomenclature = nom_data

        range_data = data.get("range")
        row_range = None
        if isinstance(range_data, dict):
            row_range = range_model.create_from_dict(range_data)
        elif isinstance(range_data, range_model):
            row_range = range_data

        brutto = float(data.get("brutto", 0.0))
        netto = float(data.get("netto", 0.0))
        name = data.get("name")

        instance = cls(
            nomenclature=nomenclature,
            brutto=brutto,
            netto=netto,
            range=row_range,
            name=name
        )
        if entity_id:
            instance.id = entity_id
            context.register(instance)

        return instance