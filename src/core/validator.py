"""
Исключение при проверки аргумента
"""
class argument_exception(Exception):
    pass


"""
Исключение при выполнении бизнес операции
"""
class operation_exception(Exception):
    pass


"""
Набор проверок данных
"""
class validator:

    @staticmethod
    def validate(value, type_=None, len_=None):
        """
        Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object, optional): Ожидаемый тип
            len_ (int, optional): Максимальная длина
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Пустой аргумент
            argument_exception: Некорректная длина аргумента
        Returns:
            bool: True если валидация пройдена
        """
        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа, если передан ожидаемый тип
        if type_ is not None and not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента на непустоту
        if len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            raise argument_exception("Некорректная длина аргумента")

        return True
