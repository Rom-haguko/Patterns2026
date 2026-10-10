from src.core.abstract_model import name_id
from src.core.exception import arguments_exception
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model


class recipe_row_model(name_id):
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

    # ─────────────────────────── Свойства и валидация ─────────────────────────────

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
        if not isinstance(value, nomenclature_model):
            raise arguments_exception("nomenclature", "Параметр nomenclature должен быть экземпляром nomenclature_model")

        self.__nomenclature = value
        if not self._name or self._name == "Строка рецепта":
            self.name = value.name[:50]
        if self.__range is None and getattr(value, "range", None) is not None:
            self.__range = value.range

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
    def gross(self) -> float:
        """
        Псевдоним (алиас) для свойства brutto.
        """
        return self.__brutto

    @gross.setter
    def gross(self, value: float) -> None:
        """
        Сеттер-алиас для свойства brutto.
        """
        self.brutto = value

    @property
    def weight_brutto(self) -> float:
        """
        Псевдоним (алиас) для свойства brutto.
        """
        return self.__brutto

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
    def net(self) -> float:
        """
        Псевдоним (алиас) для свойства netto.
        """
        return self.__netto

    @net.setter
    def net(self, value: float) -> None:
        """
        Сеттер-алиас для свойства netto.
        """
        self.netto = value

    @property
    def weight_netto(self) -> float:
        """
        Псевдоним (алиас) для свойства netto.
        """
        return self.__netto

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

    @property
    def unit(self) -> range_model:
        """
        Псевдоним (алиас) для свойства range.
        """
        return self.__range

    # ─────────────────────────── Фабричные методы ─────────────────────────────────

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


ingredient_model = recipe_row_model
