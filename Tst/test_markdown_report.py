import pytest
from src.core.validator import argument_exception
from src.logics.markdown_report import markdown_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_markdown_report_for_recipe():
    """
    <summary>
    Проверка формирования Markdown отчёта по рецепту:
    результат должен содержать бинарные данные с Markdown таблицей ингредиентов.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Сыр", "Сыр Моцарелла", group, gram)
    row = recipe_row_model.create(nom, brutto=150.0, netto=140.0, range=gram)
    recipe = recipe_model.create(name="Пицца Сырная", rows=[row])

    report = markdown_report()
    result = report.build(recipe)

    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    assert result.text == ""

    decoded = bytes(result.binary).decode("utf-8")
    assert "# Рецепт: Пицца Сырная" in decoded
    assert "| Наименование | Брутто | Нетто |" in decoded
    assert "| Сыр | 150.0 | 140.0 |" in decoded


def test_success_build_markdown_report_for_nomenclature():
    """
    <summary>
    Проверка формирования Markdown отчёта для номенклатуры:
    результат должен содержать бинарные данные с реквизитами номенклатуры.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Соль", "Соль пищевая мелкая", group, gram)

    report = markdown_report()
    result = report.build(nom)

    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    decoded = bytes(result.binary).decode("utf-8")
    assert "# Номенклатура: Соль" in decoded
    assert "| Код | Наименование | Полное наименование | Группа | Единица измерения |" in decoded
    assert nom.id in decoded
    assert "Соль" in decoded
    assert "Соль пищевая мелкая" in decoded


def test_success_build_markdown_report_for_range():
    """
    <summary>
    Проверка формирования Markdown отчёта для единицы измерения:
    результат должен содержать бинарные данные с полями единицы измерения.
    </summary>
    """
    ml = range_model.create_milliliter()
    liter = range_model.create("литр", 1000, ml)

    report = markdown_report()
    result = report.build(liter)

    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    decoded = bytes(result.binary).decode("utf-8")
    assert "# Единица измерения: литр" in decoded
    assert "| Код | Наименование | Коэффициент | Базовая единица |" in decoded
    assert liter.id in decoded
    assert "1000" in decoded
    assert "миллилитр" in decoded


def test_error_build_markdown_report_with_invalid_source():
    """
    <summary>
    Проверка генерации исключения argument_exception при передаче некорректного источника.
    </summary>
    """
    report = markdown_report()
    with pytest.raises(argument_exception):
        report.build("некорректный источник")
