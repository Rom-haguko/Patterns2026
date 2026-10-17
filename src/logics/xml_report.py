from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto

"""
Реализация отчета в формате XML
"""
class xml_report(abstract_report):

    # Словарь сопоставления наименований заголовков с XML тегами
    __tag_map = {
        "Наименование": "name",
        "Брутто": "brutto",
        "Нетто": "netto",
        "Код": "id",
        "Полное наименование": "full_name",
        "Группа": "group",
        "Единица измерения": "range",
        "Коэффициент": "conversion_factor",
        "Базовая единица": "base_range",
        "Адрес": "address",
    }

    @property
    def mimetype(self) -> str:
        """
        MIME-тип для формата XML
        """
        return "application/xml"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла
        """
        return False

    @property
    def file_extension(self) -> str:
        """
        Расширение файла XML
        """
        return "xml"

    """
    Формирование отчета в формате XML (структурированный текст)
    """
    def build(self, source) -> report_result_dto:
        title, headers, rows = self.prepare_data(source)
        root_tag = getattr(source, "__class__", type(source)).__name__.replace("_model", "")
        if isinstance(source, list):
            root_tag = "report"
            item_tag = source[0].__class__.__name__.replace("_model", "") if source else "item"
        else:
            item_tag = "row" if hasattr(source, "rows") else root_tag

        rows_xml = []
        for row in rows:
            cols_xml = []
            for header, val in zip(headers, row):
                if item_tag == "row" and header == "Наименование":
                    tag = "nomenclature"
                else:
                    tag = self.__tag_map.get(header, header.lower().replace(" ", "_"))
                cols_xml.append(f"      <{tag}>{val}</{tag}>")
            cols_str = "\n".join(cols_xml)
            if item_tag == root_tag:
                # Одиночная плоская сущность
                rows_xml.append(f"<{root_tag}>\n{cols_str}\n</{root_tag}>")
            else:
                rows_xml.append(f"    <{item_tag}>\n{cols_str}\n    </{item_tag}>")

        if item_tag == root_tag and len(rows_xml) == 1:
            content = '<?xml version="1.0" encoding="utf-8"?>\n' + rows_xml[0]
        else:
            rows_block = "\n".join(rows_xml)
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                f"<{root_tag}>\n"
                f"  <id>{getattr(source, 'id', '')}</id>\n"
                f"  <name>{getattr(source, 'name', title)}</name>\n"
                "  <rows>\n"
                f"{rows_block}\n"
                "  </rows>\n"
                f"</{root_tag}>"
            )

        return report_result_dto(text=content)
