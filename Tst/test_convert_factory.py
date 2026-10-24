import os
import json
import pytest
from datetime import datetime, date
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
from src.models.settings_model import settings_model


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


# ─────────── Тесты методов конвертации и сериализации ───────────

def test_convert_factory_convert_primitives():
    """
    <summary>
    Проверка конвертации примитивных типов и дат через convert_factory.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    d = date(2026, 10, 24)

    # Действие
    res_int = factory.convert(123)
    res_str = factory.convert("проверка")
    res_date = factory.convert(d)
    res_none = factory.convert(None)

    # Проверка
    assert res_int == 123
    assert res_str == "проверка"
    assert res_date == "2026-10-24"
    assert res_none is None


def test_convert_factory_convert_composite_structures():
    """
    <summary>
    Проверка конвертации составных структур (списки, словари).
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    data = {
        "items": [1, 2, "три"],
        "date": date(2026, 1, 1),
        "unit": range_model.create_gram()
    }

    # Действие
    result = factory.convert(data)

    # Проверка
    assert result["items"] == [1, 2, "три"]
    assert result["date"] == "2026-01-01"
    assert result["unit"]["name"] == "грамм"


def test_convert_factory_convert_range_model():
    """
    <summary>
    Проверка конвертации доменной модели единицы измерения range_model.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    kg = range_model.create_kilogramm()

    # Действие
    result = factory.convert(kg)

    # Проверка
    assert result["name"] == "килограмм"
    assert result["conversion_factor"] == 1000
    assert result["base_range"]["name"] == "грамм"


def test_convert_factory_convert_organization_model():
    """
    <summary>
    Проверка конвертации доменной модели организации organization_model.
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
    result = factory.convert(org)

    # Проверка
    assert result["name"] == "ООО Ромашка"
    assert result["inn"] == "7701234567"
    assert result["bik"] == "123456789"
    assert result["account"] == "12345678901234567890"
    assert result["ownership_form"] == "ООО"


def test_convert_factory_convert_storage_model():
    """
    <summary>
    Проверка конвертации доменной модели склада storage_model.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    wh = storage_model.create(name="Главный склад", address="г. Москва, ул. Цветочная, д. 10")

    # Действие
    result = factory.convert(wh)

    # Проверка
    assert result["name"] == "Главный склад"
    assert result["address"] == "г. Москва, ул. Цветочная, д. 10"


def test_convert_factory_convert_nomenclature_model():
    """
    <summary>
    Проверка конвертации доменной модели номенклатуры nomenclature_model.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    group = nomenclature_group_model.create_raw()
    unit = range_model.create_gram()
    item = nomenclature_model.create(name="Мука", full_name="Мука пшеничная высший сорт", group=group, range=unit)

    # Действие
    result = factory.convert(item)

    # Проверка
    assert result["name"] == "Мука"
    assert result["full_name"] == "Мука пшеничная высший сорт"
    assert result["group"]["name"] == "Сырьё"
    assert result["range"]["name"] == "грамм"


def test_convert_factory_convert_recipe_model():
    """
    <summary>
    Проверка конвертации полной технологической карты recipe_model.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    result = factory.convert(recipe)

    # Проверка
    assert "Пицца Маргарита" in result["name"]
    assert len(result["rows"]) > 0
    assert len(result["steps"]) > 0
    assert result["gross_weight"] > 0
    assert result["net_weight"] > 0


def test_convert_factory_to_json_validity():
    """
    <summary>
    Проверка формирования валидной строки JSON методом to_json.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    kg = range_model.create_kilogramm()

    # Действие
    json_text = factory.to_json(kg)
    parsed = json.loads(json_text)

    # Проверка
    assert parsed["name"] == "килограмм"
    assert parsed["conversion_factor"] == 1000
    assert parsed["base_range"]["name"] == "грамм"


def test_convert_factory_to_json_file(tmp_path):
    """
    <summary>
    Проверка сохранения результата сериализации в файл JSON.
    </summary>
    """
    # Подготовка
    factory = convert_factory()
    org = organization_model.create(name="Тест", inn="7701234567", bik="123456789", account="12345678901234567890", ownership_form="ООО")
    file_path = str(tmp_path / "test_org.json")

    # Действие
    factory.to_json_file(org, file_path)

    # Проверка
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["name"] == "Тест"
