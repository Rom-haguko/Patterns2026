from src.core.abstract_model import name_id


class entity_model(name_id):
    """
    Общий класс для наследования. Содержит стандартное определение: код, наименование
    """
    def __init__(self, name: str = None) -> None:
        super().__init__(name=name)