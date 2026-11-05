import pytest
from src.core.exception import arguments_exception
from src.logics.markdown_report import markdown_report
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model
from src.dtos.report_result_dto import report_result_dto


def test_success_build_markdown_report_for_recipe():
    """
    Проверка формирования Markdown отчёта по рецепту:
    результат должен содержать бинарные данные с Markdown таблицей ингредиентов.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Сыр", "Сыр Моцарелла", group, gram)
    row = recipe_row_model.create(nom, brutto=150.0, netto=140.0, range=gram)
    recipe = recipe_model.create(name="Пицца Сырная", rows=[row])
    report = markdown_report()

    # Действие
    result = report.build(recipe)

    # Проверки
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    assert result.text == ""
    decoded = bytes(result.binary).decode("utf-8")
    assert "# Рецепт: Пицца Сырная" in decoded
    assert "| Наименование | Брутто | Нетто |" in decoded
    assert "| Сыр | 150.0 | 140.0 |" in decoded


def test_success_build_markdown_report_for_nomenclature():
    """
    Проверка формирования Markdown отчёта для номенклатуры:
    результат должен содержать бинарные данные с реквизитами номенклатуры.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Соль", "Соль пищевая мелкая", group, gram)
    report = markdown_report()

    # Действие
    result = report.build(nom)

    # Проверки
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
    Проверка формирования Markdown отчёта для единицы измерения:
    результат должен содержать бинарные данные с полями единицы измерения.
    """
    # Подготовка
    ml = range_model.create_milliliter()
    liter = range_model.create("литр", 1000, ml)
    report = markdown_report()

    # Действие
    result = report.build(liter)

    # Проверки
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
    Проверка генерации исключения arguments_exception при передаче некорректного источника.
    """
    # Подготовка
    report = markdown_report()
    invalid_source = "некорректный источник"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        report.build(invalid_source)

    # Проверки
    assert exc_info.value is not None


def test_success_build_markdown_report_for_collection():
    """
    Проверка формирования Markdown отчёта для коллекции сущностей.
    """
    # Подготовка
    gram = range_model.create_gram()
    piece = range_model.create_piece()
    report = markdown_report()

    # Действие
    result = report.build([gram, piece])

    # Проверки
    assert isinstance(result, report_result_dto)
    decoded = bytes(result.binary).decode("utf-8")
    assert "грамм" in decoded
    assert "штука" in decoded
    assert "Всего записей: 2" in decoded
