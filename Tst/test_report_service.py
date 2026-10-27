import pytest
from main import api
from src.logics.report_service import report_service
from src.logics.storage_manager import storage_manager
from src.dtos.report_type_enum import report_type_enum


def test_report_service_get_recipe_by_name_found():
    """
    <summary>
    Проверка успешного поиска рецепта по части наименования.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    recipe = service.get_recipe_by_name("Маргарита")

    # Проверка
    assert recipe is not None
    assert "Маргарита" in recipe.name


def test_report_service_get_recipe_by_name_not_found():
    """
    <summary>
    Проверка возврата None при поиске несуществующего рецепта.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    recipe = service.get_recipe_by_name("Несуществующая пицца 12345")

    # Проверка
    assert recipe is None


def test_report_service_get_entity_found():
    """
    <summary>
    Проверка получения сущности по типу и коду.
    </summary>
    """
    # Подготовка
    service = report_service()
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    target = recipes[0]

    # Действие
    entity = service.get_entity("recipe", target.id)

    # Проверка
    assert entity is not None
    assert entity.id == target.id


def test_report_service_get_entity_not_found():
    """
    <summary>
    Проверка возврата None при запросе несуществующей сущности.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    entity = service.get_entity("recipe", "wrong_id_000")

    # Проверка
    assert entity is None


def test_report_service_build_report_with_format():
    """
    <summary>
    Проверка построения отчета в указанном формате.
    </summary>
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    response = service.build_report(recipe, report_type_enum.TXT)

    # Проверка
    assert response.status_code == 200
    assert "Наименование | Брутто | Нетто" in response.get_data(as_text=True)


def test_report_service_build_report_default():
    """
    <summary>
    Проверка построения отчета в формате по умолчанию.
    </summary>
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    with api.app.test_request_context():
        response = service.build_report(recipe)

    # Проверка
    assert response.status_code == 200
    assert response.mimetype == "text/markdown"


def test_report_service_get_report_response_invalid_type():
    """
    <summary>
    Проверка возврата ошибки при запросе неизвестного типа сущности.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    result, status = service.get_report_response("unknown_type", "123")

    # Проверка
    assert status == 400
    assert "error" in result


def test_report_service_get_report_response_not_found():
    """
    <summary>
    Проверка возврата ошибки 404 при отсутствии сущности.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    result, status = service.get_report_response("recipe", "unknown_code_999")

    # Проверка
    assert status == 404
    assert "error" in result


def test_report_service_get_report_response_invalid_format():
    """
    <summary>
    Проверка возврата ошибки при запросе неподдерживаемого формата отчета.
    </summary>
    """
    # Подготовка
    service = report_service()
    recipe = service.get_recipe_by_name("Маргарита")

    # Действие
    result, status = service.get_report_response("recipe", recipe.id, "bad_format")

    # Проверка
    assert status == 400
    assert "error" in result


def test_report_service_get_default_recipe_report():
    """
    <summary>
    Проверка формирования базового отчета по рецепту по умолчанию.
    </summary>
    """
    # Подготовка
    service = report_service()

    # Действие
    response = service.get_default_recipe_report("Маргарита")

    # Проверка
    assert response.status_code == 200
