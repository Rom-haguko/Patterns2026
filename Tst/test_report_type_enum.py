from enum import Enum
import pytest
from src.dtos.report_type_enum import report_type_enum


def test_enum_has_txt_value():
    """
    Проверка наличия значения TXT в перечислении типов отчётов.
    """
    # Подготовка
    attr_name = "TXT"

    # Действие
    has_attr = hasattr(report_type_enum, attr_name)

    # Проверки
    assert has_attr is True


def test_enum_txt_value_equals_one():
    """
    Проверка числового значения элемента TXT.
    """
    # Подготовка
    element = report_type_enum.TXT

    # Действие
    val = element.value

    # Проверки
    assert val == 1


def test_enum_is_enum_subclass():
    """
    Проверка, что report_type_enum является наследником Enum.
    """
    # Подготовка
    cls = report_type_enum

    # Действие
    is_sub = issubclass(cls, Enum)

    # Проверки
    assert is_sub is True


def test_enum_txt_is_singleton():
    """
    Проверка, что элементы перечисления являются синглтонами:
    два обращения к TXT возвращают один и тот же объект.
    """
    # Подготовка
    # (Обращение к элементу перечисления)

    # Действие
    txt1 = report_type_enum.TXT
    txt2 = report_type_enum.TXT

    # Проверки
    assert txt1 is txt2


def test_enum_has_all_required_formats():
    """
    Проверка наличия всех форматов отчетов: CSV, MARKDOWN, XML, TXT, HTML.
    """
    # Подготовка
    required_formats = ["TXT", "CSV", "MARKDOWN", "XML", "HTML"]

    # Действие
    present = [hasattr(report_type_enum, fmt) for fmt in required_formats]

    # Проверки
    assert all(present)


def test_enum_from_string_successful_conversion():
    """
    Проверка метода from_string для строковых названий форматов.
    """
    # Подготовка
    samples = [
        ("csv", report_type_enum.CSV),
        ("CSV", report_type_enum.CSV),
        ("markdown", report_type_enum.MARKDOWN),
        ("Markdown", report_type_enum.MARKDOWN),
        ("md", report_type_enum.MARKDOWN),
        ("xml", report_type_enum.XML),
        ("txt", report_type_enum.TXT),
        ("html", report_type_enum.HTML),
    ]

    # Действие
    results = [report_type_enum.from_string(name) for name, _ in samples]

    # Проверки
    for (_, expected), actual in zip(samples, results):
        assert actual == expected


def test_enum_equality_with_string():
    """
    Проверка прямого сравнения элемента перечисления со строкой.
    """
    # Подготовка
    element_csv = report_type_enum.CSV
    element_md = report_type_enum.MARKDOWN
    element_xml = report_type_enum.XML

    # Действие
    match_csv_upper = element_csv == "CSV"
    match_csv_lower = element_csv == "csv"
    match_md = element_md == "Markdown"
    match_xml = element_xml == "XML"

    # Проверки
    assert match_csv_upper is True
    assert match_csv_lower is True
    assert match_md is True
    assert match_xml is True
