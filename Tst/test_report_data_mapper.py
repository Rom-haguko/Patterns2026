from src.logics.report_data_mapper import report_data_mapper
from src.core.entity_model import entity_model
from src.models.range_model import range_model


def test_report_data_mapper_build_title():
    """
    <summary>
    Проверка формирования заголовка отчета методом _build_title.
    </summary>
    """
    # Подготовка
    entity = entity_model(name="Тестовая сущность")

    # Действие
    title = report_data_mapper._build_title(entity)

    # Проверка
    assert title == "Тестовая сущность"


def test_report_data_mapper_build_table():
    """
    <summary>
    Проверка формирования таблицы отчета методом _build_table.
    </summary>
    """
    # Подготовка
    entity = entity_model(name="Тестовая сущность")

    # Действие
    headers, rows = report_data_mapper._build_table(entity)

    # Проверка
    assert headers == ["Код", "Наименование"]
    assert rows == [[entity.id, "Тестовая сущность"]]


def test_report_data_mapper_build_footer():
    """
    <summary>
    Проверка формирования подвала отчета методом _build_footer.
    </summary>
    """
    # Подготовка
    entity = entity_model(name="Тестовая сущность")

    # Действие
    footer = report_data_mapper._build_footer(entity)

    # Проверка
    assert footer == ""


def test_report_data_mapper_default_mapper():
    """
    <summary>
    Проверка маппера по умолчанию через сборку из трех частей.
    </summary>
    """
    # Подготовка
    entity = entity_model(name="Объект")

    # Действие
    dto = report_data_mapper._default_mapper(entity)

    # Проверка
    assert dto.title == "Объект"
    assert dto.headers == ["Код", "Наименование"]
    assert dto.rows == [[entity.id, "Объект"]]
    assert dto.footer == ""


def test_report_data_mapper_none_returns_empty_dto():
    """
    <summary>
    Проверка возврата пустого DTO при передаче None.
    </summary>
    """
    # Действие
    dto = report_data_mapper.to_dto(None)

    # Проверка
    assert dto.title == "Пустой отчет"


def test_report_data_mapper_to_collection_dto():
    """
    <summary>
    Проверка формирования DTO для коллекции сущностей.
    </summary>
    """
    # Подготовка
    units = [range_model.create_gram(), range_model.create_piece()]

    # Действие
    dto = report_data_mapper.to_collection_dto(units)

    # Проверка
    assert "range_model" in dto.title
    assert len(dto.rows) == 2
    assert "Всего записей: 2" in dto.footer
