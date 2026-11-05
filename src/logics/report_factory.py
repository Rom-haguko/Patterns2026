from src.core.abstract_report_factory import abstract_report_factory
from src.core.abstract_report import abstract_report
from src.dtos.report_type_enum import report_type_enum
from src.logics.text_report import text_report
from src.logics.csv_report import csv_report
from src.logics.markdown_report import markdown_report
from src.logics.xml_report import xml_report
from src.logics.html_report import html_report
from src.models.settings_model import settings_model
from src.logics.settings_manager import settings_manager
from src.core.validator import validator
from src.core.exception import arguments_exception


class report_factory(abstract_report_factory):
    """
    Реализация фабрики для построения отчетов.
    Подбирает подходящий генератор отчета на основе перечисления report_type_enum.
    """

    def __init__(self, settings: settings_model = None):
        """
        Инициализация фабрики отчетов с регистрацией обработчиков и инкапсуляцией настроек.
        """
        self.__mapping: dict[report_type_enum, type[abstract_report]] = {
            report_type_enum.TXT: text_report,
            report_type_enum.CSV: csv_report,
            report_type_enum.MARKDOWN: markdown_report,
            report_type_enum.XML: xml_report,
            report_type_enum.HTML: html_report,
        }

        if settings is not None:
            self.__settings = settings
        else:
            try:
                manager = settings_manager()
                if not manager.is_loaded:
                    manager.load()
                self.__settings = manager.settings
            except Exception:
                self.__settings = settings_model()

    @property
    def settings(self) -> settings_model:
        """
        Настройки приложения, инкапсулированные в фабрике.
        """
        return self.__settings

    @settings.setter
    def settings(self, value: settings_model) -> None:
        """
        Установка настроек приложения.
        """
        validator.validate(value, settings_model)
        self.__settings = value

    def create(self, report_type: report_type_enum = None) -> abstract_report:
        """
        Создание инстанса отчета по переданному типу.
        Если тип не указан, создается отчет по умолчанию на основе настроек.
        """
        actual_type = report_type
        if actual_type is None:
            if self.__settings is None:
                raise arguments_exception("settings", "Настройки не инициализированы в фабрике")
            actual_type = self.__settings.response_format

        if isinstance(actual_type, str):
            try:
                actual_type = report_type_enum.from_string(actual_type)
            except Exception:
                raise arguments_exception("report_type", f"Указанный тип отчета {actual_type}")

        if actual_type not in self.__mapping:
            raise arguments_exception("report_type", f"Указанный тип отчета {actual_type}")

        report_class = self.__mapping[actual_type]
        return report_class()

    def create_default(self) -> abstract_report:
        """
        Создание инстанса отчета на основе настроек приложения по умолчанию.
        """
        return self.create()
