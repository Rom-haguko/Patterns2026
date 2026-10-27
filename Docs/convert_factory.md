# Диаграмма классов — convert_factory и конверторы

## Описание

В этой итерации я сделал подсистему сериализации доменных объектов в словари и JSON. Она разделена на три части:

- `abstract_covertor` задаёт общий контракт конвертора;
- `basic_convertor`, `datetime_convertor` и `reference_convertor` преобразуют разные типы значений;
- `convert_factory` подбирает нужный конвертор, а `json_serializer` отвечает уже непосредственно за JSON.

Контракт `convert` строгий: метод всегда принимает имя поля и значение. Отдельный метод `convert_value` нужен для рекурсивной обработки значения без обёртки в словарь. Он поддерживает `None`, перечисления, списки, кортежи, множества и словари. Если тип значения неизвестен, выбрасывается `argument_exception`, а не возвращается пустой словарь.

`reference_convertor` обходит публичные свойства объекта, складывает их в словарь и защищается от повторного входа в один и тот же объект. Для этого используется множество `visited`, а ошибки чтения свойств ограничены `AttributeError`.

Сериализованные примеры моделей лежат в папке `Docs/json/`.

## UML диаграмма классов

```mermaid
classDiagram
    direction TB

    class abstract_covertor {
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
        -__factory: abstract_convertor_factory
        -__visited: set[int]
        +convert(field: str, value: object) dict
        -_convert_reference_object(source: object) dict
        -_convert_field_value(prop_name: str, val: object) object
        -_extract_field_names(source: object) list[str]
    }

    class abstract_convertor_factory {
        <<abstract>>
        +get_convertor(value_or_type: object) abstract_covertor
        +convert_value(source: object) object
    }

    class convert_factory {
        -__mapping: dict[type, abstract_covertor]
        +basic_convertor: basic_convertor
        +datetime_convertor: datetime_convertor
        +reference_convertor: reference_convertor
        +get_convertor(value_or_type: object) abstract_covertor
        +convert_value(source: object) object
    }

    class json_serializer {
        -__factory: convert_factory
        +to_json(source: object, indent: int) str
        +to_json_file(source: object, file_path: str, indent: int) None
    }

    abstract_covertor <|-- basic_convertor : наследует
    abstract_covertor <|-- datetime_convertor : наследует
    abstract_covertor <|-- reference_convertor : наследует

    abstract_convertor_factory <|.. convert_factory : реализует

    convert_factory "1" --> "1" basic_convertor : содержит
    convert_factory "1" --> "1" datetime_convertor : содержит
    convert_factory "1" --> "1" reference_convertor : содержит

    reference_convertor --> abstract_convertor_factory : использует
    json_serializer --> convert_factory : использует
```

## Как это работает по шагам

1. `json_serializer.to_json` передаёт объект в `convert_factory.convert_value`.
2. `convert_value` сам обрабатывает `None`, перечисления и составные структуры, а для остальных значений вызывает `get_convertor`.
3. `get_convertor` выбирает конвертор по словарю типов. Если подходящего типа нет, используется `reference_convertor`.
4. `reference_convertor` обходит поля объекта и для каждого значения снова обращается к фабрике.
5. Готовый словарь возвращается в `json_serializer`, где `json.dumps` превращает его в строку JSON.
6. `json_serializer.to_json_file` сохраняет эту строку в файл в кодировке UTF-8.

JSON в конверторах не используется: они работают только со словарями и примитивными значениями. За формат файла отвечает отдельный `json_serializer`.
