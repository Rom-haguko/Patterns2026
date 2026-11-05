# Диаграмма классов — convert_factory и конверторы

## Описание

Подсистема сериализации доменных объектов в словари и JSON:

- `abstract_converter` задаёт общий контракт конвертора;
- `basic_convertor`, `datetime_convertor` и `reference_convertor` преобразуют разные типы значений;
- `convert_factory` подбирает нужный конвертор, а `json_serializer` отвечает непосредственно за JSON.

Контракт `convert` строгий: метод всегда принимает имя поля и значение. Метод `convert_value` используется для рекурсивной обработки значения без обёртки в словарь. Он поддерживает `None`, перечисления, списки, кортежи, множества и словари. Если тип значения неизвестен, выбрасывается `arguments_exception`, а не возвращается пустой словарь.

`reference_convertor` обходит публичные свойства объекта, складывает их в словарь и защищается от повторного входа в один и тот же объект. Для этого используется множество `visited`, а ошибки чтения свойств ограничены `AttributeError`.

Сериализованные примеры моделей находятся в директории `Docs/json/`.

## UML диаграмма классов

```mermaid
classDiagram
    direction TB

    class abstract_converter {
        <<abstract>>
        +convert(field: str, value: object) dict
    }

    class basic_convertor {
        +convert(field: str, value: object) dict
    }

    class datetime_convertor {
        +convert(field: str, value: object) dict
    }

    class reference_convertor {
        -__factory: abstract_converter_factory
        -__visited: set[int]
        +convert(field: str, value: object) dict
        -_convert_reference_object(source: object) dict
        -_convert_field_value(prop_name: str, val: object) object
        -_extract_field_names(source: object) list[str]
    }

    class abstract_converter_factory {
        <<abstract>>
        +get_converter(value_or_type: object) abstract_converter
        +convert_value(source: object) object
    }

    class convert_factory {
        -__mapping: dict[type, abstract_converter]
        +basic_convertor: basic_convertor
        +datetime_convertor: datetime_convertor
        +reference_convertor: reference_convertor
        +get_converter(value_or_type: object) abstract_converter
        +convert_value(source: object) object
    }

    class json_serializer {
        -__factory: convert_factory
        +to_json(source: object, indent: int) str
        +to_json_file(source: object, file_path: str, indent: int) None
    }

    abstract_converter <|-- basic_convertor : наследует
    abstract_converter <|-- datetime_convertor : наследует
    abstract_converter <|-- reference_convertor : наследует

    abstract_converter_factory <|.. convert_factory : реализует

    convert_factory "1" --> "1" basic_convertor : содержит
    convert_factory "1" --> "1" datetime_convertor : содержит
    convert_factory "1" --> "1" reference_convertor : содержит

    reference_convertor --> abstract_converter_factory : использует
    json_serializer --> convert_factory : использует
```

## Как это работает по шагам

1. `json_serializer.to_json` передаёт объект в `convert_factory.convert_value`.
2. `convert_value` обрабатывает `None`, перечисления и составные структуры через словарь обработчиков, а для остальных значений вызывает `get_converter`.
3. `get_converter` выбирает конвертор по словарю типов. Если подходящего типа нет, используется `reference_convertor`.
4. `reference_convertor` обходит поля объекта и для каждого значения обращается к фабрике.
5. Готовый словарь возвращается в `json_serializer`, где `json.dumps` превращает его в строку JSON.
6. `json_serializer.to_json_file` сохраняет эту строку в файл в кодировке UTF-8.

Конверторы работают только со словарями и примитивными значениями. За формат файла отвечает отдельный `json_serializer`.
