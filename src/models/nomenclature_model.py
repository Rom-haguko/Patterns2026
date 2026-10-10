from src.core.abstract_model import name_id
from src.core.exception import arguments_exception
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model


class nomenclature_model(name_id):
    """
    Модель номенклатурной позиции.
    Содержит краткое и полное наименование учетной единицы, 
    а также ссылки на категорию и единицу измерения.
    """

    # Предельная допустимая длина для развернутого наименования
    __max_full_name_length = 255

    def __init__(self, name: str = "", full_name: str = "", group=None, range=None):
        """
        Конструктор номенклатуры.

        :param name: Краткое наименование (до 50 символов)
        :param full_name: Полное наименование (до 255 символов)
        :param group: Категория номенклатуры (объект nomenclature_group_model)
        :param range: Единица измерения (объект range_model)
        """
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.range = range

    @property
    def full_name(self) -> str:
        """
        Возвращает полное наименование.
        """
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        """
        Устанавливает полное наименование с проверкой на пустоту и ограничением до 255 символов.
        """
        if value is None or str(value).strip() == "":
            raise arguments_exception("full_name", "Полное наименование не может быть пустым")

        value = str(value).strip()

        if len(value) > self.__max_full_name_length:
            raise arguments_exception("full_name", "Превышена максимальная длина полного наименования (255 символов)")

        self.__full_name = value

    @property
    def group(self):
        """
        Возвращает объект группы номенклатуры.
        """
        return self.__group

    @group.setter
    def group(self, value):
        """
        Устанавливает группу. Ожидает объект типа nomenclature_group_model.
        """
        if not isinstance(value, nomenclature_group_model):
            raise arguments_exception("group", "Параметр group должен быть экземпляром класса nomenclature_group_model")

        self.__group = value

    @property
    def range(self):
        """
        Возвращает объект единицы измерения.
        """
        return self.__range

    @range.setter
    def range(self, value):
        """
        Устанавливает единицу измерения. Ожидает объект типа range_model.
        """
        if not isinstance(value, range_model):
            raise arguments_exception("range", "Параметр range должен быть экземпляром класса range_model")

        self.__range = value

    @staticmethod
    def create(name: str = "", full_name: str = "", group=None, range=None) -> 'nomenclature_model':
        """
        Фабричный метод создания номенклатурной позиции.

        :param name: Краткое наименование (до 50 символов)
        :param full_name: Полное наименование (до 255 символов)
        :param group: Категория номенклатуры (nomenclature_group_model)
        :param range: Единица измерения (range_model)
        :return: Экземпляр nomenclature_model
        """
        return nomenclature_model(name=name, full_name=full_name, group=group, range=range)

    @property
    def recipe(self):
        """
        Технологическая карта (рецепт), по которой производится данная номенклатура.
        Реализует концепцию "Блюдо в блюде" (для полуфабрикатов).
        """
        return self.__recipe

    @recipe.setter
    def recipe(self, value) -> None:
        """
        Устанавливает рецепт для данной номенклатуры.
        """
        if value is not None:
            # Проверяем класс по имени, чтобы избежать проблем с циклическими импортами
            if type(value).__name__ != "recipe_model":
                raise arguments_exception("recipe", "Рецепт должен быть экземпляром recipe_model")
        self.__recipe = value