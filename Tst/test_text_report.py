import pytest
from src.core.exception import arguments_exception
from src.logics.text_report import text_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_text_report():
    """
    Проверка формирования текстового отчёта по рецепту:
    результат должен быть экземпляром report_result_dto с непустым текстом.
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

    # Проверки
    assert isinstance(result, report_result_dto)
    assert result.text != ""
    assert result.binary == []


def test_report_contains_header():
    """
    Проверка наличия заголовка таблицы в сформированном отчёте.
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

    # Проверки
    assert "Наименование" in result.text
    assert "Брутто" in result.text
    assert "Нетто" in result.text


def test_report_contains_ingredient_data():
    """
    Проверка, что отчёт содержит данные ингредиента: наименование и веса.
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

    # Проверки
    assert "Сахар" in result.text
    assert "100" in result.text
    assert "95" in result.text


def test_error_build_with_invalid_source():
    """
    Проверка генерации исключения при передаче некорректного источника
    (не экземпляра abstract_model).
    """
    # Подготовка
    report = text_report()
    invalid_source = "это не рецепт"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        report.build(invalid_source)

    # Проверки
    assert exc_info.value is not None


def test_success_build_text_report_for_nomenclature():
    """
    Проверка формирования текстового отчета для номенклатуры.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная", group, gram)
    report = text_report()

    # Действие
    result = report.build(nom)

    # Проверки
    assert "Мука" in result.text
    assert "Код | Наименование | Полное наименование | Группа | Единица измерения" in result.text


def test_success_build_text_report_for_range_model():
    """
    Проверка формирования текстового отчета для единицы измерения (range_model).
    """
    # Подготовка
    unit = range_model.create_kilogram()
    report = text_report()

    # Действие
    result = report.build(unit)

    # Проверки
    assert "килограмм" in result.text
    assert "1000" in result.text
    assert "Код | Наименование | Коэффициент | Базовая единица" in result.text


def test_success_build_text_report_for_collection():
    """
    Проверка формирования текстового отчета для коллекции сущностей.
    """
    # Подготовка
    gram = range_model.create_gram()
    piece = range_model.create_piece()
    report = text_report()

    # Действие
    result = report.build([gram, piece])

    # Проверки
    assert "грамм" in result.text
    assert "штука" in result.text
    assert "Всего записей: 2" in result.text
