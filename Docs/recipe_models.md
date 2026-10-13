# Диаграмма классов — Доменные модели рецептов (технологических карт)

## Описание
В рамках предметной области сети ресторанов «Ромашка» реализована подсистема технологических карт (рецептов) для производственного учета:
- `recipe_model`: технологическая карта блюда или заготовки. Вычисляет общий вес Брутто и Нетто путем суммирования весов всех входящих ингредиентов. Содержит ссылки на полуфабрикаты, готовую продукцию, шаги приготовления и упаковочные материалы.
- `recipe_row_model`: строка технологической карты (ингредиент блюда). Хранит ссылку на позицию номенклатуры (`nomenclature_model`), вес Брутто, вес Нетто и единицу измерения (`range_model`).
- `recipe_step_model`: этап (шаг) технологического процесса приготовления (номер, наименование, описание, продолжительность).

## UML диаграмма классов

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
