import pytest
from src.core.validator import argument_exception
from src.logics.html_report import html_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_html_report_for_recipe():
    """
    <summary>
    Проверка формирования HTML отчёта по рецепту:
    результат должен содержать HTML разметку с заголовком и таблицей строк.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Базилик", "Базилик свежий", group, gram)
    row = recipe_row_model.create(nom, brutto=10.0, netto=8.0, range=gram)
    recipe = recipe_model.create(name="Пицца с базиликом", rows=[row])

    report = html_report()
    result = report.build(recipe)

    assert isinstance(result, report_result_dto)
    assert result.text != ""
    assert result.binary == []

    text = result.text
    assert "<!DOCTYPE html>" in text
    assert "<html>" in text
    assert "<h1>Рецепт: Пицца с базиликом</h1>" in text
    assert "<th>Наименование</th>" in text
    assert "<td>Базилик</td>" in text
    assert "<td>10.0</td>" in text
    assert "<td>8.0</td>" in text
    assert "</html>" in text


def test_success_build_html_report_for_nomenclature():
    """
    <summary>
    Проверка формирования HTML отчёта для номенклатуры:
    результат должен содержать HTML разметку с реквизитами номенклатуры.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Перец", "Перец черный молотый", group, gram)

    report = html_report()
    result = report.build(nom)

    assert isinstance(result, report_result_dto)
    text = result.text
    assert "<h1>Номенклатура: Перец</h1>" in text
    assert f"<td>{nom.id}</td>" in text
    assert "<td>Перец черный молотый</td>" in text
    assert "<td>Сырьё</td>" in text


def test_success_build_html_report_for_range():
    """
    <summary>
    Проверка формирования HTML отчёта для единицы измерения:
    результат должен содержать HTML таблицу со свойствами единицы измерения.
    </summary>
    """
    gram = range_model.create_gram()

    report = html_report()
    result = report.build(gram)

    assert isinstance(result, report_result_dto)
    text = result.text
    assert "<h1>Единица измерения: грамм</h1>" in text
    assert f"<td>{gram.id}</td>" in text
    assert "<td>1</td>" in text


def test_error_build_html_report_with_invalid_source():
    """
    <summary>
    Проверка генерации исключения argument_exception при некорректном источнике.
    </summary>
    """
    report = html_report()
    with pytest.raises(argument_exception):
        report.build(["невалидный список"])
