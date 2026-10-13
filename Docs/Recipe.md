# Рецепт: Пицца Маргарита

**Категория:** Готовая продукция  
**Время приготовления:** 45 мин (подготовка 20 мин + выпечка 25 мин)  
**Выход:** 1 пицца Ø 30 см (600 г)  
**Стандарт:** Технологическая карта № ТК-001

---

## Состав (на 1 порцию)

| Наименование | Единица | Брутто | Нетто |
|---|---|---|---|
| Тесто дрожжевое (полуфабрикат) | г | 280 | 250 |
| Соус томатный (полуфабрикат) | г | 120 | 100 |
| Сыр Моцарелла | г | 180 | 150 |
| Масло оливковое | мл | 20 | 20 |
| Базилик свежий | г | 10 | 8 |
| Соль пищевая | г | 3 | 3 |

---

## Технология приготовления

### 1. Подготовка теста

1. Достать тесто дрожжевое (полуфабрикат) из холодильника за **30 минут** до начала работы.
2. Раскатать тесто на посыпанной мукой поверхности до круга диаметром **30–32 см**, толщиной **3–4 мм**.
3. Переложить на смазанный маслом противень или пекарский камень.
4. Края теста слегка подвернуть для формирования бортика (~1 см).

### 2. Нанесение соуса

1. Выложить **100 г** томатного соуса (полуфабрикат) на основу теста.
2. Распределить ложкой круговыми движениями, **отступив 2 см** от края.
3. Лёгким движением посолить поверхность соуса (1 г соли).

### 3. Сборка

1. Моцареллу нарезать кружками толщиной **5 мм** или разорвать руками.
2. Равномерно распределить по всей поверхности соуса.
3. Сбрызнуть оливковым маслом (20 мл).
4. Посолить по вкусу (2 г соли).

### 4. Выпекание

| Параметр | Значение |
|---|---|
| Температура | **250–270 °C** |
| Время | **8–12 минут** |
| Режим | Конвекция + нижний нагрев |

> Пицца считается готовой, когда края теста подрумянились, а сыр расплавился и начал слегка пузыриться.

### 5. Подача

1. Вынуть пиццу из духовки. **Дать отдохнуть 2 минуты.**
2. Разложить листья свежего базилика поверх расплавленного сыра.
3. Нарезать на **8 равных секторов** дисковым ножом.
4. Подать немедленно на разогретой тарелке или картонной подложке.

---

## Требования к качеству

| Показатель | Норма |
|---|---|
| Внешний вид | Круглая форма, равномерный румяный цвет корочки |
| Тесто | Хрустящее снаружи, мягкое внутри |
| Начинка | Сыр полностью расплавлен, без подгорания |
| Запах | Характерный аромат выпеченного теста, томатов, базилика |
| Температура подачи | Не ниже **65 °C** |
| Выход готового блюда | **600 ± 20 г** |

---

## Связанные доменные объекты

```
nomenclature_model("Тесто дрожжевое")  →  group: "Полуфабрикаты",  range: "грамм"
nomenclature_model("Соус томатный")    →  group: "Полуфабрикаты",  range: "грамм"
nomenclature_model("Мука пшеничная")   →  group: "Сырьё",          range: "килограмм"
nomenclature_model("Масло подсолнечное")→ group: "Сырьё",          range: "литр"
nomenclature_model("Соль")             →  group: "Сырьё",          range: "килограмм"
nomenclature_model("Коробка 30 см")    →  group: "Упаковка",       range: "штука"
```

## UML диаграмма доменных моделей рецепта

```mermaid
classDiagram
    direction TB

    class name_id {
        <<abstract>>
        -_id: str
        -_name: str
        +id: str
        +name: str
        +__eq__(other) bool
    }

    class recipe_model {
        -__rows: list
        -__steps: list
        -__target_nomenclature: nomenclature_model
        -__category: str
        -__output: str
        -__standard: str
        -__cooking_time: float
        -__description: str
        +gross_weight: float
        +brutto: float
        +net_weight: float
        +netto: float
        +rows: list
        +ingredients: list
        +steps: list
        +target_nomenclature: nomenclature_model
        +category: str
        +output: str
        +standard: str
        +cooking_time: float
        +description: str
        +has_semi_finished: bool
        +semi_finished_items: list
        +has_packaging: bool
        +packaging_items: list
        +add_row(row: recipe_row_model) bool
        +add_ingredient(ingredient: recipe_row_model) bool
        +remove_row(row: recipe_row_model) bool
        +remove_ingredient(ingredient: recipe_row_model) bool
        +add_step(step: recipe_step_model) bool
        +remove_step(step: recipe_step_model) bool
        +create(...) recipe_model$
        +create_pizza_margarita(...) recipe_model$
        +create_pizza_with_packaging(...) recipe_model$
        +from_markdown(markdown_text: str) recipe_model$
        +from_file(file_path: str) recipe_model$
    }

    class recipe_row_model {
        -__nomenclature: nomenclature_model
        -__brutto: float
        -__netto: float
        -__range: range_model
        +nomenclature: nomenclature_model
        +brutto: float
        +gross: float
        +netto: float
        +net: float
        +range: range_model
        +unit: range_model
        +create(...) recipe_row_model$
    }

    class recipe_step_model {
        -__step_number: int
        -__description: str
        -__time_minutes: float
        +step_number: int
        +description: str
        +time_minutes: float
        +create(...) recipe_step_model$
    }

    class nomenclature_model {
        -__max_full_name_length: int = 255
        -__full_name: str
        -__group: nomenclature_group_model
        -__range: range_model
        +full_name: str
        +group: nomenclature_group_model
        +range: range_model
        +create(...) nomenclature_model$
    }

    class nomenclature_group_model {
        +create(name: str) nomenclature_group_model$
        +create_raw() nomenclature_group_model$
        +create_semi_finished() nomenclature_group_model$
        +create_finished() nomenclature_group_model$
        +create_packaging() nomenclature_group_model$
    }

    class range_model {
        -__conversion_factor: float
        -__base_range: range_model
        +conversion_factor: float
        +base_range: range_model
        +create(...) range_model$
        +create_gram() range_model$
        +create_kilogramm() range_model$
        +create_milliliter() range_model$
        +create_liter() range_model$
        +create_piece() range_model$
    }

    class storage_manager {
        -__data: dict
        +recipe_key() str$
        +get(key: str) list
        +add(key: str, item: object) bool
        +convert() bool
        -_build_recipes() None
    }

    name_id <|-- recipe_model : наследует
    name_id <|-- recipe_row_model : наследует
    name_id <|-- recipe_step_model : наследует
    name_id <|-- nomenclature_model : наследует
    name_id <|-- nomenclature_group_model : наследует
    name_id <|-- range_model : наследует

    recipe_model "1" *-- "*" recipe_row_model : содержит строки (композиция)
    recipe_model "1" *-- "*" recipe_step_model : содержит шаги (композиция)
    recipe_model --> "0..1" nomenclature_model : target_nomenclature

    recipe_row_model --> "1" nomenclature_model : nomenclature
    recipe_row_model --> "0..1" range_model : range

    nomenclature_model --> "1" nomenclature_group_model : group
    nomenclature_model --> "1" range_model : range

    storage_manager "1" --> "*" recipe_model : кеширует / хранит
```

---

*Редакция: 2026-10-03 | Автор: Технолог ООО Ромашка*
