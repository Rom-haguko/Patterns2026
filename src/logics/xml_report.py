from src.core.abstract_report import abstract_report
from src.dtos.report_result_dto import report_result_dto
import src.logics.report_data_mapper


class xml_report(abstract_report):
    """
    Реализация отчета в формате XML.
    """

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
        MIME-тип для формата XML.
        """
        return "application/xml"

    @property
    def is_binary(self) -> bool:
        """
        Флаг формирования бинарных данных для скачивания файла.
        """
        return False

    @property
    def file_extension(self) -> str:
        """
        Расширение файла XML.
        """
        return "xml"

    def build(self, source) -> report_result_dto:
        """
        Формирование отчета в формате XML (структурированный текст).
        """
        data = self.prepare_data(source)
        root_tag = getattr(source, "__class__", type(source)).__name__.replace("_model", "")
        if isinstance(source, list):
            root_tag = "report"
            item_tag = getattr(source[0], "__class__", type(source[0])).__name__.replace("_model", "") if len(source) > 0 else "item"
        else:
            item_tag = "row" if hasattr(source, "rows") else root_tag

        rows_xml = []
        for row in data.rows:
            cols_xml = []
            for header, val in zip(data.headers, row):
                if item_tag == "row" and header == "Наименование":
                    tag = "nomenclature"
                else:
                    tag = self.__tag_map.get(header, header.lower().replace(" ", "_"))
                cols_xml.append(f"      <{tag}>{val}</{tag}>")
            cols_str = "\n".join(cols_xml)
            if item_tag == root_tag:
                rows_xml.append(f"<{root_tag}>\n{cols_str}\n</{root_tag}>")
            else:
                rows_xml.append(f"    <{item_tag}>\n{cols_str}\n    </{item_tag}>")

        rows_block = "\n".join(rows_xml)

        if hasattr(source, "rows"):
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                f"<{root_tag}>\n"
                f"  <id>{getattr(source, 'id', '')}</id>\n"
                f"  <name>{getattr(source, 'name', data.title)}</name>\n"
                "  <rows>\n"
                f"{rows_block}\n"
                "  </rows>\n"
                f"</{root_tag}>\n"
            )
        elif isinstance(source, list):
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                f"<{root_tag}>\n"
                f"{rows_block}\n"
                f"</{root_tag}>\n"
            )
        else:
            content = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                f"{rows_block}\n"
            )

        return report_result_dto(text=content)
