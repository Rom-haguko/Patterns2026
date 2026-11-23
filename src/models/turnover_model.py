from datetime import datetime
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.dtos.turnover_type_enum import turnover_type_enum
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


class turnover_model(abstract_model):
    """
    Доменная модель складского движения номенклатуры (оборот).
    Отражает факт изменения остатка: склад, номенклатура, единица измерения,
    количество и тип операции (приход или расход).
    """

    def __init__(
        self,
        storage: storage_model = None,
        nomenclature: nomenclature_model = None,
        range: range_model = None,
        quantity: float = 0.0,
        turnover_type: turnover_type_enum = turnover_type_enum.RECEIPT,
        period: datetime = None,
        name: str = None,
    ) -> None:
        """
        Инициализирует складское движение.

        :param storage: Склад, по которому проводится движение
        :param nomenclature: Учетная номенклатура
        :param range: Единица измерения
        :param quantity: Объем (количество) операции, строго больше нуля
        :param turnover_type: Тип движения (RECEIPT - приход, EXPENSE - расход)
        :param period: Дата и время проведения операции
        :param name: Описание операции
        """
        initial_name = name
        if initial_name is None:
            nom_name = getattr(nomenclature, "name", "Номенклатура") if nomenclature else "Номенклатура"
            type_label = "Приход" if turnover_type == turnover_type_enum.RECEIPT else "Расход"
            initial_name = f"{type_label}: {nom_name}"[:50]

        super().__init__(name=initial_name)

        self.__storage: storage_model = None
        self.__nomenclature: nomenclature_model = None
        self.__range: range_model = None
        self.__quantity: float = 0.0
        self.__turnover_type: turnover_type_enum = turnover_type_enum.RECEIPT
        self.__period: datetime = period if isinstance(period, datetime) else datetime.now()

        if storage is not None:
            self.storage = storage
        if nomenclature is not None:
            self.nomenclature = nomenclature
        if range is not None:
            self.range = range
        elif nomenclature is not None and getattr(nomenclature, "range", None) is not None:
            self.range = nomenclature.range

        self.quantity = quantity
        self.turnover_type = turnover_type

    @property
    def storage(self) -> storage_model:
        """
        Склад движения.
        """
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model) -> None:
        """
        Устанавливает склад движения.
        """
        if value is not None and not isinstance(value, storage_model):
            raise arguments_exception("storage", "Склад должен быть экземпляром storage_model")
        self.__storage = value

    @property
    def nomenclature(self) -> nomenclature_model:
        """
        Номенклатура движения.
        """
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model) -> None:
        """
        Устанавливает номенклатуру движения.
        """
        if value is not None and not isinstance(value, nomenclature_model):
            raise arguments_exception("nomenclature", "Номенклатура должна быть экземпляром nomenclature_model")
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        """
        Единица измерения движения.
        """
        return self.__range

    @range.setter
    def range(self, value: range_model) -> None:
        """
        Устанавливает единицу измерения.
        """
        if value is not None and not isinstance(value, range_model):
            raise arguments_exception("range", "Единица измерения должна быть экземпляром range_model")
        self.__range = value

    @property
    def quantity(self) -> float:
        """
        Количество номенклатуры в операции.
        """
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        """
        Устанавливает количество. Ожидает строго положительное число.
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("quantity", "Количество движения должно быть числом")
        if value <= 0:
            raise arguments_exception("quantity", "Количество движения должно быть строго больше нуля")
        self.__quantity = round(float(value), 4)

    @property
    def turnover_type(self) -> turnover_type_enum:
        """
        Тип движения (приход / расход).
        """
        return self.__turnover_type

    @turnover_type.setter
    def turnover_type(self, value: object) -> None:
        """
        Устанавливает тип движения.
        """
        self.__turnover_type = turnover_type_enum.from_string(value)

    @property
    def period(self) -> datetime:
        """
        Дата и время проведения складской операции.
        """
        return self.__period

    @period.setter
    def period(self, value: datetime) -> None:
        """
        Устанавливает дату и время операции.
        """
        if value is not None and not isinstance(value, datetime):
            raise arguments_exception("period", "Период движения должен быть объектом datetime")
        self.__period = value if value is not None else datetime.now()

    @staticmethod
    def create(
        storage: storage_model,
        nomenclature: nomenclature_model,
        range: range_model,
        quantity: float,
        turnover_type: object = turnover_type_enum.RECEIPT,
        period: datetime = None,
        name: str = None,
    ) -> "turnover_model":
        """
        Фабричный метод создания складского движения.
        """
        return turnover_model(
            storage=storage,
            nomenclature=nomenclature,
            range=range,
            quantity=quantity,
            turnover_type=turnover_type_enum.from_string(turnover_type),
            period=period,
            name=name,
        )
