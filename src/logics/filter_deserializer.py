from src.core.abstract_deserializer import abstract_deserializer
from src.core.exception import arguments_exception
from src.dtos.filter_dto import filter_dto
from src.dtos.filter_type_enum import filter_type_enum


class filter_deserializer(abstract_deserializer):
    """
    Десериализатор словарей входящего запроса в типизированную DTO-модель filter_dto.
    Инкапсулирует границу между внешним API и сервисом фильтрации (DDD).
    """

    def deserialize(self, data: object, target_type: type = None) -> filter_dto:
        """
        Преобразует входные словарные данные в filter_dto.

        :param data: Входные данные (dict)
        :param target_type: Опциональный целевой тип
        :return: Экземпляр filter_dto
        """
        if data is None:
            return filter_dto()

        if not isinstance(data, dict):
            raise arguments_exception("data", "Данные для десериализации фильтра должны быть словарем")

        name = str(data.get("name", "")).strip() if data.get("name") is not None else ""
        raw_name_type = data.get("name_filter_type", filter_type_enum.LIKE)
        name_filter_type = filter_type_enum.from_string(raw_name_type)

        id_val = str(data.get("id", "")).strip() if data.get("id") is not None else ""
        raw_id_type = data.get("id_filter_type", filter_type_enum.EQUALS)
        id_filter_type = filter_type_enum.from_string(raw_id_type)

        return filter_dto.create(
            name=name,
            name_filter_type=name_filter_type,
            id=id_val,
            id_filter_type=id_filter_type,
        )
