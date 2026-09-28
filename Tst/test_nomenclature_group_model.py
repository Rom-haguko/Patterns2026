import pytest
from src.core.exception import arguments_exception
from src.models.nomenclature_group_model import nomenclature_group_model


def test_nomenclature_group_creation_success():
    """
    Проверка успешной инициализации категории номенклатуры.
    Проверяется сохранение переданного имени и генерация уникального идентификатора.
    """
    category_name = "Бакалея"
    
    group = nomenclature_group_model(category_name)

    assert group.name == category_name
    assert group.id is not None


def test_nomenclature_group_raises_on_exceeding_name_limit():
    """
    Проверка обработки ошибки при пересылке имени длиннее 50 символов.
    Ожидается исключение arguments_exception согласно требованиям к длине наименования.
    """
    invalid_name = "Б" * 51

    with pytest.raises(arguments_exception) as exc_info:
        nomenclature_group_model(invalid_name)
    
    assert exc_info.value.field in ("name", "")


def test_nomenclature_group_allows_exact_50_chars_name():
    """
    Проверка граничного условия: создание категории с именем ровно в 50 символов.
    """
    boundary_name = "В" * 50

    group = nomenclature_group_model(boundary_name)

    assert group.name == boundary_name
    assert len(group.name) == 50