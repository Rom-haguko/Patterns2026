from abc import ABC
from src.core.validator import validator, operation_exception, argument_exception


class abstract_manager(ABC):
    """
    Абстрактный базовый класс для реализации загрузки и обработки данных.
    Определяет контракт для менеджеров, работающих с внешними источниками данных.
    """

    # Полный путь к файлу источника данных
    __file_name: str = ""
    # Флаг успешного завершения загрузки и обработки
    __is_loaded: bool = False
    # Сырые загруженные данные (до преобразования)
    __data: list = []

    def load(self, file_name: str = "") -> None:
        """
        Загрузить данные из источника.

        :param file_name: Путь к файлу источника данных.
        """
        pass

    def loaded(self, file_name: str = "") -> None:
        """
        Псевдоним (алиас) для метода load.

        :param file_name: Путь к файлу источника данных.
        """
        return self.load(file_name)

    def convert(self) -> bool:
        """
        Обработать загруженные сырые данные и преобразовать их в доменные объекты.

        :return: True, если преобразование выполнено успешно; иначе False.
        """
        return self.__is_loaded


__all__ = ["abstract_manager", "validator", "operation_exception", "argument_exception"]
