import pytest
from datetime import datetime, date
from src.core.validator import argument_exception
from src.dtos.report_type_enum import report_type_enum
from src.logics.convert_factory import convert_factory
from src.logics.basic_convertor import basic_convertor
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor
from src.models.range_model import range_model
from src.models.organization_model import organization_model
from src.models.storage_model import storage_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.recipe_model import recipe_model


# ─────────── Тесты инициализации и метода выбора конвертора ───────────

def test_convert_factory_init():
    """
    <summary>
    Проверка создания фабрики и доступности базовых конверторов.
    </summary>
    """
    # Подготовка и действие
    factory = convert_factory()

    # Проверка
    assert isinstance(factory.basic_convertor, basic_convertor)
    assert isinstance(factory.datetime_convertor, datetime_convertor)
    assert isinstance(factory.reference_convertor, reference_convertor)


def test_convert_factory_get_convertor_by_type():
    """
    <summary>
    Проверка подбора конвертора методом get_convertor по классу типа.
    </summary>
    """
    # Подготовка
    factory = convert_factory()

    # Действие и проверка
    assert isinstance(factory.get_convertor(int), basic_convertor)
    assert isinstance(factory.get_convertor(str), basic_convertor)
    assert isinstance(factory.get_convertor(float), basic_convertor)
    assert isinstance(factory.get_convertor(bool), basic_convertor)
    assert isinstance(factory.get_convertor(datetime), datetime_convertor)
    assert isinstance(factory.get_convertor(date), datetime_convertor)
    assert isinstance(factory.get_convertor(range_model), reference_convertor)
    assert isinstance(factory.get_convertor(organization_model), reference_convertor)


def test_convert_factory_get_convertor_by_instance():
    """
    <summary>
    Проверка подбора конвертора методом get_convertor по экземпляру объекта.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие и проверка
    assert isinstance(factory.get_convertor(42), basic_convertor)
    assert isinstance(factory.get_convertor("текст"), basic_convertor)
    assert isinstance(factory.get_convertor(datetime.now()), datetime_convertor)
    assert isinstance(factory.get_convertor(unit), reference_convertor)
    assert isinstance(factory.get_convertor(None), reference_convertor)


# ─────────── Тесты метода convert_value ───────────

def test_convert_factory_convert_value_primitives():
    """
    <summary>
    Проверка конвертации примитивных типов и дат через convert_value.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    d = date(2026, 10, 24)

    # Действие
    res_int = factory.convert_value(123)
    res_str = factory.convert_value("проверка")
    res_date = factory.convert_value(d)
    res_none = factory.convert_value(None)

    # Проверка
    assert res_int == 123
    assert res_str == "проверка"
    assert res_date == "2026-10-24"
    assert res_none is None


def test_convert_factory_convert_value_range_model():
    """
    <summary>
    Проверка конвертации доменной модели единицы измерения через convert_value.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    kg = range_model.create_kilogramm()

    # Действие
    result = factory.convert_value(kg)

    # Проверка
    assert result["name"] == "килограмм"
    assert result["conversion_factor"] == 1000
    assert result["base_range"]["name"] == "грамм"


def test_convert_factory_convert_value_organization_model():
    """
    <summary>
    Проверка конвертации доменной модели организации через convert_value.
    </summary>
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

    # Проверка
    assert result["name"] == "ООО Ромашка"
    assert result["inn"] == "7701234567"
    assert result["bik"] == "123456789"
    assert result["account"] == "12345678901234567890"
    assert result["ownership_form"] == "ООО"


def test_convert_factory_convert_value_storage_model():
    """
    <summary>
    Проверка конвертации доменной модели склада через convert_value.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    wh = storage_model.create(name="Главный склад", address="г. Москва, ул. Цветочная, д. 10")

    # Действие
    result = factory.convert_value(wh)

    # Проверка
    assert result["name"] == "Главный склад"
    assert result["address"] == "г. Москва, ул. Цветочная, д. 10"


def test_convert_factory_convert_value_nomenclature_model():
    """
    <summary>
    Проверка конвертации доменной модели номенклатуры через convert_value.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    group = nomenclature_group_model.create_raw()
    unit = range_model.create_gram()
    item = nomenclature_model.create(name="Мука", full_name="Мука пшеничная высший сорт", group=group, range=unit)

    # Действие
    result = factory.convert_value(item)

    # Проверка
    assert result["name"] == "Мука"
    assert result["full_name"] == "Мука пшеничная высший сорт"
    assert result["group"]["name"] == "Сырьё"
    assert result["range"]["name"] == "грамм"


def test_convert_factory_convert_value_recipe_model():
    """
    <summary>
    Проверка конвертации полной технологической карты через convert_value.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    result = factory.convert_value(recipe)

    # Проверка
    assert "Пицца Маргарита" in result["name"]
    assert len(result["rows"]) > 0
    assert len(result["steps"]) > 0
    assert result["gross_weight"] > 0
    assert result["net_weight"] > 0

# ─────────── Тесты составных структур и перечислений ───────────

def test_convert_factory_convert_value_list():
    """
    <summary>
    Проверка рекурсивной конвертации списка с примитивами и моделью.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие
    result = factory.convert_value([1, "текст", unit])

    # Проверка
    assert result[0] == 1
    assert result[1] == "текст"
    assert result[2]["name"] == "грамм"


def test_convert_factory_convert_value_dict():
    """
    <summary>
    Проверка рекурсивной конвертации словаря с вложенной моделью и перечислением.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    unit = range_model.create_gram()

    # Действие
    result = factory.convert_value({"unit": unit, "format": report_type_enum.CSV})

    # Проверка
    assert result["unit"]["name"] == "грамм"
    assert result["format"] == report_type_enum.CSV.value


def test_convert_factory_convert_value_enum():
    """
    <summary>
    Проверка конвертации перечисления в его значение.
    </summary>
    """
    # Подготовка
    factory = convert_factory()

    # Действие и проверка
    assert factory.convert_value(report_type_enum.TXT) == report_type_enum.TXT.value


def test_convert_factory_convert_value_unknown_type_raises():
    """
    <summary>
    Проверка ошибки при попытке сериализовать неизвестный тип.
    </summary>
    """
    # Подготовка
    factory = convert_factory()

    # Действие и проверка
    with pytest.raises(argument_exception):
        factory.convert_value(object())
