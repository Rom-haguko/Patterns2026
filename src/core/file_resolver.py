import os

class FilePathResolver:
    """
    Утилита для резолвинга (поиска) путей к конфигурационным файлам проекта.
    Помогает находить файлы даже при запуске из разных директорий и обрабатывает опечатки.
    """
    
    @staticmethod
    def resolve(file_name: str, current_file: str) -> str:
        """
        Определяет корректный путь к файлу относительно корня проекта.
        
        :param file_name: Имя или относительный путь к файлу (например, "settings.json").
        :param current_file: Абсолютный путь к файлу, из которого вызван метод (__file__).
        :return: Абсолютный путь к файлу.
        """
        # Если передан существующий абсолютный путь
        if os.path.isabs(file_name) and os.path.exists(file_name):
            return file_name
            
        current_dir = os.path.dirname(os.path.abspath(current_file))
        
        # Поиск корня проекта по наличию ключевых директорий
        while True:
            if os.path.exists(os.path.join(current_dir, "src")) and os.path.exists(os.path.join(current_dir, "Tst")):
                break
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                break
            current_dir = parent
            
        # Поиск файла в корне проекта
        candidate = os.path.join(current_dir, file_name)
        if os.path.exists(candidate):
            return candidate
            
        # Проверка альтернативных вариантов наименования
        known_typos_map = {
            "seetings.json": "settings.json",
            "settings.json": "seetings.json"
        }
        
        if file_name in known_typos_map:
            alt_path = os.path.join(current_dir, known_typos_map[file_name])
            if os.path.exists(alt_path):
                return alt_path
                
        return candidate