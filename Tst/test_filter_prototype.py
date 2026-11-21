import pytest
from src.core.exception import arguments_exception
from src.dtos.filter_type_enum import filter_type_enum
from src.dtos.filter_dto import filter_dto
from src.logics.filter_deserializer import filter_deserializer
from src.logics.prototype_filter import prototype_filter
from src.models.range_model import range_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.storage_model import storage_model


def test_filter_type_enum_from_string_success():
    # Подготовка
    raw_equals = "EQUALS"
    raw_like = "like"
    raw_int = 1

    # Действие
    enum_equals = filter_type_enum.from_string(raw_equals)
    enum_like = filter_type_enum.from_string(raw_like)
    enum_from_int = filter_type_enum.from_string(raw_int)

    # Проверки
    assert enum_equals == filter_type_enum.EQUALS
    assert enum_like == filter_type_enum.LIKE
    assert enum_from_int == filter_type_enum.EQUALS


def test_filter_type_enum_from_string_invalid():
    # Подготовка
    invalid_value = "UNKNOWN_FILTER"

    # Действие
    def action():
        filter_type_enum.from_string(invalid_value)

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_filter_dto_properties_and_validation():
    # Подготовка
    name_val = "Тест"
    id_val = "12345"

    # Действие
    dto = filter_dto.create(
        name=name_val,
        name_filter_type=filter_type_enum.EQUALS,
        id=id_val,
        id_filter_type=filter_type_enum.LIKE,
    )

    # Проверки
    assert dto.name == name_val
    assert dto.name_filter_type == filter_type_enum.EQUALS
    assert dto.id == id_val
    assert dto.id_filter_type == filter_type_enum.LIKE
    assert dto.is_empty is False


def test_filter_deserializer_success():
    # Подготовка
    raw_dict = {
        "name": "Мука",
        "name_filter_type": "LIKE",
        "id": "111",
        "id_filter_type": "EQUALS",
    }
    deserializer = filter_deserializer()

    # Действие
    dto = deserializer.deserialize(raw_dict)

    # Проверки
    assert isinstance(dto, filter_dto)
    assert dto.name == "Мука"
    assert dto.name_filter_type == filter_type_enum.LIKE
    assert dto.id == "111"
    assert dto.id_filter_type == filter_type_enum.EQUALS


def test_filter_deserializer_invalid_data():
    # Подготовка
    deserializer = filter_deserializer()

    # Действие
    def action():
        deserializer.deserialize(["не", "словарь"])

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_prototype_clone_and_empty_filter():
    # Подготовка
    gram = range_model.create_gram()
    kg = range_model.create_kilogram()
    prototype = prototype_filter([gram, kg])

    # Действие
    cloned = prototype.clone()
    filtered_empty = prototype.create(filter_dto())

    # Проверки
    assert len(cloned.data) == 2
    assert len(filtered_empty.data) == 2
    assert cloned is not prototype
    assert filtered_empty is not prototype


def test_prototype_filter_equals_and_like():
    # Подготовка
    item1 = storage_model.create("Основной склад", "Адрес 1")
    item2 = storage_model.create("Склад готовой продукции", "Адрес 2")
    prototype = prototype_filter([item1, item2])

    filter_equals = filter_dto(name="Основной склад", name_filter_type=filter_type_enum.EQUALS)
    filter_like = filter_dto(name="склад", name_filter_type=filter_type_enum.LIKE)
    filter_none = filter_dto(name="Архив", name_filter_type=filter_type_enum.EQUALS)

    # Действие
    res_equals = prototype.create(filter_equals).data
    res_like = prototype.create(filter_like).data
    res_none = prototype.create(filter_none).data

    # Проверки
    assert len(res_equals) == 1
    assert res_equals[0] == item1
    assert len(res_like) == 2
    assert len(res_none) == 0


def test_prototype_filter_by_id():
    # Подготовка
    group = nomenclature_group_model.create("Сырьё")
    prototype = prototype_filter([group])
    group_id = group.id

    filter_id = filter_dto(id=group_id, id_filter_type=filter_type_enum.EQUALS)
    filter_id_wrong = filter_dto(id="non-existent-id", id_filter_type=filter_type_enum.EQUALS)

    # Действие
    res_found = prototype.create(filter_id).data
    res_empty = prototype.create(filter_id_wrong).data

    # Проверки
    assert len(res_found) == 1
    assert res_found[0] == group
    assert len(res_empty) == 0


def test_prototype_nested_search_range_base_range():
    # Подготовка
    gram = range_model.create_gram()
    kg = range_model.create_kilogram()  # base_range = gram
    prototype = prototype_filter([kg])

    # Фильтруем кг по имени его базовой единицы "грамм"
    filter_base = filter_dto(name="грамм", name_filter_type=filter_type_enum.EQUALS)

    # Действие
    res = prototype.create(filter_base).data

    # Проверки
    assert len(res) == 1
    assert res[0] == kg


def test_prototype_nested_search_nomenclature_group():
    # Подготовка
    raw_group = nomenclature_group_model.create("Сырьё")
    gram = range_model.create_gram()
    flour = nomenclature_model.create("Мука", "Мука в/с", raw_group, gram)
    prototype = prototype_filter([flour])

    # Ищем номенклатуру по имени вложенной группы "Сырьё"
    filter_by_group = filter_dto(name="Сырьё", name_filter_type=filter_type_enum.EQUALS)

    # Действие
    res = prototype.create(filter_by_group).data

    # Проверки
    assert len(res) == 1
    assert res[0] == flour


def test_prototype_nested_search_recipe_ingredients():
    # Подготовка
    raw_group = nomenclature_group_model.create("Сырьё")
    gram = range_model.create_gram()
    flour = nomenclature_model.create("Мука", "Мука в/с", raw_group, gram)
    row = recipe_row_model.create(flour, 100.0, 100.0, gram)
    recipe = recipe_model.create(name="Пирог", rows=[row])
    prototype = prototype_filter([recipe])

    # Ищем рецепт по наименованию входящего ингредиента "Мука"
    filter_by_ingredient = filter_dto(name="Мука", name_filter_type=filter_type_enum.EQUALS)

    # Действие
    res = prototype.create(filter_by_ingredient).data

    # Проверки
    assert len(res) == 1
    assert res[0] == recipe
