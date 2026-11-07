from src.core.abstract_model import abstract_model


class deserialization_context:
    """
    Контекст десериализации (реестр идентичности Identity Map).
    Обеспечивает сохранение единственности экземпляров сущностей по их id
    и предотвращает циклическую рекурсию при перекрёстных ссылках.
    """

    def __init__(self):
        """
        Инициализирует пустой реестр идентичности объектов.
        """
        self.__identity_map: dict[str, object] = {}

    def get(self, entity_id: str) -> object:
        """
        Возвращает ранее десериализованный объект по его идентификатору.

        :param entity_id: Идентификатор сущности
        :return: Экземпляр сущности или None
        """
        if not entity_id or not isinstance(entity_id, str):
            return None
        return self.__identity_map.get(str(entity_id).strip())

    def register(self, entity: object) -> object:
        """
        Регистрирует объект в реестре идентичности по его свойству id.

        :param entity: Доменный объект
        :return: Зарегистрированный объект
        """
        if entity is not None and hasattr(entity, "id"):
            entity_id = getattr(entity, "id", None)
            if entity_id:
                self.__identity_map[str(entity_id).strip()] = entity
        return entity

    def clear(self) -> None:
        """
        Очищает реестр идентичности.
        """
        self.__identity_map.clear()
