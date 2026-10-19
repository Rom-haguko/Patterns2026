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
        data = self.prepare_data(source)
        lines = []
        if data.title:
            lines.append(f"# {data.title}\n")
        lines.append("| " + " | ".join(data.headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(data.headers)) + " |")
        for row in data.rows:
            lines.append("| " + " | ".join(str(val) for val in row) + " |")
        if data.footer:
            lines.append(f"\n{data.footer}")
        content = "\n".join(lines) + "\n"
        binary_data = list(content.encode("utf-8"))
        return report_result_dto(binary=binary_data)
