from abc import ABC
from src.core.exception import arguments_exception, operation_exception
from src.core.validator import validator


class abstract_manager(ABC):
    """
    Абстрактный базовый класс для реализации загрузки и обработки данных.
    Определяет контракт для менеджеров, работающих с внешними источниками данных.
    """

    __file_name: str = ""
    __is_loaded: bool = False
    __data: list = []

    def load(self, file_name: str = "") -> None:
        """
        Загрузить данные из источника.

        :param file_name: Путь к файлу источника данных.
        """
        pass

    def convert(self) -> bool:
        """
        Обработать загруженные сырые данные и преобразовать их в доменные объекты.

        :return: True, если преобразование выполнено успешно; иначе False.
        """
        return self.__is_loaded


__all__ = ["abstract_manager"]
