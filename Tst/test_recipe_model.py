import pytest
import os
from src.core.exception import arguments_exception
from src.core.file_resolver import FilePathResolver
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model
from src.models.organization_model import organization_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model


def test_success_init_recipe_row_model():
    """
    <summary>
    Проверка успешной инициализации строки рецепта (ингредиента)
    с корректными параметрами номенклатуры, брутто и нетто.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная высший сорт", group, gram)

    row = recipe_row_model(nom, 250.0, 200.0, gram)

    assert row.nomenclature == nom
    assert row.brutto == 250.0
    assert row.netto == 200.0
    assert row.range == gram
    assert row.name == "Мука"


def test_success_factory_create_recipe_row_model():
    """
    <summary>
    Проверка создания строки рецепта через фабричный метод recipe_row_model.create.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_semi_finished()
    nom = nomenclature_model.create("Тесто", "Тесто дрожжевое", group, gram)

    row = recipe_row_model.create(nom, 300.0, 280.0, gram, name="Тесто для основы")

    assert isinstance(row, recipe_row_model)
    assert row.name == "Тесто для основы"
    assert row.brutto == 300.0
    assert row.netto == 280.0


def test_error_recipe_row_invalid_nomenclature():
    """
    <summary>
    Проверка генерации исключения arguments_exception при передаче некорректного
    типа объекта вместо nomenclature_model.
    </summary>
    """
    with pytest.raises(arguments_exception):
        recipe_row_model(nomenclature="не_номенклатура", brutto=100.0, netto=90.0)


def test_error_recipe_row_negative_brutto():
    """
    <summary>
    Проверка генерации исключения arguments_exception при отрицательном весе брутто.
    </summary>
    """
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=-10.0, netto=5.0)


def test_error_recipe_row_negative_netto():
    """
    <summary>
    Проверка генерации исключения arguments_exception при отрицательном весе нетто.
    </summary>
    """
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=10.0, netto=-5.0)


def test_error_recipe_row_invalid_range():
    """
    <summary>
    Проверка генерации исключения arguments_exception при передаче некорректной
    единицы измерения в recipe_row_model.
    </summary>
    """
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=10.0, netto=10.0, range="не_единица_измерения")


def test_success_init_and_create_recipe_step_model():
    """
    <summary>
    Проверка создания шага приготовления через конструктор и фабричный метод.
    </summary>
    """
    step1 = recipe_step_model(1, "Замес", "Замесить тесто", 15.0)
    step2 = recipe_step_model.create(2, "Выпекание", "Выпекать в печи", 10.0)

    assert step1.step_number == 1
    assert step1.name == "Замес"
    assert step1.description == "Замесить тесто"
    assert step1.time_minutes == 15.0

    assert step2.step_number == 2
    assert step2.name == "Выпекание"
    assert step2.time_minutes == 10.0


def test_error_recipe_step_invalid_number():
    """
    <summary>
    Проверка вызова arguments_exception при передаче номера шага < 1 или не int.
    </summary>
    """
    with pytest.raises(arguments_exception):
        recipe_step_model(step_number=0, name="Шаг ноль")

    with pytest.raises(arguments_exception):
        recipe_step_model(step_number="первый", name="Шаг")


def test_success_calculate_gross_and_net_weight():
    """
    <summary>
    Проверка вычисления веса Брутто и Нетто рецепта:
    вес должен рассчитываться путем сложения весов каждого ингредиента.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Вода", "Вода", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=150.0, netto=140.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=100.0, netto=100.0, range=gram)

    recipe = recipe_model.create(name="Тесто простое", rows=[row1, row2])

    assert recipe.gross_weight == 250.0
    assert recipe.net_weight == 240.0


def test_success_calculate_weight_when_adding_ingredient():
    """
    <summary>
    Проверка пересчета веса Брутто и Нетто при динамическом добавлении
    нового ингредиента в рецепт (add_row).
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Ингредиент 1", "Ингр 1", group, gram)
    nom2 = nomenclature_model.create("Ингредиент 2", "Ингр 2", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=100.0, netto=80.0, range=gram)
    recipe = recipe_model.create(name="Тестовый рецепт", rows=[row1])

    assert recipe.gross_weight == 100.0
    assert recipe.net_weight == 80.0

    row2 = recipe_row_model.create(nom2, brutto=50.0, netto=45.0, range=gram)
    add_result = recipe.add_row(row2)

    assert add_result is True
    assert len(recipe.rows) == 2
    assert recipe.gross_weight == 150.0
    assert recipe.net_weight == 125.0


