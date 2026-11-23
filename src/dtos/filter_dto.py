from src.core.exception import arguments_exception
from src.dtos.filter_type_enum import filter_type_enum


class filter_dto:
    """
    DTO модель данных для фильтрации доменных объектов и формирования ведомостей.
    Содержит критерии поиска по наименованию и уникальному коду (id) с типами сравнения.
    """

    def __init__(
        self,
        name: str = "",
        name_filter_type: filter_type_enum = filter_type_enum.LIKE,
        id: str = "",
        id_filter_type: filter_type_enum = filter_type_enum.EQUALS,
    ) -> None:
        """
        Инициализирует параметры фильтрации.

        :param name: Искомое наименование или подстрока
        :param name_filter_type: Тип сравнения для наименования (EQUALS, LIKE)
        :param id: Искомый уникальный код (id) или подстрока
        :param id_filter_type: Тип сравнения для уникального кода (EQUALS, LIKE)
        """
        self.__name: str = ""
        self.__name_filter_type: filter_type_enum = filter_type_enum.LIKE
        self.__id: str = ""
        self.__id_filter_type: filter_type_enum = filter_type_enum.EQUALS

        self.name = name
        self.name_filter_type = name_filter_type
        self.id = id
        self.id_filter_type = id_filter_type

    @property
    def name(self) -> str:
        """
        Искомое наименование объекта.
        """
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает строковое значение наименования для фильтрации.
        """
        if value is None:
            self.__name = ""
        elif isinstance(value, str):
            self.__name = value.strip()
        else:
            raise arguments_exception("name", "Наименование для фильтрации должно быть строкой")

    @property
    def name_filter_type(self) -> filter_type_enum:
        """
        Тип фильтрации для поля наименования.
        """
        return self.__name_filter_type

    @name_filter_type.setter
    def name_filter_type(self, value: object) -> None:
        """
        Устанавливает тип фильтрации для наименования.
        """
        self.__name_filter_type = filter_type_enum.from_string(value)

    @property
    def id(self) -> str:
        """
        Искомый уникальный идентификатор (id) объекта.
        """
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """
        Устанавливает идентификатор для фильтрации.
        """
        if value is None:
            self.__id = ""
        elif isinstance(value, str):
            self.__id = value.strip()
        else:
            raise arguments_exception("id", "Идентификатор для фильтрации должен быть строкой")

    @property
    def id_filter_type(self) -> filter_type_enum:
        """
        Тип фильтрации для поля уникального кода (id).
        """
        return self.__id_filter_type

    @id_filter_type.setter
    def id_filter_type(self, value: object) -> None:
        """
        Устанавливает тип фильтрации для идентификатора.
        """
        self.__id_filter_type = filter_type_enum.from_string(value)

    @property
    def is_empty(self) -> bool:
        """
        Возвращает True, если ни один критерий фильтрации не задан.
        """
        return not bool(self.__name) and not bool(self.__id)

    @staticmethod
    def create(
        name: str = "",
        name_filter_type: object = filter_type_enum.LIKE,
        id: str = "",
        id_filter_type: object = filter_type_enum.EQUALS,
    ) -> "filter_dto":
        """
        Фабричный метод создания DTO фильтрации.
        """
        return filter_dto(
            name=name,
            name_filter_type=filter_type_enum.from_string(name_filter_type),
            id=id,
            id_filter_type=filter_type_enum.from_string(id_filter_type),
        )
