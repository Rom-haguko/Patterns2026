from src.dtos.filter_dto import filter_dto
from src.dtos.osv_row_dto import osv_row_dto
from src.dtos.turnover_type_enum import turnover_type_enum
from src.logics.convert_factory import convert_factory
from src.logics.prototype_filter import prototype_filter
from src.logics.storage_manager import storage_manager


class osv_service:
    """
    Сервис формирования оборотно-сальдовой ведомости (ОСВ).
    Выполняет агрегацию складских движений (turnover_model) по складам и номенклатуре,
    рассчитывает начальные остатки, приход, расход и конечное сальдо, а также
    применяет шаблон Прототип (prototype_filter) для фильтрации сформированной ведомости.
    """

    def __init__(self, storage: storage_manager = None) -> None:
        """
        Инициализирует сервис ОСВ.

        :param storage: Экземпляр хранилища данных (Singleton по умолчанию)
        """
        self._storage = storage if storage is not None else storage_manager()
        self._factory = convert_factory()

    def build_osv(self, filter_item: filter_dto = None) -> list[osv_row_dto]:
        """
        Формирует список строк ОСВ на основе зарегистрированных движений,
        после чего фильтрует полученный набор с помощью шаблона Прототип.

        :param filter_item: Опциональный DTO с параметрами фильтрации
        :return: Список объектов osv_row_dto
        """
        movements = self._storage.collection(self._storage.turnover_key())

        # Группировка движений по уникальному ключу (id склада, id номенклатуры)
        grouped: dict[tuple[str, str], list] = {}
        for mov in movements:
            st = getattr(mov, "storage", None)
            nom = getattr(mov, "nomenclature", None)
            if st is None or nom is None:
                continue
            key = (str(st.id), str(nom.id))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(mov)

        raw_osv_rows: list[osv_row_dto] = []
        for (st_id, nom_id), mov_list in grouped.items():
            first = mov_list[0]
            st = first.storage
            nom = first.nomenclature
            rng = first.range if getattr(first, "range", None) is not None else getattr(nom, "range", None)

            initial_balance = 0.0
            inflow = sum(
                float(m.quantity)
                for m in mov_list
                if getattr(m, "turnover_type", None) == turnover_type_enum.RECEIPT
            )
            outflow = sum(
                float(m.quantity)
                for m in mov_list
                if getattr(m, "turnover_type", None) == turnover_type_enum.EXPENSE
            )
            final_balance = initial_balance + inflow - outflow

            row = osv_row_dto(
                storage=st,
                nomenclature=nom,
                range=rng,
                initial_balance=initial_balance,
                inflow=inflow,
                outflow=outflow,
                final_balance=final_balance,
            )
            raw_osv_rows.append(row)

        # Применение шаблона Прототип для фильтрации строк ведомости
        prototype = prototype_filter(raw_osv_rows)
        filtered_prototype = prototype.create(filter_item)
        return filtered_prototype.data

    def get_osv_response(self, filter_item: filter_dto = None):
        """
        Формирует ответ REST API с результатом расчета ОСВ в виде сериализованных словарей.

        :param filter_item: Критерии фильтрации filter_dto
        :return: Кортеж (список словарей ОСВ, HTTP статус 200)
        """
        rows = self.build_osv(filter_item)
        serialized_rows = [self._factory.convert_value(row) for row in rows]
        return serialized_rows, 200
