import pytest
from src.core.exception import arguments_exception
from src.models.storage_model import storage_model


def test_storage_model_default_creation():
    """
    Проверка успешного создания объекта склада без передачи адреса (по умолчанию пустая строка).
    """
    storage = storage_model("Центральный склад")

    assert storage.name == "Центральный склад"
    assert storage.id is not None
    assert storage.address == ""


def test_storage_model_creation_with_valid_address():
    """
    Проверка успешного сохранения наименования и физического адреса места хранения.
    """
    address_str = "г. Санкт-Петербург, Революционное шоссе, д. 12"
    storage = storage_model("Склад сырья", address_str)

    assert storage.name == "Склад сырья"
    assert storage.address == address_str


def test_storage_model_non_string_address_raises_exception():
    """
    Передача числового значения вместо строки в поле address должна вызывать arguments_exception.
    """
    with pytest.raises(arguments_exception):
        storage_model("Склад готовой продукции", 999000)


def test_storage_model_empty_name_raises_exception():
    """
    Проверка валидации пустого имени склада (наследуется от name_id).
    """
    with pytest.raises(arguments_exception):
        storage_model("")


def test_storage_model_whitespace_only_name_raises_exception():
    """
    Имя склада, состоящее только из пробельных символов, отклоняется валидатором.
    """
    with pytest.raises(arguments_exception):
        storage_model("     ")


def test_storage_model_equality_with_different_types():
    """
    Оператор == должен корректно возвращать False при сравнении объекта склада со строкой или числом.
    """
    storage = storage_model("Архивный склад")

    assert storage != "Архивный склад"
    assert storage != 777


def test_storage_model_equality_with_same_names_different_ids():
    """
    Два объекта складов с одинаковыми именами, но уникальными ID, не считаются равными.
    """
    warehouse1 = storage_model("Логистический хаб")
    warehouse2 = storage_model("Логистический хаб")

    assert warehouse1 != warehouse2
    assert warehouse1.name == warehouse2.name