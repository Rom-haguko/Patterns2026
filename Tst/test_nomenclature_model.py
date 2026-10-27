import pytest
from src.core.exception import arguments_exception
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model


def test_nomenclature_model_successful_creation():
    """
    <summary>
    Проверка корректной инициализации объекта номенклатуры со всеми заполненными атрибутами.
    </summary>
    """
    # Подготовка
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    item_name = "Цемент М500"
    item_full_name = "Портландцемент марки М500 Д20 (мешок 50 кг)"

    # Действие
    item = nomenclature_model(
        name=item_name,
        full_name=item_full_name,
        group=category,
        range=measure_unit
    )

    # Проверка
    assert item.name == item_name
    assert item.full_name == item_full_name
    assert item.group is category
    assert item.range is measure_unit


def test_nomenclature_model_full_name_exact_255_length():
    """
    <summary>
    Проверка допустимости граничного значения длины полного наименования (255 символов).
    </summary>
    """
    # Подготовка
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    item_name = "Цемент М500"
    boundary_full_name = "К" * 255

    # Действие
    item = nomenclature_model(item_name, boundary_full_name, category, measure_unit)

    # Проверка
    assert len(item.full_name) == 255
    assert item.full_name == boundary_full_name


def test_nomenclature_model_full_name_exceeds_limit_raises_exception():
    """
    <summary>
    Проверка выброса исключения arguments_exception при задании полного названия длиннее 255 символов.
    </summary>
    """
    # Подготовка
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    item_name = "Цемент М500"
    overflow_full_name = "К" * 256

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        nomenclature_model(item_name, overflow_full_name, category, measure_unit)


def test_nomenclature_model_empty_full_name_raises_exception():
    """
    <summary>
    Проверка передачи пустого значения в качестве полного наименования.
    </summary>
    """
    # Подготовка
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    item_name = "Цемент М500"
    empty_full_name = ""

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        nomenclature_model(item_name, empty_full_name, category, measure_unit)


def test_nomenclature_model_wrong_group_type_raises_exception():
    """
    <summary>
    Проверка валидации типа данных для поля group (ожидается объект nomenclature_group_model).
    </summary>
    """
    # Подготовка
    measure_unit = range_model("килограмм", 1)
    invalid_group = "Сухие смеси"
    item_name = "Цемент М500"
    item_full_name = "Цемент М500 описание"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        nomenclature_model(item_name, item_full_name, invalid_group, measure_unit)


def test_nomenclature_model_wrong_range_type_raises_exception():
    """
    <summary>
    Проверка валидации типа данных для поля range (ожидается объект range_model).
    </summary>
    """
    # Подготовка
    category = nomenclature_group_model("Сухие смеси")
    invalid_range = "килограмм"
    item_name = "Цемент М500"
    item_full_name = "Цемент М500 описание"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        nomenclature_model(item_name, item_full_name, category, invalid_range)

def test_nomenclature_model_accepts_recipe_model():
    """
    <summary>
    Проверка установки рецепта, который является экземпляром recipe_model.
    </summary>
    """
    # Подготовка
    item = nomenclature_model("Мука", "Мука пшеничная", nomenclature_group_model("Сырьё"), range_model("грамм", 1))
    recipe = recipe_model.create(name="Тесто")

    # Действие
    item.recipe = recipe

    # Проверка
    assert item.recipe is recipe


def test_nomenclature_model_rejects_foreign_recipe_type():
    """
    <summary>
    Проверка отказа при установке объекта с именем класса recipe_model, но чужим типом.
    </summary>
    """
    # Подготовка
    item = nomenclature_model("Мука", "Мука пшеничная", nomenclature_group_model("Сырьё"), range_model("грамм", 1))
    fake_recipe = type("recipe_model", (), {})()

    # Действие и проверка
    with pytest.raises(arguments_exception):
        item.recipe = fake_recipe
