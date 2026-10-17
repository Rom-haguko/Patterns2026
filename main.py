import io
import flask
import connexion
from src.logics.settings_manager import settings_manager
from src.logics.storage_manager import storage_manager
from src.logics.report_factory import report_factory
from src.dtos.report_type_enum import report_type_enum
from src.dtos.report_result_dto import report_result_dto

api = connexion.FlaskApp(__name__, specification_dir="./")


def _find_entity(entity_type: str, entity_code: str):
    """
    Поиск сущности в хранилище по ее типу и коду (id или наименованию).
    """
    manager = storage_manager()
    type_normalized = entity_type.strip().lower()

    if type_normalized in ("номенклатура", "nomenclature", "nomenclature_model"):
        collection = manager.get(storage_manager.nomenclature_key())
    elif type_normalized in ("единица измерения", "единица_измерения", "range", "range_model", "единица"):
        collection = manager.get(storage_manager.range_key())
    elif type_normalized in ("рецепт", "recipe", "recipe_model"):
        collection = manager.get(storage_manager.recipe_key())
    else:
        return None, "type_not_found"

    item = next((e for e in collection if str(e.id) == entity_code or str(e.name).strip() == entity_code.strip()), None)
    if item is None:
        return None, "entity_not_found"
    return item, None


def _build_http_response(result: report_result_dto, format_type: report_type_enum):
    """
    Формирование HTTP ответа в зависимости от формата отчета.
    Для Markdown и CSV формируются бинарные данные для скачивания файла,
    для остальных форматов — структурированный текст.
    """
    if format_type in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        raw_bytes = bytes(result.binary) if result.binary else result.text.encode("utf-8")
        extension = "csv" if format_type == report_type_enum.CSV else "md"
        mimetype = "text/csv" if format_type == report_type_enum.CSV else "text/markdown"
        return flask.send_file(
            io.BytesIO(raw_bytes),
            mimetype=mimetype,
            as_attachment=True,
            download_name=f"report.{extension}"
        )

    mimetype = "text/plain"
    if format_type == report_type_enum.XML:
        mimetype = "application/xml"
    elif format_type == report_type_enum.HTML:
        mimetype = "text/html"

    return flask.Response(result.text, mimetype=mimetype)


@api.route("/api/get_report", methods=["GET"])
def get_report():
    """
    Формирование текстового отчёта по рецепту (базовый метод).
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    recipe = next((r for r in recipes if "Пицца Маргарита" in r.name), None)

    if recipe is None:
        return {"error": "Рецепт не найден"}, 404

    factory = report_factory()
    report = factory.create(report_type_enum.TXT)
    result = report.build(recipe)
    return result.text


@api.route("/api/report/<format_name>/<entity_type>/<entity_code>", methods=["GET"])
def get_report_by_format(format_name: str, entity_type: str, entity_code: str):
    """
    Формирование отчета в указанном формате для указанного типа сущности и кода.
    """
    entity, error = _find_entity(entity_type, entity_code)
    if error == "type_not_found":
        return {"error": f"Неизвестный тип сущности '{entity_type}'"}, 400
    if error == "entity_not_found":
        return {"error": f"Сущность с кодом '{entity_code}' не найдена"}, 404

    try:
        report_format = report_type_enum.from_string(format_name)
    except Exception:
        return {"error": f"Неподдерживаемый формат отчета '{format_name}'"}, 400

    factory = report_factory()
    report = factory.create(report_format)
    result = report.build(entity)
    return _build_http_response(result, report_format)


@api.route("/api/report/<entity_type>/<entity_code>/<format_name>", methods=["GET"])
def get_report_by_entity_and_format(entity_type: str, entity_code: str, format_name: str):
    """
    Псевдоним маршрута формирования отчета с порядком (тип, код, формат).
    """
    return get_report_by_format(format_name=format_name, entity_type=entity_type, entity_code=entity_code)


@api.route("/api/report/default/<entity_type>/<entity_code>", methods=["GET"])
@api.route("/api/report/<entity_type>/<entity_code>", methods=["GET"])
def get_report_default(entity_type: str, entity_code: str):
    """
    Формирование отчета для указанного типа сущности и кода с использованием create_default.
    """
    entity, error = _find_entity(entity_type, entity_code)
    if error == "type_not_found":
        return {"error": f"Неизвестный тип сущности '{entity_type}'"}, 400
    if error == "entity_not_found":
        return {"error": f"Сущность с кодом '{entity_code}' не найдена"}, 404

    factory = report_factory()
    report = factory.create_default()
    result = report.build(entity)
    return _build_http_response(result, factory.settings.response_format)


@api.route("/api/report", methods=["GET"])
def get_report_by_query():
    """
    Формирование отчета через query-параметры (format, type, code/id).
    """
    format_name = flask.request.args.get("format")
    entity_type = flask.request.args.get("type")
    entity_code = flask.request.args.get("code") or flask.request.args.get("id")

    if not entity_type or not entity_code:
        return {"error": "Параметры 'type' и 'code' (или 'id') обязательны"}, 400

    if format_name:
        return get_report_by_format(format_name=format_name, entity_type=entity_type, entity_code=entity_code)
    return get_report_default(entity_type=entity_type, entity_code=entity_code)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)