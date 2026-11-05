from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto
import src.logics.report_data_mapper


class csv_report(abstract_report):
    """
    Реализация отчета в формате CSV.
    """

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для формата CSV.
        """
        return "text/csv"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла.
        """
        return True

    @property
    def file_extension(self) -> str:
        """
        Расширение файла CSV.
        """
        return "csv"

    def build(self, source) -> report_result_dto:
        """
        Формирование отчета в формате CSV (бинарные данные).
        """
        data = self.prepare_data(source)
        header_line = ";".join(data.headers)
        data_lines = [";".join(str(val) for val in row) for row in data.rows]
        content = f"{header_line}\n" + "\n".join(data_lines) + "\n"
        binary_data = list(content.encode("utf-8"))
        return report_result_dto(binary=binary_data)
