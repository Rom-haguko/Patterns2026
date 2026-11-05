import pytest
from src.core.exception import arguments_exception
from src.logics.csv_report import csv_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_csv_report_for_recipe():
    """
    Проверка формирования CSV отчёта по рецепту:
    результат должен содержать непустые бинарные данные с заголовками и строками состава.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная", group, gram)
    row = recipe_row_model.create(nom, brutto=200.0, netto=190.0, range=gram)
    recipe = recipe_model.create(name="Пирог", rows=[row])
    report = csv_report()

    # Действие
    result = report.build(recipe)

    # Проверки
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    assert result.text == ""
    decoded = bytes(result.binary).decode("utf-8")
    assert "Наименование;Брутто;Нетто" in decoded
    assert "Мука;200.0;190.0" in decoded


def test_success_build_csv_report_for_nomenclature():
    """
    Проверка формирования CSV отчёта для номенклатуры:
    результат должен содержать бинарные данные с реквизитами номенклатуры.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Сахар", "Сахар-песок белый", group, gram)
    report = csv_report()

    # Действие
    result = report.build(nom)

    # Проверки
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    decoded = bytes(result.binary).decode("utf-8")
    assert "Код;Наименование;Полное наименование;Группа;Единица измерения" in decoded
    assert nom.id in decoded
    assert "Сахар" in decoded
    assert "Сахар-песок белый" in decoded
    assert "Сырьё" in decoded
    assert "грамм" in decoded


def test_success_build_csv_report_for_range():
    """
    Проверка формирования CSV отчёта для единицы измерения:
    результат должен содержать бинарные данные с полями единицы измерения.
    """
    # Подготовка
    gram = range_model.create_gram()
    kilo = range_model.create("килограмм", 1000, gram)
    report = csv_report()

    # Действие
    result = report.build(kilo)

    # Проверки
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    decoded = bytes(result.binary).decode("utf-8")
    assert "Код;Наименование;Коэффициент;Базовая единица" in decoded
    assert kilo.id in decoded
    assert "килограмм" in decoded
    assert "1000" in decoded
    assert "грамм" in decoded


def test_error_build_csv_report_with_invalid_source():
    """
    Проверка генерации исключения arguments_exception при некорректном источнике.
    """
    # Подготовка
    report = csv_report()
    invalid_source = 12345

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        report.build(invalid_source)

    # Проверки
    assert exc_info.value is not None


def test_success_build_csv_report_for_collection():
    """
    Проверка формирования CSV отчёта для коллекции сущностей.
    """
    # Подготовка
    gram = range_model.create_gram()
    piece = range_model.create_piece()
    report = csv_report()

    # Действие
    result = report.build([gram, piece])

    # Проверки
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    decoded = bytes(result.binary).decode("utf-8")
    assert "грамм" in decoded
    assert "штука" in decoded
    assert "Код;Наименование;Коэффициент;Базовая единица" in decoded
