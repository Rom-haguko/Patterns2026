import pytest
from src.core.exception import arguments_exception, operation_exception
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model
from src.models.storage_model import storage_model


def test_success_init_recipe_row_model():
    """
    Проверка успешной инициализации строки рецепта с корректными параметрами.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Мука", "Мука пшеничная высший сорт", group, gram)

    # Действие
    row = recipe_row_model(nom, 250.0, 200.0, gram)

    # Проверки
    assert row.nomenclature == nom
    assert row.brutto == 250.0
    assert row.netto == 200.0
    assert row.range == gram
    assert row.name == "Мука"


def test_success_factory_create_recipe_row_model():
    """
    Проверка создания строки рецепта через фабричный метод recipe_row_model.create.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_semi_finished()
    nom = nomenclature_model.create("Тесто", "Тесто дрожжевое", group, gram)

    # Действие
    row = recipe_row_model.create(nom, 300.0, 280.0, gram, name="Тесто для основы")

    # Проверки
    assert isinstance(row, recipe_row_model)
    assert row.name == "Тесто для основы"
    assert row.brutto == 300.0
    assert row.netto == 280.0


def test_error_recipe_row_invalid_nomenclature():
    """
    Проверка генерации исключения arguments_exception при передаче некорректного типа номенклатуры.
    """
    # Подготовка
    invalid_nom = "не_номенклатура"

    # Действие
    with pytest.raises(arguments_exception):
        recipe_row_model(nomenclature=invalid_nom, brutto=100.0, netto=90.0)

    # Проверки
    assert True


def test_error_recipe_row_negative_brutto():
    """
    Проверка генерации исключения arguments_exception при отрицательном весе брутто.
    """
    # Подготовка
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    # Действие
    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=-10.0, netto=5.0)

    # Проверки
    assert True


def test_error_recipe_row_negative_netto():
    """
    Проверка генерации исключения arguments_exception при отрицательном весе нетто.
    """
    # Подготовка
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    # Действие
    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=10.0, netto=-5.0)

    # Проверки
    assert True


def test_error_recipe_row_invalid_range():
    """
    Проверка генерации исключения arguments_exception при передаче некорректной единицы измерения.
    """
    # Подготовка
    nom = nomenclature_model.create("Соль", "Соль поваренная", nomenclature_group_model.create_raw(), range_model.create_gram())

    # Действие
    with pytest.raises(arguments_exception):
        recipe_row_model(nom, brutto=10.0, netto=10.0, range="не_единица_измерения")

    # Проверки
    assert True


def test_success_init_and_create_recipe_step_model():
    """
    Проверка создания шага приготовления через конструктор и фабричный метод.
    """
    # Подготовка
    # Действие
    step1 = recipe_step_model(1, "Замес", "Замесить тесто", 15.0)
    step2 = recipe_step_model.create(2, "Выпекание", "Выпекать в печи", 10.0)

    # Проверки
    assert step1.step_number == 1
    assert step1.name == "Замес"
    assert step1.description == "Замесить тесто"
    assert step1.time_minutes == 15.0

    assert step2.step_number == 2
    assert step2.name == "Выпекание"
    assert step2.time_minutes == 10.0


def test_error_recipe_step_invalid_number():
    """
    Проверка вызова arguments_exception при передаче номера шага < 1 или не int.
    """
    # Подготовка
    # Действие
    with pytest.raises(arguments_exception):
        recipe_step_model(step_number=0, name="Шаг ноль")

    # Проверки
    assert True


def test_success_recipe_remove_step():
    """
    Проверка успешного удаления шага приготовления из рецепта.
    """
    # Подготовка
    step1 = recipe_step_model.create(1, "Подготовка", "Подготовить", 5.0)
    step2 = recipe_step_model.create(2, "Замес", "Замесить", 10.0)
    recipe = recipe_model.create(name="Тестовый рецепт", steps=[step1, step2])

    # Действие
    result = recipe.remove_step(step1)

    # Проверки
    assert result is True
    assert len(recipe.steps) == 1
    assert step1 not in recipe.steps


