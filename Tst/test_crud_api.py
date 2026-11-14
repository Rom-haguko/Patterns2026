import pytest
from main import api
from src.logics.storage_manager import storage_manager
from src.logics.settings_manager import settings_manager
from src.logics.deserialization_context import deserialization_context
from src.models.settings_model import settings_model


class connexion_test_client_wrapper:
    """Обертка над тестовым клиентом Connexion для совместимости вызовов в тестах."""

    def __init__(self, client):
        self._client = client

    def _wrap(self, response):
        if not hasattr(response, "get_json"):
            response.get_json = lambda: response.json() if response.text else None
        return response

    def get(self, *args, **kwargs):
        return self._wrap(self._client.get(*args, **kwargs))

    def post(self, *args, **kwargs):
        return self._wrap(self._client.post(*args, **kwargs))

    def put(self, *args, **kwargs):
        return self._wrap(self._client.put(*args, **kwargs))

    def delete(self, *args, **kwargs):
        return self._wrap(self._client.delete(*args, **kwargs))


@pytest.fixture
def client():
    """
    Фикстура тестового клиента приложения с полной изоляцией состояния хранилища и контекста.
    """
    deserialization_context().clear()
    manager = storage_manager()
    s_mgr = settings_manager()
    saved_settings = s_mgr.settings
    snapshot = {key: list(manager.get(key)) for key in list(manager.data.keys())}
    api.app._got_first_request = False
    with api.test_client() as test_client:
        yield connexion_test_client_wrapper(test_client)
    for key, items in snapshot.items():
        manager.data[key] = list(items)
    s_mgr.settings = saved_settings
    deserialization_context().clear()


# ---------------------------------------------------------------------------
# range
# ---------------------------------------------------------------------------

def test_get_all_range_returns_200(client):
    """
    Проверка получения полного списка единиц измерения со статусом 200.
    """
    # Подготовка
    endpoint = "/api/range"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_range_by_id_returns_200(client):
    """
    Проверка получения единицы измерения по существующему идентификатору со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    first_range = manager.get(storage_manager.range_key())[0]
    endpoint = f"/api/range/{first_range.id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == first_range.id
    assert data["name"] == first_range.name


def test_get_range_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующей единицы измерения.
    """
    # Подготовка
    endpoint = "/api/range/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_range_returns_201(client):
    """
    Проверка создания новой единицы измерения со статусом 201.
    """
    # Подготовка
    endpoint = "/api/range"
    payload = {"name": "тест", "conversion_factor": 1}

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "тест"
    assert "id" in data


