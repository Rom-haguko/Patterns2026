import flask
import connexion
from src.logics.report_service import report_service

api = connexion.FlaskApp(__name__, specification_dir="./")
service = report_service()


@api.route("/api/get_report", methods=["GET"])
def get_report():
    """
    Формирование текстового отчета по рецепту.
    """
    return service.get_default_recipe_report("Пицца Маргарита")


@api.route("/api/report/<format_name>/<entity_type>/<entity_code>", methods=["GET"])
def get_report_by_format(format_name: str, entity_type: str, entity_code: str):
    """
    Формирование отчета в указанном формате для сущности.
    """
    return service.get_report_response(entity_type, entity_code, format_name)


@api.route("/api/report/default/<entity_type>/<entity_code>", methods=["GET"])
@api.route("/api/report/<entity_type>/<entity_code>", methods=["GET"])
def get_report_default(entity_type: str, entity_code: str):
    """
    Формирование отчета по умолчанию для сущности.
    """
    return service.get_report_response(entity_type, entity_code, None)


@api.route("/api/report", methods=["GET"])
def get_report_by_query():
    """
    Формирование отчета через параметры запроса.
    """
    format_name = flask.request.args.get("format")
    entity_type = flask.request.args.get("type")
    entity_code = flask.request.args.get("code") or flask.request.args.get("id")

    if not entity_type or not entity_code:
        return {"error": "Параметры 'type' и 'code' (или 'id') обязательны"}, 400

    return service.get_report_response(entity_type, entity_code, format_name)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)
