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
    Проверка успешного создания экземпляра фабрики отчётов и доступности генераторов.
    """
    # Подготовка
    # (Инициализация фабрики без внешних зависимостей)

    # Действие
    factory = report_factory()

    # Проверки
    assert isinstance(factory, report_factory)
    assert factory.settings is not None
    assert isinstance(factory.create(report_type_enum.TXT), text_report)


def test_factory_creates_text_report_for_txt_type():
    """
    Проверка, что фабрика создаёт текстовый отчёт для типа TXT.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.TXT)

    # Проверки
    assert isinstance(report, text_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_csv_report_for_csv_type():
    """
    Проверка, что фабрика создаёт CSV отчёт для типа CSV.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.CSV)

    # Проверки
    assert isinstance(report, csv_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_markdown_report_for_markdown_type():
    """
    Проверка, что фабрика создаёт Markdown отчёт для типа MARKDOWN.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.MARKDOWN)

    # Проверки
    assert isinstance(report, markdown_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_xml_report_for_xml_type():
    """
    Проверка, что фабрика создаёт XML отчёт для типа XML.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.XML)

    # Проверки
    assert isinstance(report, xml_report)
    assert isinstance(report, abstract_report)


def test_factory_creates_html_report_for_html_type():
    """
    Проверка, что фабрика создаёт HTML отчёт для типа HTML.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.HTML)

    # Проверки
    assert isinstance(report, html_report)
    assert isinstance(report, abstract_report)


def test_factory_create_with_string_type_names():
    """
    Проверка создания отчётов по строковым именам форматов.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    txt_rep = factory.create("TXT")
    csv_rep = factory.create("CSV")
    md_rep = factory.create("Markdown")
    xml_rep = factory.create("XML")
    html_rep = factory.create("HTML")

    # Проверки
    assert isinstance(txt_rep, text_report)
    assert isinstance(csv_rep, csv_report)
    assert isinstance(md_rep, markdown_report)
    assert isinstance(xml_rep, xml_report)
    assert isinstance(html_rep, html_report)


def test_factory_create_returns_new_instance_each_time():
    """
    Проверка, что каждый вызов create возвращает новый экземпляр отчёта.
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report1 = factory.create(report_type_enum.TXT)
    report2 = factory.create(report_type_enum.TXT)

    # Проверки
    assert report1 is not report2


def test_error_create_with_invalid_report_type():
    """
    Проверка генерации исключения при передаче несуществующего типа отчёта.
    """
    # Подготовка
    factory = report_factory()
    invalid_format = "несуществующий_тип"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        factory.create(invalid_format)

    # Проверки
    assert exc_info.value is not None


def test_factory_encapsulates_settings_via_constructor():
    """
    Проверка инкапсуляции настроек в фабрику через конструктор.
    """
    # Подготовка
    settings = settings_model()
    settings.response_format = report_type_enum.CSV

    # Действие
    factory = report_factory(settings=settings)

    # Проверки
    assert factory.settings is settings
    assert factory.settings.response_format == report_type_enum.CSV


def test_factory_settings_setter():
    """
    Проверка установки настроек через свойство settings.
    """
    # Подготовка
    factory = report_factory()
    new_settings = settings_model()
    new_settings.response_format = report_type_enum.HTML

    # Действие
    factory.settings = new_settings

    # Проверки
    assert factory.settings is new_settings


def test_factory_create_default_uses_encapsulated_settings():
    """
    Проверка создания отчёта по умолчанию в зависимости от формата в настройках.
    """
    # Подготовка
    settings = settings_model()
    settings.response_format = report_type_enum.CSV
    factory = report_factory(settings=settings)

    # Действие
    rep_csv = factory.create_default()

    settings.response_format = report_type_enum.MARKDOWN
    rep_md = factory.create_default()

    settings.response_format = report_type_enum.XML
    rep_xml = factory.create_default()

    settings.response_format = report_type_enum.HTML
    rep_html = factory.create_default()

    settings.response_format = report_type_enum.TXT
    rep_txt = factory.create_default()

    # Проверки
    assert isinstance(rep_csv, csv_report)
    assert isinstance(rep_md, markdown_report)
    assert isinstance(rep_xml, xml_report)
    assert isinstance(rep_html, html_report)
    assert isinstance(rep_txt, text_report)
