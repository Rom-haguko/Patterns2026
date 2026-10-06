import pytest
import os
from src.core.file_resolver import FilePathResolver

def test_resolve_returns_absolute_path_if_exists(tmp_path):
    """Проверка: если передан абсолютный путь к существующему файлу, он возвращается без изменений."""
    temp_file = tmp_path / "config.json"
    temp_file.write_text("{}")
    
    resolved = FilePathResolver.resolve(str(temp_file), __file__)
    assert resolved == str(temp_file)

def test_resolve_finds_settings_in_project_root():
    """Проверка: резолвер находит settings.json в корне проекта."""
    resolved = FilePathResolver.resolve("settings.json", __file__)
    
    # Путь должен заканчиваться на settings.json
    assert resolved.endswith("settings.json")
    # И файл должен существовать
    assert os.path.exists(resolved)

def test_resolve_handles_typo_seetings():
    """Проверка: если мы просим 'seetings.json', резолвер должен найти 'settings.json'."""
    resolved = FilePathResolver.resolve("seetings.json", __file__)
    
    # Он должен был подменить имя и найти реальный файл
    assert resolved.endswith("settings.json")
    assert os.path.exists(resolved)