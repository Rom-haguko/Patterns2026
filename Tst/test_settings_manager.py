import pytest
from src.logics.settings_manager import settings_manager
from src.core.validator import operation_exception
from src.models.settings_model import settings_model
from src.models.organization_model import organization_model


# ─────────────────────────── Вспомогательная функция ───────────────────────────

def _get_loaded_manager() -> settings_manager:
    """
    Возвращает экземпляр settings_manager с загруженными настройками.
    """
    manager = settings_manager()
    manager.load()
    return manager


# ─────────────────────────── Тесты загрузки (load) ─────────────────────────────

def test_not_raise_settings_manager_load():
    """
    <summary>
    Проверка загрузки настроек: метод load() не должен выбрасывать исключений
    при наличии корректного конфигурационного файла.
    </summary>
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
    <summary>
    Проверить загрузку настроек: после успешного вызова load() свойство settings
    должно быть инициализировано (не None).
    </summary>
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


def test_is_loaded_flag_true_after_load():
    """
    <summary>
    Проверка флага is_loaded: после успешной загрузки флаг должен быть True.
    </summary>
    """
    # Подготовка & Действие
    manager = _get_loaded_manager()

    # Проверка
    assert manager.is_loaded is True


def test_load_raises_exception_on_invalid_file():
    """
    <summary>
    Проверка обработки ошибок: при указании несуществующего файла
    метод load() должен выбрасывать operation_exception.
    </summary>
    """
    # Подготовка
    manager = settings_manager()

    # Действие & Проверка
    with pytest.raises(operation_exception):
        manager.load("non_existent_file_xyz.json")


# ─────────────────────────── Тесты Singleton ───────────────────────────────────

def test_equals_settings_manager_create():
    """
    <summary>
    Проверка шаблона Одиночка (Singleton): два созданных экземпляра settings_manager равны.
    </summary>
    """
    # Подготовка & Действие
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Проверка
    assert instance1 == instance2


def test_equals_settings_manager_setting():
    """
    <summary>
    Проверка идентичности настроек: свойство setting у двух экземпляров менеджера
    возвращает один и тот же объект.
    </summary>
    """
    # Подготовка
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Действие
    setting1 = instance1.setting
    setting2 = instance2.setting

    # Проверка
    assert setting1 == setting2


def test_same_instance_settings_manager_singleton():
    """
    <summary>
    Проверка тождественности (is): два экземпляра settings_manager должны быть
    одним и тем же объектом в памяти.
    </summary>
    """
    # Подготовка & Действие
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Проверка
    assert instance1 is instance2


# ─────────────────────────── Тесты convert ─────────────────────────────────────

def test_convert_returns_settings_model():
    """
    <summary>
    Проверка типа результата convert: после вызова load() свойство settings
    должно быть экземпляром класса settings_model.
    </summary>
    """
    # Подготовка & Действие
    manager = _get_loaded_manager()

    # Проверка
    assert isinstance(manager.settings, settings_model)


def test_convert_company_is_organization_model():
    """
    <summary>
    Проверка преобразования данных компании: после вызова convert() поле company
    должно быть экземпляром organization_model.
    </summary>
    """
    # Подготовка & Действие
    manager = _get_loaded_manager()

    # Проверка
    assert isinstance(manager.settings.company, organization_model)


def test_convert_company_name_not_empty():
    """
    <summary>
    Проверка корректности данных: после вызова convert() название организации
    не должно быть пустым.
    </summary>
    """
    # Подготовка & Действие
    manager = _get_loaded_manager()

    # Проверка
    assert manager.settings.company.name != ""


def test_convert_boss_name_from_ceo_field():
    """
    <summary>
    Проверка маппинга поля ceo: значение поля «ceo» из settings.json должно
    быть перенесено в boss_name модели настроек.
    </summary>
    """
    # Подготовка & Действие
    manager = _get_loaded_manager()

    # Проверка: в settings.json поле company.ceo = "Гуреев Р. А."
    assert manager.settings.boss_name != ""


def test_convert_with_manual_data():
    """
    <summary>
    Прямая проверка метода convert: при ручной установке __data через load-
    совместимый сценарий преобразование должно корректно заполнить settings.
    Используется временный экземпляр через монки-патч данных.
    </summary>
    """
    # Подготовка
    manager = settings_manager()
    # Подменяем сырые данные напрямую через атрибут mangled-name
    attr = f"_{settings_manager.__name__}__data"
    original_data = getattr(manager, attr, {})

    test_data = {
        "company": {
            "name": "ООО Тест",
            "inn_kpp": "1234567890/123456789",
            "ceo": "Иванов И. И.",
        },
        "account_name": "Петров П. П.",
    }
    setattr(manager, attr, test_data)

    # Действие
    result = manager.convert()

    # Проверка
    assert result is True
    assert manager.settings.company.name == "ООО Тест"
    assert manager.settings.boss_name == "Иванов И. И."
    assert manager.settings.account_name == "Петров П. П."

    # Восстановление оригинальных данных
    setattr(manager, attr, original_data)