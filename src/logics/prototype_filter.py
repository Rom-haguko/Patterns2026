from src.dtos.filter_dto import filter_dto
from src.dtos.filter_type_enum import filter_type_enum


class prototype_filter:
    """
    Универсальная реализация шаблона проектирования (Prototype)
    для фильтрации любых доменных моделей и DTO-структур (включая ОСВ).
    
    Поддерживает фильтрацию по наименованию и уникальному коду (id) с вариантами
    сравнения EQUALS и LIKE, а также рекурсивный поиск во вложенных структурах
    (базовые единицы измерения, группы, номенклатура, рецепты, склады).
    """

    def __init__(self, data: list = None) -> None:
        """
        Инициализирует прототип набором исходных данных.

        :param data: Исходная коллекция объектов для фильтрации
        """
        self.__data: list = list(data) if data is not None else []

    @property
    def data(self) -> list:
        """
        Возвращает текущую коллекцию объектов прототипа.
        """
        return self.__data

    def clone(self) -> "prototype_filter":
        """
        Клонирует текущий экземпляр прототипа с сохранением набора данных.
        """
        return prototype_filter(list(self.__data))

    def create(self, filter_item: filter_dto = None) -> "prototype_filter":
        """
        Фабричный метод создания нового прототипа с отфильтрованными данными
        на основе переданного filter_dto (контракт паттерна Прототип).

        :param filter_item: Экземпляр filter_dto с условиями фильтрации
        :return: Новый экземпляр prototype_filter с отфильтрованными объектами
        """
        if filter_item is None or filter_item.is_empty:
            return self.clone()

        filtered_items = [item for item in self.__data if self.is_match(item, filter_item)]
        return prototype_filter(filtered_items)

    def is_match(self, item: object, filter_item: filter_dto) -> bool:
        """
        Проверяет соответствие объекта заданным критериям filter_dto,
        включая проверку вложенных структур и связей.

        :param item: Проверяемый объект (доменная модель или DTO)
        :param filter_item: Критерии фильтрации
        :return: True, если объект удовлетворяет всем активным критериям
        """
        if item is None:
            return False

        if filter_item.is_empty:
            return True

        # Проверка соответствия по уникальному коду (id)
        if filter_item.id:
            id_matched = self._match_nested(
                item,
                lambda obj: self._check_attribute(obj, "id", filter_item.id, filter_item.id_filter_type),
            )
            if not id_matched:
                return False

        # Проверка соответствия по наименованию (name)
        if filter_item.name:
            name_matched = self._match_nested(
                item,
                lambda obj: self._check_name_attribute(obj, filter_item.name, filter_item.name_filter_type),
            )
            if not name_matched:
                return False

        return True

    def _compare_values(self, source: str, target: str, filter_type: filter_type_enum) -> bool:
        """
        Сравнивает два строковых значения в соответствии с типом фильтрации.

        :param source: Исходное значение из объекта
        :param target: Искомое значение из фильтра
        :param filter_type: EQUALS или LIKE
        :return: True при совпадении условий
        """
        if source is None or target is None:
            return False

        src_str = str(source).strip().lower()
        tgt_str = str(target).strip().lower()

        if filter_type == filter_type_enum.EQUALS:
            return src_str == tgt_str

        if filter_type == filter_type_enum.LIKE:
            return tgt_str in src_str

        return False

    def _check_attribute(self, obj: object, attr_name: str, target: str, filter_type: filter_type_enum) -> bool:
        """
        Проверяет значение конкретного атрибута объекта.
        """
        val = getattr(obj, attr_name, None)
        if val is None:
            return False
        return self._compare_values(str(val), target, filter_type)

    def _check_name_attribute(self, obj: object, target: str, filter_type: filter_type_enum) -> bool:
        """
        Проверяет наименование объекта (включая name, full_name, description).
        """
        name_val = getattr(obj, "name", None)
        if name_val is not None and self._compare_values(str(name_val), target, filter_type):
            return True

        full_name_val = getattr(obj, "full_name", None)
        if full_name_val is not None and self._compare_values(str(full_name_val), target, filter_type):
            return True

        return False

    def _match_nested(self, root: object, matcher_fn, visited: set = None) -> bool:
        """
        Рекурсивный поиск соответствия в объекте и всех его вложенных структурах
        с защитой от циклических ссылок.

        :param root: Корневой объект для проверки
        :param matcher_fn: Функция предикат проверки объекта
        :param visited: Множество посещенных идентификаторов объектов
        :return: True, если сам объект или хоть один вложенный удовлетворяет предикату
        """
        if root is None:
            return False

        if visited is None:
            visited = set()

        root_id = id(root)
        if root_id in visited:
            return False

        visited.add(root_id)

        try:
            if matcher_fn(root):
                return True

            nested_objects = self._get_nested_objects(root)
            for child in nested_objects:
                if self._match_nested(child, matcher_fn, visited):
                    return True

            return False
        finally:
            visited.remove(root_id)

    def _get_nested_objects(self, obj: object) -> list:
        """
        Извлекает связанные вложенные доменные объекты через универсальную рефлексию.
        Обходит все публичные атрибуты объекта без жесткой привязки к именам полей.
        
        :param obj: Инспектируемый объект
        :return: Список найденных связанных объектов
        """
        nested = []
        if obj is None:
            return nested

        for attr in dir(obj):
            if attr.startswith("_"):
                continue

            try:
                val = getattr(obj, attr, None)
            except (AttributeError, Exception):
                continue

            if val is None or callable(val):
                continue

            if isinstance(val, (list, tuple, set)):
                for item in val:
                    if item is not None and not isinstance(item, (int, float, str, bool)):
                        nested.append(item)
            elif hasattr(val, "id"):
                nested.append(val)

        return nested
