from src.core.abstract_model import name_id
from src.core.exception import arguments_exception


class recipe_step_model(name_id):
    """
    Модель этапа (шага) приготовления в технологической карте.
    Содержит номер шага, краткое наименование этапа и подробное описание действий.
    """

    def __init__(
        self,
        step_number: int = 1,
        name: str = "",
        description: str = "",
        time_minutes: float = 0.0
    ) -> None:
        """
        Инициализирует шаг технологического процесса.

        :param step_number: Порядковый номер шага (целое число >= 1)
        :param name: Название шага (до 50 символов)
        :param description: Подробное описание процесса
        :param time_minutes: Время выполнения шага в минутах (неотрицательное число)
        """
        super().__init__(name=name if name else f"Шаг {step_number}")
        self.__step_number: int = 1
        self.__description: str = ""
        self.__time_minutes: float = 0.0

        self.step_number = step_number
        self.description = description
        self.time_minutes = time_minutes

    @property
    def step_number(self) -> int:
        """
        Возвращает порядковый номер шага.
        """
        return self.__step_number

    @step_number.setter
    def step_number(self, value: int) -> None:
        """
        Устанавливает порядковый номер шага. Ожидает целое положительное число >= 1.
        """
        if not isinstance(value, int):
            raise arguments_exception("step_number", "Номер шага должен быть целым числом")

        if value < 1:
            raise arguments_exception("step_number", "Номер шага должен быть больше или равен 1")

        self.__step_number = value

    @property
    def description(self) -> str:
        """
        Возвращает подробное описание действий на данном этапе.
        """
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        """
        Устанавливает текстовое описание технологического шага.
        """
        self.__description = str(value).strip() if value is not None else ""

    @property
    def time_minutes(self) -> float:
        """
        Возвращает время выполнения шага в минутах.
        """
        return self.__time_minutes

    @time_minutes.setter
    def time_minutes(self, value: float) -> None:
        """
        Устанавливает продолжительность шага в минутах.
        """
        if not isinstance(value, (int, float)):
            raise arguments_exception("time_minutes", "Время выполнения шага должно быть числом")

        if value < 0:
            raise arguments_exception("time_minutes", "Время выполнения шага не может быть отрицательным")

        self.__time_minutes = float(value)

    @staticmethod
    def create(
        step_number: int = 1,
        name: str = "",
        description: str = "",
        time_minutes: float = 0.0
    ) -> 'recipe_step_model':
        """
        Фабричный метод создания технологического шага.

        :param step_number: Номер шага
        :param name: Название шага
        :param description: Описание процесса
        :param time_minutes: Время выполнения (минуты)
        :return: Экземпляр recipe_step_model
        """
        return recipe_step_model(
            step_number=step_number,
            name=name,
            description=description,
            time_minutes=time_minutes
        )
