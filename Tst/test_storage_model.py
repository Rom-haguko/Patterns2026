import pytest
from src.core.exception import arguments_exception
from src.models.storage_model import storage_model


def test_storage_model_default_creation():
    """
    <summary>
    Проверка успешного создания объекта склада без передачи адреса (по умолчанию пустая строка).
    </summary>
    """
    # Подготовка
    storage_name = "Центральный склад"

    # Действие
    storage = storage_model(storage_name)

    # Проверка
    assert storage.name == storage_name
    assert storage.id is not None
    assert storage.address == ""


def test_storage_model_creation_with_valid_address():
    """
    <summary>
    Проверка успешного сохранения наименования и физического адреса места хранения.
    </summary>
    """
    # Подготовка
    storage_name = "Склад сырья"
    address_str = "г. Санкт-Петербург, Революционное шоссе, д. 12"

    # Действие
    storage = storage_model(storage_name, address_str)

    # Проверка
    assert storage.name == storage_name
    assert storage.address == address_str


def test_storage_model_non_string_address_raises_exception():
    """
    <summary>
    Передача числового значения вместо строки в поле address должна вызывать arguments_exception.
    </summary>
    """
    # Подготовка
    storage_name = "Склад готовой продукции"
    invalid_address = 999000

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        storage_model(storage_name, invalid_address)


def test_storage_model_empty_name_raises_exception():
    """
    <summary>
    Проверка валидации пустого имени склада (наследуется от name_id).
    </summary>
    """
    # Подготовка
    empty_name = ""

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        storage_model(empty_name)


def test_storage_model_whitespace_only_name_raises_exception():
    """
    <summary>
    Имя склада, состоящее только из пробельных символов, отклоняется валидатором.
    </summary>
    """
    # Подготовка
    whitespace_name = "     "

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        storage_model(whitespace_name)


def test_storage_model_equality_with_different_types():
    """
    <summary>
    Оператор == должен корректно возвращать False при сравнении объекта склада со строкой или числом.
    </summary>
    """
    # Подготовка
    storage = storage_model("Архивный склад")
    different_type_string = "Архивный склад"
    different_type_number = 777

    # Действие & Проверка
    assert storage != different_type_string
    assert storage != different_type_number


def test_storage_model_equality_with_same_names_different_ids():
    """
    <summary>
    Два объекта складов с одинаковыми именами, но уникальными ID, не считаются равными.
    </summary>
    """
    # Подготовка
    storage_name = "Логистический хаб"
    warehouse1 = storage_model(storage_name)
    warehouse2 = storage_model(storage_name)

    # Действие & Проверка
    assert warehouse1 != warehouse2
    assert warehouse1.name == warehouse2.name