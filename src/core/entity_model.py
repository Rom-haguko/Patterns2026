from src.core.abstract_model import abstract_model


class entity_model(abstract_model):
    """
    Общий класс для наследования. Содержит стандартное определение: код, наименование
    """
    def __init__(self, name: str = None) -> None:
        super().__init__(name=name)