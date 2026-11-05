from src.core.validator import validator


class report_result_dto:
    """
    Модель для хранения результата формирования отчета (DTO).
    Инкапсулирует либо текстовое, либо бинарное представление результата.
    """

    def __init__(self, text: str = "", binary: list = None):
        """
        Инициализирует результат генерации отчета.

        :param text: Текстовые данные отчета
        :param binary: Бинарные данные отчета (список байтов или чисел)
        """
        binary_val = binary if binary is not None else []
        self.__text: str = text if len(binary_val) == 0 else ""
        self.__binary: list = binary_val if len(text.strip()) == 0 else []

    @property
    def text(self) -> str:
        """
        Текстовый результат формирования отчета.
        """
        return self.__text

    @property
    def binary(self) -> list:
        """
        Бинарный результат формирования отчета.
        """
        return self.__binary

    @text.setter
    def text(self, value: str) -> None:
        validator.validate(value, str)
        self.__text = value
        self.__binary = []

    @binary.setter
    def binary(self, value: list) -> None:
        validator.validate(value, list)
        self.__text = ""
        self.__binary = value