def test_error_recipe_remove_nonexistent_step_returns_false():
    """
    Проверка возврата False при удалении несуществующего шага.
    """
    # Подготовка
    step1 = recipe_step_model.create(1, "Подготовка", "Подготовить", 5.0)
    step_nonexistent = recipe_step_model.create(99, "Несуществующий", "Описание", 1.0)
    recipe = recipe_model.create(name="Тестовый рецепт", steps=[step1])

    # Действие
    result = recipe.remove_step(step_nonexistent)

    # Проверки
    assert result is False
    assert len(recipe.steps) == 1


def test_success_calculate_gross_and_net_weight():
    """
    Проверка вычисления веса Брутто и Нетто простого рецепта.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Вода", "Вода", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=150.0, netto=140.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=100.0, netto=100.0, range=gram)

    # Действие
    recipe = recipe_model.create(name="Тесто простое", rows=[row1, row2])

    # Проверки
    assert recipe.gross_weight == 250.0
    assert recipe.net_weight == 240.0


def test_success_calculate_weight_when_adding_ingredient():
    """
    Проверка пересчета веса Брутто и Нетто при добавлении нового ингредиента.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Ингредиент 1", "Ингр 1", group, gram)
    nom2 = nomenclature_model.create("Ингредиент 2", "Ингр 2", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=100.0, netto=80.0, range=gram)
    recipe = recipe_model.create(name="Тестовый рецепт", rows=[row1])

    # Действие
    row2 = recipe_row_model.create(nom2, brutto=50.0, netto=45.0, range=gram)
    add_result = recipe.add_row(row2)

    # Проверки
    assert add_result is True
    assert len(recipe.rows) == 2
    assert recipe.gross_weight == 150.0
    assert recipe.net_weight == 125.0


def test_success_calculate_weight_when_removing_ingredient():
    """
    Проверка пересчета веса Брутто и Нетто при исключении ингредиента.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Сахар", "Сахар", group, gram)

    row1 = recipe_row_model.create(nom1, brutto=200.0, netto=180.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=50.0, netto=50.0, range=gram)
    recipe = recipe_model.create(name="Сладкое тесто", rows=[row1, row2])

    # Действие
    remove_result = recipe.remove_row(row2)

    # Проверки
    assert remove_result is True
    assert len(recipe.rows) == 1
    assert recipe.gross_weight == 200.0
    assert recipe.net_weight == 180.0


def test_add_duplicate_row_returns_false():
    """
    Проверка добавления дубликата ингредиента.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create("Соль", "Соль", group, gram)
    row = recipe_row_model.create(nom, brutto=5.0, netto=5.0, range=gram)
    recipe = recipe_model.create(name="Рецепт с солью", rows=[row])
    initial_gross = recipe.gross_weight

    # Действие
    result = recipe.add_row(row)

    # Проверки
    assert result is False
    assert len(recipe.rows) == 1
    assert recipe.gross_weight == initial_gross


def test_remove_nonexistent_row_returns_false():
    """
    Проверка удаления отсутствующего ингредиента.
    """
    # Подготовка
    gram = range_model.create_gram()
    group = nomenclature_group_model.create_raw()
    nom1 = nomenclature_model.create("Мука", "Мука", group, gram)
    nom2 = nomenclature_model.create("Дрожжи", "Дрожжи", group, gram)
    row1 = recipe_row_model.create(nom1, brutto=100.0, netto=100.0, range=gram)
    row2 = recipe_row_model.create(nom2, brutto=10.0, netto=10.0, range=gram)
    recipe = recipe_model.create(name="Рецепт", rows=[row1])

    # Действие
    result = recipe.remove_row(row2)

    # Проверки
    assert result is False
    assert len(recipe.rows) == 1


def test_recipe_key_returns_recipe_model():
    """
    Проверка статического метода storage_manager.recipe_key().
    """
    # Подготовка
    # Действие
    key = storage_manager.recipe_key()

    # Проверки
    assert key == "recipe_model"


