import pytest
from src.core.exception import arguments_exception
from src.dtos.filter_dto import filter_dto
from src.dtos.filter_type_enum import filter_type_enum
from src.dtos.osv_row_dto import osv_row_dto
from src.dtos.turnover_type_enum import turnover_type_enum
from src.logics.osv_service import osv_service
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model
from src.models.turnover_model import turnover_model


def test_turnover_type_enum_from_string():
    # Подготовка
    raw_income = "RECEIPT"
    raw_expense = "EXPENSE"

    # Действие
    t_income = turnover_type_enum.from_string(raw_income)
    t_expense = turnover_type_enum.from_string(raw_expense)

    # Проверки
    assert t_income == turnover_type_enum.RECEIPT
    assert t_expense == turnover_type_enum.EXPENSE


def test_turnover_model_creation_success():
    # Подготовка
    st = storage_model.create("Склад 1", "Адрес 1")
    rng = range_model.create_gram()
    grp = nomenclature_group_model.create("Сырьё")
    nom = nomenclature_model.create("Соль", "Соль 1кг", grp, rng)

    # Действие
    mov = turnover_model.create(st, nom, rng, 50.0, turnover_type_enum.RECEIPT)

    # Проверки
    assert mov.storage == st
    assert mov.nomenclature == nom
    assert mov.quantity == 50.0
    assert mov.turnover_type == turnover_type_enum.RECEIPT


def test_turnover_model_creation_invalid_quantity():
    # Подготовка
    st = storage_model.create("Склад 1", "Адрес 1")
    rng = range_model.create_gram()
    grp = nomenclature_group_model.create("Сырьё")
    nom = nomenclature_model.create("Соль", "Соль 1кг", grp, rng)

    # Действие
    def action():
        turnover_model.create(st, nom, rng, 0.0, turnover_type_enum.RECEIPT)

    # Проверки
    with pytest.raises(arguments_exception):
        action()


def test_osv_row_dto_balances():
    # Подготовка
    st = storage_model.create("Склад 1", "Адрес 1")
    rng = range_model.create_gram()
    grp = nomenclature_group_model.create("Сырьё")
    nom = nomenclature_model.create("Соль", "Соль 1кг", grp, rng)

    # Действие
    row = osv_row_dto(
        storage=st,
        nomenclature=nom,
        range=rng,
        initial_balance=10.0,
        inflow=40.0,
        outflow=15.0,
        final_balance=35.0,
    )

    # Проверки
    assert row.storage == st
    assert row.nomenclature == nom
    assert row.initial_balance == 10.0
    assert row.inflow == 40.0
    assert row.outflow == 15.0
    assert row.final_balance == 35.0


def test_osv_service_build_osv_unfiltered():
    # Подготовка
    storage = storage_manager()
    service = osv_service(storage)

    # Действие
    rows = service.build_osv()

    # Проверки
    assert len(rows) >= 3
    flour_row = next((r for r in rows if "мука" in r.nomenclature.name.lower()), None)
    assert flour_row is not None
    assert flour_row.initial_balance == 0.0
    assert flour_row.inflow == 100.0
    assert flour_row.outflow == 20.0
    assert flour_row.final_balance == 80.0

    sugar_row = next((r for r in rows if "сахар" in r.nomenclature.name.lower()), None)
    assert sugar_row is not None
    assert sugar_row.initial_balance == 0.0
    assert sugar_row.inflow == 50.0
    assert sugar_row.outflow == 10.0
    assert sugar_row.final_balance == 40.0


def test_osv_service_build_osv_filtered_by_nomenclature():
    # Подготовка
    storage = storage_manager()
    service = osv_service(storage)
    filter_flour = filter_dto(name="Мука", name_filter_type=filter_type_enum.LIKE)

    # Действие
    rows = service.build_osv(filter_flour)

    # Проверки
    assert len(rows) == 1
    row = rows[0]
    assert "мука" in row.nomenclature.name.lower()
    assert row.inflow == 100.0
    assert row.outflow == 20.0
    assert row.final_balance == 80.0


def test_osv_service_build_osv_filtered_by_storage():
    # Подготовка
    storage = storage_manager()
    service = osv_service(storage)
    filter_storage = filter_dto(name="Склад готовой продукции", name_filter_type=filter_type_enum.EQUALS)

    # Действие
    rows = service.build_osv(filter_storage)

    # Проверки
    assert len(rows) == 1
    row = rows[0]
    assert row.storage.name == "Склад готовой продукции"
    assert "пицца" in row.nomenclature.name.lower()
    assert row.inflow == 15.0
    assert row.outflow == 5.0
    assert row.final_balance == 10.0
