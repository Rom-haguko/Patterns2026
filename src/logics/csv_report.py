from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате CSV
"""
class csv_report(abstract_report):

    """
    Формирование отчета в формате CSV (бинарные данные)
    """
    def build(self, source) -> report_result_dto:
        if not isinstance(source, (recipe_model, nomenclature_model, range_model)):
            raise argument_exception("Некорректный тип источника данных для CSV отчета")

        if isinstance(source, recipe_model):
            header = "Наименование;Брутто;Нетто"
            rows = [f"{item.nomenclature.name};{item.brutto};{item.netto}" for item in source.rows]
            content = f"{header}\n" + "\n".join(rows) + "\n"

        elif isinstance(source, nomenclature_model):
            group_name = source.group.name if source.group else ""
            range_name = source.range.name if source.range else ""
            header = "Код;Наименование;Полное наименование;Группа;Единица измерения"
            content = f"{header}\n{source.id};{source.name};{source.full_name};{group_name};{range_name}\n"

        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            header = "Код;Наименование;Коэффициент;Базовая единица"
            content = f"{header}\n{source.id};{source.name};{source.conversion_factor};{base_name}\n"

        binary_data = list(content.encode("utf-8"))
        result = report_result_dto(binary=binary_data)
        return result
