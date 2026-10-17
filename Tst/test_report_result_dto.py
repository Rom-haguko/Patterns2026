import pytest
from src.dtos.report_result_dto import report_result_dto
from src.core.exception import arguments_exception

# ─────────────────────────── Тесты создания report_result_dto ─────────────────────

def test_success_create_dto_with_text():
    """
    <summary>
    Проверка создания DTO с текстовым результатом:
    при передаче текста бинарные данные должны быть пустыми.
    </summary>
    """
    # Подготовка & Действие
    dto = report_result_dto(text="Привет, мир")

    # Проверка
    assert dto.text == "Привет, мир"
    assert dto.binary == []

def test_success_create_dto_with_binary():
    """
    <summary>
    Проверка создания DTO с бинарным результатом:
    при передаче бинарных данных текст должен быть пустым.
    </summary>
    """
    # Подготовка & Действие
    dto = report_result_dto(binary=[1, 2, 3, 4])

    # Проверка
    assert dto.text == ""
    assert dto.binary == [1, 2, 3, 4]

# ─────────────────────────── Тесты сеттеров report_result_dto ─────────────────────

def test_text_setter_clears_binary():
    """
    <summary>
    Проверка сеттера текста: при установке нового текста
    бинарные данные должны очищаться.
    </summary>
    """
    # Подготовка
    dto = report_result_dto(binary=[1, 2, 3])

    # Действие
    dto.text = "Новый текст"

    # Проверка
    assert dto.text == "Новый текст"
    assert dto.binary == []

def test_error_text_setter_with_invalid_type():
    """
    <summary>
    Проверка валидации сеттера текста: при передаче не строки
    должно выбрасываться исключение.
    </summary>
    """
    # Подготовка
    dto = report_result_dto()

    # Действие & Проверка
    with pytest.raises(Exception):
        dto.text = 12345