import pytest
from src.core.validator import argument_exception
from src.logics.xml_report import xml_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_xml_report_for_recipe():
    """
    <summary>
    Проверка формирования XML отчёта по рецепту:
    результат должен содержать структурированный XML с тегами recipe, rows, row.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Томаты", "Томаты свежие", group, gram)
    row = recipe_row_model.create(nom, brutto=120.0, netto=100.0, range=gram)
    recipe = recipe_model.create(name="Соус", rows=[row])

    report = xml_report()
    result = report.build(recipe)

    assert isinstance(result, report_result_dto)
    assert result.text != ""
    assert result.binary == []

    text = result.text
    assert '<?xml version="1.0" encoding="utf-8"?>' in text
    assert "<recipe>" in text
    assert f"<id>{recipe.id}</id>" in text
    assert "<name>Соус</name>" in text
    assert "<rows>" in text
    assert "<nomenclature>Томаты</nomenclature>" in text
    assert "<brutto>120.0</brutto>" in text
    assert "<netto>100.0</netto>" in text
    assert "</recipe>" in text


def test_success_build_xml_report_for_nomenclature():
    """
    <summary>
    Проверка формирования XML отчёта для номенклатуры:
    результат должен содержать теги nomenclature, id, name, full_name, group, range.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Масло", "Масло оливковое", group, gram)

    report = xml_report()
    result = report.build(nom)

    assert isinstance(result, report_result_dto)
    text = result.text
    assert "<nomenclature>" in text
    assert f"<id>{nom.id}</id>" in text
    assert "<name>Масло</name>" in text
    assert "<full_name>Масло оливковое</full_name>" in text
    assert "<group>Сырьё</group>" in text
    assert "<range>грамм</range>" in text
    assert "</nomenclature>" in text


def test_success_build_xml_report_for_range():
    """
    <summary>
    Проверка формирования XML отчёта для единицы измерения:
    результат должен содержать теги range, id, name, conversion_factor, base_range.
    </summary>
    """
    piece = range_model.create_piece()

    report = xml_report()
    result = report.build(piece)

    assert isinstance(result, report_result_dto)
    text = result.text
    assert "<range>" in text
    assert f"<id>{piece.id}</id>" in text
    assert "<name>штука</name>" in text
    assert "<conversion_factor>1</conversion_factor>" in text
    assert "</range>" in text


def test_error_build_xml_report_with_invalid_source():
    """
    <summary>
    Проверка генерации исключения argument_exception при некорректном источнике.
    </summary>
    """
    report = xml_report()
    with pytest.raises(argument_exception):
        report.build(None)
