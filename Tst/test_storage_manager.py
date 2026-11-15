import json
import pytest
from src.logics.storage_manager import storage_manager
from src.logics.handlers.group_handler import group_handler
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


def test_equals_storage_manager_singleton():
    """
    Проверка паттерна Singleton: два созданных экземпляра storage_manager
    равны по значению (__eq__).
    """
    # Подготовка
    cls = storage_manager

    # Действие
    instance1 = cls()
    instance2 = cls()

    # Проверки
    assert instance1 == instance2


def test_same_instance_storage_manager_singleton():
    """
    Проверка тождественности (is): два экземпляра storage_manager должны быть
    одним и тем же объектом в памяти.
    """
    # Подготовка
    cls = storage_manager

    # Действие
    instance1 = cls()
    instance2 = cls()

    # Проверки
    assert instance1 is instance2


def test_not_none_get_storage_manager_keys():
    """
    Проверка работы с кешем: при запросе данных по базовым ключам возвращаются
    инициализированные списки.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    ranges = manager.collection(storage_manager.range_key())
    nomenclatures = manager.collection(storage_manager.nomenclature_key())
    groups = manager.collection(storage_manager.group_key())
    storages = manager.collection(storage_manager.storage_key())

    # Проверки
    assert isinstance(ranges, list)
    assert isinstance(nomenclatures, list)
    assert isinstance(groups, list)
    assert isinstance(storages, list)


def test_collection_unknown_key_returns_empty_list():
    """
    Проверка поведения collection() при обращении по неизвестному ключу:
    должен вернуться пустой список без исключений.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    result = manager.collection("unknown_key_xyz")

    # Проверки
    assert isinstance(result, list)
    assert len(result) == 0


def test_convert_ranges_not_empty():
    """
    Проверка данных первого старта: коллекция единиц измерения не должна быть пустой
    после инициализации менеджера.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    ranges = manager.collection(storage_manager.range_key())

    # Проверки
    assert len(ranges) > 0


def test_convert_groups_not_empty():
    """
    Проверка данных первого старта: коллекция групп номенклатуры не должна быть пустой.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    groups = manager.collection(storage_manager.group_key())

    # Проверки
    assert len(groups) > 0


def test_convert_nomenclature_not_empty():
    """
    Проверка данных первого старта: коллекция номенклатурных позиций не должна
    быть пустой после инициализации.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    nomenclatures = manager.collection(storage_manager.nomenclature_key())

    # Проверки
    assert len(nomenclatures) > 0


def test_convert_storages_not_empty():
    """
    Проверка данных первого старта: коллекция складов не должна быть пустой
    после инициализации.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    storages = manager.collection(storage_manager.storage_key())

    # Проверки
    assert len(storages) > 0


def test_convert_ranges_contain_correct_types():
    """
    Проверка типов объектов в коллекции единиц измерения: каждый элемент
    должен быть экземпляром range_model.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    ranges = manager.collection(storage_manager.range_key())

    # Проверки
    assert all(isinstance(r, range_model) for r in ranges)


def test_convert_groups_contain_correct_types():
    """
    Проверка типов объектов в коллекции групп: каждый элемент должен быть
    экземпляром nomenclature_group_model.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    groups = manager.collection(storage_manager.group_key())

    # Проверки
    assert all(isinstance(g, nomenclature_group_model) for g in groups)


def test_convert_nomenclature_contain_correct_types():
    """
    Проверка типов объектов в коллекции номенклатуры: каждый элемент должен быть
    экземпляром nomenclature_model.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    nomenclatures = manager.collection(storage_manager.nomenclature_key())

    # Проверки
    assert all(isinstance(n, nomenclature_model) for n in nomenclatures)


def test_convert_storages_contain_correct_types():
    """
    Проверка типов объектов в коллекции складов: каждый элемент должен быть
    экземпляром storage_model.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    storages = manager.collection(storage_manager.storage_key())

    # Проверки
    assert all(isinstance(s, storage_model) for s in storages)


def test_convert_ranges_names_not_empty():
    """
    Проверка корректности данных первого старта: наименование каждой единицы
    измерения не должно быть пустым.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    ranges = manager.collection(storage_manager.range_key())

    # Проверки
    assert all(r.name != "" for r in ranges)


def test_convert_nomenclature_have_valid_group_and_range():
    """
    Проверка связей номенклатуры: каждая позиция должна иметь установленные
    группу (group) и единицу измерения (range).
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    nomenclatures = manager.collection(storage_manager.nomenclature_key())

    # Проверки
    for item in nomenclatures:
        assert item.group is not None
        assert item.range is not None


