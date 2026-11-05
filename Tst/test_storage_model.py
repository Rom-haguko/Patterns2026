import pytest
from src.core.exception import arguments_exception
from src.models.storage_model import storage_model


def test_storage_model_default_creation():
    """
    Проверка успешного создания объекта склада без передачи адреса (по умолчанию пустая строка).
    """
    # Подготовка
    storage_name = "Центральный склад"

    # Действие
    storage = storage_model(storage_name)

    # Проверки
    assert storage.name == storage_name
    assert storage.id is not None
    assert storage.address == ""


def test_storage_model_creation_with_valid_address():
    """
    Проверка успешного сохранения наименования и физического адреса места хранения.
    """
    # Подготовка
    storage_name = "Склад сырья"
    address_str = "г. Санкт-Петербург, Революционное шоссе, д. 12"

    # Действие
    storage = storage_model(storage_name, address_str)

    # Проверки
    assert storage.name == storage_name
    assert storage.address == address_str


def test_storage_model_non_string_address_raises_exception():
    """
    Передача числового значения вместо строки в поле address должна вызывать arguments_exception.
    """
    # Подготовка
    storage_name = "Склад готовой продукции"
    invalid_address = 999000

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        storage_model(storage_name, invalid_address)

    # Проверки
    assert exc_info.value is not None


def test_storage_model_empty_name_raises_exception():
    """
    Проверка валидации пустого имени склада (наследуется от abstract_model).
    """
    # Подготовка
    empty_name = ""

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        storage_model(empty_name)

    # Проверки
    assert exc_info.value is not None


def test_storage_model_whitespace_only_name_raises_exception():
    """
    Имя склада, состоящее только из пробельных символов, отклоняется валидатором.
    """
    # Подготовка
    whitespace_name = "     "

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        storage_model(whitespace_name)

    # Проверки
    assert exc_info.value is not None


def test_storage_model_equality_with_different_types():
    """
    Оператор == должен корректно возвращать False при сравнении объекта склада со строкой или числом.
    """
    # Подготовка
    storage = storage_model("Архивный склад")
    different_type_string = "Архивный склад"
    different_type_number = 777

    # Действие
    is_equal_string = storage == different_type_string
    is_equal_number = storage == different_type_number

    # Проверки
    assert is_equal_string is False
    assert is_equal_number is False


def test_storage_model_equality_with_same_names_different_ids():
    """
    Два объекта складов с одинаковыми именами, но уникальными ID, не считаются равными.
    """
    # Подготовка
    storage_name = "Логистический хаб"
    warehouse1 = storage_model(storage_name)
    warehouse2 = storage_model(storage_name)

    # Действие
    is_equal = warehouse1 == warehouse2

    # Проверки
    assert is_equal is False
    assert warehouse1.name == warehouse2.name
