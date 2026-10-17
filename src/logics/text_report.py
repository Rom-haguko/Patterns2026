from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto

"""
Реализация текстового представления отчета
"""
class text_report(abstract_report):

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для текстового формата
        """
        return "text/plain"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        return False

    @property
    def file_extension(self) -> str:
        """
        Расширение файла текстового отчета
        """
        return "txt"

    """
    Переопределенный метод формирования отчета
    """
    def build(self, source) -> report_result_dto:
        _, headers, rows = self.prepare_data(source)
        lines = []
        lines.append(" | ".join(headers) + " ")
        for row in rows:
            lines.append(" | ".join(str(val) for val in row))
        content = "\n".join(lines) + "\n"

        result = report_result_dto()
        result.text = content
        return result