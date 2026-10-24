# Диаграмма классов — convert_factory и конверторы

## Описание
Подсистема для перевода объектов в словари и JSON:
- abstract_covertor — базовый абстрактный класс с методом convert.
- basic_convertor — переводит простые типы (числа, строки, булевы значения) в словарь.
- datetime_convertor — переводит дату и время в строковый формат ISO 8601.
- reference_convertor — переводит ссылочные типы (доменные модели) в словари, обходя их поля и защищая от циклов.
- convert_factory — фабрика, которая выбирает нужный конвертор через get_convertor и собирает итоговую структуру.

Сериализованные примеры моделей лежат в папке Docs/json/.

## UML диаграмма классов

```mermaid
classDiagram
    direction TB

    class abstract_covertor {
        <<abstract>>
        +convert(field: str, value: object) dict
        +Convert(field: str, value: object) dict
    }

    class basic_convertor {
        +convert(field: str, value: object) dict
    }

    class datetime_convertor {
        +convert(field: str, value: object) dict
    }

    class reference_convertor {
        -__factory: convert_factory
        -__visited: set
        +convert(field: str, value: object) dict
    }

    class convert_factory {
        -__basic_convertor: basic_convertor
        -__datetime_convertor: datetime_convertor
        -__reference_convertor: reference_convertor
        +get_convertor(value_or_type: object) abstract_covertor
        +convert(source: object) object
        +serialize(source: object) object
        +to_json(source: object, indent: int) str
        +to_json_file(source: object, file_path: str, indent: int) None
    }

    abstract_covertor <|-- basic_convertor : наследует
    abstract_covertor <|-- datetime_convertor : наследует
    abstract_covertor <|-- reference_convertor : наследует

    convert_factory "1" --> "1" basic_convertor : содержит
    convert_factory "1" --> "1" datetime_convertor : содержит
    convert_factory "1" --> "1" reference_convertor : содержит
    reference_convertor --> convert_factory : использует
```
