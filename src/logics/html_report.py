from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате HTML
"""
class html_report(abstract_report):

    """
    Формирование отчета в формате HTML (структурированный текст)
    """
    def build(self, source) -> report_result_dto:
        if not isinstance(source, (recipe_model, nomenclature_model, range_model)):
            raise argument_exception("Некорректный тип источника данных для HTML отчета")

        if isinstance(source, recipe_model):
            rows_html = []
            for item in source.rows:
                row_str = (
                    "      <tr>\n"
                    f"        <td>{item.nomenclature.name}</td>\n"
                    f"        <td>{item.brutto}</td>\n"
                    f"        <td>{item.netto}</td>\n"
                    "      </tr>"
                )
                rows_html.append(row_str)
            rows_block = "\n".join(rows_html)
            content = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                '  <meta charset="utf-8">\n'
                f"  <title>Рецепт: {source.name}</title>\n"
                "</head>\n"
                "<body>\n"
                f"  <h1>{source.name}</h1>\n"
                "  <table border=\"1\">\n"
                "    <thead>\n"
                "      <tr>\n"
                "        <th>Наименование</th>\n"
                "        <th>Брутто</th>\n"
                "        <th>Нетто</th>\n"
                "      </tr>\n"
                "    </thead>\n"
                "    <tbody>\n"
                f"{rows_block}\n"
                "    </tbody>\n"
                "  </table>\n"
                "</body>\n"
                "</html>"
            )

        elif isinstance(source, nomenclature_model):
            group_name = source.group.name if source.group else ""
            range_name = source.range.name if source.range else ""
            content = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                '  <meta charset="utf-8">\n'
                f"  <title>Номенклатура: {source.name}</title>\n"
                "</head>\n"
                "<body>\n"
                f"  <h1>{source.name}</h1>\n"
                "  <table border=\"1\">\n"
                f"    <tr><th>Код</th><td>{source.id}</td></tr>\n"
                f"    <tr><th>Наименование</th><td>{source.name}</td></tr>\n"
                f"    <tr><th>Полное наименование</th><td>{source.full_name}</td></tr>\n"
                f"    <tr><th>Группа</th><td>{group_name}</td></tr>\n"
                f"    <tr><th>Единица измерения</th><td>{range_name}</td></tr>\n"
                "  </table>\n"
                "</body>\n"
                "</html>"
            )

        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            content = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                '  <meta charset="utf-8">\n'
                f"  <title>Единица измерения: {source.name}</title>\n"
                "</head>\n"
                "<body>\n"
                f"  <h1>{source.name}</h1>\n"
                "  <table border=\"1\">\n"
                f"    <tr><th>Код</th><td>{source.id}</td></tr>\n"
                f"    <tr><th>Наименование</th><td>{source.name}</td></tr>\n"
                f"    <tr><th>Коэффициент</th><td>{source.conversion_factor}</td></tr>\n"
                f"    <tr><th>Базовая единица</th><td>{base_name}</td></tr>\n"
                "  </table>\n"
                "</body>\n"
                "</html>"
            )

        result = report_result_dto(text=content)
        return result
