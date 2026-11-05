from src.logics.report_data_mapper import report_data_mapper
from src.core.abstract_model import abstract_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model
from src.models.organization_model import organization_model
from src.models.nomenclature_group_model import nomenclature_group_model


class test_model(abstract_model):
    """
    Тестовая сущность для проверки абстрактного маппера данных.
    """
    def __init__(self, name: str = None):
        super().__init__(name=name)


def test_report_data_mapper_build_title():
    """
    Проверка формирования заголовка отчета методом _build_title.
    """
    # Подготовка
    entity = test_model(name="Тестовая сущность")

    # Действие
    title = report_data_mapper._build_title(entity)

    # Проверки
    assert title == "Тестовая сущность"


def test_report_data_mapper_build_table():
    """
    Проверка формирования таблицы отчета методом _build_table.
    """
    # Подготовка
    entity = test_model(name="Тестовая сущность")

    # Действие
    headers, rows = report_data_mapper._build_table(entity)

    # Проверки
    assert headers == ["Код", "Наименование"]
    assert rows == [[entity.id, "Тестовая сущность"]]


def test_report_data_mapper_build_footer():
    """
    Проверка формирования подвала отчета методом _build_footer.
    """
    # Подготовка
    entity = test_model(name="Тестовая сущность")

    # Действие
    footer = report_data_mapper._build_footer(entity)

    # Проверки
    assert footer == ""


def test_report_data_mapper_default_mapper():
    """
    Проверка маппера по умолчанию через сборку из трех частей.
    """
    # Подготовка
    entity = test_model(name="Объект")

    # Действие
    dto = report_data_mapper._default_mapper(entity)

    # Проверки
    assert dto.title == "Объект"
    assert dto.headers == ["Код", "Наименование"]
    assert dto.rows == [[entity.id, "Объект"]]
    assert dto.footer == ""


def test_report_data_mapper_none_returns_empty_dto():
    """
    Проверка возврата пустого DTO при передаче None.
    """
    # Подготовка
    source = None

    # Действие
    dto = report_data_mapper.to_dto(source)

    # Проверки
    assert dto.title == "Пустой отчет"


def test_report_data_mapper_to_collection_dto():
    """
    Проверка формирования DTO для коллекции сущностей.
    """
    # Подготовка
    units = [range_model.create_gram(), range_model.create_piece()]

    # Действие
    dto = report_data_mapper.to_collection_dto(units)

    # Проверки
    assert "range_model" in dto.title
    assert len(dto.rows) == 2
    assert "Всего записей: 2" in dto.footer


def test_report_data_mapper_storage_and_organization_and_group():
    """
    Проверка специализированных мапперов storage_model, organization_model, nomenclature_group_model.
    """
    # Подготовка
    st = storage_model.create("Склад №1", "Адрес 1")
    org = organization_model("ООО Тест", "7701987654", "044525999", "40702810938000005678", "ООО")
    grp = nomenclature_group_model.create("Сырьё")

    # Действие
    st_dto = report_data_mapper.to_dto(st)
    org_dto = report_data_mapper.to_dto(org)
    grp_dto = report_data_mapper.to_dto(grp)

    # Проверки
    assert st_dto.headers == ["Код", "Наименование", "Адрес"]
    assert st_dto.rows[0][1] == "Склад №1"
    assert "ИНН" in org_dto.headers
    assert org_dto.rows[0][1] == "ООО Тест"
    assert grp_dto.headers == ["Код", "Наименование"]
    assert grp_dto.rows[0][1] == "Сырьё"
