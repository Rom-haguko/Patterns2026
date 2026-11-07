from datetime import date, datetime, time
import pytest
from src.core.exception import arguments_exception
from src.dtos.report_type_enum import report_type_enum
from src.logics.deserialization_context import deserialization_context
from src.logics.deserializer_factory import deserializer_factory
from src.logics.json_deserializer import json_deserializer
from src.logics.json_serializer import json_serializer
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model
from src.models.settings_model import settings_model
from src.models.storage_model import storage_model


def test_deserializer_init_with_defaults():
    """
    Проверка создания десериализатора с фабрикой по умолчанию.
    """
    # Подготовка
    # Действие
    deserializer = json_deserializer()

    # Проверки
    assert deserializer is not None
    assert isinstance(deserializer.factory, deserializer_factory)


def test_deserializer_init_with_custom_factory():
    """
    Проверка создания десериализатора с внешней фабрикой.
    """
    # Подготовка
    context = deserialization_context()
    factory = deserializer_factory(context)

    # Действие
    deserializer = json_deserializer(factory)

    # Проверки
    assert deserializer.factory is factory
    assert deserializer.factory.context is context


def test_deserialize_primitives_from_json():
    """
    Проверка десериализации базовых примитивных типов.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    val_int = deserializer.from_json("42", int)
    val_float = deserializer.from_json("3.14", float)
    val_str = deserializer.from_json('"тестовая строка"', str)
    val_bool = deserializer.from_json("true", bool)
    val_none = deserializer.from_json("null")

    # Проверки
    assert val_int == 42
    assert val_float == 3.14
    assert val_str == "тестовая строка"
    assert val_bool is True
    assert val_none is None


def test_deserialize_datetime_and_date():
    """
    Проверка десериализации дат и времени из строковых представлений ISO 8601.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    dt_val = deserializer.from_json('"2026-10-24T15:30:00"', datetime)
    d_val = deserializer.from_json('"2026-10-24"', date)
    t_val = deserializer.from_json('"15:30:00"', time)

    # Проверки
    assert isinstance(dt_val, datetime)
    assert dt_val.year == 2026
    assert dt_val.month == 10
    assert dt_val.day == 24
    assert dt_val.hour == 15

    assert isinstance(d_val, date)
    assert d_val == date(2026, 10, 24)

    assert isinstance(t_val, time)
    assert t_val.hour == 15
    assert t_val.minute == 30


def test_deserialize_range_model_nested():
    """
    Проверка рекурсивной десериализации единиц измерения с базовой единицей.
    """
    # Подготовка
    payload = {
        "id": "3020f2e6-5182-477f-a912-05b3c8c2ae82",
        "name": "килограмм",
        "conversion_factor": 1000,
        "base_range": {
            "id": "fe9b7053-57bf-4e79-b5de-d0c3c1983fb5",
            "name": "грамм",
            "conversion_factor": 1,
            "base_range": None,
        },
    }
    deserializer = json_deserializer()

    # Действие
    unit = deserializer.from_dict(payload, range_model)

    # Проверки
    assert isinstance(unit, range_model)
    assert unit.name == "килограмм"
    assert unit.conversion_factor == 1000
    assert unit.id == "3020f2e6-5182-477f-a912-05b3c8c2ae82"

    assert isinstance(unit.base_range, range_model)
    assert unit.base_range.name == "грамм"
    assert unit.base_range.conversion_factor == 1
    assert unit.base_range.id == "fe9b7053-57bf-4e79-b5de-d0c3c1983fb5"
    assert unit.base_range.base_range is None

    assert unit.to_base(2.5) == 2500.0


def test_deserialize_nomenclature_group_model():
    """
    Проверка десериализации категории номенклатуры.
    """
    # Подготовка
    payload = {
        "id": "e4d90bde-8f19-4ec1-9aeb-0ca408ef7813",
        "name": "Сырьё",
    }
    deserializer = json_deserializer()

    # Действие
    group = deserializer.from_dict(payload, nomenclature_group_model)

    # Проверки
    assert isinstance(group, nomenclature_group_model)
    assert group.id == "e4d90bde-8f19-4ec1-9aeb-0ca408ef7813"
    assert group.name == "Сырьё"


