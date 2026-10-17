from src.core.abstract_report import abstract_report
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.core.validator import argument_exception
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате XML
"""
class xml_report(abstract_report):

    """
    Формирование отчета в формате XML (структурированный текст)
    """
    def build(self, source) -> report_result_dto:
        if not isinstance(source, (recipe_model, nomenclature_model, range_model)):
            raise argument_exception("Некорректный тип источника данных для XML отчета")

        if isinstance(source, recipe_model):
            rows_xml = []
            for item in source.rows:
                row_str = (
                    "    <row>\n"
                    f"      <nomenclature>{item.nomenclature.name}</nomenclature>\n"
                    f"      <brutto>{item.brutto}</brutto>\n"
                    f"      <netto>{item.netto}</netto>\n"
                    "    </row>"
                )
                rows_xml.append(row_str)
            rows_block = "\n".join(rows_xml)
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                "<recipe>\n"
                f"  <id>{source.id}</id>\n"
                f"  <name>{source.name}</name>\n"
                "  <rows>\n"
                f"{rows_block}\n"
                "  </rows>\n"
                "</recipe>"
            )

        elif isinstance(source, nomenclature_model):
            group_name = source.group.name if source.group else ""
            range_name = source.range.name if source.range else ""
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                "<nomenclature>\n"
                f"  <id>{source.id}</id>\n"
                f"  <name>{source.name}</name>\n"
                f"  <full_name>{source.full_name}</full_name>\n"
                f"  <group>{group_name}</group>\n"
                f"  <range>{range_name}</range>\n"
                "</nomenclature>"
            )

        elif isinstance(source, range_model):
            base_name = source.base_range.name if source.base_range else ""
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                "<range>\n"
                f"  <id>{source.id}</id>\n"
                f"  <name>{source.name}</name>\n"
                f"  <conversion_factor>{source.conversion_factor}</conversion_factor>\n"
                f"  <base_range>{base_name}</base_range>\n"
                "</range>"
            )

        result = report_result_dto(text=content)
        return result
