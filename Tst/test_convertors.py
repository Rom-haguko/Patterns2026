import pytest
from datetime import datetime, date, time
from src.core.abstract_covertor import abstract_covertor
from src.core.validator import argument_exception
from src.logics.basic_convertor import basic_convertor
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor
from src.logics.convert_factory import convert_factory
from src.models.range_model import range_model
from src.models.organization_model import organization_model


class dummy_circular_node:
    """
    Вспомогательный тестовый класс для проверки циклов ссылок.
    """
    def __init__(self, name: str):
        self.id = "node-id"
        self.name = name
        self.next_node = None


# ─────────── Тесты abstract_covertor ───────────

def test_abstract_covertor_cannot_be_instantiated():
    """
    <summary>
    Проверка невозможности создания экземпляра абстрактного класса abstract_covertor.
    </summary>
    """
    # Действие и проверка
    with pytest.raises(TypeError):
        abstract_covertor()


# ─────────── Тесты basic_convertor ───────────

def test_basic_convertor_int():
    """
    <summary>
    Проверка конвертации целочисленного значения.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("count", 10)

    # Проверка
    assert result == {"count": 10}


def test_basic_convertor_float():
    """
    <summary>
    Проверка конвертации вещественного числа.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("weight", 250.5)

    # Проверка
    assert result == {"weight": 250.5}


def test_basic_convertor_str():
    """
    <summary>
    Проверка конвертации строкового значения.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("title", "Пицца")

    # Проверка
    assert result == {"title": "Пицца"}


def test_basic_convertor_bool():
    """
    <summary>
    Проверка конвертации логического значения.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие
    result = convertor.convert("is_active", True)

    # Проверка
    assert result == {"is_active": True}


def test_basic_convertor_requires_field_and_value():
    """
    <summary>
    Проверка строгого контракта: метод convert требует имя поля и значение.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие и проверка
    with pytest.raises(TypeError):
        convertor.convert(100)


def test_basic_convertor_empty_field_raises():
    """
    <summary>
    Проверка возбуждения исключения при пустом имени поля.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие и проверка
    with pytest.raises(argument_exception):
        convertor.convert("", 10)


def test_basic_convertor_invalid_type_raises():
    """
    <summary>
    Проверка возбуждения исключения при передаче неподдерживаемого типа данных.
    </summary>
    """
    # Подготовка
    convertor = basic_convertor()

    # Действие и проверка
    with pytest.raises(argument_exception):
        convertor.convert("date", datetime.now())


# ─────────── Тесты datetime_convertor ───────────

def test_datetime_convertor_datetime():
    """
    <summary>
    Проверка конвертации объекта datetime в формат ISO 8601.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()
    dt = datetime(2026, 10, 24, 12, 30, 45)

    # Действие
    result = convertor.convert("created_at", dt)

    # Проверка
    assert result == {"created_at": "2026-10-24T12:30:45"}


def test_datetime_convertor_date():
    """
    <summary>
    Проверка конвертации объекта date в формат ISO 8601.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()
    d = date(2026, 10, 24)

    # Действие
    result = convertor.convert("doc_date", d)

    # Проверка
    assert result == {"doc_date": "2026-10-24"}


def test_datetime_convertor_time():
    """
    <summary>
    Проверка конвертации объекта time в формат ISO 8601.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()
    t = time(15, 45, 0)

    # Действие
    result = convertor.convert("work_time", t)

    # Проверка
    assert result == {"work_time": "15:45:00"}


def test_datetime_convertor_requires_field_and_value():
    """
    <summary>
    Проверка строгого контракта: метод convert требует имя поля и значение.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие и проверка
    with pytest.raises(TypeError):
        convertor.convert(date(2026, 10, 24))


def test_datetime_convertor_invalid_type_raises():
    """
    <summary>
    Проверка возбуждения исключения при передаче строки вместо даты.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие и проверка
    with pytest.raises(argument_exception):
        convertor.convert("created_at", "2026-10-24")


def test_datetime_convertor_empty_field_raises():
    """
    <summary>
    Проверка возбуждения исключения при пустом имени поля даты.
    </summary>
    """
    # Подготовка
    convertor = datetime_convertor()

    # Действие и проверка
    with pytest.raises(argument_exception):
        convertor.convert("   ", date(2026, 10, 24))


# ─────────── Тесты reference_convertor ───────────

def test_reference_convertor_simple_entity():
    """
    <summary>
    Проверка конвертации простой доменной сущности без вложенных сущностей.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    unit = range_model.create_gram()

    # Действие
    result = convertor.convert("unit", unit)

    # Проверка
    assert result["unit"]["name"] == "грамм"
    assert result["unit"]["conversion_factor"] == 1
    assert result["unit"]["base_range"] is None
    assert "id" in result["unit"]


def test_reference_convertor_with_field_name():
    """
    <summary>
    Проверка конвертации сущности с указанием имени поля.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    unit = range_model.create_gram()

    # Действие
    result = convertor.convert("unit", unit)

    # Проверка
    assert "unit" in result
    assert result["unit"]["name"] == "грамм"


def test_reference_convertor_nested_reference():
    """
    <summary>
    Проверка конвертации составной сущности с вложенной ссылочной сущностью.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor
    kg = range_model.create_kilogramm()

    # Действие
    result = convertor.convert("unit", kg)

    # Проверка
    assert result["unit"]["name"] == "килограмм"
    assert result["unit"]["conversion_factor"] == 1000
    assert result["unit"]["base_range"] is not None
    assert result["unit"]["base_range"]["name"] == "грамм"


def test_reference_convertor_none_value():
    """
    <summary>
    Проверка обработки значения None.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor

    # Действие
    res_field = convertor.convert("parent", None)

    # Проверка
    assert res_field == {"parent": None}


def test_reference_convertor_circular_reference():
    """
    <summary>
    Проверка корректной обработки циклической ссылки без бесконечной рекурсии.
    </summary>
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

    # Проверка
    assert result["node"]["name"] == "Первый"
    assert result["node"]["next_node"]["name"] == "Второй"
    assert result["node"]["next_node"]["next_node"] == {"id": "node-id"}


def test_reference_convertor_primitive_type_raises():
    """
    <summary>
    Проверка возбуждения исключения при передаче примитивного типа в конвертор ссылок.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    convertor = factory.reference_convertor

    # Действие и проверка
    with pytest.raises(argument_exception):
        convertor.convert("number", 123)