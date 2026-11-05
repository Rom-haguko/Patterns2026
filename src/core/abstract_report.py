from abc import ABC, abstractmethod
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception, operation_exception
from src.dtos.report_result_dto import report_result_dto
from src.dtos.report_data_dto import report_data_dto


class abstract_report(ABC):
    """
    Абстрактный класс для формирования отчетов.
    Определяет общий контракт генерации отчетов в различных форматах.
    """

    _data_mapper = None

    @classmethod
    def set_data_mapper(cls, mapper) -> None:
        """
        Регистрация маппера данных (Dependency Inversion / Clean Architecture).

        :param mapper: Реализация маппера данных.
        """
        cls._data_mapper = mapper

    @classmethod
    def get_data_mapper(cls):
        """
        Получение зарегистрированного маппера данных.

        :raises operation_exception: Если маппер данных не был зарегистрирован.
        """
        if cls._data_mapper is None:
            raise operation_exception("Маппер данных отчета не зарегистрирован")
        return cls._data_mapper

    @property
    @abstractmethod
    def mimetype(self) -> str:
        """
        MIME-тип отчета.
        """
        pass

    @property
    @abstractmethod
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла.
        """
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Расширение файла отчета.
        """
        pass

    def prepare_data(self, source) -> report_data_dto:
        """
        Полиморфное извлечение данных отчета в виде DTO через внешний маппер.
        Доменные модели остаются чистыми (DDD): они ничего не знают об отчетах.
        Поддерживает одиночную сущность, список сущностей или уже готовый DTO.

        :param source: Источник данных (сущность, список сущностей или DTO).
        :return: Объект передачи данных report_data_dto.
        """
        if source is None:
            raise arguments_exception("source", "Источник данных не может быть пустым")

        if isinstance(source, report_data_dto):
            return source

        if isinstance(source, list):
            return self.prepare_collection(source)

        if not isinstance(source, abstract_model):
            raise arguments_exception("source", "Источник данных должен быть экземпляром abstract_model")

        mapper = self.get_data_mapper()
        return mapper.to_dto(source)

    def prepare_collection(self, source: list) -> report_data_dto:
        """
        Формирует DTO для коллекции сущностей через внешний маппер:
        общий заголовок, объединенная таблица, итоговый подвал.

        :param source: Список доменных сущностей.
        :return: Объект передачи данных report_data_dto.
        """
        if len(source) == 0:
            return report_data_dto(title="Пустой отчет")

        for item in source:
            if not isinstance(item, abstract_model):
                raise arguments_exception("source", "Все элементы списка должны быть экземплярами abstract_model")

        mapper = self.get_data_mapper()
        return mapper.to_collection_dto(source)

    @abstractmethod
    def build(self, source) -> report_result_dto:
        """
        Сформировать отчет по переданному источнику данных.

        :param source: Источник данных (сущность, список или DTO).
        :return: Результат генерации отчета report_result_dto.
        """
        pass
