from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате HTML
"""
class html_report(abstract_report):

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для формата HTML
        """
        return "text/html"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        return False

    @property
    def file_extension(self) -> str:
        """
        Расширение файла HTML
        """
        return "html"

    """
    Формирование отчета в формате HTML (структурированный текст)
    """
    def build(self, source) -> report_result_dto:
        data = self.prepare_data(source)
        th_tags = "".join(f"\n        <th>{h}</th>" for h in data.headers)
        tr_tags = []
        for row in data.rows:
            td_tags = "".join(f"\n        <td>{val}</td>" for val in row)
            tr_tags.append(f"      <tr>{td_tags}\n      </tr>")
        rows_html = "\n".join(tr_tags)
        footer_html = ""
        if data.footer:
            footer_html = (
                "\n    <tfoot>\n"
                f"      <tr><td colspan=\"{len(data.headers)}\">{data.footer}</td></tr>\n"
                "    </tfoot>"
            )
        content = (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            '  <meta charset="utf-8">\n'
            f"  <title>{data.title}</title>\n"
            "</head>\n"
            "<body>\n"
            f"  <h1>{data.title}</h1>\n"
            '  <table border="1">\n'
            "    <thead>\n"
            f"      <tr>{th_tags}\n"
            "      </tr>\n"
            "    </thead>\n"
            "    <tbody>\n"
            f"{rows_html}\n"
            "    </tbody>"
            f"{footer_html}\n"
            "  </table>\n"
            "</body>\n"
            "</html>"
        )
        return report_result_dto(text=content)
