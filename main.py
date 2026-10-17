from src.logics.settings_manager import settings_manager
from src.logics.storage_manager import storage_manager
from src.logics.report_factory import report_factory
from src.dtos.report_type_enum import report_type_enum
import flask
import connexion

api = connexion.FlaskApp(__name__, specification_dir="./")

@api.route("/api/get_report", methods=["GET"])
def get_report():
    """
    Формирование текстового отчёта по рецепту.
    """
    # Менеджер хранилища (синглтон)
    manager = storage_manager()

    # Список рецептов из кеша
    recipes = manager.get(storage_manager.recipe_key())

    # Поиск рецепта по имени
    recipe = next((r for r in recipes if "Пицца Маргарита" in r.name), None)

    # Обработка отсутствия рецепта
    if recipe is None:
        return {"error": "Рецепт не найден"}, 404

    # Фабрика отчётов
    factory = report_factory()
    report = factory.create(report_type_enum.TXT)

    # Формирование отчёта
    result = report.build(recipe)

    return result.text

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)