import pytest
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception


class test_entity(abstract_model):
    """
    Вспомогательный тестовый класс для проверки базовой функциональности абстрактного класса abstract_model.
    """
    def __init__(self, name: str = None):
        super().__init__(name=name)


def test_abstract_model_get_id_not_null():
    """
    Проверка генерации идентификатора: при создании объекта свойство id не должно быть пустым.
    """
    # Подготовка
    entity = test_entity()

    # Действие
    result = entity.id

    # Проверки
    assert result != ""


def test_abstract_model_id_is_unique():
    """
    Проверка уникальности идентификаторов: два созданных экземпляра должны иметь различные id.
    """
    # Подготовка
    entity1 = test_entity(name="t1")
    entity2 = test_entity(name="t1")

    # Действие
    is_unique = entity1.id != entity2.id

    # Проверки
    assert is_unique


def test_abstract_model_id_is_equal():
    """
    Проверка сравнения сущностей: объекты с одинаковым идентификатором id считаются равными.
    """
    # Подготовка
    entity1 = test_entity(name="t1")
    entity2 = test_entity(name="t2")
    custom_id = "test-uuid-12345"

    # Действие
    entity1.id = custom_id
    entity2.id = custom_id

    # Проверки
    assert entity1 == entity2


def test_abstract_model_init_whitespace_name_raises():
    """
    Проверка валидации: передача строки из пробелов при инициализации вызывает arguments_exception.
    """
    # Подготовка
    whitespace_name = "   "

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        test_entity(name=whitespace_name)

    # Проверки
    assert exc_info.value is not None


def test_abstract_model_init_empty_name_raises():
    """
    Проверка валидации: передача пустой строки при инициализации вызывает arguments_exception.
    """
    # Подготовка
    empty_name = ""

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        test_entity(name=empty_name)

    # Проверки
    assert exc_info.value is not None


def test_abstract_model_setter_empty_name_raises():
    """
    Проверка валидации: попытка установить пустое имя через сеттер вызывает arguments_exception.
    """
    # Подготовка
    entity = test_entity(name="Корректное имя")
    empty_name = ""

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        entity.name = empty_name

    # Проверки
    assert exc_info.value is not None
