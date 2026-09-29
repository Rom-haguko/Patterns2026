import pytest
from src.core.exception import arguments_exception
from src.models.nomenclature_group_model import nomenclature_group_model


def test_nomenclature_group_creation_success():
    """
    <summary>
    Проверка успешной инициализации категории номенклатуры.
    Проверяется сохранение переданного имени и генерация уникального идентификатора.
    </summary>
    """
    # Подготовка
    category_name = "Бакалея"
    
    # Действие
    group = nomenclature_group_model(category_name)

    # Проверка
    assert group.name == category_name
    assert group.id is not None


def test_nomenclature_group_raises_on_exceeding_name_limit():
    """
    <summary>
    Проверка обработки ошибки при передаче имени длиннее 50 символов.
    Ожидается исключение arguments_exception согласно требованиям к длине наименования.
    </summary>
    """
    # Подготовка
    invalid_name = "Б" * 51

    # Действие & Проверка
    with pytest.raises(arguments_exception) as exc_info:
        nomenclature_group_model(invalid_name)
    
    assert exc_info.value.field in ("name", "")


def test_nomenclature_group_allows_exact_50_chars_name():
    """
    <summary>
    Проверка граничного условия: создание категории с именем ровно в 50 символов.
    </summary>
    """
    # Подготовка
    boundary_name = "В" * 50

    # Действие
    group = nomenclature_group_model(boundary_name)

    # Проверка
    assert group.name == boundary_name
    assert len(group.name) == 50