def test_add_duplicate_not_added():
    """
    Проверка уникальности: повторное добавление одного и того же объекта
    (по id) не должно увеличивать размер коллекции.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Тест-дубликат-группа")
    coll = manager.collection(storage_manager.group_key())
    manager.save(storage_manager.group_key(), group)
    size_after_first = len(coll)

    try:
        # Действие
        result = manager.save(storage_manager.group_key(), group)
        size_after_second = len(coll)

        # Проверки
        assert result is False
        assert size_after_first == size_after_second
    finally:
        if group in coll:
            coll.remove(group)


def test_add_different_objects_both_added():
    """
    Проверка добавления различных объектов: два разных экземпляра с одинаковым именем
    должны добавляться как отдельные элементы (у каждого свой id).
    """
    # Подготовка
    manager = storage_manager()
    group1 = nomenclature_group_model("Уникальная-группа-A")
    group2 = nomenclature_group_model("Уникальная-группа-A")
    coll = manager.collection(storage_manager.group_key())
    size_before = len(coll)

    try:
        # Действие
        result1 = manager.save(storage_manager.group_key(), group1)
        result2 = manager.save(storage_manager.group_key(), group2)
        size_after = len(coll)

        # Проверки
        assert result1 is True
        assert result2 is True
        assert size_after == size_before + 2
    finally:
        if group1 in coll:
            coll.remove(group1)
        if group2 in coll:
            coll.remove(group2)


def test_add_none_returns_false():
    """
    Проверка защиты от None: попытка добавить None в коллекцию должна
    вернуть False и не изменить коллекцию.
    """
    # Подготовка
    manager = storage_manager()
    size_before = len(manager.collection(storage_manager.range_key()))

    # Действие
    result = manager.save(storage_manager.range_key(), None)

    # Проверки
    assert result is False
    assert len(manager.collection(storage_manager.range_key())) == size_before


def test_add_returns_true_on_new_item():
    """
    Проверка возвращаемого значения add(): при добавлении нового (уникального)
    объекта метод должен вернуть True.
    """
    # Подготовка
    manager = storage_manager()
    new_storage = storage_model("Склад-новый-тест", "ул. Тестовая, д. 99")
    coll = manager.collection(storage_manager.storage_key())

    try:
        # Действие
        result = manager.save(storage_manager.storage_key(), new_storage)

        # Проверки
        assert result is True
        assert new_storage in manager.collection(storage_manager.storage_key())
    finally:
        if new_storage in coll:
            coll.remove(new_storage)


def test_data_property_returns_dict():
    """
    Проверка свойства data: должен возвращаться словарь с ключами всех
    базовых коллекций.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    data = manager.data

    # Проверки
    assert isinstance(data, dict)
    assert storage_manager.range_key() in data
    assert storage_manager.nomenclature_key() in data
    assert storage_manager.group_key() in data
    assert storage_manager.storage_key() in data


def test_export_all_to_json_writes_all_collections(tmp_path):
    """
    Проверка экспорта всех коллекций хранилища в один JSON-файл.
    """
    # Подготовка
    manager = storage_manager()
    target = tmp_path / "all_data.json"

    # Действие
    result = manager.export_all_to_json(str(target))

    # Проверки
    assert result is True
    assert target.exists()

    data = json.loads(target.read_text(encoding="utf-8"))
    expected_keys = {
        storage_manager.range_key(),
        storage_manager.nomenclature_key(),
        storage_manager.group_key(),
        storage_manager.storage_key(),
        storage_manager.recipe_key(),
    }
    assert set(data.keys()) == expected_keys

    for key in expected_keys:
        assert isinstance(data[key], list)
        assert len(data[key]) == len(manager.collection(key))
        assert [item["id"] for item in data[key]] == [item.id for item in manager.collection(key)]

    recipes = data[storage_manager.recipe_key()]
    assert len(recipes) > 0
    assert len(recipes[0]["rows"]) > 0
    assert recipes[0]["rows"][0]["nomenclature"]["recipe"] is not None


def test_storage_manager_has_no_update_or_delete_methods():
    """
    Проверка соблюдения принципа SRP: у базового storage_manager
    отсутствуют методы update и delete.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    has_update = hasattr(manager, "update")
    has_delete = hasattr(manager, "delete")

    # Проверки
    assert has_update is False
    assert has_delete is False


def test_storage_manager_save_and_load_contract():
    """
    Проверка контракта сохранения и загрузки данных через save и load.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Тестовая группа save_load")

    try:
        # Действие
        saved = manager.save(storage_manager.group_key(), group)
        loaded = manager.collection(storage_manager.group_key())

        # Проверки
        assert saved is True
        assert group in loaded
    finally:
        loaded = manager.collection(storage_manager.group_key())
        if group in loaded:
            loaded.remove(group)


