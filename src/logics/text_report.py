from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.core.validator import validator
from src.dtos.report_result_dto import report_result_dto

"""
Реализация текстового представления отчета по рецепту
"""
class text_report(abstract_report):
    # Рецепт
    __receipt: recipe_model

    """
    Переопределенный метод формирования отчета
    """
    def build(self, source):
        validator.validate(source, recipe_model)
        self.__receipt = source

        header = "Наименование | Брутто | Нетто "
        data = ""
        
        for item in self.__receipt.rows:
            data += f"{item.nomenclature.name} | {item.brutto} | {item.netto}\n"

        result = report_result_dto()
        result.text = f"{header}\n{data}"

        return result