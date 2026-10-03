from src.logics.storage_manager import storage_manager


def test_equals_storage_manager_singleton():
    """
    Проверка паттерна Одиночка (Singleton): два созданных экземпляра storage_manager ссылаются на один объект.
    """
    # Подготовка & Действие
    instance1 = storage_manager()
    instance2 = storage_manager()

    # Проверка
    assert instance1 == instance2
    assert instance1 is instance2


def test_not_none_get_storage_manager_keys():
    """
    Проверка работы с кешем: при запросе данных по базовым ключам возвращаются инициализированные списки.
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