def test_deserialize_nomenclature_model_with_relations():
    """
    Проверка десериализации номенклатуры со связанной группой и единицей измерения.
    """
    # Подготовка
    payload = {
        "id": "4399e732-77cb-4a22-884e-94d888cd1fd5",
        "name": "Мука пшеничная",
        "full_name": "Мука пшеничная высший сорт, 50 кг мешок",
        "group": {
            "id": "e4d90bde-8f19-4ec1-9aeb-0ca408ef7813",
            "name": "Сырьё",
        },
        "range": {
            "id": "3020f2e6-5182-477f-a912-05b3c8c2ae82",
            "name": "килограмм",
            "conversion_factor": 1000,
            "base_range": None,
        },
        "recipe": None,
    }
    deserializer = json_deserializer()

    # Действие
    item = deserializer.from_dict(payload, nomenclature_model)

    # Проверки
    assert isinstance(item, nomenclature_model)
    assert item.id == "4399e732-77cb-4a22-884e-94d888cd1fd5"
    assert item.name == "Мука пшеничная"
    assert item.full_name == "Мука пшеничная высший сорт, 50 кг мешок"
    assert isinstance(item.group, nomenclature_group_model)
    assert item.group.name == "Сырьё"
    assert isinstance(item.range, range_model)
    assert item.range.name == "килограмм"
    assert item.recipe is None


def test_deserialize_storage_model():
    """
    Проверка десериализации карточки склада.
    """
    # Подготовка
    payload = {
        "id": "263d1fdf-f0cd-4ba7-95b4-d738435f927a",
        "name": "Центральный склад",
        "address": "г. Москва, ул. Цветочная, д. 10",
    }
    deserializer = json_deserializer()

    # Действие
    storage = deserializer.from_dict(payload, storage_model)

    # Проверки
    assert isinstance(storage, storage_model)
    assert storage.id == "263d1fdf-f0cd-4ba7-95b4-d738435f927a"
    assert storage.name == "Центральный склад"
    assert storage.address == "г. Москва, ул. Цветочная, д. 10"


def test_deserialize_organization_model():
    """
    Проверка десериализации реквизитов организации.
    """
    # Подготовка
    payload = {
        "id": "3b913027-e9f8-47d8-ac11-539e723042fb",
        "name": "ООО Ромашка",
        "inn": "7701234567",
        "bik": "123456789",
        "account": "12345678901234567890",
        "ownership_form": "ООО",
        "corr_account": "30101810200000000000",
    }
    deserializer = json_deserializer()

    # Действие
    org = deserializer.from_dict(payload, organization_model)

    # Проверки
    assert isinstance(org, organization_model)
    assert org.id == "3b913027-e9f8-47d8-ac11-539e723042fb"
    assert org.name == "ООО Ромашка"
    assert org.inn == "7701234567"
    assert org.bik == "123456789"
    assert org.account == "12345678901234567890"
    assert org.ownership_form == "ООО"
    assert org.corr_account == "30101810200000000000"


def test_deserialize_settings_model():
    """
    Проверка десериализации конфигурации системы с вложенной организацией и перечислением.
    """
    # Подготовка
    payload = {
        "id": "4ce4e6d7-0814-451b-8e81-fd0df59b8029",
        "name": "Конфигурация системы",
        "boss_name": "Гуреев Р. А.",
        "account_name": "Иванова А. С.",
        "response_format": 3,
        "company": {
            "id": "59684403-5e0e-4ea5-a98c-51e2f6a604ac",
            "name": "ООО Ромашка",
            "inn": "7701234567",
            "bik": "044525225",
            "account": "40702810938000012345",
            "ownership_form": "ООО",
            "corr_account": "30101810400000000225",
        },
    }
    deserializer = json_deserializer()

    # Действие
    settings = deserializer.from_dict(payload, settings_model)

    # Проверки
    assert isinstance(settings, settings_model)
    assert settings.id == "4ce4e6d7-0814-451b-8e81-fd0df59b8029"
    assert settings.name == "Конфигурация системы"
    assert settings.boss_name == "Гуреев Р. А."
    assert settings.account_name == "Иванова А. С."
    assert settings.response_format == report_type_enum.MARKDOWN
    assert isinstance(settings.company, organization_model)
    assert settings.company.name == "ООО Ромашка"


