import flask
from src.dtos.report_type_enum import report_type_enum
from src.logics.storage_manager import storage_manager
from src.logics.dependency_validator import entity_dependency_validator
from src.logics.handlers.range_handler import range_handler
from src.logics.handlers.group_handler import group_handler
from src.logics.handlers.nomenclature_handler import nomenclature_handler
from src.logics.handlers.storage_handler import storage_handler
from src.logics.handlers.recipe_handler import recipe_handler
from src.logics.handlers.organization_handler import organization_handler
from src.logics.handlers.settings_handler import settings_handler

_storage = storage_manager()
_validator = entity_dependency_validator()

_handlers = {
    "range": range_handler(_storage, _validator),
    "nomenclature-group": group_handler(_storage, _validator),
    "nomenclature": nomenclature_handler(_storage, _validator),
    "storage": storage_handler(_storage, _validator),
    "recipe": recipe_handler(_storage, _validator),
    "organization": organization_handler(_storage, _validator),
    "settings": settings_handler(_storage, _validator),
}


def _body() -> dict:
    """Извлекает JSON-тело запроса без исключений."""
    return flask.request.get_json(force=True, silent=True) or {}


# ---------------------------------------------------------------------------
# Отчёты
# ---------------------------------------------------------------------------

def api_get_report_formats():
    """GET /api/report-formats — список доступных форматов отчётов."""
    return [member.name for member in report_type_enum], 200


# ---------------------------------------------------------------------------
# range
# ---------------------------------------------------------------------------

def get_all_range():
    return _handlers["range"].get_all()


def create_range(**kwargs):
    return _handlers["range"].create(_body())


def get_range_by_id(entity_id: str, **kwargs):
    return _handlers["range"].get_by_id(entity_id)


def update_range(entity_id: str, **kwargs):
    return _handlers["range"].update(entity_id, _body())


def delete_range(entity_id: str, **kwargs):
    return _handlers["range"].delete(entity_id)


# ---------------------------------------------------------------------------
# nomenclature-group
# ---------------------------------------------------------------------------

def get_all_nomenclature_group():
    return _handlers["nomenclature-group"].get_all()


def create_nomenclature_group(**kwargs):
    return _handlers["nomenclature-group"].create(_body())


def get_nomenclature_group_by_id(entity_id: str, **kwargs):
    return _handlers["nomenclature-group"].get_by_id(entity_id)


def update_nomenclature_group(entity_id: str, **kwargs):
    return _handlers["nomenclature-group"].update(entity_id, _body())


def delete_nomenclature_group(entity_id: str, **kwargs):
    return _handlers["nomenclature-group"].delete(entity_id)


# ---------------------------------------------------------------------------
# nomenclature
# ---------------------------------------------------------------------------

def get_all_nomenclature():
    return _handlers["nomenclature"].get_all()


def create_nomenclature(**kwargs):
    return _handlers["nomenclature"].create(_body())


def get_nomenclature_by_id(entity_id: str, **kwargs):
    return _handlers["nomenclature"].get_by_id(entity_id)


def update_nomenclature(entity_id: str, **kwargs):
    return _handlers["nomenclature"].update(entity_id, _body())


def delete_nomenclature(entity_id: str, **kwargs):
    return _handlers["nomenclature"].delete(entity_id)


# ---------------------------------------------------------------------------
# storage
# ---------------------------------------------------------------------------

def get_all_storage():
    return _handlers["storage"].get_all()


def create_storage(**kwargs):
    return _handlers["storage"].create(_body())


def get_storage_by_id(entity_id: str, **kwargs):
    return _handlers["storage"].get_by_id(entity_id)


def update_storage(entity_id: str, **kwargs):
    return _handlers["storage"].update(entity_id, _body())


def delete_storage(entity_id: str, **kwargs):
    return _handlers["storage"].delete(entity_id)


# ---------------------------------------------------------------------------
# recipe
# ---------------------------------------------------------------------------

def get_all_recipe():
    return _handlers["recipe"].get_all()


def create_recipe(**kwargs):
    return _handlers["recipe"].create(_body())


def get_recipe_by_id(entity_id: str, **kwargs):
    return _handlers["recipe"].get_by_id(entity_id)


def update_recipe(entity_id: str, **kwargs):
    return _handlers["recipe"].update(entity_id, _body())


def delete_recipe(entity_id: str, **kwargs):
    return _handlers["recipe"].delete(entity_id)


# ---------------------------------------------------------------------------
# organization
# ---------------------------------------------------------------------------

def get_all_organization():
    return _handlers["organization"].get_all()


def create_organization(**kwargs):
    return _handlers["organization"].create(_body())


def get_organization_by_id(entity_id: str, **kwargs):
    return _handlers["organization"].get_by_id(entity_id)


def update_organization(entity_id: str, **kwargs):
    return _handlers["organization"].update(entity_id, _body())


def delete_organization(entity_id: str, **kwargs):
    return _handlers["organization"].delete(entity_id)


# ---------------------------------------------------------------------------
# settings
# ---------------------------------------------------------------------------

def get_all_settings():
    return _handlers["settings"].get_all()


def create_settings(**kwargs):
    return _handlers["settings"].create(_body())


def get_settings_by_id(entity_id: str, **kwargs):
    return _handlers["settings"].get_by_id(entity_id)


def update_settings(entity_id: str, **kwargs):
    return _handlers["settings"].update(entity_id, _body())


def delete_settings(entity_id: str, **kwargs):
    return _handlers["settings"].delete(entity_id)

