import os
import re
from src.core.abstract_model import name_id
from src.core.exception import arguments_exception
from src.models.recipe_row_model import recipe_row_model
from src.models.recipe_step_model import recipe_step_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model


class recipe_model(name_id):
    """
    Модель технологической карты (рецепта).
    Хранит состав блюда (список строк-ингредиентов), технологические этапы приготовления,
    выход готовой продукции, норматив и рассчитывает общий вес Брутто и Нетто.
    """

    def __init__(
        self,
        name: str = "",
        rows: list = None,
        steps: list = None,
        target_nomenclature: nomenclature_model = None,
        category: str = "",
        output: str = "",
        standard: str = "",
        cooking_time: float = 0.0,
        description: str = ""
    ) -> None:
        """
        Инициализирует технологическую карту (рецепт).

        :param name: Наименование рецепта (до 50 символов)
        :param rows: Список строк-ингредиентов (recipe_row_model)
        :param steps: Список технологических шагов (recipe_step_model)
        :param target_nomenclature: Готовая продукция, выпускаемая по рецепту
        :param category: Категория рецепта (например, "Готовая продукция")
        :param output: Выход готового блюда (например, "1 пицца Ø 30 см (600 г)")
        :param standard: Нормативный документ (например, "Технологическая карта № ТК-001")
        :param cooking_time: Время приготовления в минутах
        :param description: Общее описание или примечания
        """
        super().__init__(name=name)

        self.__rows: list[recipe_row_model] = []
        self.__steps: list[recipe_step_model] = []
        self.__target_nomenclature: nomenclature_model = None
        self.__category: str = ""
        self.__output: str = ""
        self.__standard: str = ""
        self.__cooking_time: float = 0.0
        self.__description: str = ""

        if rows:
            for row in rows:
                self.add_row(row)

        if steps:
            for step in steps:
                self.add_step(step)

        if target_nomenclature is not None:
            self.target_nomenclature = target_nomenclature

        self.category = category
        self.output = output
        self.standard = standard
        self.cooking_time = cooking_time
        self.description = description

    # ─────────────────────────── Расчётные свойства веса ───────────────────────────

    @property
    def gross_weight(self) -> float:
        """
        Общий вес Брутто рецепта (сумма весов Брутто каждого ингредиента).
        """
        return round(sum(row.brutto for row in self.__rows), 4)

    @property
    def brutto(self) -> float:
        """
        Псевдоним (алиас) для свойства gross_weight.
        """
        return self.gross_weight

    @property
    def gross(self) -> float:
        """
        Псевдоним (алиас) для свойства gross_weight.
        """
        return self.gross_weight

    @property
    def weight_brutto(self) -> float:
        """
        Псевдоним (алиас) для свойства gross_weight.
        """
        return self.gross_weight

    @property
    def net_weight(self) -> float:
        """
        Общий вес Нетто рецепта (сумма весов Нетто каждого ингредиента).
        """
        return round(sum(row.netto for row in self.__rows), 4)

    @property
    def netto(self) -> float:
        """
        Псевдоним (алиас) для свойства net_weight.
        """
        return self.net_weight

    @property
    def net(self) -> float:
        """
        Псевдоним (алиас) для свойства net_weight.
        """
        return self.net_weight

    @property
    def weight_netto(self) -> float:
        """
        Псевдоним (алиас) для свойства net_weight.
        """
        return self.net_weight

    # ─────────────────────────── Управление ингредиентами ─────────────────────────

    @property
    def rows(self) -> list:
        """
        Список строк рецепта (ингредиентов).
        """
        return self.__rows

    @property
    def ingredients(self) -> list:
        """
        Псевдоним (алиас) для свойства rows.
        """
        return self.__rows

    def add_row(self, row: recipe_row_model) -> bool:
        """
        Добавляет строку (ингредиент) в рецепт.

        :param row: Экземпляр recipe_row_model
        :return: True, если ингредиент добавлен; False, если он уже присутствует
        """
        if not isinstance(row, recipe_row_model):
            raise arguments_exception("row", "Ингредиент должен быть экземпляром recipe_row_model")

        if row in self.__rows:
            return False

        self.__rows.append(row)
        return True

    def add_ingredient(self, ingredient: recipe_row_model) -> bool:
        """
        Псевдоним (алиас) для метода add_row.
        """
        return self.add_row(ingredient)

    def remove_row(self, row: recipe_row_model) -> bool:
        """
        Исключает строку (ингредиент) из рецепта.

        :param row: Экземпляр recipe_row_model
        :return: True, если строка удалена; False, если строка не найдена
        """
        if row in self.__rows:
            self.__rows.remove(row)
            return True
        return False

    def remove_ingredient(self, ingredient: recipe_row_model) -> bool:
        """
        Псевдоним (алиас) для метода remove_row.
        """
        return self.remove_row(ingredient)

    def delete_row(self, row: recipe_row_model) -> bool:
        """
        Псевдоним (алиас) для метода remove_row.
        """
        return self.remove_row(row)

    def delete_ingredient(self, ingredient: recipe_row_model) -> bool:
        """
        Псевдоним (алиас) для метода remove_row.
        """
        return self.remove_row(ingredient)

    # ─────────────────────────── Управление шагами приготовления ───────────────────

    @property
    def steps(self) -> list:
        """
        Список технологических этапов (шагов) рецепта.
        """
        return self.__steps

    def add_step(self, step: recipe_step_model) -> bool:
        """
        Добавляет этап приготовления в технологическую карту.

        :param step: Экземпляр recipe_step_model
        :return: True при успешном добавлении; False, если шаг уже присутствует
        """
        if not isinstance(step, recipe_step_model):
            raise arguments_exception("step", "Шаг рецепта должен быть экземпляром recipe_step_model")

        if step in self.__steps:
            return False

        self.__steps.append(step)
        return True

    def remove_step(self, step: recipe_step_model) -> bool:
        """
        Удаляет этап приготовления из рецепта.
        """
        if step in self.__steps:
            self.__steps.remove(step)
            return True
        return False

    # ─────────────────────────── Прочие свойства ───────────────────────────────────

    @property
    def target_nomenclature(self) -> nomenclature_model:
        """
        Готовая продукция, создаваемая по рецепту.
        """
        return self.__target_nomenclature

    @target_nomenclature.setter
    def target_nomenclature(self, value: nomenclature_model) -> None:
        """
        Устанавливает готовую продукцию рецепта.
        """
        if value is not None and not isinstance(value, nomenclature_model):
            raise arguments_exception("target_nomenclature", "Целевая номенклатура должна быть nomenclature_model")

        self.__target_nomenclature = value

    @property
    def category(self) -> str:
        """
        Категория блюда (например, "Готовая продукция").
        """
        return self.__category

    @category.setter
    def category(self, value: str) -> None:
        """
        Устанавливает категорию блюда.
        """
        self.__category = str(value).strip() if value is not None else ""

    @property
    def output(self) -> str:
        """
        Выход готового блюда (например, "1 пицца Ø 30 см (600 г)").
        """
        return self.__output

    @output.setter
    def output(self, value: str) -> None:
        """
        Устанавливает выход готового блюда.
        """
        self.__output = str(value).strip() if value is not None else ""

    @property
    def standard(self) -> str:
        """
        Стандарт или номер технологической карты.
        """
        return self.__standard

    @standard.setter
    def standard(self, value: str) -> None:
        """
        Устанавливает стандарт или номер ТК.
        """
        self.__standard = str(value).strip() if value is not None else ""

    @property
    def cooking_time(self) -> float:
        """
        Время приготовления в минутах.
        """
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: float) -> None:
        """
        Устанавливает время приготовления в минутах.
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("cooking_time", "Время приготовления должно быть числом")

        if value < 0:
            raise arguments_exception("cooking_time", "Время приготовления не может быть отрицательным")

        self.__cooking_time = float(value)

    @property
    def description(self) -> str:
        """
        Описание технологической карты.
        """
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        """
        Устанавливает описание технологической карты.
        """
        self.__description = str(value).strip() if value is not None else ""

    # ─────────────────────────── Проверки состава (полуфабрикаты / упаковка) ───────

    @property
    def semi_finished_items(self) -> list:
        """
        Возвращает список ингредиентов, относящихся к категории 'Полуфабрикаты'.
        """
        result = []
        for row in self.__rows:
            if (
                row.nomenclature is not None
                and row.nomenclature.group is not None
                and row.nomenclature.group.name == "Полуфабрикаты"
            ):
                result.append(row)
        return result

    @property
    def has_semi_finished(self) -> bool:
        """
        Флаг наличия полуфабрикатов в составе рецепта.
        """
        return len(self.semi_finished_items) > 0

    @property
    def packaging_items(self) -> list:
        """
        Возвращает список ингредиентов, относящихся к категории 'Упаковка'.
        """
        result = []
        for row in self.__rows:
            if (
                row.nomenclature is not None
                and row.nomenclature.group is not None
                and row.nomenclature.group.name == "Упаковка"
            ):
                result.append(row)
        return result

    @property
    def has_packaging(self) -> bool:
        """
        Флаг наличия упаковки в составе рецепта.
        """
        return len(self.packaging_items) > 0

    # ─────────────────────────── Фабричные методы ─────────────────────────────────

    @staticmethod
    def create(
        name: str = "",
        rows: list = None,
        steps: list = None,
        target_nomenclature: nomenclature_model = None,
        category: str = "",
        output: str = "",
        standard: str = "",
        cooking_time: float = 0.0,
        description: str = ""
    ) -> 'recipe_model':
        """
        Универсальный фабричный метод создания технологической карты (рецепта).

        :param name: Название рецепта
        :param rows: Список строк-ингредиентов
        :param steps: Список шагов приготовления
        :param target_nomenclature: Целевая номенклатура
        :param category: Категория
        :param output: Выход блюда
        :param standard: Норматив ТК
        :param cooking_time: Время приготовления
        :param description: Описание
        :return: Экземпляр recipe_model
        """
        return recipe_model(
            name=name,
            rows=rows,
            steps=steps,
            target_nomenclature=target_nomenclature,
            category=category,
            output=output,
            standard=standard,
            cooking_time=cooking_time,
            description=description
        )

    @staticmethod
    def create_pizza_margarita(
        ranges: list = None,
        groups: list = None,
        nomenclatures: list = None
    ) -> 'recipe_model':
        """
        Фабричный метод создания рецепта 'Пицца Маргарита' строго по спецификации Docs/Recipe.md.
        Содержит полуфабрикаты ('Тесто дрожжевое', 'Соус томатный') и рассчитывает Брутто и Нетто.

        :param ranges: Справочник единиц измерения (опционально)
        :param groups: Справочник групп номенклатуры (опционально)
        :param nomenclatures: Справочник номенклатуры (опционально)
        :return: Настроенный экземпляр recipe_model
        """
        # Вспомогательные функции поиска
        def get_range(name: str) -> range_model:
            if ranges:
                item = next((r for r in ranges if r.name == name), None)
                if item: return item
            if name == "грамм": return range_model.create_gram()
            if name == "миллилитр": return range_model.create_milliliter()
            if name == "килограмм": return range_model.create_kilogramm()
            if name == "штука": return range_model.create_piece()
            return range_model.create(name)

        def get_group(name: str) -> nomenclature_group_model:
            if groups:
                item = next((g for g in groups if g.name == name), None)
                if item: return item
            if name == "Сырьё": return nomenclature_group_model.create_raw()
            if name == "Полуфабрикаты": return nomenclature_group_model.create_semi_finished()
            if name == "Готовая продукция": return nomenclature_group_model.create_finished()
            if name == "Упаковка": return nomenclature_group_model.create_packaging()
            return nomenclature_group_model.create(name)

        def get_nomenclature(name: str, grp_name: str, rng_name: str, full_name: str = "") -> nomenclature_model:
            if nomenclatures:
                item = next((n for n in nomenclatures if n.name == name), None)
                if item: return item
            g = get_group(grp_name)
            r = get_range(rng_name)
            return nomenclature_model.create(name, full_name or name, g, r)

        gram = get_range("грамм")
        ml = get_range("миллилитр")

        # Номенклатурные позиции по Recipe.md
        dough = get_nomenclature("Тесто дрожжевое", "Полуфабрикаты", "грамм", "Тесто дрожжевое, полуфабрикат")
        sauce = get_nomenclature("Соус томатный", "Полуфабрикаты", "грамм", "Соус томатный, полуфабрикат")
        mozzarella = get_nomenclature("Сыр Моцарелла", "Сырьё", "грамм", "Сыр Моцарелла для пиццы")
        olive_oil = get_nomenclature("Масло оливковое", "Сырьё", "миллилитр", "Масло оливковое Extra Virgin")
        basil = get_nomenclature("Базилик свежий", "Сырьё", "грамм", "Базилик свежий листья")
        salt = get_nomenclature("Соль пищевая", "Сырьё", "грамм", "Соль пищевая поваренная")

        # Строки рецепта (состав на 1 порцию)
        # Брутто 280, Нетто 250
        row1 = recipe_row_model.create(dough, 280.0, 250.0, gram, "Тесто дрожжевое (полуфабрикат)")
        # Брутто 120, Нетто 100
        row2 = recipe_row_model.create(sauce, 120.0, 100.0, gram, "Соус томатный (полуфабрикат)")
        # Брутто 180, Нетто 150
        row3 = recipe_row_model.create(mozzarella, 180.0, 150.0, gram, "Сыр Моцарелла")
        # Брутто 20, Нетто 20
        row4 = recipe_row_model.create(olive_oil, 20.0, 20.0, ml, "Масло оливковое")
        # Брутто 10, Нетто 8
        row5 = recipe_row_model.create(basil, 10.0, 8.0, gram, "Базилик свежий")
        # Брутто 3, Нетто 3
        row6 = recipe_row_model.create(salt, 3.0, 3.0, gram, "Соль пищевая")

        # Технологические этапы по Recipe.md
        steps = [
            recipe_step_model.create(1, "Подготовка теста", "Раскатать тесто до круга 30–32 см толщиной 3–4 мм", 20.0),
            recipe_step_model.create(2, "Нанесение соуса", "Выложить 100 г соуса, распределить, отступив 2 см от края", 3.0),
            recipe_step_model.create(3, "Сборка", "Нарезать моцареллу, распределить, сбрызнуть маслом, посолить", 5.0),
            recipe_step_model.create(4, "Выпекание", "Выпекать при 250–270 °C в течение 8–12 минут", 10.0),
            recipe_step_model.create(5, "Подача", "Разложить свежий базилик, нарезать на 8 секторов, подать горячей", 2.0),
        ]

        pizza_nom = get_nomenclature(
            "Пицца Маргарита", "Готовая продукция", "штука", "Пицца Маргарита классическая 30 см"
        )

        recipe = recipe_model.create(
            name="Пицца Маргарита",
            rows=[row1, row2, row3, row4, row5, row6],
            steps=steps,
            target_nomenclature=pizza_nom,
            category="Готовая продукция",
            output="1 пицца Ø 30 см (600 г)",
            standard="Технологическая карта № ТК-001",
            cooking_time=45.0,
            description="Классическая неаполитанская пицца Маргарита со свежим базиликом и моцареллой"
        )

        return recipe

    @staticmethod
    def create_pizza_with_packaging(
        ranges: list = None,
        groups: list = None,
        nomenclatures: list = None
    ) -> 'recipe_model':
        """
        Фабричный метод создания рецепта 'Пицца Маргарита с упаковкой' для службы доставки.
        Содержит как полуфабрикаты, так и упаковочный материал ('Коробка под пиццу 30 см').

        :param ranges: Справочник единиц измерения (опционально)
        :param groups: Справочник групп номенклатуры (опционально)
        :param nomenclatures: Справочник номенклатуры (опционально)
        :return: Настроенный экземпляр recipe_model с упаковкой
        """
        # Базовый рецепт пиццы
        base_recipe = recipe_model.create_pizza_margarita(
            ranges=ranges,
            groups=groups,
            nomenclatures=nomenclatures
        )

        def get_range(name: str) -> range_model:
            if ranges:
                item = next((r for r in ranges if r.name == name), None)
                if item: return item
            if name == "штука": return range_model.create_piece()
            return range_model.create(name)

        def get_group(name: str) -> nomenclature_group_model:
            if groups:
                item = next((g for g in groups if g.name == name), None)
                if item: return item
            return nomenclature_group_model.create_packaging()

        def get_nomenclature(name: str) -> nomenclature_model:
            if nomenclatures:
                item = next((n for n in nomenclatures if n.name == name), None)
                if item: return item
            g = get_group("Упаковка")
            r = get_range("штука")
            return nomenclature_model.create(name, "Картонная коробка 300х300х40 мм", g, r)

        box_nom = get_nomenclature("Коробка под пиццу 30 см")
        piece = get_range("штука")

        # Добавляем упаковку в состав (брутто: 150 г коробка, нетто: 0 г съедобной части)
        box_row = recipe_row_model.create(box_nom, 150.0, 0.0, piece, "Коробка 30 см (упаковка)")

        packaged_rows = [
            recipe_row_model.create(r.nomenclature, r.brutto, r.netto, r.range, r.name)
            for r in base_recipe.rows
        ]
        packaged_rows.append(box_row)

        recipe = recipe_model.create(
            name="Пицца Маргарита с упаковкой",
            rows=packaged_rows,
            steps=base_recipe.steps,
            target_nomenclature=base_recipe.target_nomenclature,
            category="Готовая продукция",
            output="1 пицца Ø 30 см в упаковке (750 г)",
            standard="Технологическая карта № ТК-001/Д",
            cooking_time=47.0,
            description="Пицца Маргарита в индивидуальной картонной коробке для курьерской доставки"
        )

        return recipe

    @staticmethod
    def from_markdown(
        markdown_text: str,
        ranges: list = None,
        groups: list = None,
        nomenclatures: list = None
    ) -> 'recipe_model':
        """
        Создаёт экземпляр recipe_model путем парсинга текста Markdown-спецификации.

        :param markdown_text: Содержимое файла рецепта в формате Markdown
        :param ranges: Доступные единицы измерения для привязки
        :param groups: Доступные группы номенклатуры для привязки
        :param nomenclatures: Доступная номенклатура для привязки
        :return: Сформированный объект recipe_model
        """
        if not markdown_text or not markdown_text.strip():
            raise arguments_exception("markdown_text", "Текст markdown не может быть пустым")

        # Извлечение наименования
        name_match = re.search(r"#\s*Рецепт:\s*([^\n\r]+)", markdown_text)
        if not name_match:
            name_match = re.search(r"#\s*([^\n\r]+)", markdown_text)
        recipe_name = name_match.group(1).strip() if name_match else "Рецепт"
        if len(recipe_name) > 50:
            recipe_name = recipe_name[:50]

        # Извлечение метаданных
        cat_match = re.search(r"\*\*Категория:\*\*\s*([^\n\r]+)", markdown_text)
        category = cat_match.group(1).strip() if cat_match else ""

        time_match = re.search(r"\*\*Время приготовления:\*\*\s*(\d+)", markdown_text)
        cooking_time = float(time_match.group(1)) if time_match else 0.0

        out_match = re.search(r"\*\*Выход:\*\*\s*([^\n\r]+)", markdown_text)
        output = out_match.group(1).strip() if out_match else ""

        std_match = re.search(r"\*\*Стандарт:\*\*\s*([^\n\r]+)", markdown_text)
        standard = std_match.group(1).strip() if std_match else ""

        # Хелперы разрешения сущностей
        def resolve_range(r_name: str) -> range_model:
            cleaned = r_name.strip().lower()
            mapping = {"г": "грамм", "мл": "миллилитр", "кг": "килограмм", "л": "литр", "шт": "штука"}
            full_unit = mapping.get(cleaned, cleaned)
            if ranges:
                found = next((r for r in ranges if r.name.lower() in (cleaned, full_unit)), None)
                if found: return found
            if full_unit == "грамм": return range_model.create_gram()
            if full_unit == "миллилитр": return range_model.create_milliliter()
            if full_unit == "килограмм": return range_model.create_kilogramm()
            if full_unit == "штука": return range_model.create_piece()
            return range_model.create(full_unit)

        def resolve_group(g_name: str) -> nomenclature_group_model:
            if groups:
                found = next((g for g in groups if g.name == g_name), None)
                if found: return found
            if g_name == "Полуфабрикаты": return nomenclature_group_model.create_semi_finished()
            if g_name == "Сырьё": return nomenclature_group_model.create_raw()
            if g_name == "Готовая продукция": return nomenclature_group_model.create_finished()
            if g_name == "Упаковка": return nomenclature_group_model.create_packaging()
            return nomenclature_group_model.create(g_name)

        def resolve_nomenclature(raw_name: str, unit_name: str) -> nomenclature_model:
            clean_name = re.sub(r"\(.*?\)", "", raw_name).strip()
            if nomenclatures:
                found = next((n for n in nomenclatures if n.name.lower() == clean_name.lower() or clean_name.lower() in n.name.lower()), None)
                if found: return found

            grp_name = "Полуфабрикаты" if "полуфабрикат" in raw_name.lower() else "Сырьё"
            return nomenclature_model.create(
                clean_name[:50],
                raw_name,
                resolve_group(grp_name),
                resolve_range(unit_name)
            )

        # Парсинг таблицы состава: | Наименование | Единица | Брутто | Нетто |
        rows = []
        table_pattern = re.compile(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+(?:\.\d+)?)\s*\|\s*(\d+(?:\.\d+)?)\s*\|")
        for line in markdown_text.splitlines():
            line_str = line.strip()
            if "Наименование" in line_str or "---" in line_str:
                continue
            m = table_pattern.match(line_str)
            if m:
                raw_nom_name = m.group(1).strip()
                unit_str = m.group(2).strip()
                brutto_val = float(m.group(3))
                netto_val = float(m.group(4))

                nom = resolve_nomenclature(raw_nom_name, unit_str)
                rng = resolve_range(unit_str)
                row = recipe_row_model.create(
                    nomenclature=nom,
                    brutto=brutto_val,
                    netto=netto_val,
                    range=rng,
                    name=raw_nom_name[:50]
                )
                rows.append(row)

        # Парсинг шагов приготовления
        steps = []
        step_pattern = re.compile(r"###\s*(\d+)\.\s*([^\n\r]+)")
        for m in step_pattern.finditer(markdown_text):
            num = int(m.group(1))
            st_name = m.group(2).strip()
            steps.append(recipe_step_model.create(step_number=num, name=st_name))

        return recipe_model.create(
            name=recipe_name,
            rows=rows,
            steps=steps,
            category=category,
            output=output,
            standard=standard,
            cooking_time=cooking_time
        )

    @staticmethod
    def from_file(
        file_path: str,
        ranges: list = None,
        groups: list = None,
        nomenclatures: list = None
    ) -> 'recipe_model':
        """
        Загружает и парсит рецепт из Markdown-файла.

        :param file_path: Путь к файлу с рецептом
        :param ranges: Справочник единиц измерения
        :param groups: Справочник групп
        :param nomenclatures: Справочник номенклатуры
        :return: Экземпляр recipe_model
        """
        if not os.path.exists(file_path):
            raise arguments_exception("file_path", f"Файл не найден: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return recipe_model.from_markdown(content, ranges, groups, nomenclatures)