def test_deserialize_recipe_step_model():
    """
    Проверка десериализации отдельного технологического шага рецепта.
    """
    # Подготовка
    payload = {
        "id": "6c8a9a07-9000-4ea4-8ec8-f4844eb2e6b1",
        "step_number": 1,
        "name": "Подготовка теста",
        "description": "Раскатать тесто до круга 30–32 см",
        "time_minutes": 20.0,
    }
    deserializer = json_deserializer()

    # Действие
    step = deserializer.from_dict(payload, recipe_step_model)

    # Проверки
    assert isinstance(step, recipe_step_model)
    assert step.id == "6c8a9a07-9000-4ea4-8ec8-f4844eb2e6b1"
    assert step.step_number == 1
    assert step.name == "Подготовка теста"
    assert step.description == "Раскатать тесто до круга 30–32 см"
    assert step.time_minutes == 20.0


def test_deserialize_recipe_row_model():
    """
    Проверка десериализации строки технологической карты.
    """
    # Подготовка
    payload = {
        "id": "c7ca7242-0ae5-4ee8-a0e3-e00d6f45faa8",
        "name": "Сыр Моцарелла",
        "brutto": 180.0,
        "netto": 150.0,
        "nomenclature": {
            "id": "d049f7e8-7ba6-4556-9ff5-c49ad5f98bb2",
            "name": "Сыр Моцарелла",
            "full_name": "Сыр Моцарелла для пиццы",
            "group": {"id": "111", "name": "Сырьё"},
            "range": {"id": "222", "name": "грамм", "conversion_factor": 1, "base_range": None},
        },
        "range": {
            "id": "222",
            "name": "грамм",
            "conversion_factor": 1,
            "base_range": None,
        },
    }
    deserializer = json_deserializer()

    # Действие
    row = deserializer.from_dict(payload, recipe_row_model)

    # Проверки
    assert isinstance(row, recipe_row_model)
    assert row.id == "c7ca7242-0ae5-4ee8-a0e3-e00d6f45faa8"
    assert row.name == "Сыр Моцарелла"
    assert row.brutto == 180.0
    assert row.netto == 150.0
    assert isinstance(row.nomenclature, nomenclature_model)
    assert isinstance(row.range, range_model)