def test_success_calculate_weight_when_removing_ingredient():
    """
    <summary>
    Проверка пересчета веса Брутто и Нетто при исключении ингредиента
    из рецепта (remove_row).
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Сахар", "Сахар", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=200.0, netto=180.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=50.0, netto=50.0, range=gram)

    recipe = recipe_model.create(name="Сладкое тесто", rows=[row1, row2])
    assert recipe.gross_weight == 250.0
    assert recipe.net_weight == 230.0

    remove_result = recipe.remove_row(row2)

    assert remove_result is True
    assert len(recipe.rows) == 1
    assert recipe.gross_weight == 200.0
    assert recipe.net_weight == 180.0


def test_add_duplicate_row_returns_false():
    """
    <summary>
    Проверка добавления дубликата ингредиента: повторное добавление
    того же объекта recipe_row_model возвращает False и не меняет вес.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Соль", "Соль", group, gram)
    row = recipe_row_model.create(nom, brutto=5.0, netto=5.0, range=gram)

    recipe = recipe_model.create(name="Рецепт с солью", rows=[row])
    initial_gross = recipe.gross_weight

    result = recipe.add_row(row)

    assert result is False
    assert len(recipe.rows) == 1
    assert recipe.gross_weight == initial_gross


def test_remove_nonexistent_row_returns_false():
    """
    <summary>
    Проверка удаления отсутствующего ингредиента: вызов remove_row
    для строки, которой нет в рецепте, возвращает False.
    </summary>
    """
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Дрожжи", "Дрожжи", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=100.0, netto=100.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=10.0, netto=10.0, range=gram)

    recipe = recipe_model.create(name="Рецепт", rows=[row1])

    result = recipe.remove_row(row2)

    assert result is False
    assert len(recipe.rows) == 1


def test_recipe_key_returns_recipe_model():
    """
    <summary>
    Проверка статического метода storage_manager.recipe_key():
    возвращает строковый идентификатор коллекции 'recipe_model'.
    </summary>
    """
    assert storage_manager.recipe_key() == "recipe_model"


def test_first_start_recipes_present_in_storage():
    """
    <summary>
    Проверка наличия рецептов при первом старте:
    storage_manager должен содержать непустую коллекцию рецептов.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())

    assert isinstance(recipes, list)
    assert len(recipes) > 0
    assert all(isinstance(r, recipe_model) for r in recipes)


def test_first_start_contains_pizza_margarita():
    """
    <summary>
    Проверка наличия рецепта 'Пицца Маргарита' при первом старте:
    рецепт с таким наименованием должен присутствовать в хранилище.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    margarita = next((r for r in recipes if "Пицца Маргарита" in r.name), None)

    assert margarita is not None
    assert isinstance(margarita, recipe_model)


