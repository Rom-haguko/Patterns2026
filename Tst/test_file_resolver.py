import os
import pytest
from src.core.file_resolver import file_path_resolver


def test_resolve_returns_absolute_path_if_exists(tmp_path):
    """
    Проверка возврата абсолютного пути к существующему файлу без модификаций.
    """
    # Подготовка
    temp_file = tmp_path / "config.json"
    temp_file.write_text("{}", encoding="utf-8")

    # Действие
    resolved = file_path_resolver.resolve(str(temp_file), __file__)

    # Проверки
    assert resolved == str(temp_file)


def test_resolve_finds_settings_in_project_root():
    """
    Проверка определения пути к файлу settings.json в корне проекта.
    """
    # Подготовка
    target_file = "settings.json"

    # Действие
    resolved = file_path_resolver.resolve(target_file, __file__)

    # Проверки
    assert resolved.endswith("settings.json")
    assert os.path.exists(resolved)


def test_resolve_finds_relative_path_from_nested_caller():
    """
    Проверка корректного резолвинга относительного имени файла при вызове из вложенной директории.
    """
    # Подготовка
    nested_caller = os.path.join(os.path.dirname(__file__), "sub", "caller.py")
    target_file = "settings.json"

    # Действие
    resolved = file_path_resolver.resolve(target_file, nested_caller)

    # Проверки
    assert resolved.endswith("settings.json")
    assert os.path.isabs(resolved)
