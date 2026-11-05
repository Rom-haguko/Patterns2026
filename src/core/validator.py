from src.core.exception import arguments_exception, operation_exception


class validator:
    """
    Утилитный класс для валидации аргументов и типов данных.
    """

    @staticmethod
    def validate(value, type_=None, len_=None):
        """
        Валидация аргумента по типу и длине.

        :param value: Значение аргумента
        :param type_: Ожидаемый тип (опционально)
        :param len_: Максимальная допустимая длина (опционально)
        :raises arguments_exception: При несоответствии типа или длины
        :return: True, если валидация пройдена
        """
        if value is None:
            raise arguments_exception("value", "Пустой аргумент")

        if type_ is not None and not isinstance(value, type_):
            raise arguments_exception("value", f"Некорректный тип! Ожидается {type_}. Текущий тип {type(value)}")

        str_val = str(value).strip()
        if len(str_val) == 0:
            raise arguments_exception("value", "Пустой аргумент")

        if len_ is not None and len(str_val) > len_:
            raise arguments_exception("value", "Некорректная длина аргумента")

        return True
