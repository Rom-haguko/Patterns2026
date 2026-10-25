import os
import json
import pytest
from datetime import datetime, date
from src.logics.json_serializer import json_serializer
from src.logics.convert_factory import convert_factory
from src.models.range_model import range_model
from src.models.organization_model import organization_model
from src.models.recipe_model import recipe_model


# ─────────── Тесты инициализации ───────────

def test_json_serializer_init():
    """
    <summary>
    Проверка создания сериализатора с фабрикой по умолчанию.
    </summary>
    """
    # Действие
    serializer = json_serializer()

    # Проверка
    assert serializer is not None


def test_json_serializer_init_with_factory():
    """
    <summary>
    Проверка создания сериализатора с переданной фабрикой.
    </summary>
    """
    # Подготовка
    factory = convert_factory()

    # Действие
    serializer = json_serializer(factory)

    # Проверка
    assert serializer is not None


# ─────────── Тесты метода convert ───────────

def test_json_serializer_convert_primitives():
    """
    <summary>
    Проверка конвертации примитивных типов через сериализатор.
    </summary>
    """
    # Подготовка
    serializer = json_serializer()
    d = date(2026, 10, 24)

    # Действие
    res_int = serializer.convert(123)
    res_str = serializer.convert("проверка")
    res_date = serializer.convert(d)
    res_none = serializer.convert(None)

    # Проверка
    assert res_int == 123
    assert res_str == "проверка"
    assert res_date == "2026-10-24"
    assert res_none is None


def test_json_serializer_convert_range_model():
    """
    <summary>
    Проверка конвертации доменной модели единицы измерения через сериализатор.
    </summary>
    """
    # Подготовка
    serializer = json_serializer()
    kg = range_model.create_kilogramm()

    # Действие
    result = serializer.convert(kg)

    # Проверка
    assert result["name"] == "килограмм"
    assert result["conversion_factor"] == 1000
    assert result["base_range"]["name"] == "грамм"


def test_json_serializer_convert_organization_model():
    """
    <summary>
    Проверка конвертации доменной модели организации через сериализатор.
    </summary>
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
    result = serializer.convert(org)

    # Проверка
    assert result["name"] == "ООО Ромашка"
    assert result["inn"] == "7701234567"
    assert result["bik"] == "123456789"


def test_json_serializer_convert_recipe_model():
    """
    <summary>
    Проверка конвертации полной технологической карты через сериализатор.
    </summary>
    """
    # Подготовка
    serializer = json_serializer()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    result = serializer.convert(recipe)

    # Проверка
    assert "Пицца Маргарита" in result["name"]
    assert len(result["rows"]) > 0
    assert len(result["steps"]) > 0
    assert result["gross_weight"] > 0
    assert result["net_weight"] > 0


# ─────────── Тесты метода to_json ───────────

def test_json_serializer_to_json_validity():
    """
    <summary>
    Проверка формирования валидной строки JSON методом to_json.
    </summary>
    """
    # Подготовка
    serializer = json_serializer()
    kg = range_model.create_kilogramm()

    # Действие
    json_text = serializer.to_json(kg)
    parsed = json.loads(json_text)

    # Проверка
    assert parsed["name"] == "килограмм"
    assert parsed["conversion_factor"] == 1000
    assert parsed["base_range"]["name"] == "грамм"


def test_json_serializer_to_json_recipe():
    """
    <summary>
    Проверка формирования валидной строки JSON для рецепта.
    </summary>
    """
    # Подготовка
    serializer = json_serializer()
    recipe = recipe_model.create_pizza_margarita()

    # Действие
    json_text = serializer.to_json(recipe)
    parsed = json.loads(json_text)

    # Проверка
    assert "Пицца Маргарита" in parsed["name"]
    assert len(parsed["rows"]) > 0


# ─────────── Тесты метода to_json_file ───────────

def test_json_serializer_to_json_file(tmp_path):
    """
    <summary>
    Проверка сохранения результата сериализации в файл JSON.
    </summary>
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

    # Проверка
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["name"] == "Тест"