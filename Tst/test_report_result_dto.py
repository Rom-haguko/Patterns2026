import pytest
from src.dtos.report_result_dto import report_result_dto
from src.core.exception import arguments_exception


def test_success_create_dto_with_text():
    """
    Проверка создания DTO с текстовым результатом:
    при передаче текста бинарные данные должны быть пустыми.
    """
    # Подготовка
    content = "Привет, мир"

    # Действие
    dto = report_result_dto(text=content)

    # Проверки
    assert dto.text == content
    assert dto.binary == []


def test_success_create_dto_with_binary():
    """
    Проверка создания DTO с бинарным результатом:
    при передаче бинарных данных текст должен быть пустым.
    """
    # Подготовка
    data = [1, 2, 3, 4]

    # Действие
    dto = report_result_dto(binary=data)

    # Проверки
    assert dto.text == ""
    assert dto.binary == data


def test_text_setter_clears_binary():
    """
    Проверка сеттера текста: при установке нового текста
    бинарные данные должны очищаться.
    """
    # Подготовка
    dto = report_result_dto(binary=[1, 2, 3])
    new_text = "Новый текст"

    # Действие
    dto.text = new_text

    # Проверки
    assert dto.text == new_text
    assert dto.binary == []


def test_error_text_setter_with_invalid_type():
    """
    Проверка валидации сеттера текста: при передаче не строки
    должно выбрасываться исключение arguments_exception.
    """
    # Подготовка
    dto = report_result_dto()
    invalid_text = 12345

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        dto.text = invalid_text

    # Проверки
    assert exc_info.value is not None


def test_success_binary_setter_clears_text():
    """
    Проверка сеттера бинарных данных: установка binary должна очищать text.
    """
    # Подготовка
    dto = report_result_dto(text="Тестовый текст")
    new_binary = [1, 2, 3]

    # Действие
    dto.binary = new_binary

    # Проверки
    assert dto.binary == new_binary
    assert dto.text == ""


def test_error_binary_setter_with_invalid_type():
    """
    Проверка валидации сеттера binary: при передаче не списка
    должно выбрасываться исключение arguments_exception.
    """
    # Подготовка
    dto = report_result_dto()
    invalid_binary = "не список"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        dto.binary = invalid_binary

    # Проверки
    assert exc_info.value is not None
