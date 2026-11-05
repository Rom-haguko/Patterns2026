import pytest
from main import api
from src.logics.report_service import report_service
from src.logics.storage_manager import storage_manager
from src.dtos.report_type_enum import report_type_enum


def test_report_service_get_recipe_by_name_found():
    """
    Проверка успешного поиска рецепта по части наименования.
    """
    # Подготовка
    service = report_service()
    search_name = "Маргарита"

    # Действие
    recipe = service.get_recipe_by_name(search_name)

    # Проверки
    assert recipe is not None
    assert search_name in recipe.name


def test_report_service_get_recipe_by_name_not_found():
    """
    Проверка возврата None при поиске несуществующего рецепта.
    """
    # Подготовка
    service = report_service()
    non_existent_name = "Несуществующая пицца 12345"

    # Действие
    recipe = service.get_recipe_by_name(non_existent_name)

    # Проверки
    assert recipe is None


def test_report_service_get_entity_found():
    """
    Проверка получения сущности по типу и коду.
    """
    # Подготовка
    service = report_service()
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    target = recipes[0]

    # Действие
    entity = service.get_entity("recipe", target.id)

    # Проверки
    assert entity is not None
    assert entity.id == target.id


def test_report_service_get_entity_not_found():
    """
    Проверка возврата None при запросе несуществующей сущности.
    """
    # Подготовка
    service = report_service()
    wrong_id = "wrong_id_000"

    # Действие
    entity = service.get_entity("recipe", wrong_id)

    # Проверки
    assert entity is None


def test_report_service_build_report_with_format():
    """
    Проверка построения отчета в указанном формате TXT.
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    response = service.build_report(recipe, report_type_enum.TXT)

    # Проверки
    assert response.status_code == 200
    assert "Наименование | Брутто | Нетто" in response.get_data(as_text=True)


def test_report_service_build_report_default():
    """
    Проверка построения отчета в формате по умолчанию.
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    with api.app.test_request_context():
        response = service.build_report(recipe)

    # Проверки
    assert response.status_code == 200
    assert response.mimetype == "text/markdown"


def test_report_service_get_report_response_invalid_type():
    """
    Проверка возврата ошибки при запросе неизвестного типа сущности.
    """
    # Подготовка
    service = report_service()

    # Действие
    result, status = service.get_report_response("unknown_type", "123")

    # Проверки
    assert status == 400
    assert "error" in result


def test_report_service_get_report_response_not_found():
    """
    Проверка возврата ошибки 404 при отсутствии сущности.
    """
    # Подготовка
    service = report_service()

    # Действие
    result, status = service.get_report_response("recipe", "unknown_code_999")

    # Проверки
    assert status == 404
    assert "error" in result


def test_report_service_get_report_response_invalid_format():
    """
    Проверка возврата ошибки при запросе неподдерживаемого формата отчета.
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    result, status = service.get_report_response("recipe", recipe.id, "bad_format")

    # Проверки
    assert status == 400
    assert "error" in result


def test_report_service_get_default_recipe_report():
    """
    Проверка формирования базового отчета по рецепту по умолчанию.
    """
    # Подготовка
    service = report_service()
    recipe_name = "Маргарита"

    # Действие
    response = service.get_default_recipe_report(recipe_name)

    # Проверки
    assert response.status_code == 200
