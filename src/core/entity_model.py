from src.core.abstract_model import name_id


"""
Общий класс для наследования. Содержит стандартное определение: код, наименование
"""
class entity_model(name_id):
    __name:str = ""

    """
    Наименование
    """
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        self.__name = value.strip()
