import os
import pytest
from main import api
from src.core.abstract_observable import abstract_observable
from src.core.event_type import event_type
from src.core.exception import arguments_exception, operation_exception
from src.dtos.log_entry_dto import log_entry_dto
from src.logics.api_server import api_server
from src.logics.handlers.range_handler import range_handler
from src.logics.log_service import log_service
from src.logics.observer import observer
from src.logics.osv_service import osv_service
from src.logics.settings_manager import settings_manager
from src.logics.storage_manager import storage_manager
from src.models.settings_model import settings_model


class _custom_observable(abstract_observable):
    """Тестовый наблюдатель для проверки контракта observer."""

    def __init__(self) -> None:
        self.events: list[tuple[str, object]] = []

    def handler(self, event_types: str, params: object = None) -> None:
        self.events.append((event_types, params))


@pytest.fixture
def isolated_observer(tmp_path):
    """
    Фикстура изоляции списка наблюдателей и буфера log_service.
    Восстанавливает исходное состояние observer.handlers после каждого теста.
    """
    saved_handlers = list(observer.handlers)
    observer.handlers.clear()

    log_file = tmp_path / "test_app.log"
    logger = log_service(log_file_name=str(log_file), auto_register=True)

    try:
        yield logger
    finally:
        logger.clear()
        observer.handlers.clear()
        observer.handlers.extend(saved_handlers)


@pytest.fixture
def isolated_api_client(tmp_path):
    """
    Фикстура тестового клиента API с изоляцией хранилища, настроек, наблюдателей и логов.
    """
    saved_handlers = list(observer.handlers)
    saved_log_service = api_server._log_service
    manager = storage_manager()
    s_mgr = settings_manager()
    saved_settings = s_mgr.settings
    snapshot = {key: list(manager.collection(key)) for key in list(manager.data.keys())}

    observer.handlers.clear()
    log_file = tmp_path / "api_test.log"
    test_logger = log_service(log_file_name=str(log_file), auto_register=True)
    api_server._log_service = test_logger

    try:
        with api.test_client() as test_client:
            yield test_client, test_logger
    finally:
        for key, items in snapshot.items():
            manager.data[key] = list(items)
        s_mgr.settings = saved_settings
        test_logger.clear()
        api_server._log_service = saved_log_service
        observer.handlers.clear()
        observer.handlers.extend(saved_handlers)


def test_observer_add_create_delete(isolated_observer):
    """
    Проверка регистрации, оповещения и удаления наблюдателя через observer.
    """
    # Подготовка
    custom = _custom_observable()
    dto = log_entry_dto(entity_type="api_server", message="ping")
    observer.add(custom)
    observer.add(custom)

    # Действие
    observer.create(event_type.web_request(), dto)
    observer.delete(custom)
    observer.create(event_type.web_request(), log_entry_dto(message="after_delete"))

    # Проверки
    assert len(custom.events) == 1
    assert custom.events[0][0] == event_type.web_request()
    assert isinstance(custom.events[0][1], log_entry_dto)
    assert custom.events[0][1].message == "ping"


