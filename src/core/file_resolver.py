import os


class file_path_resolver:
    """
    Утилита для определения абсолютных путей к конфигурационным файлам проекта.
    """

    @staticmethod
    def resolve(file_name: str, current_file: str) -> str:
        """
        Определяет корректный абсолютный путь к файлу относительно корня проекта.

        :param file_name: Имя или относительный путь к файлу.
        :param current_file: Абсолютный путь к файлу, инициирующему вызов (__file__).
        :return: Абсолютный путь к файлу.
        """
        if os.path.isabs(file_name) and os.path.exists(file_name):
            return file_name

        current_dir = os.path.dirname(os.path.abspath(current_file))

        while True:
            has_src = os.path.exists(os.path.join(current_dir, "src")) or os.path.exists(os.path.join(current_dir, "Src"))
            has_markers = (
                os.path.exists(os.path.join(current_dir, "Tst"))
                or os.path.exists(os.path.join(current_dir, "pytest.ini"))
                or os.path.exists(os.path.join(current_dir, "main.py"))
            )
            if has_src and has_markers:
                break
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                break
            current_dir = parent

        candidate = os.path.join(current_dir, file_name)
        return candidate