def test_deserialize_recipe_file_with_nested_semi_finished():
    """
    Проверка десериализации сложного рецепта из Docs/json/recipe.json с полуфабрикатами.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    recipe = deserializer.from_json_file("Docs/json/recipe.json", recipe_model)

    # Проверки
    assert isinstance(recipe, recipe_model)
    assert recipe.name == "Пицца Маргарита"
    assert recipe.id == "22354c67-11eb-43e7-8144-37f752e3bae6"
    assert len(recipe.rows) == 6
    assert len(recipe.steps) == 5

    assert isinstance(recipe.target_nomenclature, nomenclature_model)
    assert recipe.target_nomenclature.name == "Пицца Маргарита"

    # Проверка вычисляемых свойств (должны совпадать после восстановления графа)
    assert recipe.gross_weight == pytest.approx(573.989, rel=1e-3)
    assert recipe.net_weight == pytest.approx(531.0, rel=1e-3)

    # Проверка концепции 'Блюдо в блюде' для полуфабриката 'Тесто дрожжевое'
    dough_row = recipe.rows[0]
    assert dough_row.nomenclature.name == "Тесто дрожжевое"
    assert dough_row.nomenclature.recipe is not None
    assert isinstance(dough_row.nomenclature.recipe, recipe_model)
    assert dough_row.nomenclature.recipe.name == "Тесто дрожжевое (заготовка)"
    assert len(dough_row.nomenclature.recipe.rows) == 2


def test_round_trip_export_import_matches_storage_manager(tmp_path):
    """
    Сквозной тест: экспорт хранилища в JSON и обратная десериализация с полным сравнением.
    """
    # Подготовка
    manager = storage_manager()
    export_file = tmp_path / "all_data_export.json"
    manager.export_all_to_json(str(export_file))
    deserializer = json_deserializer()

    # Действие
    restored = deserializer.from_json_file(str(export_file))

    # Проверки
    collection_keys = [
        storage_manager.range_key(),
        storage_manager.group_key(),
        storage_manager.nomenclature_key(),
        storage_manager.storage_key(),
        storage_manager.recipe_key(),
    ]

    for key in collection_keys:
        original_items = manager.get(key)
        restored_items = restored.get(key, [])

        assert len(original_items) == len(restored_items), f"Количество сущностей не совпадает для ключа {key}"

        for orig, loaded in zip(original_items, restored_items):
            # Проверка равенства сущностей по id (__eq__)
            assert orig == loaded
            assert orig.id == loaded.id
            assert orig.name == loaded.name

    # Дополнительные проверки доменных атрибутов рецепта
    original_recipes = manager.get(storage_manager.recipe_key())
    restored_recipes = restored.get(storage_manager.recipe_key())
    for orig_rec, loaded_rec in zip(original_recipes, restored_recipes):
        assert orig_rec.gross_weight == pytest.approx(loaded_rec.gross_weight, rel=1e-3)
        assert orig_rec.net_weight == pytest.approx(loaded_rec.net_weight, rel=1e-3)
        assert orig_rec.category == loaded_rec.category
        assert orig_rec.output == loaded_rec.output
        assert len(orig_rec.rows) == len(loaded_rec.rows)
        assert len(orig_rec.steps) == len(loaded_rec.steps)


def test_deserialize_docs_all_data_json_structure():
    """
    Проверка десериализации исходного эталонного файла Docs/json/all_data.json.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    data = deserializer.from_json_file("Docs/json/all_data.json")

    # Проверки
    assert isinstance(data, dict)
    assert len(data["range_model"]) == 5
    assert len(data["nomenclature_group_model"]) == 4
    assert len(data["nomenclature_model"]) == 13
    assert len(data["storage_model"]) == 6
    assert len(data["recipe_model"]) == 2

    # Проверка типов объектов в коллекциях
    assert all(isinstance(x, range_model) for x in data["range_model"])
    assert all(isinstance(x, nomenclature_group_model) for x in data["nomenclature_group_model"])
    assert all(isinstance(x, nomenclature_model) for x in data["nomenclature_model"])
    assert all(isinstance(x, storage_model) for x in data["storage_model"])
    assert all(isinstance(x, recipe_model) for x in data["recipe_model"])


def test_storage_manager_import_all_from_json_method(tmp_path):
    """
    Проверка встроенного метода import_all_from_json в storage_manager.
    """
    # Подготовка
    manager = storage_manager()
    temp_snapshot = tmp_path / "temp_snapshot.json"
    manager.export_all_to_json(str(temp_snapshot))

    # Действие
    success = manager.import_all_from_json(str(temp_snapshot), clear_existing=False)

    # Проверки
    assert success is True
    # Поскольку сущности с такими id уже в хранилище, дубликаты не должны добавиться (add возвращает False)
    assert len(manager.get(storage_manager.range_key())) == 5


def test_identity_map_preserves_shared_instance():
    """
    Проверка сохранения единственности разделяемого экземпляра (Identity Map).
    """
    # Подготовка
    payload = {
        "range_model": [
            {"id": "unit-1", "name": "грамм", "conversion_factor": 1, "base_range": None},
        ],
        "nomenclature_model": [
            {
                "id": "nom-1",
                "name": "Соль",
                "full_name": "Соль 1",
                "group": {"id": "g-1", "name": "Сырьё"},
                "range": {"id": "unit-1", "name": "грамм", "conversion_factor": 1, "base_range": None},
            },
            {
                "id": "nom-2",
                "name": "Сахар",
                "full_name": "Сахар 1",
                "group": {"id": "g-1", "name": "Сырьё"},
                "range": {"id": "unit-1", "name": "грамм", "conversion_factor": 1, "base_range": None},
            },
        ],
    }
    deserializer = json_deserializer()

    # Действие
    result = deserializer.from_dict(payload)

    # Проверки
    nom1 = result["nomenclature_model"][0]
    nom2 = result["nomenclature_model"][1]
    assert nom1.range is nom2.range
    assert nom1.group is nom2.group


