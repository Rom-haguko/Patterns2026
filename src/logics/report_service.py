from src.logics.storage_manager import storage_manager
from src.logics.report_factory import report_factory
from src.dtos.report_type_enum import report_type_enum


class report_service:
    """
    Сервис формирования отчетов для API.
    Инкапсулирует работу с хранилищем, фабрикой отчетов и форматами.
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

    def build_report(self, entity, report_format=None):
        """
        Строит отчет по сущности в указанном формате или формате по умолчанию.
        """
        if report_format is not None:
            if isinstance(report_format, str):
                report_format = report_type_enum.from_string(report_format)
            report = self.__factory.create(report_format)
        else:
            report = self.__factory.create_default()

        result = report.build(entity)
        return report.to_http_response(result)

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

    def get_default_recipe_report(self, name_part: str = "Пицца Маргарита"):
        """
        Формирует базовый текстовый отчет по рецепту.
        """
        recipe = self.get_recipe_by_name(name_part)
        if recipe is None:
            return {"error": "Рецепт не найден"}, 404

        return self.build_report(recipe, report_type_enum.TXT)
