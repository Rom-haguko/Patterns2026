# Диаграмма классов — json_deserializer и фабрика десериализаторов

## Описание

Подсистема десериализации JSON в доменные модели и структуры данных:

- `abstract_deserializer` задаёт общий контракт десериализатора;
- `basic_deserializer`, `datetime_deserializer` и `model_deserializer` преобразуют различные типы данных;
- `deserializer_factory` подбирает нужный десериализатор по зарегистрированным типам базовых значений и динамически разрешает классы моделей по строковым ключам и свойству `type`;
- `deserialization_context` (Singleton) обеспечивает работу реестра идентичности (Identity Map), гарантируя единственность экземпляров по идентификатору `id` и предотвращая дублирование в памяти и циклическую рекурсию;
- `json_deserializer` предоставляет фасадный интерфейс для загрузки данных из строк и файлов JSON;
- Доменные модели реализуют собственный фабричный метод `create_from_dict`, инкапсулируя правила конструирования конкретной сущности.

Контракт `deserialize` принимает сырые данные и опциональный целевой тип. Метод `deserialize_value` фабрики рекурсивно обрабатывает коллекции (`list`, `dict`), перечисления и вложенные доменные модели.

`model_deserializer` выступает тонким координатором: разрешает класс модели динамически по полю `type` или явному типу, проверяет реестр идентичности и делегирует непосредственное создание объекта фабричному методу `create_from_dict` самой модели.

## UML диаграмма классов

```mermaid
classDiagram
    direction TB

    class abstract_deserializer {
        <<abstract>>
        +deserialize(data: object, target_type: type) object
    }

    class basic_deserializer {
        +deserialize(data: object, target_type: type) object
    }

    class datetime_deserializer {
        +deserialize(data: object, target_type: type) object
    }

    class model_deserializer {
        -__factory: abstract_deserializer_factory
        -__context: deserialization_context
        +deserialize(data: object, target_type: type) object
        -_extract_id(data: dict) str
        -_resolve_target_type(data: dict, target_type: type) type
        +_resolve_class_from_string(name: str) type
    }

    class abstract_deserializer_factory {
        <<abstract>>
        +get_deserializer(target_type_or_key: object) abstract_deserializer
        +deserialize_value(data: object, target_type: object) object
    }

    class deserializer_factory {
        -__context: deserialization_context
        -__basic_deserializer: basic_deserializer
        -__datetime_deserializer: datetime_deserializer
        -__model_deserializer: model_deserializer
        -__type_mapping: dict
        +_resolve_model_type(target_type_or_key: object) type
        +get_deserializer(target_type_or_key: object) abstract_deserializer
        +deserialize_value(data: object, target_type: object) object
    }

    class deserialization_context {
        -instance: deserialization_context$
        -__identity_map: dict
        +get(entity_id: str) object
        +register(entity: object) object
        +clear() None
    }

    class json_deserializer {
        -__factory: deserializer_factory
        +from_dict(data: object, target_type: object) object
        +from_json(json_string: str, target_type: object) object
        +from_json_file(file_path: str, target_type: object) object
    }

    class abstract_model {
        <<abstract>>
        +id: str
        +name: str
        +type: str
    }

    abstract_deserializer <|-- basic_deserializer : наследует
    abstract_deserializer <|-- datetime_deserializer : наследует
    abstract_deserializer <|-- model_deserializer : наследует

    abstract_deserializer_factory <|.. deserializer_factory : реализует

    deserializer_factory "1" --> "1" basic_deserializer : содержит
    deserializer_factory "1" --> "1" datetime_deserializer : содержит
    deserializer_factory "1" --> "1" model_deserializer : содержит
    deserializer_factory "1" --> "1" deserialization_context : использует

    model_deserializer --> abstract_deserializer_factory : использует
    model_deserializer --> deserialization_context : использует
    json_deserializer --> deserializer_factory : использует
    model_deserializer ..> abstract_model : создает через create_from_dict
```

## Как это работает по шагам

1. `json_deserializer.from_json_file` считывает содержимое файла и передаёт строку в `json_deserializer.from_json`.
2. `from_json` выполняет синтаксический анализ JSON через `json.loads` и передаёт разобранную структуру в `from_dict`.
3. `from_dict` обращается к методу `deserializer_factory.deserialize_value`.
4. `deserialize_value` выполняет диспетчеризацию по типу данных:
   - Списки обходятся поэлементно с рекурсивным вызовом `deserialize_value`.
   - Для словарей коллекций ключи динамически разрешаются в типы моделей, и элементы десериализуются в соответствующие классы.
   - Для словарей с метаданными типа вызывается `model_deserializer.deserialize`.
5. `model_deserializer`:
   - Извлекает идентификатор `id` и проверяет реестр идентичности `deserialization_context` (Identity Map), возвращая готовый экземпляр при повторном обращении.
   - Динамически определяет целевой класс по явному типу или значению поля `type` (полный квалифицированный путь класса или имя модели).
   - Делегирует создание объекта фабричному методу целевой модели `create_from_dict`.
   - Регистрирует созданный объект в `deserialization_context`.
6. Каждая доменная модель в методе `create_from_dict`:
   - Извлекает собственные поля из словаря.
   - Рекурсивно восстанавливает вложенные связанные модели через их фабричные методы.
   - Инициализирует доменный объект с валидацией бизнес-правил.
7. Восстановленный граф доменных объектов возвращается вызывающему коду.
