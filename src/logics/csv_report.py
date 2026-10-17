from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате CSV
"""
class csv_report(abstract_report):

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для формата CSV
        """
        return "text/csv"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        return True

    @property
    def file_extension(self) -> str:
        """
        Расширение файла CSV
        """
        return "csv"

    """
    Формирование отчета в формате CSV (бинарные данные)
    """
    def build(self, source) -> report_result_dto:
        _, headers, rows = self.prepare_data(source)
        header_line = ";".join(headers)
        data_lines = [";".join(str(val) for val in row) for row in rows]
        content = f"{header_line}\n" + "\n".join(data_lines) + "\n"

        binary_data = list(content.encode("utf-8"))
        result = report_result_dto(binary=binary_data)
        return result
