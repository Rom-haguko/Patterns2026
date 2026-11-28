from src.core.exception import arguments_exception


class log_entry_dto:
    """
    Типизированный DTO для передачи параметров события в Наблюдатель
    и хранения записи системного журнала.
    """

    def __init__(
        self,
        entity_type: str = "",
        entity_id: str = "",
        message: str = "",
        event: str = "",
        description: str = "",
        timestamp: str = "",
    ) -> None:
        """
        Инициализирует DTO записи журнала событий.

        :param entity_type: Тип сущности или подсистемы.
        :param entity_id: Идентификатор сущности.
        :param message: Описание деталей события.
        :param event: Код события из event_type.
        :param description: Человекочитаемое описание события.
        :param timestamp: Временная метка события.
        """
        self.__timestamp: str = ""
        self.__event: str = ""
        self.__description: str = ""
        self.__entity_type: str = ""
        self.__entity_id: str = ""
        self.__message: str = ""

        self.timestamp = timestamp
        self.event = event
        self.description = description
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = message

    @staticmethod
    def _validate_str(value: object, field: str) -> str:
        """
        Проверяет, что значение является строкой или None, и очищает пробелы.
        """
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        raise arguments_exception(field=field, message=f"Поле '{field}' должно быть строкой")

    @property
    def timestamp(self) -> str:
        """
        Временная метка фиксации события.
        """
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: str) -> None:
        """
        Устанавливает временную метку события.
        """
        self.__timestamp = self._validate_str(value, "timestamp")

    @property
    def event(self) -> str:
        """
        Код системного события.
        """
        return self.__event

    @event.setter
    def event(self, value: str) -> None:
        """
        Устанавливает код системного события.
        """
        self.__event = self._validate_str(value, "event")

    @property
    def description(self) -> str:
        """
        Человекочитаемое описание типа события.
        """
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        """
        Устанавливает описание типа события.
        """
        self.__description = self._validate_str(value, "description")

    @property
    def entity_type(self) -> str:
        """
        Тип сущности или подсистемы-источника.
        """
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: str) -> None:
        """
        Устанавливает тип сущности или подсистемы-источника.
        """
        self.__entity_type = self._validate_str(value, "entity_type")

    @property
    def entity_id(self) -> str:
        """
        Идентификатор сущности.
        """
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value: str) -> None:
        """
        Устанавливает идентификатор сущности.
        """
        self.__entity_id = self._validate_str(value, "entity_id")

    @property
    def message(self) -> str:
        """
        Подробное сообщение о событии.
        """
        return self.__message

    @message.setter
    def message(self, value: str) -> None:
        """
        Устанавливает подробное сообщение о событии.
        """
        self.__message = self._validate_str(value, "message")
