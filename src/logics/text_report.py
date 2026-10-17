from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.validator import validator, argument_exception
from src.dtos.report_result_dto import report_result_dto

"""
Реализация текстового представления отчета
"""
class text_report(abstract_report):

    """
    Переопределенный метод формирования отчета
    """
    def build(self, source) -> report_result_dto:
        if not isinstance(source, (recipe_model, nomenclature_model, range_model)):
            raise argument_exception("Некорректный тип источника данных для текстового отчета")

        if isinstance(source, recipe_model):
            header = "Наименование | Брутто | Нетто "
            data = ""
            for item in source.rows:
                data += f"{item.nomenclature.name} | {item.brutto} | {item.netto}\n"
            text = f"{header}\n{data}"

        elif isinstance(source, nomenclature_model):
            group_name = source.group.name if source.group else ""
            range_name = source.range.name if source.range else ""
            header = "Код | Наименование | Полное наименование | Группа | Единица измерения"
            data = f"{source.id} | {source.name} | {source.full_name} | {group_name} | {range_name}"
            text = f"{header}\n{data}"

        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            header = "Код | Наименование | Коэффициент | Базовая единица"
            data = f"{source.id} | {source.name} | {source.conversion_factor} | {base_name}"
            text = f"{header}\n{data}"

        result = report_result_dto()
        result.text = text
        return result