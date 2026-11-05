from datetime import date, datetime, time
import pytest
from src.core.abstract_converter import abstract_converter
from src.core.exception import arguments_exception
from src.logics.basic_convertor import basic_convertor
from src.logics.convert_factory import convert_factory
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor
from src.models.organization_model import organization_model
from src.models.range_model import range_model


class dummy_circular_node:
    """
    Вспомогательный тестовый класс для проверки циклов ссылок.
    """
    def __init__(self, name: str):
        self.id = "node-id"
        self.name = name
        self.next_node = None


class attribute_error_node:
    """
    Вспомогательный тестовый класс со свойством, которое бросает AttributeError.
    """
    def __init__(self, name: str):
        self.name = name

    @property
    def broken(self):
        raise AttributeError("Свойство недоступно")


class recursion_error_node:
    """
    Вспомогательный тестовый класс со свойством, которое бросает RecursionError.
    """
    @property
    def broken(self):
        raise RecursionError("Циклический обход")


def test_abstract_converter_cannot_be_instantiated():
    """
    Проверка невозможности создания экземпляра абстрактного класса abstract_converter.
    """
    # Подготовка
    # Действие
    with pytest.raises(TypeError):
        abstract_converter()

    # Проверки
    assert True


def test_basic_convertor_int():
    """
    Проверка конвертации целочисленного значения.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("count", 10)

    # Проверки
    assert result == {"count": 10}


def test_basic_convertor_float():
    """
    Проверка конвертации вещественного числа.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("weight", 250.5)

    # Проверки
    assert result == {"weight": 250.5}


def test_basic_convertor_str():
    """
    Проверка конвертации строкового значения.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("title", "Пицца")

    # Проверки
    assert result == {"title": "Пицца"}


def test_basic_convertor_bool():
    """
    Проверка конвертации логического значения.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("is_active", True)

    # Проверки
    assert result == {"is_active": True}


def test_basic_convertor_requires_field_and_value():
    """
    Проверка строгого контракта: метод convert требует имя поля и значение.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    with pytest.raises(TypeError):
        convertor.convert(100)

    # Проверки
    assert True


def test_basic_convertor_empty_field_raises():
    """
    Проверка возбуждения исключения при пустом имени поля.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    with pytest.raises(arguments_exception):
        convertor.convert("", 10)

    # Проверки
    assert True


def test_basic_convertor_invalid_type_raises():
    """
    Проверка возбуждения исключения при передаче неподдерживаемого типа данных.
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    with pytest.raises(arguments_exception):
        convertor.convert("date", datetime.now())

    # Проверки
    assert True


def test_datetime_convertor_datetime():
    """
    Проверка конвертации объекта datetime в формат ISO 8601.
    """
    # Подготовка
    convertor = datetime_convertor()
    dt = datetime(2026, 10, 24, 12, 30, 45)

    # Действие
    result = convertor.convert("created_at", dt)

    # Проверки
    assert result == {"created_at": "2026-10-24T12:30:45"}


def test_datetime_convertor_date():
    """
    Проверка конвертации объекта date в формат ISO 8601.
    """
    # Подготовка
    convertor = datetime_convertor()
    d = date(2026, 10, 24)

    # Действие
    result = convertor.convert("doc_date", d)

    # Проверки
    assert result == {"doc_date": "2026-10-24"}


def test_datetime_convertor_time():
    """
    Проверка конвертации объекта time в формат ISO 8601.
    """
    # Подготовка
    convertor = datetime_convertor()
    t = time(15, 45, 0)

    # Действие
    result = convertor.convert("work_time", t)

    # Проверки
    assert result == {"work_time": "15:45:00"}


def test_datetime_convertor_requires_field_and_value():
    """
    Проверка строгого контракта: метод convert требует имя поля и значение.
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие
    with pytest.raises(TypeError):
        convertor.convert(date(2026, 10, 24))

    # Проверки
    assert True


def test_datetime_convertor_invalid_type_raises():
    """
    Проверка возбуждения исключения при передаче строки вместо даты.
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие
    with pytest.raises(arguments_exception):
        convertor.convert("created_at", "2026-10-24")

    # Проверки
    assert True


def test_datetime_convertor_empty_field_raises():
    """
    Проверка возбуждения исключения при пустом имени поля даты.
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие
    with pytest.raises(arguments_exception):
        convertor.convert("   ", date(2026, 10, 24))

    # Проверки
    assert True


def test_reference_convertor_simple_entity():
    """
    Проверка конвертации простой доменной сущности без вложенных сущностей.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    unit = range_model.create_gram()

    # Действие
    result = convertor.convert("unit", unit)

    # Проверки
    assert result["unit"]["name"] == "грамм"
    assert result["unit"]["conversion_factor"] == 1
    assert result["unit"]["base_range"] is None
    assert "id" in result["unit"]


def test_reference_convertor_with_field_name():
    """
    Проверка конвертации сущности с указанием имени поля.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    unit = range_model.create_gram()

    # Действие
    result = convertor.convert("unit", unit)

    # Проверки
    assert "unit" in result
    assert result["unit"]["name"] == "грамм"


def test_reference_convertor_nested_reference():
    """
    Проверка конвертации составной сущности с вложенной ссылочной сущностью.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    kg = range_model.create_kilogram()

    # Действие
    result = convertor.convert("unit", kg)

    # Проверки
    assert result["unit"]["name"] == "килограмм"
    assert result["unit"]["conversion_factor"] == 1000
    assert result["unit"]["base_range"] is not None
    assert result["unit"]["base_range"]["name"] == "грамм"


def test_reference_convertor_none_value():
    """
    Проверка обработки значения None.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor

    # Действие
    res_field = convertor.convert("parent", None)

    # Проверки
    assert res_field == {"parent": None}


def test_reference_convertor_circular_reference():
    """
    Проверка корректной обработки циклической ссылки без бесконечной рекурсии.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    node1 = dummy_circular_node("Первый")
    node2 = dummy_circular_node("Второй")
    node1.next_node = node2
    node2.next_node = node1

    # Действие
    result = convertor.convert("node", node1)

    # Проверки
    assert result["node"]["name"] == "Первый"
    assert result["node"]["next_node"]["name"] == "Второй"
    assert result["node"]["next_node"]["next_node"] == {"id": "node-id"}


def test_reference_convertor_primitive_type_raises():
    """
    Проверка возбуждения исключения при передаче примитивного типа в конвертор ссылок.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor

    # Действие
    with pytest.raises(arguments_exception):
        convertor.convert("number", 123)

    # Проверки
    assert True


def test_reference_convertor_skips_attribute_error():
    """
    Проверка пропуска свойства, которое бросает AttributeError.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    node = attribute_error_node("Тестовый узел")

    # Действие
    result = convertor.convert("node", node)

    # Проверки
    assert result["node"]["name"] == "Тестовый узел"
    assert "broken" not in result["node"]


def test_reference_convertor_propagates_recursion_error():
    """
    Проверка проброса RecursionError при обходе свойства.
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    node = recursion_error_node()

    # Действие
    with pytest.raises(RecursionError):
        convertor.convert("node", node)

    # Проверки
    assert True
