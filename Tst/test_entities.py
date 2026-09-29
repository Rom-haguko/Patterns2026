import pytest
from src.core.abstract_model import name_id
from src.core.exception import arguments_exception


class test_entity(name_id):
    """
    <summary>
    Вспомогательный тестовый класс для проверки базовой функциональности абстрактного класса name_id.
    </summary>
    """
    def __init__(self, name: str = None):
        super().__init__(name=name)


def test_abstract_model_get_id_not_null():
    """
    <summary>
    Проверка генерации идентификатора: при создании объекта свойство id не должно быть пустым.
    </summary>
    """
    # Подготовка
    entity = test_entity()

    # Действие
    result = entity.id

    # Проверка
    assert result != ""


def test_abstract_model_id_is_unique():
    """
    <summary>
    Проверка уникальности идентификаторов: два созданных экземпляра должны иметь различные id.
    </summary>
    """
    # Подготовка
    entity1 = test_entity(name="t1")
    entity2 = test_entity(name="t1")

    # Действие
    is_unique = entity1.id != entity2.id

    # Проверка
    assert is_unique


def test_abstract_model_id_is_equal():
    """
    <summary>
    Проверка сравнения сущностей: объекты с одинаковым идентификатором id считаются равными.
    </summary>
    """
    # Подготовка
    entity1 = test_entity(name="t1")
    entity2 = test_entity(name="t2")
    custom_id = "test-uuid-12345"

    # Действие
    entity1.id = custom_id
    entity2.id = custom_id

    # Проверка
    assert entity1 == entity2


def test_abstract_model_invalid_name_raises_error():
    """
    <summary>
    Проверка валидации наименования: передача пустой строки, строки из пробелов или сброс имени вызывают arguments_exception.
    </summary>
    """
    # Подготовка: тестовые некорректные значения
    whitespace_name = "   "
    empty_name = ""

    # Действие & Проверка: инициализация с именем из одних пробелов
    with pytest.raises(arguments_exception):
        test_entity(name=whitespace_name)

    # Действие & Проверка: инициализация с пустым именем
    with pytest.raises(arguments_exception):
        test_entity(name=empty_name)

    # Подготовка: объект с корректным начальным именем
    entity = test_entity(name="Корректное имя")

    # Действие & Проверка: попытка установить пустое имя через сеттер
    with pytest.raises(arguments_exception):
        entity.name = empty_name