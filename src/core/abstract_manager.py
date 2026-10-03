from abc import ABC
from src.core.validator import validator, operation_exception, argument_exception


"""
Абстрактный класс для реализации загрузки и обработки данных
"""

class abstract_manager(ABC):
    # полный путь к файлу
    __file_name: str = ""
    # Флаг. Загрузка и обработка завершена успешно
    __is_loaded: bool = False
    # Загружены сырые данные
    __data: list = []

    """
    Загрузить данные
    """
    def load(self, file_name: str = "") -> None:
        pass

    def loaded(self, file_name: str = "") -> None:
        return self.load(file_name)

    """
    Обработать загруженные данные
    """
    def convert(self) -> bool:
        return self.__is_loaded


__all__ = ["abstract_manager", "validator", "operation_exception", "argument_exception"]