def test_first_start_recipes_present_in_storage():
    """
    Проверка наличия рецептов при первом старте.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    recipes = manager.get(storage_manager.recipe_key())

    # Проверки
    assert isinstance(recipes, list)
    assert len(recipes) > 0
    assert all(isinstance(r, recipe_model) for r in recipes)


def test_first_start_contains_pizza_margarita():
    """
    Проверка наличия рецепта Пицца Маргарита при первом старте.
    """
    # Подготовка
    manager = storage_manager()

    # Действие
    recipes = manager.get(storage_manager.recipe_key())
    margarita = next((r for r in recipes if "Пицца Маргарита" in r.name), None)

    # Проверки
    assert margarita is not None
    assert isinstance(margarita, recipe_model)


def test_first_start_margarita_contains_semi_finished():
    """
    Проверка наличия полуфабрикатов в рецепте Пицца Маргарита.
    """
    # Подготовка
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())

    # Действие
    margarita = next((r for r in recipes if r.name == "Пицца Маргарита"), None)

    # Проверки
    assert margarita is not None
    assert margarita.has_semi_finished is True
    assert len(margarita.semi_finished_items) >= 2

    semi_names = [r.nomenclature.name for r in margarita.semi_finished_items]
    assert any("Тесто дрожжевое" in name for name in semi_names)
    assert any("Соус томатный" in name for name in semi_names)


def test_first_start_contains_recipe_with_packaging():
    """
    Проверка наличия упаковки в рецепте.
    """
    # Подготовка
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())

    # Действие
    packaged_recipe = next((r for r in recipes if r.has_packaging), None)

    # Проверки
    assert packaged_recipe is not None
    assert packaged_recipe.has_packaging is True
    assert len(packaged_recipe.packaging_items) > 0
    assert any("Коробка" in r.nomenclature.name for r in packaged_recipe.packaging_items)


def test_first_start_margarita_gross_and_net_weights():
    """
    Проверка точного расчета веса Брутто и Нетто для рецепта Пицца Маргарита
    с учетом рекурсивного раскрытия полуфабрикатов.
    """
    # Подготовка
    manager = storage_manager()
    recipes = manager.get(storage_manager.recipe_key())

    # Действие
    margarita = next((r for r in recipes if r.name == "Пицца Маргарита"), None)

    # Проверки
    assert margarita is not None
    assert margarita.gross_weight == pytest.approx(574.0, abs=1.0)
    assert margarita.net_weight == 531.0


def test_domain_models_factory_methods():
    """
    Проверка фабричных методов доменных моделей.
    """
    # Подготовка
    # Действие
    unit_gram = range_model.create_gram()
    unit_kilo = range_model.create_kilogram()
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
    org = organization_model.create(
        "ООО Ромашка",
        inn="7701234567",
        bik="044525225",
        account="40702810900000000001",
        ownership_form="ООО"
    )

    # Проверки
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


def test_recipe_deep_recursive_three_levels():
    """
    Проверка глубокой рекурсии (3+ уровня вложенности):
    Пирог -> Тесто дрожжевое -> Закваска -> Мука и Вода.
    """
    # Подготовка
    gram = range_model.create_gram()
    raw_group = nomenclature_group_model.create_raw()
    semi_group = nomenclature_group_model.create_semi_finished()

    # Уровень 3: Сырье
    flour = nomenclature_model.create("Мука для закваски", "Мука", raw_group, gram)
    water = nomenclature_model.create("Вода для закваски", "Вода", raw_group, gram)

    # Уровень 2: Закваска (Рецепт 1)
    sourdough_row1 = recipe_row_model.create(flour, brutto=60.0, netto=50.0, range=gram)
    sourdough_row2 = recipe_row_model.create(water, brutto=40.0, netto=40.0, range=gram)
    sourdough_recipe = recipe_model.create("Закваска", rows=[sourdough_row1, sourdough_row2])
    # Нетто закваски = 50 + 40 = 90 г, Брутто = 100 г

    sourdough_nom = nomenclature_model.create("Закваска", "Закваска", semi_group, gram, recipe=sourdough_recipe)

    # Уровень 1: Тесто дрожжевое (Рецепт 2)
    # Использует 45 г закваски (фактор масштабирования 45 / 90 = 0.5)
    # Брутто из закваски = 100 * 0.5 = 50 г
    sugar = nomenclature_model.create("Сахар", "Сахар", raw_group, gram)
    dough_row1 = recipe_row_model.create(sourdough_nom, brutto=50.0, netto=45.0, range=gram)
    dough_row2 = recipe_row_model.create(sugar, brutto=20.0, netto=20.0, range=gram)
    dough_recipe = recipe_model.create("Тесто дрожжевое", rows=[dough_row1, dough_row2])
    # Нетто теста = 45 + 20 = 65 г. Брутто теста = 50 (закваска) + 20 (сахар) = 70 г

    dough_nom = nomenclature_model.create("Тесто дрожжевое", "Тесто", semi_group, gram, recipe=dough_recipe)

    # Уровень 0: Пирог (Рецепт 3)
    # Использует 65 г теста (фактор масштабирования 65 / 65 = 1.0)
    # Брутто из теста = 70 г
    apple = nomenclature_model.create("Яблоко", "Яблоко", raw_group, gram)
    pie_row1 = recipe_row_model.create(dough_nom, brutto=70.0, netto=65.0, range=gram)
    pie_row2 = recipe_row_model.create(apple, brutto=100.0, netto=80.0, range=gram)
    pie_recipe = recipe_model.create("Пирог яблочный", rows=[pie_row1, pie_row2])

    # Действие
    total_gross = pie_recipe.gross_weight
    total_net = pie_recipe.net_weight

    # Проверки
    # Рекурсивный брутто: яблоко (100) + тесто (70) = 170.0 г
    # Рекурсивный нетто: яблоко (80) + тесто (65) = 145.0 г
    assert total_gross == pytest.approx(170.0, abs=0.01)
    assert total_net == pytest.approx(145.0, abs=0.01)


def test_recipe_circular_dependency_raises_operation_exception():
    """
    Проверка обнаружения циклической зависимости в полуфабрикатах (Блюдо A -> Блюдо B -> Блюдо A).
    Должно возбуждаться исключение operation_exception.
    """
    # Подготовка
    gram = range_model.create_gram()
    semi_group = nomenclature_group_model.create_semi_finished()

    # Заготовка рецепта A
    recipe_a = recipe_model.create("Рецепт A", rows=[])
    nom_a = nomenclature_model.create("Номенклатура A", "Номенклатура A", semi_group, gram, recipe=recipe_a)

    # Рецепт B ссылается на номенклатуру A
    row_for_b = recipe_row_model.create(nom_a, brutto=100.0, netto=90.0, range=gram)
    recipe_b = recipe_model.create("Рецепт B", rows=[row_for_b])
    nom_b = nomenclature_model.create("Номенклатура B", "Номенклатура B", semi_group, gram, recipe=recipe_b)

    # Рецепт A ссылается на номенклатуру B (цикл!)
    row_for_a = recipe_row_model.create(nom_b, brutto=100.0, netto=90.0, range=gram)
    recipe_a.add_row(row_for_a)

    # Действие
    with pytest.raises(operation_exception):
        _ = recipe_a.gross_weight

    # Проверки
    assert True


def test_recipe_mixed_units_kg_and_gram():
    """
    Проверка корректности расчета веса при смешанных единицах измерения (кг и грамм).
    """
    # Подготовка
    gram = range_model.create_gram()
    kg = range_model.create_kilogram()
    raw_group = nomenclature_group_model.create_raw()

    flour = nomenclature_model.create("Мука", "Мука", raw_group, kg)
    salt = nomenclature_model.create("Соль", "Соль", raw_group, gram)

    # 1.5 кг муки (брутто 1.5 кг, нетто 1.4 кг)
    row_flour = recipe_row_model.create(flour, brutto=1.5, netto=1.4, range=kg)
    # 20 г соли (брутто 20 г, нетто 20 г)
    row_salt = recipe_row_model.create(salt, brutto=20.0, netto=20.0, range=gram)

    # Действие
    recipe = recipe_model.create("Замес мучной", rows=[row_flour, row_salt])
    gross_flour_base = row_flour.range.to_base(row_flour.brutto)
    net_flour_base = row_flour.range.to_base(row_flour.netto)

    # Проверки
    assert gross_flour_base == 1500.0
    assert net_flour_base == 1400.0
    assert recipe.gross_weight == 21.5
    assert recipe.net_weight == 21.4
