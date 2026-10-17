import pytest
from main import api
from src.logics.storage_manager import storage_manager
from src.dtos.report_type_enum import report_type_enum


@pytest.fixture
def client():
    """
    Фикстура для создания тестового клиента Flask приложения.
    """
    app = api.app
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_api_legacy_get_report_success(client):
    """
    <summary>
    Проверка работы существующего эндпоинта /api/get_report:
    должен возвращать 200 и текст с ингредиентами.
    </summary>
    """
    response = client.get("/api/get_report")
    assert response.status_code == 200
    assert "Наименование | Брутто | Нетто" in response.get_data(as_text=True)


def test_api_get_report_csv_recipe_download(client):
    """
    <summary>
    Проверка скачивания файла CSV для рецепта:
    возвращает статус 200, заголовок Content-Disposition и бинарный CSV.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    recipe = recipes[0]

    response = client.get(f"/api/report/csv/recipe/{recipe.id}")
    assert response.status_code == 200
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert "report.csv" in response.headers.get("Content-Disposition", "")
    data = response.get_data(as_text=True)
    assert "Наименование;Брутто;Нетто" in data


def test_api_get_report_markdown_recipe_download(client):
    """
    <summary>
    Проверка скачивания файла Markdown для рецепта:
    возвращает статус 200, заголовок Content-Disposition и бинарный Markdown.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    recipe = recipes[0]

    response = client.get(f"/api/report/markdown/recipe/{recipe.id}")
    assert response.status_code == 200
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert "report.md" in response.headers.get("Content-Disposition", "")
    data = response.get_data(as_text=True)
    assert f"# Рецепт: {recipe.name}" in data


def test_api_get_report_xml_nomenclature_structured_text(client):
    """
    <summary>
    Проверка получения структурированного XML для номенклатуры:
    возвращает статус 200 и валидную XML структуру.
    </summary>
    """
    manager = storage_manager()
    items = manager.get(storage_manager.nomenclature_key())
    nom = items[0]

    response = client.get(f"/api/report/xml/номенклатура/{nom.id}")
    assert response.status_code == 200
    assert "application/xml" in response.headers.get("Content-Type", "")
    data = response.get_data(as_text=True)
    assert "<nomenclature>" in data
    assert f"<id>{nom.id}</id>" in data
    assert f"<name>{nom.name}</name>" in data


def test_api_get_report_html_range_structured_text(client):
    """
    <summary>
    Проверка получения структурированного HTML для единицы измерения:
    возвращает статус 200 и HTML разметку.
    </summary>
    """
    manager = storage_manager()
    ranges = manager.get(storage_manager.range_key())
    unit = ranges[0]

    response = client.get(f"/api/report/html/единица_измерения/{unit.id}")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")
    data = response.get_data(as_text=True)
    assert "<!DOCTYPE html>" in data
    assert f"<h1>{unit.name}</h1>" in data


def test_api_get_report_default_endpoint(client):
    """
    <summary>
    Проверка эндпоинта /api/report/default/<type>/<code> с использованием create_default:
    возвращает статус 200.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    recipe = recipes[0]

    response = client.get(f"/api/report/default/recipe/{recipe.id}")
    assert response.status_code == 200
    assert len(response.data) > 0


def test_api_get_report_by_query_params(client):
    """
    <summary>
    Проверка эндпоинта /api/report через параметры запроса (format, type, code).
    </summary>
    """
    manager = storage_manager()
    items = manager.get(storage_manager.nomenclature_key())
    nom = items[0]

    response = client.get(f"/api/report?format=xml&type=номенклатура&code={nom.id}")
    assert response.status_code == 200
    assert "<nomenclature>" in response.get_data(as_text=True)


def test_api_error_invalid_format(client):
    """
    <summary>
    Проверка возврата ошибки 400 при передаче неизвестного формата отчёта.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    recipe = recipes[0]

    response = client.get(f"/api/report/unknown_format/recipe/{recipe.id}")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_api_error_invalid_entity_type(client):
    """
    <summary>
    Проверка возврата ошибки 400 при передаче неизвестного типа сущности.
    </summary>
    """
    response = client.get("/api/report/xml/неизвестный_тип/12345")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_api_error_entity_not_found(client):
    """
    <summary>
    Проверка возврата ошибки 404 при отсутствии сущности с указанным кодом.
    </summary>
    """
    response = client.get("/api/report/xml/recipe/non_existent_id_99999")
    assert response.status_code == 404
    assert "error" in response.get_json()
