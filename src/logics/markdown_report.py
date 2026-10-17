from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате Markdown
"""
class markdown_report(abstract_report):

    """
    Формирование отчета в формате Markdown (бинарные данные)
    """
    def build(self, source) -> report_result_dto:
        if not isinstance(source, (recipe_model, nomenclature_model, range_model)):
            raise argument_exception("Некорректный тип источника данных для Markdown отчета")

        if isinstance(source, recipe_model):
            lines = [
                f"# Рецепт: {source.name}",
                "",
                "| Наименование | Брутто | Нетто |",
                "| --- | --- | --- |",
            ]
            for item in source.rows:
                lines.append(f"| {item.nomenclature.name} | {item.brutto} | {item.netto} |")
            content = "\n".join(lines) + "\n"

        elif isinstance(source, nomenclature_model):
            group_name = source.group.name if source.group else ""
            range_name = source.range.name if source.range else ""
            lines = [
                f"# Номенклатура: {source.name}",
                "",
                "| Код | Наименование | Полное наименование | Группа | Единица измерения |",
                "| --- | --- | --- | --- | --- |",
                f"| {source.id} | {source.name} | {source.full_name} | {group_name} | {range_name} |",
            ]
            content = "\n".join(lines) + "\n"

        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            lines = [
                f"# Единица измерения: {source.name}",
                "",
                "| Код | Наименование | Коэффициент | Базовая единица |",
                "| --- | --- | --- | --- |",
                f"| {source.id} | {source.name} | {source.conversion_factor} | {base_name} |",
            ]
            content = "\n".join(lines) + "\n"

        binary_data = list(content.encode("utf-8"))
        result = report_result_dto(binary=binary_data)
        return result
