import flask
import connexion
from src.logics.storage_manager import storage_manager
from src.logics.report_factory import report_factory
from src.dtos.report_type_enum import report_type_enum

api = connexion.FlaskApp(__name__, specification_dir="./")


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
    return report.to_http_response(result)


@api.route("/api/report/<format_name>/<entity_type>/<entity_code>", methods=["GET"])
def get_report_by_format(format_name: str, entity_type: str, entity_code: str):
    """
    Формирование отчета в указанном формате для указанного типа сущности и кода.
    """
    manager = storage_manager()
    if manager.get_by_type(entity_type) is None:
        return {"error": f"Неизвестный тип сущности '{entity_type}'"}, 400

    entity = manager.get_by_type_and_code(entity_type, entity_code)
    if entity is None:
        return {"error": f"Сущность с кодом '{entity_code}' не найдена"}, 404

    try:
        report_format = report_type_enum.from_string(format_name)
    except Exception:
        return {"error": f"Неподдерживаемый формат отчета '{format_name}'"}, 400

    factory = report_factory()
    report = factory.create(report_format)
    result = report.build(entity)
    return report.to_http_response(result)




@api.route("/api/report/default/<entity_type>/<entity_code>", methods=["GET"])
@api.route("/api/report/<entity_type>/<entity_code>", methods=["GET"])
def get_report_default(entity_type: str, entity_code: str):
    """
    Формирование отчета для указанного типа сущности и кода с использованием create_default.
    """
    manager = storage_manager()
    if manager.get_by_type(entity_type) is None:
        return {"error": f"Неизвестный тип сущности '{entity_type}'"}, 400

    entity = manager.get_by_type_and_code(entity_type, entity_code)
    if entity is None:
        return {"error": f"Сущность с кодом '{entity_code}' не найдена"}, 404

    factory = report_factory()
    report = factory.create_default()
    result = report.build(entity)
    return report.to_http_response(result)


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