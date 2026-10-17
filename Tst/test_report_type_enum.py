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