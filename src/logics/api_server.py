import flask
from src.dtos.report_type_enum import report_type_enum
from src.logics.storage_manager import storage_manager
from src.logics.dependency_validator import entity_dependency_validator
from src.logics.deserializer_factory import deserializer_factory
from src.logics.report_service import report_service
from src.logics.handlers.range_handler import range_handler
from src.logics.handlers.group_handler import group_handler
from src.logics.handlers.nomenclature_handler import nomenclature_handler
from src.logics.handlers.storage_handler import storage_handler
from src.logics.handlers.recipe_handler import recipe_handler
from src.logics.handlers.organization_handler import organization_handler
from src.logics.handlers.settings_handler import settings_handler


class api_server:
    """
    ООП-сервер API.
    Инкапсулирует инициализацию хранилища, валидатора зависимостей,
    десериализатора и специализированных хендлеров доменных сущностей.
    """

    _storage: storage_manager = None
    _validator: entity_dependency_validator = None
    _deserializer: deserializer_factory = None
    _report_service: report_service = None
    _handlers: dict = {}

    @classmethod
    def initialize(cls) -> None:
        """
        Инициализация зависимостей и реестра обработчиков сущностей.
        """
        if cls._storage is None:
            cls._storage = storage_manager()
        if cls._validator is None:
            cls._validator = entity_dependency_validator()
        if cls._deserializer is None:
            cls._deserializer = deserializer_factory()
        if cls._report_service is None:
            cls._report_service = report_service(cls._storage)

        cls._handlers = {
            "range": range_handler(cls._storage, cls._validator, cls._deserializer),
            "nomenclature-group": group_handler(cls._storage, cls._validator, cls._deserializer),
            "nomenclature": nomenclature_handler(cls._storage, cls._validator, cls._deserializer),
            "storage": storage_handler(cls._storage, cls._validator, cls._deserializer),
            "recipe": recipe_handler(cls._storage, cls._validator, cls._deserializer),
            "organization": organization_handler(cls._storage, cls._validator, cls._deserializer),
            "settings": settings_handler(cls._storage, cls._validator, cls._deserializer),
        }

    @classmethod
    def get_report_service(cls) -> report_service:
        """
        Возвращает инициализированный сервис отчетов.
        """
        if cls._report_service is None:
            cls.initialize()
        return cls._report_service

    @classmethod
    def get_handler(cls, key: str):
        """
        Возвращает зарегистрированный обработчик по ключу сущности.
        """
        if not cls._handlers:
            cls.initialize()
        return cls._handlers[key]

    @staticmethod
    def _body() -> dict:
        """
        Извлекает JSON-тело входящего запроса.
        """
        return flask.request.get_json(force=True, silent=True) or {}

    # ---------------------------------------------------------------------------
    # Отчёты
    # ---------------------------------------------------------------------------

    @classmethod
    def api_get_report_formats(cls):
        """GET /api/report-formats — список доступных форматов отчётов."""
        return [member.name for member in report_type_enum], 200

    @classmethod
    def get_default_report(cls, **kwargs):
        """GET /api/get_report — формирование текстового отчета по умолчанию."""
        return cls.get_report_service().get_default_recipe_report("Пицца Маргарита")

    @classmethod
    def get_report_by_query(cls, **kwargs):
        """GET /api/report — формирование отчета через параметры строки запроса."""
        format_name = flask.request.args.get("format")
        entity_type = flask.request.args.get("type")
        entity_code = flask.request.args.get("code")

        if not entity_type or not entity_code:
            return {"error": "Параметры 'type' и 'code' обязательны"}, 400

        return cls.get_report_service().get_report_response(entity_type, entity_code, format_name)

    @classmethod
    def get_report_default(cls, entity_type: str, entity_code: str, **kwargs):
        """GET /api/report/default/{entity_type}/{entity_code} — формирование отчета по умолчанию."""
        return cls.get_report_service().get_report_response(entity_type, entity_code, None)

    @classmethod
    def get_report_by_entity(cls, entity_type: str, entity_code: str, **kwargs):
        """GET /api/report/{entity_type}/{entity_code} — формирование отчета по умолчанию для сущности."""
        return cls.get_report_service().get_report_response(entity_type, entity_code, None)

    @classmethod
    def get_report_by_format(cls, format_name: str, entity_type: str, entity_code: str, **kwargs):
        """GET /api/report/{format_name}/{entity_type}/{entity_code} — формирование отчета в формате."""
        return cls.get_report_service().get_report_response(entity_type, entity_code, format_name)

    # ---------------------------------------------------------------------------
    # range
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_range(cls):
        return cls.get_handler("range").get_all()

    @classmethod
    def create_range(cls, **kwargs):
        return cls.get_handler("range").create(cls._body())

    @classmethod
    def get_range_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("range").get_by_id(entity_id)

    @classmethod
    def update_range(cls, entity_id: str, **kwargs):
        return cls.get_handler("range").update(entity_id, cls._body())

    @classmethod
    def delete_range(cls, entity_id: str, **kwargs):
        return cls.get_handler("range").delete(entity_id)

    # ---------------------------------------------------------------------------
    # nomenclature-group
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_nomenclature_group(cls):
        return cls.get_handler("nomenclature-group").get_all()

    @classmethod
    def create_nomenclature_group(cls, **kwargs):
        return cls.get_handler("nomenclature-group").create(cls._body())

    @classmethod
    def get_nomenclature_group_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature-group").get_by_id(entity_id)

    @classmethod
    def update_nomenclature_group(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature-group").update(entity_id, cls._body())

    @classmethod
    def delete_nomenclature_group(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature-group").delete(entity_id)

    # ---------------------------------------------------------------------------
    # nomenclature
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_nomenclature(cls):
        return cls.get_handler("nomenclature").get_all()

    @classmethod
    def create_nomenclature(cls, **kwargs):
        return cls.get_handler("nomenclature").create(cls._body())

    @classmethod
    def get_nomenclature_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature").get_by_id(entity_id)

    @classmethod
    def update_nomenclature(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature").update(entity_id, cls._body())

    @classmethod
    def delete_nomenclature(cls, entity_id: str, **kwargs):
        return cls.get_handler("nomenclature").delete(entity_id)

    # ---------------------------------------------------------------------------
    # storage
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_storage(cls):
        return cls.get_handler("storage").get_all()

    @classmethod
    def create_storage(cls, **kwargs):
        return cls.get_handler("storage").create(cls._body())

    @classmethod
    def get_storage_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("storage").get_by_id(entity_id)

    @classmethod
    def update_storage(cls, entity_id: str, **kwargs):
        return cls.get_handler("storage").update(entity_id, cls._body())

    @classmethod
    def delete_storage(cls, entity_id: str, **kwargs):
        return cls.get_handler("storage").delete(entity_id)

    # ---------------------------------------------------------------------------
    # recipe
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_recipe(cls):
        return cls.get_handler("recipe").get_all()

    @classmethod
    def create_recipe(cls, **kwargs):
        return cls.get_handler("recipe").create(cls._body())

    @classmethod
    def get_recipe_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("recipe").get_by_id(entity_id)

    @classmethod
    def update_recipe(cls, entity_id: str, **kwargs):
        return cls.get_handler("recipe").update(entity_id, cls._body())

    @classmethod
    def delete_recipe(cls, entity_id: str, **kwargs):
        return cls.get_handler("recipe").delete(entity_id)

    # ---------------------------------------------------------------------------
    # organization
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_organization(cls):
        return cls.get_handler("organization").get_all()

    @classmethod
    def create_organization(cls, **kwargs):
        return cls.get_handler("organization").create(cls._body())

    @classmethod
    def get_organization_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("organization").get_by_id(entity_id)

    @classmethod
    def update_organization(cls, entity_id: str, **kwargs):
        return cls.get_handler("organization").update(entity_id, cls._body())

    @classmethod
    def delete_organization(cls, entity_id: str, **kwargs):
        return cls.get_handler("organization").delete(entity_id)

    # ---------------------------------------------------------------------------
    # settings
    # ---------------------------------------------------------------------------

    @classmethod
    def get_all_settings(cls):
        return cls.get_handler("settings").get_all()

    @classmethod
    def create_settings(cls, **kwargs):
        return cls.get_handler("settings").create(cls._body())

    @classmethod
    def get_settings_by_id(cls, entity_id: str, **kwargs):
        return cls.get_handler("settings").get_by_id(entity_id)

    @classmethod
    def update_settings(cls, entity_id: str, **kwargs):
        return cls.get_handler("settings").update(entity_id, cls._body())

    @classmethod
    def delete_settings(cls, entity_id: str, **kwargs):
        return cls.get_handler("settings").delete(entity_id)


api_server.initialize()
