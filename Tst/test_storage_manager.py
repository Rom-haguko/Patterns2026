import json
import pytest
from src.logics.storage_manager import storage_manager
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
    # Действие
    instance1 = storage_manager()
    instance2 = storage_manager()

    # Проверки
    assert instance1 == instance2


def test_same_instance_storage_manager_singleton():
    """
    Проверка тождественности (is): два экземпляра storage_manager должны быть
    одним и тем же объектом в памяти.
    """
    # Подготовка
    # Действие
    instance1 = storage_manager()
    instance2 = storage_manager()

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
    ranges = manager.get(storage_manager.range_key())
    nomenclatures = manager.get(storage_manager.nomenclature_key())
    groups = manager.get(storage_manager.group_key())
    storages = manager.get(storage_manager.storage_key())

    # Проверки
    assert isinstance(ranges, list)
    assert isinstance(nomenclatures, list)
    assert isinstance(groups, list)
    assert isinstance(storages, list)


def test_get_unknown_key_returns_empty_list():
    """
    Проверка поведения get() при обращении по неизвестному ключу:
    должен вернуться пустой список без исключений.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    result = manager.get("unknown_key_xyz")

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
    ranges = manager.get(storage_manager.range_key())

    # Проверки
    assert len(ranges) > 0


def test_convert_groups_not_empty():
    """
    Проверка данных первого старта: коллекция групп номенклатуры не должна быть пустой.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    groups = manager.get(storage_manager.group_key())

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
    nomenclatures = manager.get(storage_manager.nomenclature_key())

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
    storages = manager.get(storage_manager.storage_key())

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
    ranges = manager.get(storage_manager.range_key())

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
    groups = manager.get(storage_manager.group_key())

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
    nomenclatures = manager.get(storage_manager.nomenclature_key())

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
    storages = manager.get(storage_manager.storage_key())

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
    ranges = manager.get(storage_manager.range_key())

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
    nomenclatures = manager.get(storage_manager.nomenclature_key())

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
    coll = manager.get(storage_manager.group_key())
    manager.add(storage_manager.group_key(), group)
    size_after_first = len(coll)

    try:
        # Действие
        result = manager.add(storage_manager.group_key(), group)
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
    coll = manager.get(storage_manager.group_key())
    size_before = len(coll)

    try:
        # Действие
        result1 = manager.add(storage_manager.group_key(), group1)
        result2 = manager.add(storage_manager.group_key(), group2)
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
    size_before = len(manager.get(storage_manager.range_key()))

    # Действие
    result = manager.add(storage_manager.range_key(), None)

    # Проверки
    assert result is False
    assert len(manager.get(storage_manager.range_key())) == size_before


def test_add_returns_true_on_new_item():
    """
    Проверка возвращаемого значения add(): при добавлении нового (уникального)
    объекта метод должен вернуть True.
    """
    # Подготовка
    manager = storage_manager()
    new_storage = storage_model("Склад-новый-тест", "ул. Тестовая, д. 99")
    coll = manager.get(storage_manager.storage_key())

    try:
        # Действие
        result = manager.add(storage_manager.storage_key(), new_storage)

        # Проверки
        assert result is True
        assert new_storage in manager.get(storage_manager.storage_key())
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
        assert len(data[key]) == len(manager.get(key))
        assert [item["id"] for item in data[key]] == [item.id for item in manager.get(key)]

    recipes = data[storage_manager.recipe_key()]
    assert len(recipes) > 0
    assert len(recipes[0]["rows"]) > 0
    assert recipes[0]["rows"][0]["nomenclature"]["recipe"] is not None


def test_storage_manager_update_existing_item():
    """
    Проверка успешного обновления существующего объекта в хранилище.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа для обновления")
    manager.add(storage_manager.group_key(), group)
    updated_group = nomenclature_group_model.create_from_dict({"id": group.id, "name": "Обновленное наименование"})

    try:
        # Действие
        result = manager.update(storage_manager.group_key(), updated_group)

        # Проверки
        assert result is True
        found = next((item for item in manager.get(storage_manager.group_key()) if item.id == group.id), None)
        assert found is not None
        assert found.name == "Обновленное наименование"
    finally:
        manager.delete(storage_manager.group_key(), group.id)


def test_storage_manager_update_non_existing_returns_false():
    """
    Проверка возврата False при обновлении несуществующего объекта.
    """
    # Подготовка
    manager = storage_manager()
    dummy = nomenclature_group_model.create_from_dict({"id": "non-existent-id", "name": "Не существует"})

    # Действие
    result = manager.update(storage_manager.group_key(), dummy)

    # Проверки
    assert result is False


def test_storage_manager_delete_existing_item():
    """
    Проверка успешного удаления объекта из хранилища.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа для удаления")
    manager.add(storage_manager.group_key(), group)

    try:
        # Действие
        result = manager.delete(storage_manager.group_key(), group.id)

        # Проверки
        assert result is True
        found = next((item for item in manager.get(storage_manager.group_key()) if item.id == group.id), None)
        assert found is None
    finally:
        manager.delete(storage_manager.group_key(), group.id)


def test_storage_manager_delete_non_existing_returns_false():
    """
    Проверка возврата False при удалении несуществующего объекта.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    result = manager.delete(storage_manager.group_key(), "non-existent-id")

    # Проверки
    assert result is False


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


def test_storage_manager_update_with_id_change():
    """
    Проверка обновления объекта с изменением идентификатора.
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Группа со сменой ID")
    manager.add(storage_manager.group_key(), group)
    new_group = nomenclature_group_model.create_from_dict({"id": "new-group-id", "name": "Новое имя"})

    try:
        # Действие
        result = manager.update(storage_manager.group_key(), new_group, entity_id=group.id)

        # Проверки
        assert result is True
        assert manager.delete(storage_manager.group_key(), "new-group-id") is True
    finally:
        manager.delete(storage_manager.group_key(), group.id)
        manager.delete(storage_manager.group_key(), "new-group-id")

