from src.logics.settings_manager import settings_manager
from src.core.validator import operation_exception


def test_not_raise_settings_manager_load():
    """
    Проверка загрузки настроек: метод load() не должен выбрасывать исключений при наличии конфигурационного файла.
    """
    # Подготовка
    manager = settings_manager()

    # Действие & Проверка
    try:
        manager.load()
        assert True
    except operation_exception:
        assert False
    except Exception:
        assert False


def test_not_empty_settings_manager_load():
    """
    Проверить загрузку настроек: после успешного вызова load() свойство settings должно быть инициализировано.
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    try:
        manager.load()
    except Exception:
        assert False

    # Проверка
    assert manager.settings is not None


def test_equals_settings_manager_create():
    """
    Проверка шаблона Одиночка (Singleton): два созданных экземпляра settings_manager равны.
    """
    # Подготовка & Действие
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Проверка
    assert instance1 == instance2


def test_equals_settings_manager_setting():
    """
    Проверка идентичности настроек: свойство setting у двух экземпляров менеджера возвращает один и тот же объект.
    """
    # Подготовка
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Действие
    setting1 = instance1.setting
    setting2 = instance2.setting

    # Проверка
    assert setting1 == setting2