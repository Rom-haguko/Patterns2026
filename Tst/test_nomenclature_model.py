import pytest
from src.core.exception import arguments_exception
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model


def test_nomenclature_model_successful_creation():
    """
    Проверка корректной инициализации объекта номенклатуры со всеми заполненными атрибутами.
    """
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")

    item = nomenclature_model(
        name="Цемент М500",
        full_name="Портландцемент марки М500 Д20 (мешок 50 кг)",
        group=category,
        range=measure_unit
    )

    assert item.name == "Цемент М500"
    assert item.full_name == "Портландцемент марки М500 Д20 (мешок 50 кг)"
    assert item.group is category
    assert item.range is measure_unit


def test_nomenclature_model_full_name_exact_255_length():
    """
    Проверка допустимости граничного значения длины полного наименования (255 символов).
    """
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    boundary_full_name = "К" * 255

    item = nomenclature_model("Цемент М500", boundary_full_name, category, measure_unit)

    assert len(item.full_name) == 255
    assert item.full_name == boundary_full_name


def test_nomenclature_model_full_name_exceeds_limit_raises_exception():
    """
    Проверка выброса исключения arguments_exception при задании полного названия длиннее 255 символов.
    """
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")
    overflow_full_name = "К" * 256

    with pytest.raises(arguments_exception):
        nomenclature_model("Цемент М500", overflow_full_name, category, measure_unit)


def test_nomenclature_model_empty_full_name_raises_exception():
    """
    Проверка передачи пустого значения в качестве полного наименования.
    """
    measure_unit = range_model("килограмм", 1)
    category = nomenclature_group_model("Сухие смеси")

    with pytest.raises(arguments_exception):
        nomenclature_model("Цемент М500", "", category, measure_unit)


def test_nomenclature_model_wrong_group_type_raises_exception():
    """
    Проверка валидации типа данных для поля group (ожидается объект nomenclature_group_model).
    """
    measure_unit = range_model("килограмм", 1)

    with pytest.raises(arguments_exception):
        nomenclature_model("Цемент М500", "Цемент М500 описание", "Сухие смеси", measure_unit)


def test_nomenclature_model_wrong_range_type_raises_exception():
    """
    Проверка валидации типа данных для поля range (ожидается объект range_model).
    """
    category = nomenclature_group_model("Сухие смеси")

    with pytest.raises(arguments_exception):
        nomenclature_model("Цемент М500", "Цемент М500 описание", category, "килограмм")