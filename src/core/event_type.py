class event_type:
    """
    Перечень строковых типов событий системы для шаблона Наблюдатель.
    """

    @staticmethod
    def change_settings() -> str:
        """
        Событие изменения параметров настроек.
        """
        return "change_settings"

    @staticmethod
    def load_settings() -> str:
        """
        Событие загрузки параметров настроек.
        """
        return "load_settings"

    @staticmethod
    def crud_create() -> str:
        """
        Событие создания сущности (CRUD).
        """
        return "crud_create"

    @staticmethod
    def crud_update() -> str:
        """
        Событие обновления сущности (CRUD).
        """
        return "crud_update"

    @staticmethod
    def crud_delete() -> str:
        """
        Событие удаления сущности (CRUD).
        """
        return "crud_delete"

    @staticmethod
    def warehouse_turnover() -> str:
        """
        Событие регистрации складского движения.
        """
        return "warehouse_turnover"

    @staticmethod
    def warehouse_osv() -> str:
        """
        Событие формирования оборотно-сальдовой ведомости (складской отчет).
        """
        return "warehouse_osv"

    @staticmethod
    def web_request() -> str:
        """
        Событие вызова Web-метода API.
        """
        return "web_request"

    @staticmethod
    def events() -> dict[str, str]:
        """
        Возвращает словарь всех зарегистрированных типов событий и их описаний.
        """
        result: dict[str, str] = {}
        for attr_name in dir(event_type):
            if attr_name.startswith("_") or attr_name == "events":
                continue
            method = getattr(event_type, attr_name)
            if callable(method):
                doc = method.__doc__.strip().split("\n")[0] if method.__doc__ else attr_name
                result[method()] = doc
        return result
