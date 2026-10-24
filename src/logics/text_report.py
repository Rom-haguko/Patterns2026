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
        data = self.prepare_data(source)
        lines = [data.title, " | ".join(data.headers)]
        for row in data.rows:
            lines.append(" | ".join(str(val) for val in row))
        if data.footer:
            lines.append(data.footer)
        content = "\n".join(lines) + "\n"
        return report_result_dto(text=content)