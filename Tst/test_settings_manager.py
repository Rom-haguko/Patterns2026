import pytest
from src.core.exception import arguments_exception, operation_exception
from src.dtos.report_type_enum import report_type_enum
from src.logics.settings_manager import settings_manager
from src.models.organization_model import organization_model
from src.models.settings_model import settings_model


def _get_loaded_manager() -> settings_manager:
    """
    Возвращает экземпляр settings_manager с загруженными настройками.
    """
    manager = settings_manager()
    manager.load()
    return manager


def test_not_raise_settings_manager_load():
    """
    Проверка загрузки настроек: метод load() не должен выбрасывать исключений
    при наличии корректного конфигурационного файла.
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    manager.load()

    # Проверки
    assert manager.is_loaded is True


def test_not_empty_settings_manager_load():
    """
    Проверка загрузки настроек: после успешного вызова load() свойство settings
    должно быть инициализировано.
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    manager.load()

    # Проверки
    assert manager.settings is not None


def test_is_loaded_flag_true_after_load():
    """
    Проверка флага is_loaded: после успешной загрузки флаг должен быть True.
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    manager.load()

    # Проверки
    assert manager.is_loaded is True


def test_load_raises_exception_on_invalid_file():
    """
    Проверка обработки ошибок: при указании несуществующего файла
    метод load() должен выбрасывать operation_exception.
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    with pytest.raises(operation_exception):
        manager.load("non_existent_file_xyz.json")

    # Проверки
    assert True


def test_equals_settings_manager_create():
    """
    Проверка шаблона Singleton: два созданных экземпляра settings_manager равны.
    """
    # Подготовка
    # Действие
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Проверки
    assert instance1 == instance2


def test_equals_settings_manager_setting():
    """
    Проверка идентичности настроек: свойство settings у двух экземпляров менеджера
    возвращает один и тот же объект.
    """
    # Подготовка
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Действие
    setting1 = instance1.settings
    setting2 = instance2.settings

    # Проверки
    assert setting1 == setting2


def test_same_instance_settings_manager_singleton():
    """
    Проверка тождественности (is): два экземпляра settings_manager должны быть
    одним и тем же объектом в памяти.
    """
    # Подготовка
    # Действие
    instance1 = settings_manager()
    instance2 = settings_manager()

    # Проверки
    assert instance1 is instance2


def test_convert_returns_settings_model():
    """
    Проверка типа результата convert: после вызова load() свойство settings
    должно быть экземпляром класса settings_model.
    """
    # Подготовка
    manager = _get_loaded_manager()

    # Действие
    settings = manager.settings

    # Проверки
    assert isinstance(settings, settings_model)


def test_convert_company_is_organization_model():
    """
    Проверка преобразования данных компании: после вызова convert() поле company
    должно быть экземпляром organization_model.
    """
    # Подготовка
    manager = _get_loaded_manager()

    # Действие
    company = manager.settings.company

    # Проверки
    assert isinstance(company, organization_model)


def test_convert_company_name_not_empty():
    """
    Проверка корректности данных: после вызова convert() название организации
    не должно быть пустым.
    """
    # Подготовка
    manager = _get_loaded_manager()

    # Действие
    company_name = manager.settings.company.name

    # Проверки
    assert company_name != ""


def test_convert_boss_name_from_ceo_field():
    """
    Проверка маппинга поля ceo: значение поля boss_name модели настроек не должно быть пустым.
    """
    # Подготовка
    manager = _get_loaded_manager()

    # Действие
    boss_name = manager.settings.boss_name

    # Проверки
    assert boss_name != ""


def test_convert_with_manual_data():
    """
    Прямая проверка метода convert: при ручной установке данных через атрибут класса
    преобразование должно корректно заполнить settings.
    """
    # Подготовка
    manager = settings_manager()
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

    try:
        # Действие
        result = manager.convert()

        # Проверки
        assert result is True
        assert manager.settings.company.name == "ООО Тест"
        assert manager.settings.boss_name == "Иванов И. И."
        assert manager.settings.account_name == "Петров П. П."
    finally:
        setattr(manager, attr, original_data)
        manager.load()


def test_convert_response_format_from_settings_file():
    """
    Проверка загрузки формата ответа из файла настроек settings.json.
    """
    # Подготовка
    manager = _get_loaded_manager()

    # Действие
    format_type = manager.settings.response_format

    # Проверки
    assert format_type == report_type_enum.MARKDOWN


def test_convert_with_custom_response_format():
    """
    Проверка загрузки формата ответа при явном указании в данных.
    """
    # Подготовка
    manager = settings_manager()
    attr = f"_{settings_manager.__name__}__data"
    original_data = getattr(manager, attr, {})

    test_data = {
        "response_format": "CSV"
    }
    setattr(manager, attr, test_data)

    try:
        # Действие
        manager.convert()

        # Проверки
        assert manager.settings.response_format == report_type_enum.CSV
    finally:
        setattr(manager, attr, original_data)
        manager.load()


def test_settings_model_response_format_property():
    """
    Проверка установки и чтения формата ответа через модель настроек.
    """
    # Подготовка
    model = settings_model()

    # Действие
    model.response_format = report_type_enum.XML
    xml_format = model.response_format
    model.response_format = "HTML"
    html_format = model.response_format

    # Проверки
    assert xml_format == report_type_enum.XML
    assert html_format == report_type_enum.HTML


def test_settings_model_response_format_invalid_raises():
    """
    Проверка генерации исключения при некорректном формате ответа.
    """
    # Подготовка
    model = settings_model()

    # Действие
    with pytest.raises(arguments_exception):
        model.response_format = "НЕВЕРНЫЙ_ФОРМАТ"

    # Проверки
    assert True
