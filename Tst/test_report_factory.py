import pytest
from src.core.exception import arguments_exception
from src.logics.report_factory import report_factory
from src.logics.text_report import text_report
from src.core.abstract_report import abstract_report
from src.dtos.report_type_enum import report_type_enum

# ─────────────────────────── Тесты создания report_factory ─────────────────────

def test_success_create_report_factory():
    """
    <summary>
    Проверка успешного создания экземпляра фабрики отчётов.
    </summary>
    """
    # Подготовка & Действие
    factory = report_factory()

    # Проверка
    assert isinstance(factory, report_factory)

def test_factory_creates_text_report_for_txt_type():
    """
    <summary>
    Проверка, что фабрика создаёт текстовый отчёт для типа TXT.
    </summary>
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.TXT)

    # Проверка
    assert isinstance(report, text_report)
    assert isinstance(report, abstract_report)

def test_factory_create_returns_new_instance_each_time():
    """
    <summary>
    Проверка, что каждый вызов create возвращает новый экземпляр отчёта,
    а не переиспользует ранее созданный.
    </summary>
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report1 = factory.create(report_type_enum.TXT)
    report2 = factory.create(report_type_enum.TXT)

    # Проверка
    assert report1 is not report2

def test_error_create_with_invalid_report_type():
    """
    <summary>
    Проверка генерации исключения при передаче несуществующего типа отчёта.
    </summary>
    """
    # Подготовка
    factory = report_factory()

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        factory.create("несуществующий_тип")