def test_observer_invalid_source_raises_exception(isolated_observer):
    """
    Проверка валидации типа наблюдателя при добавлении в observer.
    """
    # Подготовка
    invalid_source = "not_an_observable"

    # Действие
    def action():
        observer.add(invalid_source)

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_observer_delete_invalid_source_raises_exception(isolated_observer):
    """
    Проверка валидации типа наблюдателя при удалении из observer.
    """
    # Подготовка
    invalid_source = 12345

    # Действие
    def action():
        observer.delete(invalid_source)

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_observer_create_non_string_event_raises_exception(isolated_observer):
    """
    Проверка валидации типа события при вызове observer.create.
    """
    # Подготовка
    invalid_event = 999

    # Действие
    def action():
        observer.create(invalid_event, log_entry_dto(message="test"))

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_log_service_writes_dto_to_file_and_buffer(isolated_observer):
    """
    Проверка записи типизированного log_entry_dto наблюдателем log_service в файл и буфер.
    """
    # Подготовка
    logger = isolated_observer
    payload = log_entry_dto(entity_type="range_model", entity_id="id-1", message="Создана единица тонна")

    # Действие
    observer.create(event_type.crud_create(), payload)

    # Проверки
    assert len(logger.entries) == 1
    entry = logger.entries[0]
    assert isinstance(entry, log_entry_dto)
    assert entry.event == event_type.crud_create()
    assert entry.entity_type == "range_model"
    assert entry.entity_id == "id-1"
    assert entry.description != ""
    assert entry.timestamp != ""
    assert os.path.exists(logger.log_file_path)
    with open(logger.log_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "тонна" in content


def test_log_service_handles_none_params(isolated_observer):
    """
    Проверка корректной обработки события при params=None в log_service.
    """
    # Подготовка
    logger = isolated_observer

    # Действие
    observer.create(event_type.web_request(), None)

    # Проверки
    assert len(logger.entries) == 1
    entry = logger.entries[0]
    assert isinstance(entry, log_entry_dto)
    assert entry.event == event_type.web_request()
    assert entry.message == ""
    assert entry.description != ""


def test_crud_operations_logged_via_observer(isolated_observer):
    """
    Проверка логирования CRUD-операций (create, update, delete) через наблюдателя.
    """
    # Подготовка
    logger = isolated_observer
    manager = storage_manager()
    snapshot = list(manager.collection(storage_manager.range_key()))
    handler = range_handler(manager)

    try:
        # Действие
        created_body, status_create = handler.create({"name": "центнер", "coefficient": 100000.0})
        entity_id = created_body["id"]
        _, status_update = handler.update(entity_id, {"name": "центнер_обн", "coefficient": 100000.0})
        _, status_delete = handler.delete(entity_id)

        # Проверки
        assert status_create == 201
        assert status_update == 200
        assert status_delete == 204
        assert all(isinstance(entry, log_entry_dto) for entry in logger.entries)
        events = [entry.event for entry in logger.entries]
        assert event_type.crud_create() in events
        assert event_type.crud_update() in events
        assert event_type.crud_delete() in events
    finally:
        manager.data[storage_manager.range_key()] = snapshot


def test_crud_negative_scenarios_do_not_publish_events(isolated_observer):
    """
    Проверка отсутствия ложных CRUD-событий при ошибках валидации, поиска и конфликте (400/404/409).
    """
    # Подготовка
    logger = isolated_observer
    manager = storage_manager()
    snapshot = list(manager.collection(storage_manager.range_key()))
    handler = range_handler(manager)
    existing = snapshot[0]

    try:
        # Действие
        _, status_400 = handler.create({"name": "", "coefficient": -1})
        _, status_409 = handler.create({"id": existing.id, "name": existing.name, "coefficient": 1.0})
        _, status_404_update = handler.update("missing-id-999", {"name": "новое", "coefficient": 1.0})
        _, status_404_delete = handler.delete("missing-id-999")

        # Проверки
        assert status_400 == 400
        assert status_409 == 409
        assert status_404_update == 404
        assert status_404_delete == 404
        assert len(logger.entries) == 0
    finally:
        manager.data[storage_manager.range_key()] = snapshot


def test_warehouse_operations_logged_via_observer(isolated_observer):
    """
    Проверка логирования складских операций (движения и формирование ОСВ).
    """
    # Подготовка
    logger = isolated_observer
    manager = storage_manager()
    service = osv_service(manager)
    saved_turnovers = list(manager.collection(storage_manager.turnover_key()))

    try:
        # Действие
        manager.data[storage_manager.turnover_key()] = []
        manager._build_turnovers()
        rows = service.build_osv()

        # Проверки
        assert len(rows) > 0
        assert all(isinstance(entry, log_entry_dto) for entry in logger.entries)
        events = [entry.event for entry in logger.entries]
        assert event_type.warehouse_turnover() in events
        assert event_type.warehouse_osv() in events
    finally:
        manager.data[storage_manager.turnover_key()] = saved_turnovers


def test_settings_manager_events_logged_without_duplicates(isolated_observer):
    """
    Проверка публикации событий load_settings и change_settings только через settings_manager.
    """
    # Подготовка
    logger = isolated_observer
    s_mgr = settings_manager()
    saved_settings = s_mgr.settings
    new_settings = settings_model(name="Новые настройки")
    new_settings.boss_name = "Петров П. П."

    try:
        # Действие
        s_mgr.load()
        s_mgr.settings = new_settings

        # Проверки
        load_events = [e for e in logger.entries if e.event == event_type.load_settings()]
        change_events = [e for e in logger.entries if e.event == event_type.change_settings()]
        assert len(load_events) == 1
        assert len(change_events) == 1
    finally:
        s_mgr.settings = saved_settings


def test_settings_manager_load_failure_does_not_publish_load_event(isolated_observer):
    """
    Проверка отсутствия события load_settings при ошибке чтения несуществующего файла настроек.
    """
    # Подготовка
    logger = isolated_observer
    s_mgr = settings_manager()

    # Действие
    def action():
        s_mgr.load("non_existent_settings_file.json")

    # Проверки
    with pytest.raises(operation_exception):
        action()
    load_events = [e for e in logger.entries if e.event == event_type.load_settings()]
    assert len(load_events) == 0


def test_log_entry_dto_validation_and_normalization():
    """
    Проверка валидации строковых полей, приведения None к пустой строке и strip в log_entry_dto.
    """
    # Подготовка
    raw_type = "  range_model  "

    # Действие
    dto = log_entry_dto(entity_type=raw_type, entity_id=None, message="  создан объект  ")

    # Проверки
    assert dto.entity_type == "range_model"
    assert dto.entity_id == ""
    assert dto.message == "создан объект"
    with pytest.raises(arguments_exception):
        log_entry_dto(entity_type=123)


def test_event_type_events_registry():
    """
    Проверка полноты справочника событий event_type.events().
    """
    # Подготовка
    expected_events = {
        event_type.change_settings(),
        event_type.load_settings(),
        event_type.crud_create(),
        event_type.crud_update(),
        event_type.crud_delete(),
        event_type.warehouse_turnover(),
        event_type.warehouse_osv(),
        event_type.web_request(),
    }

    # Действие
    events_map = event_type.events()

    # Проверки
    assert expected_events.issubset(set(events_map.keys()))
    assert all(isinstance(desc, str) and len(desc.strip()) > 0 for desc in events_map.values())


def test_observer_multiple_subscribers_and_delete_unregistered(isolated_observer):
    """
    Проверка рассылки события нескольким наблюдателям и безопасного удаления незарегистрированного наблюдателя.
    """
    # Подготовка
    first = _custom_observable()
    second = _custom_observable()
    unregistered = _custom_observable()
    observer.add(first)
    observer.add(second)

    # Действие
    observer.delete(unregistered)
    observer.create(event_type.web_request(), log_entry_dto(message="broadcast"))

    # Проверки
    assert len(first.events) == 1
    assert len(second.events) == 1
    assert first.events[0][1].message == "broadcast"
    assert second.events[0][1].message == "broadcast"


def test_log_service_string_params_and_auto_register_false(isolated_observer, tmp_path):
    """
    Проверка обработки строкового params, режима auto_register=False, clear() и копии entries в log_service.
    """
    # Подготовка
    manual_log = tmp_path / "manual.log"
    manual_logger = log_service(log_file_name=str(manual_log), auto_register=False)

    # Действие
    observer.create(event_type.web_request(), "прямое строковое сообщение")
    count_before_register = len(manual_logger.entries)
    observer.add(manual_logger)
    observer.create(event_type.web_request(), "сообщение после подписки")
    entries_copy = manual_logger.entries
    entries_copy.clear()

    # Проверки
    assert count_before_register == 0
    assert len(manual_logger.entries) == 1
    assert manual_logger.entries[0].message == "сообщение после подписки"
    manual_logger.clear()
    assert len(manual_logger.entries) == 0


def test_web_methods_logged_via_api_server(isolated_api_client):
    """
    Проверка логирования вызовов Web-методов, CRUD, ОСВ и изменения настроек через API.
    """
    # Подготовка
    client, logger = isolated_api_client
    settings_list = client.get("/api/settings").json()
    target_settings = settings_list[0]
    settings_id = target_settings["id"]
    logger.clear()

    # Действие
    res_get = client.get("/api/range")
    res_osv = client.post("/api/osv", json={})
    res_put = client.put(
        f"/api/settings/{settings_id}",
        json={
            "id": settings_id,
            "name": target_settings.get("name") or "Настройки",
            "boss_name": "Сидоров С. С.",
            "account_name": target_settings.get("account_name", ""),
            "response_format": "Markdown",
        },
    )

    # Проверки
    assert res_get.status_code == 200
    assert res_osv.status_code == 200
    assert res_put.status_code == 200
    assert all(isinstance(entry, log_entry_dto) for entry in logger.entries)
    events = [entry.event for entry in logger.entries]
    web_messages = [entry.message for entry in logger.entries if entry.event == event_type.web_request()]
    assert any("GET /api/range" in msg for msg in web_messages)
    assert any("POST /api/osv" in msg for msg in web_messages)
    assert any(f"PUT /api/settings/{settings_id}" in msg for msg in web_messages)
    assert event_type.warehouse_osv() in events
    assert event_type.crud_update() in events
    assert event_type.change_settings() in events
