from src.core.abstract_model import name_id


class nomenclature_group_model(name_id):
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