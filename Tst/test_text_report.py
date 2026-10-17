import pytest
from src.core.validator import argument_exception
from src.logics.text_report import text_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto

# ─────────────────────────── Тесты формирования text_report ─────────────────────

def test_success_build_text_report():
    """
    <summary>
    Проверка формирования текстового отчёта по рецепту:
    результат должен быть экземпляром report_result_dto с непустым текстом.
    </summary>
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная высший сорт", group, gram)
    row = recipe_row_model.create(nom, brutto=250.0, netto=240.0, range=gram)
    recipe = recipe_model.create(name="Тестовый рецепт", rows=[row])

    report = text_report()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert isinstance(result, report_result_dto)
    assert result.text != ""
    assert result.binary == []

def test_report_contains_header():
    """
    <summary>
    Проверка наличия заголовка таблицы в сформированном отчёте.
    </summary>
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Соль", "Соль пищевая", group, gram)
    row = recipe_row_model.create(nom, brutto=5.0, netto=5.0, range=gram)
    recipe = recipe_model.create(name="Рецепт с солью", rows=[row])

    report = text_report()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert "Наименование" in result.text
    assert "Брутто" in result.text
    assert "Нетто" in result.text

def test_report_contains_ingredient_data():
    """
    <summary>
    Проверка, что отчёт содержит данные ингредиента: наименование и веса.
    </summary>
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Сахар", "Сахар-песок белый", group, gram)
    row = recipe_row_model.create(nom, brutto=100.0, netto=95.0, range=gram)
    recipe = recipe_model.create(name="Сладкий рецепт", rows=[row])

    report = text_report()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert "Сахар" in result.text
    assert "100" in result.text
    assert "95" in result.text

def test_error_build_with_invalid_source():
    """
    <summary>
    Проверка генерации исключения при передаче некорректного источника
    (не экземпляра recipe_model).
    </summary>
    """
    # Подготовка
    report = text_report()

    # Действие & Проверка
    with pytest.raises(argument_exception):
        report.build("это не рецепт")