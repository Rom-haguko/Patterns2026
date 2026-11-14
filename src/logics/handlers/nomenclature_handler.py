from src.logics.handlers.base_handler import base_crud_handler
from src.logics.storage_manager import storage_manager
from src.models.nomenclature_model import nomenclature_model


class nomenclature_handler(base_crud_handler):
    """
    Обработчик CRUD-операций для номенклатурных позиций (nomenclature_model).
    """

    @property
    def _storage_key(self) -> str:
        return storage_manager.nomenclature_key()

    @property
    def _model_class(self) -> type:
        return nomenclature_model

    def _prepare_data(self, data: dict) -> dict:
        resolved = dict(data)
        if "group_id" in resolved and "group" not in resolved:
            groups = self._storage.get(storage_manager.group_key())
            found_group = next((g for g in groups if g.id == resolved["group_id"]), None)
            if found_group is not None:
                resolved["group"] = found_group
        if "range_id" in resolved and "range" not in resolved:
            ranges = self._storage.get(storage_manager.range_key())
            found_range = next((r for r in ranges if r.id == resolved["range_id"]), None)
            if found_range is not None:
                resolved["range"] = found_range
        return resolved
