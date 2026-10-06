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
        # 1. Если передан абсолютный путь и файл существует - возвращаем его
        if os.path.isabs(file_name) and os.path.exists(file_name):
            return file_name
            
        current_dir = os.path.dirname(os.path.abspath(current_file))
        
        # 2. Умный поиск корня проекта: поднимаемся вверх по дереву папок,
        # пока не найдем директорию, содержащую папки 'src' и 'Tst'.
        while True:
            if os.path.exists(os.path.join(current_dir, "src")) and os.path.exists(os.path.join(current_dir, "Tst")):
                break
            parent = os.path.dirname(current_dir)
            if parent == current_dir:  # Достигли корня диска
                break
            current_dir = parent
            
        # 3. Пытаемся найти файл по точному имени в корне проекта
        candidate = os.path.join(current_dir, file_name)
        if os.path.exists(candidate):
            return candidate
            
        # 4. Фолбэк (защита от опечаток в названии, например seetings.json)
        known_typos_map = {
            "seetings.json": "settings.json",
            "settings.json": "seetings.json"
        }
        
        if file_name in known_typos_map:
            alt_path = os.path.join(current_dir, known_typos_map[file_name])
            if os.path.exists(alt_path):
                return alt_path
                
        # Если ничего не нашли, возвращаем исходное имя.
        # Метод open() сам выбросит FileNotFoundError, который settings_manager перехватит.
        return candidate