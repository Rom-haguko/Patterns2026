import pytest
from enum import Enum
from src.dtos.report_type_enum import report_type_enum

# ─────────────────────────── Тесты структуры report_type_enum ─────────────────────

def test_enum_has_txt_value():
    """
    <summary>
    Проверка наличия значения TXT в перечислении типов отчётов.
    </summary>
    """
    # Действие & Проверка
    assert hasattr(report_type_enum, "TXT")

def test_enum_txt_value_equals_one():
    """
    <summary>
    Проверка числового значения элемента TXT.
    </summary>
    """
    # Действие & Проверка
    assert report_type_enum.TXT.value == 1

def test_enum_is_enum_subclass():
    """
    <summary>
    Проверка, что report_type_enum является наследником Enum.
    </summary>
    """
    # Действие & Проверка
    assert issubclass(report_type_enum, Enum)

def test_enum_txt_is_singleton():
    """
    <summary>
    Проверка, что элементы перечисления являются синглтонами:
    два обращения к TXT возвращают один и тот же объект.
    </summary>
    """
    # Подготовка & Действие
    txt1 = report_type_enum.TXT
    txt2 = report_type_enum.TXT

    # Проверка
    assert txt1 is txt2


def test_enum_has_all_required_formats():
    """
    <summary>
    Проверка наличия всех форматов отчетов: CSV, MARKDOWN, XML, TXT, HTML.
    </summary>
    """
    assert hasattr(report_type_enum, "TXT")
    assert hasattr(report_type_enum, "CSV")
    assert hasattr(report_type_enum, "MARKDOWN")
    assert hasattr(report_type_enum, "XML")
    assert hasattr(report_type_enum, "HTML")


def test_enum_from_string_successful_conversion():
    """
    <summary>
    Проверка метода from_string для строковых названий форматов.
    </summary>
    """
    assert report_type_enum.from_string("csv") == report_type_enum.CSV
    assert report_type_enum.from_string("CSV") == report_type_enum.CSV
    assert report_type_enum.from_string("markdown") == report_type_enum.MARKDOWN
    assert report_type_enum.from_string("Markdown") == report_type_enum.MARKDOWN
    assert report_type_enum.from_string("md") == report_type_enum.MARKDOWN
    assert report_type_enum.from_string("xml") == report_type_enum.XML
    assert report_type_enum.from_string("txt") == report_type_enum.TXT
    assert report_type_enum.from_string("html") == report_type_enum.HTML


def test_enum_equality_with_string():
    """
    <summary>
    Проверка прямого сравнения элемента перечисления со строкой.
    </summary>
    """
    assert report_type_enum.CSV == "CSV"
    assert report_type_enum.CSV == "csv"
    assert report_type_enum.MARKDOWN == "Markdown"
    assert report_type_enum.XML == "XML"