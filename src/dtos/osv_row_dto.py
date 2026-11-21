from src.models.storage_model import storage_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.exception import arguments_exception


class osv_row_dto:
    """
    DTO строка оборотно-сальдовой ведомости (ОСВ).
    Хранит информацию о складе, номенклатуре, единице измерения, начальном остатке,
    оборотах (приход, расход) и конечном остатке.
    """

    def __init__(
        self,
        storage: storage_model,
        nomenclature: nomenclature_model,
        range: range_model,
        initial_balance: float = 0.0,
        inflow: float = 0.0,
        outflow: float = 0.0,
        final_balance: float = 0.0,
    ) -> None:
        """
        Инициализирует строку оборотно-сальдовой ведомости.

        :param storage: Склад хранения
        :param nomenclature: Учетная номенклатура
        :param range: Единица измерения
        :param initial_balance: Сальдо на начало периода
        :param inflow: Оборот прихода за период
        :param outflow: Оборот расхода за период
        :param final_balance: Сальдо на конец периода
        """
        if storage is not None and not isinstance(storage, storage_model):
            raise arguments_exception("storage", "Склад должен быть экземпляром storage_model")
        if nomenclature is not None and not isinstance(nomenclature, nomenclature_model):
            raise arguments_exception("nomenclature", "Номенклатура должна быть экземпляром nomenclature_model")
        if range is not None and not isinstance(range, range_model):
            raise arguments_exception("range", "Единица измерения должна быть экземпляром range_model")

        self.__storage: storage_model = storage
        self.__nomenclature: nomenclature_model = nomenclature
        self.__range: range_model = range
        self.__initial_balance: float = round(float(initial_balance), 4)
        self.__inflow: float = round(float(inflow), 4)
        self.__outflow: float = round(float(outflow), 4)
        self.__final_balance: float = round(float(final_balance), 4)

    @property
    def storage(self) -> storage_model:
        """
        Склад хранения.
        """
        return self.__storage

    @property
    def nomenclature(self) -> nomenclature_model:
        """
        Номенклатурная позиция.
        """
        return self.__nomenclature

    @property
    def range(self) -> range_model:
        """
        Единица измерения.
        """
        return self.__range

    @property
    def initial_balance(self) -> float:
        """
        Начальный остаток (сальдо).
        """
        return self.__initial_balance

    @property
    def inflow(self) -> float:
        """
        Суммарный приход (поступление) за период.
        """
        return self.__inflow

    @property
    def outflow(self) -> float:
        """
        Суммарный расход (списание) за период.
        """
        return self.__outflow

    @property
    def final_balance(self) -> float:
        """
        Конечный остаток (сальдо на конец).
        """
        return self.__final_balance
