from datetime import date, datetime
import json
import os
import pytest
from src.dtos.report_type_enum import report_type_enum
from src.logics.convert_factory import convert_factory
from src.logics.json_serializer import json_serializer
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.settings_model import settings_model


def test_json_serializer_init():
    """
    Проверка создания сериализатора с фабрикой по умолчанию.
    """
    # Подготовка
    # Действие
    serializer = json_serializer()

    # Проверки
    assert serializer is not None


def test_json_serializer_init_with_factory():
    """
    Проверка создания сериализатора с переданной фабрикой.
    """
    # Подготовка
    factory = convert_factory()

    # Действие
    serializer = json_serializer(factory)

    # Проверки
    assert serializer is not None


def test_json_serializer_to_json_primitives():
    """
    Проверка сериализации примитивных типов в JSON.
    """
    # Подготовка
    serializer = json_serializer()
    d = date(2026, 10, 24)

    # Действие
    res_int = serializer.to_json(123)
    res_str = serializer.to_json("проверка")
    res_date = serializer.to_json(d)
    res_none = serializer.to_json(None)

    # Проверки
    assert json.loads(res_int) == 123
    assert json.loads(res_str) == "проверка"
    assert json.loads(res_date) == "2026-10-24"
    assert json.loads(res_none) is None


def test_json_serializer_to_json_range_model():
    """
    Проверка сериализации доменной модели единицы измерения в JSON.
    """
    # Подготовка
    serializer = json_serializer()
    kg = range_model.create_kilogram()

    # Действие
    json_text = serializer.to_json(kg)
    parsed = json.loads(json_text)

    # Проверки
    assert parsed["name"] == "килограмм"
    assert parsed["conversion_factor"] == 1000
    assert parsed["base_range"]["name"] == "грамм"


def test_json_serializer_to_json_organization_model():
    """
    Проверка сериализации доменной модели организации в JSON.
    """
    # Подготовка
    serializer = json_serializer()
    org = organization_model.create(
        name="ООО Ромашка",
        inn="7701234567",
        bik="123456789",
        account="12345678901234567890",
        ownership_form="ООО"
    )

    # Действие
    json_text = serializer.to_json(org)
    parsed = json.loads(json_text)

    # Проверки
    assert parsed["name"] == "ООО Ромашка"
    assert parsed["inn"] == "7701234567"
    assert parsed["bik"] == "123456789"


def test_json_serializer_to_json_recipe_model():
    """
    Проверка сериализации полной технологической карты в JSON.
    """
    # Подготовка
    serializer = json_serializer()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    json_text = serializer.to_json(recipe)
    parsed = json.loads(json_text)

    # Проверки
    assert "Пицца Маргарита" in parsed["name"]
    assert len(parsed["rows"]) > 0
    assert len(parsed["steps"]) > 0
    assert parsed["gross_weight"] > 0
    assert parsed["net_weight"] > 0


def test_json_serializer_to_json_validity():
    """
    Проверка формирования валидной строки JSON методом to_json.
    """
    # Подготовка
    serializer = json_serializer()
    kg = range_model.create_kilogram()

    # Действие
    json_text = serializer.to_json(kg)
    parsed = json.loads(json_text)

    # Проверки
    assert parsed["name"] == "килограмм"
    assert parsed["conversion_factor"] == 1000
    assert parsed["base_range"]["name"] == "грамм"


def test_json_serializer_to_json_file(tmp_path):
    """
    Проверка сохранения результата сериализации в файл JSON.
    """
    # Подготовка
    serializer = json_serializer()
    org = organization_model.create(
        name="Тест",
        inn="7701234567",
        bik="123456789",
        account="12345678901234567890",
        ownership_form="ООО"
    )
    file_path = str(tmp_path / "test_org.json")

    # Действие
    serializer.to_json_file(org, file_path)

    # Проверки
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["name"] == "Тест"


def test_json_serializer_nested_recipe():
    """
    Проверка сериализации вложенного рецепта внутри номенклатуры строки.
    """
    # Подготовка
    serializer = json_serializer()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    parsed = json.loads(serializer.to_json(recipe))
    nested_recipe = parsed["rows"][0]["nomenclature"]["recipe"]

    # Проверки
    assert isinstance(nested_recipe, dict)
    assert nested_recipe["name"] == "Тесто дрожжевое (заготовка)"
    assert len(nested_recipe["rows"]) > 0


def test_json_serializer_settings_model_with_enum():
    """
    Проверка сериализации модели настроек с перечислением формата ответа.
    """
    # Подготовка
    serializer = json_serializer()
    settings = settings_model()
    settings.boss_name = "Гуреев Р. А."
    settings.response_format = report_type_enum.CSV

    # Действие
    parsed = json.loads(serializer.to_json(settings))

    # Проверки
    assert parsed["boss_name"] == "Гуреев Р. А."
    assert parsed["response_format"] == report_type_enum.CSV.value