def test_first_start_margarita_contains_semi_finished():
    """
    <summary>
    Проверка требования: рецепт должен содержать полуфабрикаты.
    Для рецепта Пицца Маргарита свойство has_semi_finished должно быть True,
    а в составе присутствовать Тесто дрожжевое и Соус томатный.
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    margarita = next((r for r in recipes if r.name == "Пицца Маргарита"), None)

    assert margarita is not None
    assert margarita.has_semi_finished is True
    assert len(margarita.semi_finished_items) >= 2

    semi_names = [r.nomenclature.name for r in margarita.semi_finished_items]
    assert any("Тесто дрожжевое" in name for name in semi_names)
    assert any("Соус томатный" in name for name in semi_names)


def test_first_start_contains_recipe_with_packaging():
    """
    <summary>
    Проверка требования: рецепт с упаковкой.
    В хранилище должен присутствовать рецепт, содержащий категорию 'Упаковка' (has_packaging is True).
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    packaged_recipe = next((r for r in recipes if r.has_packaging), None)

    assert packaged_recipe is not None
    assert packaged_recipe.has_packaging is True
    assert len(packaged_recipe.packaging_items) > 0
    assert any("Коробка" in r.nomenclature.name for r in packaged_recipe.packaging_items)


def test_first_start_margarita_gross_and_net_weights():
    """
    <summary>
    Проверка точного расчета веса Брутто и Нетто для рецепта Пицца Маргарита
    с учетом рекурсивного раскрытия полуфабрикатов (Блюдо в блюде):
    Брутто теста = 250 (пересчет из внутреннего рецепта)
    Брутто соуса = 111 (пересчет из внутреннего рецепта)
    Брутто сыра = 180, масла = 20, базилика = 10, соли = 3
    Итого Брутто ≈ 574
    Нетто = 250 + 100 + 150 + 20 + 8 + 3 = 531
    </summary>
    """
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())
    margarita = next((r for r in recipes if r.name == "Пицца Маргарита"), None)

    assert margarita is not None
    assert margarita.gross_weight == pytest.approx(574.0, abs=1.0)
    assert margarita.net_weight == 531.0


def test_domain_models_factory_methods():
    """
    <summary>
    Проверка работоспособности фабричных методов, добавленных в доменные модели:
    range_model, nomenclature_group_model, nomenclature_model, storage_model, organization_model.
    </summary>
    """
    unit_gram = range_model.create_gram()
    unit_kilo = range_model.create_kilogramm()
    unit_ml = range_model.create_milliliter()
    unit_l = range_model.create_liter(unit_ml)
    unit_pcs = range_model.create_piece()
    unit_custom = range_model.create("коробка", 1)

    group_raw = nomenclature_group_model.create_raw()
    group_semi = nomenclature_group_model.create_semi_finished()
    group_fin = nomenclature_group_model.create_finished()
    group_pack = nomenclature_group_model.create_packaging()
    group_custom = nomenclature_group_model.create("Специи")

    nom = nomenclature_model.create("Перец", "Перец черный молотый", group_raw, unit_gram)
    store = storage_model.create("Склад №9", "ул. Ленина, 1")
    org = organization_model.create("ООО Ромашка", inn="7701234567", bik="044525225", account="40702810900000000001", ownership_form="ООО")

    assert isinstance(unit_gram, range_model) and unit_gram.name == "грамм"
    assert isinstance(unit_kilo, range_model) and unit_kilo.conversion_factor == 1000
    assert isinstance(unit_ml, range_model) and unit_ml.name == "миллилитр"
    assert isinstance(unit_l, range_model) and unit_l.name == "литр"
    assert isinstance(unit_pcs, range_model) and unit_pcs.name == "штука"
    assert isinstance(unit_custom, range_model) and unit_custom.name == "коробка"

    assert isinstance(group_raw, nomenclature_group_model) and group_raw.name == "Сырьё"
    assert isinstance(group_semi, nomenclature_group_model) and group_semi.name == "Полуфабрикаты"
    assert isinstance(group_fin, nomenclature_group_model) and group_fin.name == "Готовая продукция"
    assert isinstance(group_pack, nomenclature_group_model) and group_pack.name == "Упаковка"
    assert isinstance(group_custom, nomenclature_group_model) and group_custom.name == "Специи"

    assert isinstance(nom, nomenclature_model) and nom.name == "Перец"
    assert isinstance(store, storage_model) and store.name == "Склад №9"
    assert isinstance(org, organization_model) and org.name == "ООО Ромашка"