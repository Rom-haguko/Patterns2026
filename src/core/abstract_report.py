import io
import flask
from abc import ABC, abstractmethod
from src.core.abstract_model import abstract_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto

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

    def prepare_data(self, source) -> tuple[str, list[str], list[list]]:
        """
        Полиморфное извлечение табличных данных из источника.
        """
        if source is None:
            raise argument_exception("Источник данных не может быть пустым")

        if isinstance(source, list):
            if len(source) == 0:
                return "Отчет", [], []
            first = source[0]
            if not isinstance(first, abstract_model):
                raise argument_exception("Элементы списка должны быть экземплярами abstract_model")
            _, headers, _ = first.to_report_data()
            all_rows = []
            for item in source:
                if not isinstance(item, abstract_model):
                    raise argument_exception("Все элементы списка должны быть экземплярами abstract_model")
                _, _, item_rows = item.to_report_data()
                all_rows.extend(item_rows)
            title = f"Список {first.__class__.__name__}"
            return title, headers, all_rows

        if not isinstance(source, abstract_model):
            raise argument_exception("Источник данных должен быть экземпляром abstract_model")

        return source.to_report_data()

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

    @abstractmethod
    def build(self, source: abstract_model) -> report_result_dto:
        pass