def test_deserialize_empty_string_raises_arguments_exception():
    """
    Проверка выброса arguments_exception при передаче пустой строки JSON.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        deserializer.from_json("")

    # Проверки
    assert exc_info.type is arguments_exception


def test_deserialize_invalid_json_syntax_raises_arguments_exception():
    """
    Проверка выброса arguments_exception при передаче строки с некорректным синтаксисом JSON.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        deserializer.from_json("невалидный { json")

    # Проверки
    assert exc_info.type is arguments_exception


def test_deserialize_empty_file_path_raises_arguments_exception():
    """
    Проверка выброса arguments_exception при передаче пустого пути к файлу.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        deserializer.from_json_file("")

    # Проверки
    assert exc_info.type is arguments_exception


def test_deserialize_non_dict_for_model_raises_arguments_exception():
    """
    Проверка выброса arguments_exception при попытке десериализации не-словаря в доменную модель.
    """
    # Подготовка
    deserializer = json_deserializer()

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        deserializer.from_dict("некорректные данные", range_model)

    # Проверки
    assert exc_info.type is arguments_exception


def test_deserialize_with_type_indicator_short_name():
    """
    Проверка автоматического определения типа модели по короткому полю 'type' в JSON без явного target_type.
    """
    # Подготовка
    payload = {
        "type": "range_model",
        "id": "11111111-2222-3333-4444-555555555555",
        "name": "килограмм",
        "conversion_factor": 1000,
        "base_range": None,
    }
    deserializer = json_deserializer()

    # Действие
    result = deserializer.from_dict(payload)

    # Проверки
    assert isinstance(result, range_model)
    assert result.name == "килограмм"
    assert result.id == "11111111-2222-3333-4444-555555555555"


def test_deserialize_with_type_indicator_full_qualname():
    """
    Проверка автоматического определения типа модели по полному пути класса в поле 'type'.
    """
    # Подготовка
    payload = {
        "type": "src.models.storage_model.storage_model",
        "id": "22222222-3333-4444-5555-666666666666",
        "name": "Основной склад",
        "address": "г. Москва, ул. Ленина, д. 1",
    }
    deserializer = json_deserializer()

    # Действие
    result = deserializer.from_dict(payload)

    # Проверки
    assert isinstance(result, storage_model)
    assert result.name == "Основной склад"
    assert result.address == "г. Москва, ул. Ленина, д. 1"


def test_abstract_model_type_property_format():
    """
    Проверка формирования полного квалифицированного имени класса через свойство type в abstract_model.
    """
    # Подготовка
    unit = range_model("грамм")

    # Действие
    type_name = unit.type

    # Проверки
    assert type_name == f"{unit.__class__.__module__}.{unit.__class__.__qualname__}"
    assert type_name.endswith("range_model")


def test_storage_manager_import_dynamic_order_of_collections(tmp_path):
    """
    Проверка динамической загрузки коллекций в storage_manager без привязки к фиксированному порядку ключей.
    """
    # Подготовка
    manager = storage_manager()
    reversed_snapshot = tmp_path / "reversed_order.json"
    data = {
        storage_manager.recipe_key(): manager.get(storage_manager.recipe_key()),
        storage_manager.storage_key(): manager.get(storage_manager.storage_key()),
        storage_manager.nomenclature_key(): manager.get(storage_manager.nomenclature_key()),
        storage_manager.group_key(): manager.get(storage_manager.group_key()),
        storage_manager.range_key(): manager.get(storage_manager.range_key()),
    }
    json_serializer().to_json_file(data, str(reversed_snapshot))

    # Действие
    success = manager.import_all_from_json(str(reversed_snapshot), clear_existing=True)

    # Проверки
    assert success is True
    assert len(manager.get(storage_manager.range_key())) > 0
    assert len(manager.get(storage_manager.nomenclature_key())) > 0
    assert len(manager.get(storage_manager.recipe_key())) > 0