def test_storage_manager_load_lsp_contract(tmp_path):
    """
    Проверка соответствия storage_manager контракту abstract_manager.load:
    - load() без аргументов инициализирует/конвертирует первичные данные
    - load(file_name) выполняет загрузку из JSON-файла
    """
    # Подготовка
    manager = storage_manager()
    saved_state = {key: list(manager.collection(key)) for key in list(manager.data.keys())}
    temp_file = tmp_path / "test_load_export.json"
    manager.export_all_to_json(str(temp_file))

    try:
        # Действие
        result_default = manager.load()
        result_file = manager.load(str(temp_file))

        # Проверки
        assert result_default is None
        assert result_file is None
        assert len(manager.collection(storage_manager.range_key())) > 0
    finally:
        for key, items in saved_state.items():
            col = manager.collection(key)
            col.clear()
            col.extend(items)


def test_handler_update_visibility_in_storage():
    """
    Проверка механики обновления сущности через хендлер и подтверждение
    видимости изменения в хранилище storage_manager.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа до обновления")
    manager.save(storage_manager.group_key(), group)
    handler = group_handler(manager)
    update_payload = {"name": "Группа после обновления"}

    try:
        # Действие
        response, status = handler.update(group.id, update_payload)

        # Проверки
        assert status == 200
        assert response["name"] == "Группа после обновления"
        stored_item = next((item for item in manager.collection(storage_manager.group_key()) if item.id == group.id), None)
        assert stored_item is not None
        assert stored_item.name == "Группа после обновления"
    finally:
        collection = manager.collection(storage_manager.group_key())
        to_remove = next((item for item in collection if item.id == group.id), None)
        if to_remove is not None:
            collection.remove(to_remove)


def test_handler_update_non_existing_returns_404():
    """
    Проверка возврата ошибки 404 хендлером при попытке обновления несуществующей сущности.
    """
    # Подготовка
    manager = storage_manager()
    handler = group_handler(manager)

    # Действие
    response, status = handler.update("non-existent-id", {"name": "Любое имя"})

    # Проверки
    assert status == 404
    assert "error" in response


def test_handler_delete_visibility_in_storage():
    """
    Проверка механики удаления сущности через хендлер и подтверждение
    видимости удаления в хранилище storage_manager.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа для удаления хендлером")
    manager.save(storage_manager.group_key(), group)
    handler = group_handler(manager)

    try:
        # Действие
        response, status = handler.delete(group.id)

        # Проверки
        assert status == 204
        assert response == ""
        stored_item = next((item for item in manager.collection(storage_manager.group_key()) if item.id == group.id), None)
        assert stored_item is None
    finally:
        collection = manager.collection(storage_manager.group_key())
        to_clean = next((item for item in collection if item.id == group.id), None)
        if to_clean is not None:
            collection.remove(to_clean)


def test_handler_delete_non_existing_returns_404():
    """
    Проверка возврата ошибки 404 хендлером при удалении несуществующей сущности.
    """
    # Подготовка
    manager = storage_manager()
    handler = group_handler(manager)

    # Действие
    response, status = handler.delete("non-existent-id")

    # Проверки
    assert status == 404
    assert "error" in response


def test_storage_manager_organization_and_settings_keys():
    """
    Проверка ключей и маппинга типов для организаций и настроек.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    org_key = storage_manager.organization_key()
    set_key = storage_manager.settings_key()

    # Проверки
    assert org_key == "organization_model"
    assert set_key == "settings_model"
    assert manager.get_by_type("organization") is not None
    assert manager.get_by_type("settings") is not None


def test_handler_update_with_id_change_visibility_in_storage():
    """
    Проверка обновления сущности со сменой идентификатора через хендлер
    и подтверждение видимости изменения в хранилище.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа с новым ID")
    manager.save(storage_manager.group_key(), group)
    handler = group_handler(manager)
    new_id = "new-custom-group-id"
    payload = {"id": new_id, "name": "Группа с новым именем"}

    try:
        # Действие
        response, status = handler.update(group.id, payload)

        # Проверки
        assert status == 200
        assert response["id"] == new_id
        collection = manager.collection(storage_manager.group_key())
        old_found = next((item for item in collection if item.id == group.id), None)
        new_found = next((item for item in collection if item.id == new_id), None)
        assert old_found is None
        assert new_found is not None
        assert new_found.name == "Группа с новым именем"
    finally:
        collection = manager.collection(storage_manager.group_key())
        for tid in (group.id, new_id):
            item = next((x for x in collection if x.id == tid), None)
            if item is not None:
                collection.remove(item)