def test_update_range_valid(client):
    """
    Проверка успешного обновления существующей единицы измерения со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/range", json={"name": "для_обновления", "conversion_factor": 1})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/range/{created_id}"
    update_payload = {"name": "обновленная_еи", "conversion_factor": 10}

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "обновленная_еи"
    assert data["conversion_factor"] == 10


def test_update_linked_range_id_conflict_returns_409(client):
    """
    Проверка запрета изменения идентификатора у связанной единицы измерения (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    linked_range = manager.get(storage_manager.range_key())[0]
    endpoint = f"/api/range/{linked_range.id}"
    update_payload = {"id": "new-conflicting-id", "name": "новое_имя", "conversion_factor": 1}

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_delete_free_range_returns_204_and_404_on_get(client):
    """
    Проверка удаления несвязанной единицы измерения (204) с контрольным подтверждением (404).
    """
    # Подготовка
    create_response = client.post("/api/range", json={"name": "для_удаления", "conversion_factor": 1})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/range/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_linked_range_returns_409(client):
    """
    Проверка запрета удаления единицы измерения, используемой в номенклатуре (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    linked_range_id = manager.get(storage_manager.range_key())[0].id
    endpoint = f"/api/range/{linked_range_id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


# ---------------------------------------------------------------------------
# nomenclature-group
# ---------------------------------------------------------------------------

def test_get_all_nomenclature_group_returns_200(client):
    """
    Проверка получения полного списка групп номенклатуры со статусом 200.
    """
    # Подготовка
    endpoint = "/api/nomenclature-group"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_nomenclature_group_by_id_returns_200(client):
    """
    Проверка получения группы номенклатуры по ID со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    group = manager.get(storage_manager.group_key())[0]
    endpoint = f"/api/nomenclature-group/{group.id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == group.id
    assert data["name"] == group.name


def test_get_nomenclature_group_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующей группы номенклатуры.
    """
    # Подготовка
    endpoint = "/api/nomenclature-group/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_nomenclature_group_returns_201(client):
    """
    Проверка создания новой группы номенклатуры со статусом 201.
    """
    # Подготовка
    endpoint = "/api/nomenclature-group"
    payload = {"name": "Новая тестовая группа"}

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Новая тестовая группа"
    assert "id" in data


def test_update_nomenclature_group_valid(client):
    """
    Проверка успешного обновления группы номенклатуры со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/nomenclature-group", json={"name": "Группа для изменения"})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/nomenclature-group/{created_id}"
    update_payload = {"name": "Обновленная группа"}

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "Обновленная группа"


def test_update_linked_group_id_conflict_returns_409(client):
    """
    Проверка запрета изменения ID группы, к которой привязана номенклатура (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    linked_group = manager.get(storage_manager.group_key())[0]
    endpoint = f"/api/nomenclature-group/{linked_group.id}"
    payload = {"id": "new-conflicting-group-id", "name": "Новое имя группы"}

    # Действие
    response = client.put(endpoint, json=payload)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_delete_free_group_returns_204_and_404_on_get(client):
    """
    Проверка удаления свободной группы номенклатуры (204) с контрольной проверкой 404.
    """
    # Подготовка
    create_response = client.post("/api/nomenclature-group", json={"name": "Временная группа"})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/nomenclature-group/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_linked_group_returns_409(client):
    """
    Проверка запрета удаления группы номенклатуры, содержащей позиции номенклатуры (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    linked_group_id = manager.get(storage_manager.group_key())[0].id
    endpoint = f"/api/nomenclature-group/{linked_group_id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


# ---------------------------------------------------------------------------
# nomenclature
# ---------------------------------------------------------------------------

def test_get_all_nomenclature_returns_200(client):
    """
    Проверка получения полного списка позиций номенклатуры со статусом 200.
    """
    # Подготовка
    endpoint = "/api/nomenclature"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_nomenclature_by_id_returns_200(client):
    """
    Проверка получения позиции номенклатуры по ID со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    nom = manager.get(storage_manager.nomenclature_key())[0]
    endpoint = f"/api/nomenclature/{nom.id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == nom.id
    assert data["name"] == nom.name


def test_get_nomenclature_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующей позиции номенклатуры.
    """
    # Подготовка
    endpoint = "/api/nomenclature/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_nomenclature_returns_201(client):
    """
    Проверка создания новой позиции номенклатуры со статусом 201.
    """
    # Подготовка
    manager = storage_manager()
    group_id = manager.get(storage_manager.group_key())[0].id
    range_id = manager.get(storage_manager.range_key())[0].id
    endpoint = "/api/nomenclature"
    payload = {
        "name": "Новая номенклатура",
        "full_name": "Новая номенклатура полное описание",
        "group_id": group_id,
        "range_id": range_id,
    }

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Новая номенклатура"
    assert "id" in data


def test_update_nomenclature_valid(client):
    """
    Проверка успешного обновления позиции номенклатуры со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    group_id = manager.get(storage_manager.group_key())[0].id
    range_id = manager.get(storage_manager.range_key())[0].id
    create_response = client.post("/api/nomenclature", json={
        "name": "Номенклатура под изменение",
        "full_name": "Номенклатура под изменение полное наименование",
        "group_id": group_id,
        "range_id": range_id,
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/nomenclature/{created_id}"
    update_payload = {
        "name": "Обновленная номенклатура",
        "full_name": "Обновленная номенклатура полное описание",
        "group_id": group_id,
        "range_id": range_id,
    }

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "Обновленная номенклатура"


def test_update_linked_nomenclature_id_conflict_returns_409(client):
    """
    Проверка запрета изменения ID номенклатуры, используемой в строках рецепта (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    linked_nomenclature = next(
        n for n in manager.get(storage_manager.nomenclature_key())
        if any(
            getattr(row, "nomenclature", None) is not None
            and getattr(row.nomenclature, "id", None) == n.id
            for recipe in recipes
            for row in getattr(recipe, "rows", [])
        )
    )
    endpoint = f"/api/nomenclature/{linked_nomenclature.id}"
    update_payload = {
        "id": "new-conflicting-nom-id",
        "name": "Измененное имя",
        "full_name": "Измененное полное имя",
        "group_id": linked_nomenclature.group.id,
        "range_id": linked_nomenclature.range.id,
    }

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_delete_free_nomenclature_returns_204_and_404_on_get(client):
    """
    Проверка удаления свободной позиции номенклатуры (204) с контрольным подтверждением 404.
    """
    # Подготовка
    manager = storage_manager()
    group_id = manager.get(storage_manager.group_key())[0].id
    range_id = manager.get(storage_manager.range_key())[0].id
    create_response = client.post("/api/nomenclature", json={
        "name": "Свободная номенклатура",
        "full_name": "Свободная номенклатура полное описание",
        "group_id": group_id,
        "range_id": range_id,
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/nomenclature/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_linked_nomenclature_returns_409(client):
    """
    Проверка запрета удаления позиции номенклатуры, используемой в строках рецептов (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    linked_nomenclature = next(
        n for n in manager.get(storage_manager.nomenclature_key())
        if any(
            getattr(row, "nomenclature", None) is not None
            and getattr(row.nomenclature, "id", None) == n.id
            for recipe in recipes
            for row in getattr(recipe, "rows", [])
        )
    )
    endpoint = f"/api/nomenclature/{linked_nomenclature.id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_delete_target_nomenclature_returns_409_with_recipe_dependencies(client):
    """
    Проверка запрета удаления номенклатуры-результата рецепта (Пицца Маргарита)
    со списком зависимых рецептов (статус 409).
    """
    # Подготовка
    manager = storage_manager()
    target_nomenclature = next(
        n for n in manager.get(storage_manager.nomenclature_key())
        if n.name == "Пицца Маргарита"
    )
    endpoint = f"/api/nomenclature/{target_nomenclature.id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert any("Пицца Маргарита" in dep for dep in data["dependencies"])


# ---------------------------------------------------------------------------
# storage
# ---------------------------------------------------------------------------

def test_get_all_storage_returns_200(client):
    """
    Проверка получения полного списка складов со статусом 200.
    """
    # Подготовка
    endpoint = "/api/storage"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_storage_by_id_returns_200(client):
    """
    Проверка получения склада по существующему ID со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    first_storage = manager.get(storage_manager.storage_key())[0]
    endpoint = f"/api/storage/{first_storage.id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == first_storage.id
    assert data["name"] == first_storage.name


def test_get_storage_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующего склада.
    """
    # Подготовка
    endpoint = "/api/storage/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_storage_returns_201(client):
    """
    Проверка создания нового склада со статусом 201.
    """
    # Подготовка
    endpoint = "/api/storage"
    payload = {"name": "Новый тестовый склад", "address": "ул. Тестовая, д. 10"}

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Новый тестовый склад"
    assert "id" in data


def test_update_storage_valid(client):
    """
    Проверка успешного обновления данных склада со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/storage", json={"name": "Склад для изменения", "address": "ул. Старая, 1"})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/storage/{created_id}"
    update_payload = {"name": "Обновленный склад", "address": "ул. Новая, 2"}

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "Обновленный склад"
    assert data["address"] == "ул. Новая, 2"


def test_delete_free_storage_returns_204_and_404_on_get(client):
    """
    Проверка удаления склада (204) с контрольной проверкой 404.
    """
    # Подготовка
    create_response = client.post("/api/storage", json={"name": "Склад под удаление", "address": "Адрес"})
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/storage/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# recipe
# ---------------------------------------------------------------------------

def test_get_all_recipe_returns_200(client):
    """
    Проверка получения полного списка рецептов со статусом 200.
    """
    # Подготовка
    endpoint = "/api/recipe"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_recipe_by_id_returns_200(client):
    """
    Проверка получения рецепта по существующему идентификатору со статусом 200.
    """
    # Подготовка
    manager = storage_manager()
    first_recipe = manager.get(storage_manager.recipe_key())[0]
    endpoint = f"/api/recipe/{first_recipe.id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == first_recipe.id
    assert data["name"] == first_recipe.name


def test_get_recipe_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующего рецепта.
    """
    # Подготовка
    endpoint = "/api/recipe/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_recipe_returns_201(client):
    """
    Проверка создания нового рецепта через POST со статусом 201.
    """
    # Подготовка
    endpoint = "/api/recipe"
    payload = {
        "name": "Новый тестовый рецепт",
        "description": "Описание рецепта",
        "cooking_time": 15.0,
    }

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Новый тестовый рецепт"
    assert "id" in data


def test_update_recipe_valid(client):
    """
    Проверка успешного обновления рецепта со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/recipe", json={
        "name": "Рецепт под изменение",
        "description": "Старое описание",
        "cooking_time": 10.0,
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/recipe/{created_id}"
    update_payload = {
        "name": "Обновленный рецепт",
        "description": "Новое описание",
        "cooking_time": 20.0,
    }

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "Обновленный рецепт"


def test_delete_free_recipe_returns_204_and_404_on_get(client):
    """
    Проверка удаления свободного рецепта (204) с контрольной проверкой 404.
    """
    # Подготовка
    create_response = client.post("/api/recipe", json={
        "name": "Рецепт для удаления",
        "description": "Краткое описание",
        "cooking_time": 5.0,
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/recipe/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# organization
# ---------------------------------------------------------------------------

def test_get_all_organization_returns_200(client):
    """
    Проверка получения полного списка организаций со статусом 200.
    """
    # Подготовка
    endpoint = "/api/organization"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_organization_by_id_returns_200(client):
    """
    Проверка получения организации по ID со статусом 200.
    """
    # Подготовка
    all_response = client.get("/api/organization")
    org_id = all_response.get_json()[0]["id"]
    endpoint = f"/api/organization/{org_id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == org_id
    assert "name" in data


def test_get_organization_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующей организации.
    """
    # Подготовка
    endpoint = "/api/organization/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_organization_returns_201(client):
    """
    Проверка создания новой организации со статусом 201.
    """
    # Подготовка
    endpoint = "/api/organization"
    payload = {
        "name": "ООО Новая Компания",
        "inn": "7701234567",
        "bik": "044525225",
        "account": "40702810938000012345",
        "ownership_form": "ООО",
    }

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "ООО Новая Компания"
    assert "id" in data


def test_update_organization_valid(client):
    """
    Проверка успешного обновления организации со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/organization", json={
        "name": "Компания под обновление",
        "inn": "7701234567",
        "bik": "044525225",
        "account": "40702810938000012345",
        "ownership_form": "ООО",
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/organization/{created_id}"
    update_payload = {
        "name": "ООО Обновленная",
        "inn": "7701234567",
        "bik": "044525225",
        "account": "40702810938000012345",
        "ownership_form": "ООО",
    }

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "ООО Обновленная"


def test_delete_free_organization_returns_204_and_404_on_get(client):
    """
    Проверка удаления свободной организации (204) с контрольной проверкой 404.
    """
    # Подготовка
    create_response = client.post("/api/organization", json={
        "name": "Организация для удаления",
        "inn": "7701234567",
        "bik": "044525225",
        "account": "40702810938000012345",
        "ownership_form": "ООО",
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/organization/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_linked_organization_returns_409(client):
    """
    Проверка запрета удаления организации, на которую ссылаются настройки (статус 409).
    """
    # Подготовка
    all_response = client.get("/api/organization")
    org_id = all_response.get_json()[0]["id"]
    endpoint = f"/api/organization/{org_id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


# ---------------------------------------------------------------------------
# settings
# ---------------------------------------------------------------------------

def test_get_all_settings_returns_200(client):
    """
    Проверка получения списка конфигураций настроек со статусом 200.
    """
    # Подготовка
    endpoint = "/api/settings"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_settings_by_id_returns_200(client):
    """
    Проверка получения настроек по ID со статусом 200.
    """
    # Подготовка
    all_response = client.get("/api/settings")
    settings_id = all_response.get_json()[0]["id"]
    endpoint = f"/api/settings/{settings_id}"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == settings_id


def test_get_settings_by_id_not_found(client):
    """
    Проверка возврата ошибки 404 при запросе несуществующей конфигурации настроек.
    """
    # Подготовка
    endpoint = "/api/settings/nonexistent-id"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_settings_returns_201(client):
    """
    Проверка создания нового объекта настроек со статусом 201.
    """
    # Подготовка
    endpoint = "/api/settings"
    payload = {
        "name": "Пользовательские настройки",
        "boss_name": "Руководитель",
        "account_name": "Бухгалтер",
        "response_format": "MARKDOWN",
    }

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Пользовательские настройки"
    assert "id" in data


def test_update_settings_valid(client):
    """
    Проверка успешного обновления конфигурации настроек со статусом 200.
    """
    # Подготовка
    create_response = client.post("/api/settings", json={
        "name": "Настройки до обновления",
        "boss_name": "Руководитель 1",
        "account_name": "Бухгалтер 1",
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/settings/{created_id}"
    update_payload = {
        "name": "Обновленные настройки",
        "boss_name": "Руководитель Новый",
        "account_name": "Бухгалтер Новый",
    }

    # Действие
    response = client.put(endpoint, json=update_payload)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_id
    assert data["name"] == "Обновленные настройки"
    assert data["boss_name"] == "Руководитель Новый"


def test_delete_free_settings_returns_204_and_404_on_get(client):
    """
    Проверка удаления объекта настроек (204) с контрольной проверкой 404.
    """
    # Подготовка
    create_response = client.post("/api/settings", json={
        "name": "Настройки под удаление",
        "boss_name": "Временный",
        "account_name": "Временный",
    })
    created_id = create_response.get_json()["id"]
    endpoint = f"/api/settings/{created_id}"

    # Действие
    delete_response = client.delete(endpoint)
    get_response = client.get(endpoint)

    # Проверки
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# formats & misc
# ---------------------------------------------------------------------------

def test_get_report_formats_returns_list(client):
    """
    Проверка получения списка поддерживаемых форматов отчетов со статусом 200.
    """
    # Подготовка
    endpoint = "/api/report-formats"

    # Действие
    response = client.get(endpoint)

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, str) for item in data)


def test_settings_manager_uses_deserialization():
    """
    Проверка корректной десериализации настроек приложения при вызове load.
    """
    # Подготовка
    deserialization_context().clear()
    manager = settings_manager()

    try:
        # Действие
        load_result = manager.load()

        # Проверки
        assert load_result is True
        assert isinstance(manager.settings, settings_model)
        assert manager.settings.company is not None
        assert bool(manager.settings.boss_name.strip())
    finally:
        deserialization_context().clear()


def test_create_range_invalid_missing_name_returns_400(client):
    """
    Проверка возврата ошибки 400 при попытке создания единицы измерения с некорректным наименованием.
    """
    # Подготовка
    payload = {"name": "", "conversion_factor": 10}
    endpoint = "/api/range"

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_create_organization_invalid_inn_returns_400(client):
    """
    Проверка возврата ошибки 400 при передаче невалидного ИНН организации.
    """
    # Подготовка
    payload = {
        "name": "Невалидная организация",
        "inn": "123",
        "bik": "044525225",
        "account": "40702810938000012345",
        "ownership_form": "ООО",
        "corr_account": "30101810400000000225",
    }
    endpoint = "/api/organization"

    # Действие
    response = client.post(endpoint, json=payload)

    # Проверки
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_update_range_not_found_returns_404(client):
    """
    Проверка возврата ошибки 404 при попытке обновления несуществующей единицы измерения.
    """
    # Подготовка
    endpoint = "/api/range/non-existent-id-9999"
    payload = {"name": "Новое имя", "conversion_factor": 5}

    # Действие
    response = client.put(endpoint, json=payload)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_delete_range_not_found_returns_404(client):
    """
    Проверка возврата ошибки 404 при попытке удаления несуществующей единицы измерения.
    """
    # Подготовка
    endpoint = "/api/range/non-existent-id-9999"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_update_linked_recipe_id_conflict_returns_409(client):
    """
    Проверка возврата ошибки 409 при попытке изменения идентификатора связанного рецепта-полуфабриката.
    """
    # Подготовка
    manager = storage_manager()
    linked_nomenclature = next(n for n in manager.get(storage_manager.nomenclature_key()) if n.recipe is not None)
    linked_recipe = linked_nomenclature.recipe
    manager.add(storage_manager.recipe_key(), linked_recipe)
    endpoint = f"/api/recipe/{linked_recipe.id}"
    payload = {
        "id": "new-recipe-conflict-id",
        "name": linked_recipe.name,
        "description": "Попытка смены id",
        "cooking_time": 10,
    }

    # Действие
    response = client.put(endpoint, json=payload)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_delete_linked_recipe_returns_409(client):
    """
    Проверка возврата ошибки 409 при попытке удаления рецепта, на который ссылается номенклатура-полуфабрикат.
    """
    # Подготовка
    manager = storage_manager()
    linked_nomenclature = next(n for n in manager.get(storage_manager.nomenclature_key()) if n.recipe is not None)
    linked_recipe = linked_nomenclature.recipe
    manager.add(storage_manager.recipe_key(), linked_recipe)
    endpoint = f"/api/recipe/{linked_recipe.id}"

    # Действие
    response = client.delete(endpoint)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_update_linked_organization_id_conflict_returns_409(client):
    """
    Проверка возврата ошибки 409 при попытке изменения идентификатора организации, привязанной к настройкам.
    """
    # Подготовка
    manager = storage_manager()
    org = manager.get(storage_manager.organization_key())[0]
    endpoint = f"/api/organization/{org.id}"
    payload = {
        "id": "new-org-conflict-id",
        "name": org.name,
        "inn": org.inn,
        "bik": org.bik,
        "account": org.account,
        "ownership_form": org.ownership_form,
        "corr_account": org.corr_account,
    }

    # Действие
    response = client.put(endpoint, json=payload)

    # Проверки
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
    assert "dependencies" in data
    assert len(data["dependencies"]) > 0


def test_update_free_range_id_success(client):
    """
    Проверка успешного обновления идентификатора свободной единицы измерения в хранилище.
    """
    # Подготовка
    create_response = client.post("/api/range", json={"name": "Временная единица", "conversion_factor": 1})
    created = create_response.get_json()
    old_id = created["id"]
    new_id = f"{old_id}-renamed"

    # Действие
    update_payload = {"id": new_id, "name": "Временная переименованная", "conversion_factor": 2}
    update_response = client.put(f"/api/range/{old_id}", json=update_payload)

    # Проверки
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data["id"] == new_id
    assert client.get(f"/api/range/{old_id}").status_code == 404
    assert client.get(f"/api/range/{new_id}").status_code == 200
