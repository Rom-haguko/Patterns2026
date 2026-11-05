from datetime import date, datetime
from enum import Enum
import pytest
from src.core.exception import arguments_exception
from src.dtos.report_type_enum import report_type_enum
from src.logics.basic_convertor import basic_convertor
from src.logics.convert_factory import convert_factory
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.storage_model import storage_model


def test_convert_factory_init():
    """
    Проверка создания фабрики и доступности базовых конверторов.
    """
    # Подготовка
    # Действие
    factory = convert_factory()

    # Проверки
    assert isinstance(factory.basic_convertor, basic_convertor)
    assert isinstance(factory.datetime_convertor, datetime_convertor)
    assert isinstance(factory.reference_convertor, reference_convertor)


def test_convert_factory_get_converter_by_type():
    """
    Проверка подбора конвертора методом get_converter по классу типа.
    """
    # Подготовка
    factory = convert_factory()

    # Действие
    int_conv = factory.get_converter(int)
    str_conv = factory.get_converter(str)
    float_conv = factory.get_converter(float)
    bool_conv = factory.get_converter(bool)
    dt_conv = factory.get_converter(datetime)
    date_conv = factory.get_converter(date)
    range_conv = factory.get_converter(range_model)
    org_conv = factory.get_converter(organization_model)

    # Проверки
    assert isinstance(int_conv, basic_convertor)
    assert isinstance(str_conv, basic_convertor)
    assert isinstance(float_conv, basic_convertor)
    assert isinstance(bool_conv, basic_convertor)
    assert isinstance(dt_conv, datetime_convertor)
    assert isinstance(date_conv, datetime_convertor)
    assert isinstance(range_conv, reference_convertor)
    assert isinstance(org_conv, reference_convertor)


def test_convert_factory_get_converter_by_instance():
    """
    Проверка подбора конвертора методом get_converter по экземпляру объекта.
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие
    int_conv = factory.get_converter(42)
    str_conv = factory.get_converter("текст")
    dt_conv = factory.get_converter(datetime.now())
    unit_conv = factory.get_converter(unit)
    none_conv = factory.get_converter(None)

    # Проверки
    assert isinstance(int_conv, basic_convertor)
    assert isinstance(str_conv, basic_convertor)
    assert isinstance(dt_conv, datetime_convertor)
    assert isinstance(unit_conv, reference_convertor)
    assert isinstance(none_conv, reference_convertor)


def test_convert_factory_convert_value_primitives():
    """
    Проверка конвертации примитивных типов и дат через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    d = date(2026, 10, 24)

    # Действие
    res_int = factory.convert_value(123)
    res_str = factory.convert_value("проверка")
    res_date = factory.convert_value(d)
    res_none = factory.convert_value(None)

    # Проверки
    assert res_int == 123
    assert res_str == "проверка"
    assert res_date == "2026-10-24"
    assert res_none is None


def test_convert_factory_convert_value_range_model():
    """
    Проверка конвертации доменной модели единицы измерения через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    kg = range_model.create_kilogram()

    # Действие
    result = factory.convert_value(kg)

    # Проверки
    assert result["name"] == "килограмм"
    assert result["conversion_factor"] == 1000
    assert result["base_range"]["name"] == "грамм"


def test_convert_factory_convert_value_organization_model():
    """
    Проверка конвертации доменной модели организации через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    org = organization_model.create(
        name="ООО Ромашка",
        inn="7701234567",
        bik="123456789",
        account="12345678901234567890",
        ownership_form="ООО"
    )

    # Действие
    result = factory.convert_value(org)

    # Проверки
    assert result["name"] == "ООО Ромашка"
    assert result["inn"] == "7701234567"
    assert result["bik"] == "123456789"
    assert result["account"] == "12345678901234567890"
    assert result["ownership_form"] == "ООО"


def test_convert_factory_convert_value_storage_model():
    """
    Проверка конвертации доменной модели склада через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    wh = storage_model.create(name="Главный склад", address="г. Москва, ул. Цветочная, д. 10")

    # Действие
    result = factory.convert_value(wh)

    # Проверки
    assert result["name"] == "Главный склад"
    assert result["address"] == "г. Москва, ул. Цветочная, д. 10"


def test_convert_factory_convert_value_nomenclature_model():
    """
    Проверка конвертации доменной модели номенклатуры через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    group = nomenclature_group_model.create_raw()
    unit = range_model.create_gram()
    item = nomenclature_model.create(name="Мука", full_name="Мука пшеничная высший сорт", group=group, range=unit)

    # Действие
    result = factory.convert_value(item)

    # Проверки
    assert result["name"] == "Мука"
    assert result["full_name"] == "Мука пшеничная высший сорт"
    assert result["group"]["name"] == "Сырьё"
    assert result["range"]["name"] == "грамм"


def test_convert_factory_convert_value_recipe_model():
    """
    Проверка конвертации полной технологической карты через convert_value.
    """
    # Подготовка
    factory = convert_factory()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    result = factory.convert_value(recipe)

    # Проверки
    assert "Пицца Маргарита" in result["name"]
    assert len(result["rows"]) > 0
    assert len(result["steps"]) > 0
    assert result["gross_weight"] > 0
    assert result["net_weight"] > 0


def test_convert_factory_convert_value_list():
    """
    Проверка рекурсивной конвертации списка с примитивами и моделью.
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие
    result = factory.convert_value([1, "текст", unit])

    # Проверки
    assert result[0] == 1
    assert result[1] == "текст"
    assert result[2]["name"] == "грамм"


def test_convert_factory_convert_value_dict():
    """
    Проверка рекурсивной конвертации словаря с вложенной моделью и перечислением.
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие
    result = factory.convert_value({"unit": unit, "format": report_type_enum.CSV})

    # Проверки
    assert result["unit"]["name"] == "грамм"
    assert result["format"] == report_type_enum.CSV.value


def test_convert_factory_convert_value_enum():
    """
    Проверка конвертации перечисления в его значение.
    """
    # Подготовка
    factory = convert_factory()

    # Действие
    result = factory.convert_value(report_type_enum.TXT)

    # Проверки
    assert result == report_type_enum.TXT.value


def test_convert_factory_convert_value_unknown_type_raises():
    """
    Проверка ошибки при попытке сериализовать неизвестный тип.
    """
    # Подготовка
    factory = convert_factory()

    # Действие
    with pytest.raises(arguments_exception):
        factory.convert_value(object())

    # Проверки
    assert True


def test_convert_factory_convert_value_enum_with_object_value():
    """
    Проверка использования имени перечисления, если его значение не примитивное.
    """
    # Подготовка
    class payload_enum(Enum):
        DICT = {"x": 1}

    factory = convert_factory()

    # Действие
    result = factory.convert_value(payload_enum.DICT)

    # Проверки
    assert result == "DICT"
