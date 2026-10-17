import pytest
from src.core.exception import arguments_exception
from src.logics.report_factory import report_factory
from src.logics.text_report import text_report
from src.logics.csv_report import csv_report
from src.logics.markdown_report import markdown_report
from src.logics.xml_report import xml_report
from src.logics.html_report import html_report
from src.core.abstract_report import abstract_report
from src.dtos.report_type_enum import report_type_enum
from src.models.settings_model import settings_model


def test_success_create_report_factory():
    """
    <summary>
    Проверка успешного создания экземпляра фабрики отчётов.
    </summary>
    """
    factory = report_factory()
    assert isinstance(factory, report_factory)


def test_factory_creates_text_report_for_txt_type():
    """
    <summary>
    Проверка, что фабрика создаёт текстовый отчёт для типа TXT.
    </summary>
    """
    factory = report_factory()
    report = factory.create(report_type_enum.TXT)
    assert isinstance(report, text_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_csv_report_for_csv_type():
    """
    <summary>
    Проверка, что фабрика создаёт CSV отчёт для типа CSV.
    </summary>
    """
    factory = report_factory()
    report = factory.create(report_type_enum.CSV)
    assert isinstance(report, csv_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_markdown_report_for_markdown_type():
    """
    <summary>
    Проверка, что фабрика создаёт Markdown отчёт для типа MARKDOWN.
    </summary>
    """
    factory = report_factory()
    report = factory.create(report_type_enum.MARKDOWN)
    assert isinstance(report, markdown_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_xml_report_for_xml_type():
    """
    <summary>
    Проверка, что фабрика создаёт XML отчёт для типа XML.
    </summary>
    """
    factory = report_factory()
    report = factory.create(report_type_enum.XML)
    assert isinstance(report, xml_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_html_report_for_html_type():
    """
    <summary>
    Проверка, что фабрика создаёт HTML отчёт для типа HTML.
    </summary>
    """
    factory = report_factory()
    report = factory.create(report_type_enum.HTML)
    assert isinstance(report, html_report)
    assert isinstance(report, abstract_report)


def test_factory_create_with_string_type_names():
    """
    <summary>
    Проверка создания отчётов по строковым именам форматов.
    </summary>
    """
    factory = report_factory()
    assert isinstance(factory.create("TXT"), text_report)
    assert isinstance(factory.create("CSV"), csv_report)
    assert isinstance(factory.create("Markdown"), markdown_report)
    assert isinstance(factory.create("XML"), xml_report)
    assert isinstance(factory.create("HTML"), html_report)


def test_factory_create_returns_new_instance_each_time():
    """
    <summary>
    Проверка, что каждый вызов create возвращает новый экземпляр отчёта.
    </summary>
    """
    factory = report_factory()
    report1 = factory.create(report_type_enum.TXT)
    report2 = factory.create(report_type_enum.TXT)
    assert report1 is not report2


def test_error_create_with_invalid_report_type():
    """
    <summary>
    Проверка генерации исключения при передаче несуществующего типа отчёта.
    </summary>
    """
    factory = report_factory()
    with pytest.raises(arguments_exception):
        factory.create("несуществующий_тип")


def test_factory_encapsulates_settings_via_constructor():
    """
    <summary>
    Проверка инкапсуляции настроек в фабрику через конструктор.
    </summary>
    """
    settings = settings_model()
    settings.response_format = report_type_enum.CSV
    factory = report_factory(settings=settings)
    assert factory.settings is settings
    assert factory.settings.response_format == report_type_enum.CSV


def test_factory_settings_setter():
    """
    <summary>
    Проверка установки настроек через свойство settings.
    </summary>
    """
    factory = report_factory()
    new_settings = settings_model()
    new_settings.response_format = report_type_enum.HTML
    factory.settings = new_settings
    assert factory.settings is new_settings


def test_factory_create_default_uses_encapsulated_settings():
    """
    <summary>
    Проверка, что метод create_default создаёт отчёт нужного типа
    в зависимости от формата, заданного в настройках.
    </summary>
    """
    settings = settings_model()

    settings.response_format = report_type_enum.CSV
    factory = report_factory(settings=settings)
    assert isinstance(factory.create_default(), csv_report)

    settings.response_format = report_type_enum.MARKDOWN
    assert isinstance(factory.create_default(), markdown_report)

    settings.response_format = report_type_enum.XML
    assert isinstance(factory.create_default(), xml_report)

    settings.response_format = report_type_enum.HTML
    assert isinstance(factory.create_default(), html_report)

    settings.response_format = report_type_enum.TXT
    assert isinstance(factory.create_default(), text_report)