from datetime import datetime
import os
from src.core.abstract_observable import abstract_observable
from src.core.event_type import event_type
from src.core.file_resolver import file_path_resolver
from src.core.validator import validator
from src.dtos.log_entry_dto import log_entry_dto
from src.logics.observer import observer


class log_service(abstract_observable):
    """
    Сервис логирования системных событий на основе шаблона Наблюдатель.
    Подписывается на события через observer и сохраняет типизированные записи
    log_entry_dto в лог-файл и внутренний буфер.
    """

    def __init__(self, log_file_name: str = "logs/app.log", auto_register: bool = True) -> None:
        """
        Инициализирует сервис логирования.

        :param log_file_name: Относительный путь к лог-файлу от корня проекта.
        :param auto_register: Автоматически подписаться на observer при создании.
        """
        validator.validate(log_file_name, str)
        self.__log_file_path: str = file_path_resolver.resolve(log_file_name.strip(), __file__)
        self.__entries: list[log_entry_dto] = []
        self.__descriptions: dict[str, str] = event_type.events()

        log_dir = os.path.dirname(self.__log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        if auto_register:
            observer.add(self)

    @property
    def log_file_path(self) -> str:
        """
        Абсолютный путь к файлу лога.
        """
        return self.__log_file_path

    @property
    def entries(self) -> list[log_entry_dto]:
        """
        Копия списка зафиксированных записей журнала (log_entry_dto).
        """
        return list(self.__entries)

    def clear(self) -> None:
        """
        Очищает внутренний буфер записей лога.
        """
        self.__entries.clear()

    def _build_entry(self, event_types: str, params: object) -> log_entry_dto:
        """
        Формирует типизированный DTO записи журнала из входящего события.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        description = self.__descriptions.get(event_types, event_types)

        if isinstance(params, log_entry_dto):
            return log_entry_dto(
                entity_type=params.entity_type,
                entity_id=params.entity_id,
                message=params.message,
                event=event_types,
                description=params.description or description,
                timestamp=params.timestamp or timestamp,
            )

        message = str(params) if params is not None else ""
        return log_entry_dto(
            message=message,
            event=event_types,
            description=description,
            timestamp=timestamp,
        )

    def _format_entry(self, entry: log_entry_dto) -> str:
        """
        Форматирует DTO записи журнала в строку для вывода в лог-файл.
        """
        target = entry.entity_type
        if entry.entity_id:
            target = f"{target}:{entry.entity_id}" if target else entry.entity_id
        parts = [f"[{entry.timestamp}]", f"[{entry.event}]"]
        if entry.description:
            parts.append(entry.description)
        if target:
            parts.append(f"({target})")
        if entry.message:
            parts.append(f"- {entry.message}")
        return " ".join(parts)

    def handler(self, event_types: str, params: object = None) -> None:
        """
        Обрабатывает событие от observer: формирует log_entry_dto,
        сохраняет его в буфер и записывает отформатированную строку в файл.

        :param event_types: Строковый тип события.
        :param params: Типизированный log_entry_dto или строковые параметры события.
        """
        entry = self._build_entry(event_types, params)
        self.__entries.append(entry)

        with open(self.__log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(self._format_entry(entry) + "\n")
