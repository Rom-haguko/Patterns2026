import io
import flask
from src.logics.storage_manager import storage_manager
from src.logics.report_factory import report_factory
from src.dtos.report_type_enum import report_type_enum
from src.dtos.report_result_dto import report_result_dto


class report_service:
    """
    Сервис формирования отчетов для API.
    Инкапсулирует работу с хранилищем, фабрикой отчетов и генерацией HTTP-ответов.
    """

    def __init__(self, storage=None, factory=None):
        self.__storage = storage if storage is not None else storage_manager()
        self.__factory = factory if factory is not None else report_factory()

    def get_recipe_by_name(self, name_part: str):
        """
        Ищет рецепт в хранилище по части наименования.
        """
        recipes = self.__storage.get(storage_manager.recipe_key())
        return next((r for r in recipes if name_part in r.name), None)

    def get_entity(self, entity_type: str, entity_code: str):
        """
        Ищет сущность в хранилище по типу и коду.
        """
        return self.__storage.get_by_type_and_code(entity_type, entity_code)

    def to_http_response(self, report, result: report_result_dto):
        """
        Формирует HTTP-ответ веб-фреймворка Flask на основе сгенерированного отчета.
        """
        if report.is_binary:
            raw_bytes = bytes(result.binary) if result.binary else result.text.encode("utf-8")
            return flask.send_file(
                io.BytesIO(raw_bytes),
                mimetype=report.mimetype,
                as_attachment=True,
                download_name=f"report.{report.file_extension}"
            )
        return flask.Response(result.text, mimetype=report.mimetype)

    def build_report(self, entity, report_format=None):
        """
        Строит отчет по сущности в указанном формате или формате по умолчанию.
        """
        if report_format is not None:
            if isinstance(report_format, str):
                report_format = report_type_enum.from_string(report_format)
            report = self.__factory.create(report_format)
        else:
            report = self.__factory.create()

        result = report.build(entity)
        return self.to_http_response(report, result)

    def get_report_response(self, entity_type: str, entity_code: str, format_name: str = None):
        """
        Формирует HTTP-ответ с отчетом по типу сущности, ее коду и формату.
        """
        if self.__storage.get_by_type(entity_type) is None:
            return {"error": f"Неизвестный тип сущности '{entity_type}'"}, 400

        entity = self.get_entity(entity_type, entity_code)
        if entity is None:
            return {"error": f"Сущность с кодом '{entity_code}' не найдена"}, 404

        if format_name:
            try:
                report_format = report_type_enum.from_string(format_name)
            except Exception:
                return {"error": f"Неподдерживаемый формат отчета '{format_name}'"}, 400
        else:
            report_format = None

        return self.build_report(entity, report_format)

    def get_default_recipe_report(self, recipe_name: str = "Пицца Маргарита"):
        """
        Формирует отчет для заданного рецепта по умолчанию.
        """
        recipe = self.get_recipe_by_name(recipe_name)
        if recipe is None:
            return {"error": f"Рецепт '{recipe_name}' не найден"}, 404

        return self.build_report(recipe, report_type_enum.TXT)
