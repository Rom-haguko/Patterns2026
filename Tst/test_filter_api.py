import pytest
from main import api


class connexion_test_client_wrapper:
    """Обертка над тестовым клиентом Connexion для совместимости вызовов в тестах."""

    def __init__(self, client):
        self._client = client

    def _wrap(self, response):
        """Оборачивает объект ответа для совместимости с get_json."""
        if not hasattr(response, "get_json"):
            response.get_json = lambda: response.json() if response.text else None
        return response

    def get(self, *args, **kwargs):
        """Выполняет GET запрос."""
        return self._wrap(self._client.get(*args, **kwargs))

    def post(self, *args, **kwargs):
        """Выполняет POST запрос."""
        return self._wrap(self._client.post(*args, **kwargs))

    def put(self, *args, **kwargs):
        """Выполняет PUT запрос."""
        return self._wrap(self._client.put(*args, **kwargs))

    def delete(self, *args, **kwargs):
        """Выполняет DELETE запрос."""
        return self._wrap(self._client.delete(*args, **kwargs))


@pytest.fixture
def client():
    # Подготовка тестового клиента Connexion
    with api.test_client() as test_client:
        yield connexion_test_client_wrapper(test_client)


def test_filter_api_range_like(client):
    # Подготовка
    payload = {
        "name": "кило",
        "name_filter_type": "LIKE",
    }

    # Действие
    response = client.post("/api/filter/range", json=payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any("килограмм" in item.get("name", "").lower() for item in data)


def test_filter_api_nomenclature_nested_group(client):
    # Подготовка: поиск номенклатуры по имени группы 'Сырьё'
    payload = {
        "name": "Сырьё",
        "name_filter_type": "EQUALS",
    }

    # Действие
    response = client.post("/api/filter/nomenclature", json=payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_filter_api_recipe(client):
    # Подготовка
    payload = {
        "name": "Маргарита",
        "name_filter_type": "LIKE",
    }

    # Действие
    response = client.post("/api/filter/recipe", json=payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any("маргарита" in item.get("name", "").lower() for item in data)


def test_filter_api_unknown_entity_404(client):
    # Подготовка
    payload = {"name": "тест"}

    # Действие
    response = client.post("/api/filter/unknown_model_type", json=payload)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_filter_schema_api_nomenclature(client):
    # Подготовка
    entity_type = "nomenclature"

    # Действие
    response = client.get(f"/api/filter/{entity_type}/schema")

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data.get("available_fields") == ["name", "id"]
    assert "group" in data.get("nested_search_supported", [])
    assert "range" in data.get("nested_search_supported", [])
    assert "recipe" in data.get("nested_search_supported", [])

    filterable = data.get("filterable_nested_fields", [])
    assert len(filterable) >= 3
    group_entry = next((item for item in filterable if item.get("field") == "group"), None)
    assert group_entry is not None
    assert group_entry.get("nested_fields") == ["name", "id"]


def test_filter_schema_api_unknown_entity_404(client):
    # Подготовка
    entity_type = "non_existent_model"

    # Действие
    response = client.get(f"/api/filter/{entity_type}/schema")

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_osv_api_unfiltered(client):
    # Подготовка
    payload = {}

    # Действие
    response = client.post("/api/osv", json=payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 3

    flour_row = next((r for r in data if "мука" in r.get("nomenclature", {}).get("name", "").lower()), None)
    assert flour_row is not None
    assert flour_row.get("initial_balance") == 0.0
    assert flour_row.get("inflow") == 100.0
    assert flour_row.get("outflow") == 20.0
    assert flour_row.get("final_balance") == 80.0


def test_osv_api_filtered(client):
    # Подготовка
    payload = {
        "name": "Мука",
        "name_filter_type": "LIKE",
    }

    # Действие
    response = client.post("/api/osv", json=payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    row = data[0]
    nom_data = row.get("nomenclature", {})
    assert "мука" in nom_data.get("name", "").lower()
    assert row.get("inflow") == 100.0
    assert row.get("outflow") == 20.0
    assert row.get("final_balance") == 80.0
