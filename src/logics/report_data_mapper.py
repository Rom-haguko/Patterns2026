from src.dtos.report_data_dto import report_data_dto
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.storage_model import storage_model
from src.models.organization_model import organization_model
from src.models.nomenclature_group_model import nomenclature_group_model


class report_data_mapper:
    """
    Маппер для преобразования доменных моделей в DTO отчетов.
    Реализует разделение ответственности по DDD: доменные модели
    содержат только бизнес-логику, адаптация к отчетам вынесена отдельно.
    
    Использует Registry pattern: регистрация мапперов по типу доменной модели.
    """
    _mappers = {}

    @classmethod
    def register(cls, model_class, mapper_func) -> None:
        """
        Регистрирует функцию-маппер для указанного типа доменной модели.
        """
        cls._mappers[model_class] = mapper_func

    @classmethod
    def to_dto(cls, entity) -> report_data_dto:
        """
        Преобразует доменную модель в DTO отчета, выбирая подходящий маппер.
        """
        if entity is None:
            return report_data_dto(title="Пустой отчет")

        mapper = cls._mappers.get(type(entity))
        if mapper is not None:
            return mapper(entity)
        return cls._default_mapper(entity)

    @classmethod
    def to_collection_dto(cls, entities: list) -> report_data_dto:
        """
        Формирует DTO для коллекции сущностей: общий заголовок, объединенная таблица, итоговый подвал.
        """
        if not entities:
            return report_data_dto(title="Пустой отчет")

        first = entities[0]
        first_dto = cls.to_dto(first)
        all_rows = []
        for item in entities:
            item_dto = cls.to_dto(item)
            all_rows.extend(item_dto.rows)

        return report_data_dto(
            title=f"Список {first.__class__.__name__}",
            headers=first_dto.headers,
            rows=all_rows,
            footer=f"Всего записей: {len(all_rows)}"
        )

    @staticmethod
    def _default_mapper(entity) -> report_data_dto:
        """
        Маппер по умолчанию: используется, если для типа сущности не зарегистрирован специализированный.
        """
        headers = ["Код", "Наименование"]
        rows = [[entity.id, entity.name]]
        return report_data_dto(
            title=entity.name or entity.__class__.__name__,
            headers=headers,
            rows=rows
        )


# ─────────────────────────── Регистрация специализированных мапперов ─────────────

def _map_nomenclature(entity: nomenclature_model) -> report_data_dto:
    headers = ["Код", "Наименование", "Полное наименование", "Группа", "Единица измерения"]
    group_name = entity.group.name if entity.group else ""
    range_name = entity.range.name if entity.range else ""
    rows = [[entity.id, entity.name, entity.full_name, group_name, range_name]]
    return report_data_dto(
        title=f"Номенклатура: {entity.name}",
        headers=headers,
        rows=rows
    )


def _map_range(entity: range_model) -> report_data_dto:
    headers = ["Код", "Наименование", "Коэффициент", "Базовая единица"]
    base_name = entity.base_range.name if entity.base_range else ""
    rows = [[entity.id, entity.name, entity.conversion_factor, base_name]]
    return report_data_dto(
        title=f"Единица измерения: {entity.name}",
        headers=headers,
        rows=rows
    )


def _map_recipe(entity: recipe_model) -> report_data_dto:
    headers = ["Наименование", "Брутто", "Нетто"]
    rows = [[item.nomenclature.name, item.brutto, item.netto] for item in entity.rows]
    return report_data_dto(
        title=f"Рецепт: {entity.name}",
        headers=headers,
        rows=rows,
        footer=f"Итого Брутто: {entity.gross_weight}, Итого Нетто: {entity.net_weight}"
    )


def _map_storage(entity: storage_model) -> report_data_dto:
    headers = ["Код", "Наименование", "Адрес"]
    rows = [[entity.id, entity.name, entity.address]]
    return report_data_dto(
        title=entity.name,
        headers=headers,
        rows=rows
    )


def _map_organization(entity: organization_model) -> report_data_dto:
    headers = ["Код", "Наименование", "ИНН", "БИК", "Счет", "Форма собственности", "Корр. счет"]
    rows = [[entity.id, entity.name, entity.inn, entity.bik, entity.account, entity.ownership_form, entity.corr_account]]
    return report_data_dto(
        title=entity.name,
        headers=headers,
        rows=rows
    )


def _map_nomenclature_group(entity: nomenclature_group_model) -> report_data_dto:
    headers = ["Код", "Наименование"]
    rows = [[entity.id, entity.name]]
    return report_data_dto(
        title=f"Группа номенклатуры: {entity.name}",
        headers=headers,
        rows=rows
    )


# Регистрация всех мапперов при загрузке модуля
report_data_mapper.register(nomenclature_model, _map_nomenclature)
report_data_mapper.register(range_model, _map_range)
report_data_mapper.register(recipe_model, _map_recipe)
report_data_mapper.register(storage_model, _map_storage)
report_data_mapper.register(organization_model, _map_organization)
report_data_mapper.register(nomenclature_group_model, _map_nomenclature_group)