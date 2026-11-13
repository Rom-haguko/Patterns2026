from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception


class nomenclature_group_model(abstract_model):
    """
    Модель категории (группы) номенклатуры.
    Служит для классификации и объединения товаров или материалов 
    (например, «Сырье», «Полуфабрикаты», «Готовая продукция»).
    """

    def __init__(self, name: str = ""):
        """
        Инициализирует экземпляр группы номенклатуры.

        :param name: Наименование группы (максимум 50 символов).
        """
        super().__init__()
        self.name = name

    @staticmethod
    def create(name: str = "") -> 'nomenclature_group_model':
        """
        Универсальный фабричный метод создания группы номенклатуры.

        :param name: Наименование группы
        :return: Экземпляр nomenclature_group_model
        """
        return nomenclature_group_model(name=name)

    @staticmethod
    def create_raw() -> 'nomenclature_group_model':
        """
        Фабричный метод создания группы 'Сырьё'.
        """
        return nomenclature_group_model(name="Сырьё")

    @staticmethod
    def create_semi_finished() -> 'nomenclature_group_model':
        """
        Фабричный метод создания группы 'Полуфабрикаты'.
        """
        return nomenclature_group_model(name="Полуфабрикаты")

    @staticmethod
    def create_finished() -> 'nomenclature_group_model':
        """
        Фабричный метод создания группы 'Готовая продукция'.
        """
        return nomenclature_group_model(name="Готовая продукция")

    @staticmethod
    def create_packaging() -> 'nomenclature_group_model':
        """
        Фабричный метод создания группы 'Упаковка'.
        """
        return nomenclature_group_model(name="Упаковка")

    @classmethod
    def create_from_dict(cls, data: dict) -> "nomenclature_group_model":
        """
        Фабричный метод создания группы номенклатуры из словаря.

        :param data: Словарь с данными группы
        :return: Экземпляр nomenclature_group_model
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Для создания nomenclature_group_model требуется словарь")

        from src.logics.deserialization_context import deserialization_context

        context = deserialization_context()
        entity_id = str(data.get("id", "")).strip()
        if entity_id:
            cached = context.get(entity_id)
            if cached is not None:
                return cached

        name = data.get("name", "")
        instance = cls(name=name)
        if entity_id:
            instance.id = entity_id
            context.register(instance)

        return instance

