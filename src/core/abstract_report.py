import io
import flask
from abc import ABC, abstractmethod
from src.core.abstract_model import abstract_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto
from src.dtos.report_data_dto import report_data_dto
from src.logics.report_data_mapper import report_data_mapper

"""
Абстрактный класс для формирования отчета
"""
class abstract_report(ABC):

    @property
    @abstractmethod
    def mimetype(self) -> str:
        """
        MIME-тип отчета
        """
        pass

    @property
    @abstractmethod
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Расширение файла отчета
        """
        pass

    def prepare_data(self, source) -> report_data_dto:
        """
        Полиморфное извлечение данных отчета в виде DTO через внешний маппер.
        Доменные модели остаются чистыми (DDD): они ничего не знают об отчетах.
        Поддерживает одиночную сущность или список сущностей.
        """
        if source is None:
            raise argument_exception("Источник данных не может быть пустым")

        if isinstance(source, list):
            return self.prepare_collection(source)

        if not isinstance(source, abstract_model):
            raise argument_exception("Источник данных должен быть экземпляром abstract_model")

        return report_data_mapper.to_dto(source)

    def prepare_collection(self, source: list) -> report_data_dto:
        """
        Формирует DTO для коллекции сущностей через внешний маппер:
        общий заголовок, объединенная таблица, итоговый подвал.
        """
        if len(source) == 0:
            return report_data_dto(title="Пустой отчет")

        for item in source:
            if not isinstance(item, abstract_model):
                raise argument_exception("Все элементы списка должны быть экземплярами abstract_model")

        return report_data_mapper.to_collection_dto(source)

    def to_http_response(self, result: report_result_dto):
        """
        Полиморфное формирование HTTP-ответа.
        """
        if self.is_binary:
            raw_bytes = bytes(result.binary) if result.binary else result.text.encode("utf-8")
            return flask.send_file(
                io.BytesIO(raw_bytes),
                mimetype=self.mimetype,
                as_attachment=True,
                download_name=f"report.{self.file_extension}"
            )
        return flask.Response(result.text, mimetype=self.mimetype)

    """
    Сформировать отчет
    """
    @abstractmethod
    def build(self, source: abstract_model) -> report_result_dto:
        pass