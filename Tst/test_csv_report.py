import pytest
from src.core.validator import argument_exception
from src.logics.csv_report import csv_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_csv_report_for_recipe():
    """
    <summary>
    Проверка формирования CSV отчёта по рецепту:
    результат должен содержать непустые бинарные данные с заголовками и строками состава.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная", group, gram)
    row = recipe_row_model.create(nom, brutto=200.0, netto=190.0, range=gram)
    recipe = recipe_model.create(name="Пирог", rows=[row])

    report = csv_report()
    result = report.build(recipe)

    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    assert result.text == ""

    decoded = bytes(result.binary).decode("utf-8")
    assert "Наименование;Брутто;Нетто" in decoded
    assert "Мука;200.0;190.0" in decoded


def test_success_build_csv_report_for_nomenclature():
    """
    <summary>
    Проверка формирования CSV отчёта для номенклатуры:
    результат должен содержать бинарные данные с реквизитами номенклатуры.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Сахар", "Сахар-песок белый", group, gram)

    report = csv_report()
    result = report.build(nom)

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
    <summary>
    Проверка формирования CSV отчёта для единицы измерения:
    результат должен содержать бинарные данные с полями единицы измерения.
    </summary>
    """
    gram = range_model.create_gram()
    kilo = range_model.create("килограмм", 1000, gram)

    report = csv_report()
    result = report.build(kilo)

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
    <summary>
    Проверка генерации исключения argument_exception при некорректном источнике.
    </summary>
    """
    report = csv_report()
    with pytest.raises(argument_exception):
        report.build(12345)
