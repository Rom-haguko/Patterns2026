import pytest
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


# ─────────────────────────── Тесты Singleton ───────────────────────────────────

def test_equals_storage_manager_singleton():
    """
    <summary>
    Проверка паттерна Одиночка (Singleton): два созданных экземпляра storage_manager
    равны по значению (__eq__).
    </summary>
    """
    # Подготовка & Действие
    instance1 = storage_manager()
    instance2 = storage_manager()

    # Проверка
    assert instance1 == instance2


def test_same_instance_storage_manager_singleton():
    """
    <summary>
    Проверка тождественности (is): два экземпляра storage_manager должны быть
    одним и тем же объектом в памяти.
    </summary>
    """
    # Подготовка & Действие
    instance1 = storage_manager()
    instance2 = storage_manager()

    # Проверка
    assert instance1 is instance2


# ─────────────────────────── Тесты ключей и get() ──────────────────────────────

def test_not_none_get_storage_manager_keys():
    """
    <summary>
    Проверка работы с кешем: при запросе данных по базовым ключам возвращаются
    инициализированные списки.
    </summary>
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    ranges = manager.get(storage_manager.range_key())
    nomenclatures = manager.get(storage_manager.nomenclature_key())
    groups = manager.get(storage_manager.group_key())
    storages = manager.get(storage_manager.storage_key())

    # Проверка
    assert isinstance(ranges, list)
    assert isinstance(nomenclatures, list)
    assert isinstance(groups, list)
    assert isinstance(storages, list)


def test_get_unknown_key_returns_empty_list():
    """
    <summary>
    Проверка поведения get() при обращении по неизвестному ключу:
    должен вернуться пустой список без исключений.
    </summary>
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    result = manager.get("unknown_key_xyz")

    # Проверка
    assert isinstance(result, list)
    assert len(result) == 0


# ─────────────────────────── Тесты первого старта (convert) ────────────────────

def test_convert_ranges_not_empty():
    """
    <summary>
    Проверка данных первого старта: коллекция единиц измерения не должна быть пустой
    после инициализации менеджера.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()

    # Проверка
    assert len(manager.get(storage_manager.range_key())) > 0


def test_convert_groups_not_empty():
    """
    <summary>
    Проверка данных первого старта: коллекция групп номенклатуры не должна быть пустой.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()

    # Проверка
    assert len(manager.get(storage_manager.group_key())) > 0


def test_convert_nomenclature_not_empty():
    """
    <summary>
    Проверка данных первого старта: коллекция номенклатурных позиций не должна
    быть пустой после инициализации.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()

    # Проверка
    assert len(manager.get(storage_manager.nomenclature_key())) > 0


def test_convert_storages_not_empty():
    """
    <summary>
    Проверка данных первого старта: коллекция складов не должна быть пустой
    после инициализации.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()

    # Проверка
    assert len(manager.get(storage_manager.storage_key())) > 0


def test_convert_ranges_contain_correct_types():
    """
    <summary>
    Проверка типов объектов в коллекции единиц измерения: каждый элемент
    должен быть экземпляром range_model.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    ranges = manager.get(storage_manager.range_key())

    # Проверка
    assert all(isinstance(r, range_model) for r in ranges)


def test_convert_groups_contain_correct_types():
    """
    <summary>
    Проверка типов объектов в коллекции групп: каждый элемент должен быть
    экземпляром nomenclature_group_model.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    groups = manager.get(storage_manager.group_key())

    # Проверка
    assert all(isinstance(g, nomenclature_group_model) for g in groups)


def test_convert_nomenclature_contain_correct_types():
    """
    <summary>
    Проверка типов объектов в коллекции номенклатуры: каждый элемент должен быть
    экземпляром nomenclature_model.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    nomenclatures = manager.get(storage_manager.nomenclature_key())

    # Проверка
    assert all(isinstance(n, nomenclature_model) for n in nomenclatures)


def test_convert_storages_contain_correct_types():
    """
    <summary>
    Проверка типов объектов в коллекции складов: каждый элемент должен быть
    экземпляром storage_model.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    storages = manager.get(storage_manager.storage_key())

    # Проверка
    assert all(isinstance(s, storage_model) for s in storages)


