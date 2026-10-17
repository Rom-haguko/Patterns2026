from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате Markdown
"""
class markdown_report(abstract_report):

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для формата Markdown
        """
        return "text/markdown"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        return True

    @property
    def file_extension(self) -> str:
        """
        Расширение файла Markdown
        """
        return "md"

    """
    Формирование отчета в формате Markdown (бинарные данные)
    """
    def build(self, source) -> report_result_dto:
        title, headers, rows = self.prepare_data(source)
        lines = []
        if title:
            lines.append(f"# {title}\n")
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(val) for val in row) + " |")
        content = "\n".join(lines) + "\n"

        binary_data = list(content.encode("utf-8"))
        result = report_result_dto(binary=binary_data)
        return result