def test_convert_ranges_names_not_empty():
    """
    <summary>
    Проверка корректности данных первого старта: наименование каждой единицы
    измерения не должно быть пустым.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    ranges = manager.get(storage_manager.range_key())

    # Проверка
    assert all(r.name != "" for r in ranges)


def test_convert_nomenclature_have_valid_group_and_range():
    """
    <summary>
    Проверка связей номенклатуры: каждая позиция должна иметь установленные
    группу (group) и единицу измерения (range).
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    nomenclatures = manager.get(storage_manager.nomenclature_key())

    # Проверка
    for item in nomenclatures:
        assert item.group is not None
        assert item.range is not None


# ─────────────────────────── Тесты уникальности (add) ──────────────────────────

def test_add_duplicate_not_added():
    """
    <summary>
    Проверка уникальности: повторное добавление одного и того же объекта
    (по id) не должно увеличивать размер коллекции.
    </summary>
    """
    # Подготовка
    manager = storage_manager()
    group = nomenclature_group_model("Тест-дубликат-группа")
    # Добавляем первый раз
    manager.add(storage_manager.group_key(), group)
    size_after_first = len(manager.get(storage_manager.group_key()))

    # Действие: добавляем тот же объект повторно
    result = manager.add(storage_manager.group_key(), group)
    size_after_second = len(manager.get(storage_manager.group_key()))

    # Проверка
    assert result is False
    assert size_after_first == size_after_second


def test_add_different_objects_both_added():
    """
    <summary>
    Проверка добавления различных объектов: два разных экземпляра с одинаковым именем
    должны добавляться как отдельные элементы (у каждого свой id).
    </summary>
    """
    # Подготовка
    manager = storage_manager()
    group1 = nomenclature_group_model("Уникальная-группа-A")
    group2 = nomenclature_group_model("Уникальная-группа-A")
    size_before = len(manager.get(storage_manager.group_key()))

    # Действие
    result1 = manager.add(storage_manager.group_key(), group1)
    result2 = manager.add(storage_manager.group_key(), group2)
    size_after = len(manager.get(storage_manager.group_key()))

    # Проверка
    assert result1 is True
    assert result2 is True
    assert size_after == size_before + 2


def test_add_none_returns_false():
    """
    <summary>
    Проверка защиты от None: попытка добавить None в коллекцию должна
    вернуть False и не изменить коллекцию.
    </summary>
    """
    # Подготовка
    manager = storage_manager()
    size_before = len(manager.get(storage_manager.range_key()))

    # Действие
    result = manager.add(storage_manager.range_key(), None)

    # Проверка
    assert result is False
    assert len(manager.get(storage_manager.range_key())) == size_before


def test_add_returns_true_on_new_item():
    """
    <summary>
    Проверка возвращаемого значения add(): при добавлении нового (уникального)
    объекта метод должен вернуть True.
    </summary>
    """
    # Подготовка
    manager = storage_manager()
    new_storage = storage_model("Склад-новый-тест", "ул. Тестовая, д. 99")

    # Действие
    result = manager.add(storage_manager.storage_key(), new_storage)

    # Проверка
    assert result is True
    assert new_storage in manager.get(storage_manager.storage_key())


# ─────────────────────────── Тест data property ────────────────────────────────

def test_data_property_returns_dict():
    """
    <summary>
    Проверка свойства data: должен возвращаться словарь с ключами всех
    базовых коллекций.
    </summary>
    """
    # Подготовка & Действие
    manager = storage_manager()
    data = manager.data

    # Проверка
    assert isinstance(data, dict)
    assert storage_manager.range_key() in data
    assert storage_manager.nomenclature_key() in data
    assert storage_manager.group_key() in data
    assert storage_manager.storage_key() in data