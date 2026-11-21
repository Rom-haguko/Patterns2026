import importlib
from src.core.abstract_deserializer import abstract_deserializer
from src.core.abstract_deserializer_factory import abstract_deserializer_factory
from src.core.abstract_model import abstract_model
from src.core.exception import arguments_exception
from src.logics.deserialization_context import deserialization_context


class model_deserializer(abstract_deserializer):
    """
    Десериализатор доменных сущностей.
    Координирует сборку объектов через их стандартные конструкторы __init__,
    разрешая тип модели по строковому ключу или явному типу,
    разрешая ссылки на связанные сущности и регистрируя инстансы в контексте идентичности.
    """

    def __init__(
        self,
        factory: abstract_deserializer_factory = None,
        context: deserialization_context = None,
    ):
        """
        Инициализирует координатор десериализации моделей.

        :param factory: Фабрика десериализаторов для рекурсивной обработки
        :param context: Контекст реестра идентичности
        """
        self.__factory = factory
        self.__context = context if context is not None else deserialization_context()
        self.__reference_resolvers = {
            "nomenclature_model": self._resolve_nomenclature_refs,
            "range_model": self._resolve_range_refs,
            "recipe_model": self._resolve_recipe_refs,
            "settings_model": self._resolve_settings_refs,
        }
        self.__model_builders = {
            "range_model": self._build_range,
            "nomenclature_group_model": self._build_nomenclature_group,
            "nomenclature_model": self._build_nomenclature,
            "storage_model": self._build_storage,
            "organization_model": self._build_organization,
            "settings_model": self._build_settings,
            "recipe_step_model": self._build_recipe_step,
            "recipe_row_model": self._build_recipe_row,
            "recipe_model": self._build_recipe,
        }

    @property
    def context(self) -> deserialization_context:
        """
        Текущий контекст идентичности.
        """
        return self.__context

    def _find_entity_by_id(self, storage, key: str, entity_id: str) -> object | None:
        """
        Унифицированный поиск сущности в хранилище по ключу коллекции и идентификатору.
        """
        if not entity_id or storage is None:
            return None
        target_id = str(entity_id).strip()
        items = storage.collection(key)
        return next((item for item in items if str(getattr(item, "id", "")).strip() == target_id), None)

    def _resolve_nomenclature_refs(self, resolved: dict, storage) -> dict:
        from src.logics.storage_manager import storage_manager
        if "range" in resolved and isinstance(resolved["range"], dict) and self.__factory:
            resolved["range"] = self.__factory.deserialize_value(resolved["range"], "range_model")
        if "group" in resolved and isinstance(resolved["group"], dict) and self.__factory:
            resolved["group"] = self.__factory.deserialize_value(resolved["group"], "nomenclature_group_model")

        if "group_id" in resolved and "group" not in resolved:
            found_group = self._find_entity_by_id(storage, storage_manager.group_key(), resolved["group_id"])
            if found_group is not None:
                resolved["group"] = found_group
        if "range_id" in resolved and "range" not in resolved:
            found_range = self._find_entity_by_id(storage, storage_manager.range_key(), resolved["range_id"])
            if found_range is not None:
                resolved["range"] = found_range
        if "recipe_id" in resolved and "recipe" not in resolved:
            found_recipe = self._find_entity_by_id(storage, storage_manager.recipe_key(), resolved["recipe_id"])
            if found_recipe is not None:
                resolved["recipe"] = found_recipe
        return resolved

    def _resolve_range_refs(self, resolved: dict, storage) -> dict:
        from src.logics.storage_manager import storage_manager
        if "base_range" in resolved and isinstance(resolved["base_range"], dict) and self.__factory:
            resolved["base_range"] = self.__factory.deserialize_value(resolved["base_range"], "range_model")

        if "base_range_id" in resolved and "base_range" not in resolved:
            found_range = self._find_entity_by_id(storage, storage_manager.range_key(), resolved["base_range_id"])
            if found_range is not None:
                resolved["base_range"] = found_range
        return resolved

    def _resolve_recipe_refs(self, resolved: dict, storage) -> dict:
        from src.logics.storage_manager import storage_manager
        if "target_nomenclature_id" in resolved and "target_nomenclature" not in resolved:
            found_nom = self._find_entity_by_id(storage, storage_manager.nomenclature_key(), resolved["target_nomenclature_id"])
            if found_nom is not None:
                resolved["target_nomenclature"] = found_nom
        if "rows" in resolved and isinstance(resolved["rows"], list):
            resolved_rows = []
            for row_data in resolved["rows"]:
                if isinstance(row_data, dict):
                    row_copy = dict(row_data)
                    if "nomenclature_id" in row_copy and "nomenclature" not in row_copy:
                        found = self._find_entity_by_id(storage, storage_manager.nomenclature_key(), row_copy["nomenclature_id"])
                        if found is not None:
                            row_copy["nomenclature"] = found
                    if "range_id" in row_copy and "range" not in row_copy:
                        found_r = self._find_entity_by_id(storage, storage_manager.range_key(), row_copy["range_id"])
                        if found_r is not None:
                            row_copy["range"] = found_r
                    resolved_rows.append(row_copy)
                else:
                    resolved_rows.append(row_data)
            resolved["rows"] = resolved_rows
        return resolved

    def _resolve_settings_refs(self, resolved: dict, storage) -> dict:
        from src.logics.storage_manager import storage_manager
        if "company" in resolved and isinstance(resolved["company"], dict):
            comp_data = dict(resolved["company"])
            if not comp_data.get("inn") and comp_data.get("inn_kpp"):
                inn_part = str(comp_data["inn_kpp"]).split("/")[0].strip()
                if len(inn_part) in (10, 12) and inn_part.isdigit():
                    comp_data["inn"] = inn_part
            resolved["company"] = comp_data

            if not resolved.get("boss_name") and comp_data.get("ceo"):
                resolved["boss_name"] = str(comp_data["ceo"]).strip()

        if "company_id" in resolved and "company" not in resolved:
            found_org = self._find_entity_by_id(storage, storage_manager.organization_key(), resolved["company_id"])
            if found_org is not None:
                resolved["company"] = found_org
        return resolved

    def _resolve_references(self, data: dict, model_cls: type) -> dict:
        """
        Разрешает ссылки на связанные сущности по идентификаторам через хранилище и контекст.
        Использует словарь стратегий вместо каскадных условных операторов.
        """
        resolved = dict(data)
        from src.logics.storage_manager import storage_manager
        storage = storage_manager()

        model_name = getattr(model_cls, "__name__", "")
        resolver = self.__reference_resolvers.get(model_name)
        if resolver is not None:
            return resolver(resolved, storage)
        return resolved

    def _build_range(self, data: dict) -> object:
        from src.models.range_model import range_model
        name = data.get("name", "")
        conversion_factor = data.get("conversion_factor", 1)
        base_data = data.get("base_range")
        base_range = None
        if isinstance(base_data, dict) and self.__factory:
            base_range = self.__factory.deserialize_value(base_data, range_model)
        elif isinstance(base_data, range_model):
            base_range = base_data
        return range_model(name=name, conversion_factor=conversion_factor, base_range=base_range)

    def _build_nomenclature_group(self, data: dict) -> object:
        from src.models.nomenclature_group_model import nomenclature_group_model
        name = data.get("name", "")
        return nomenclature_group_model(name=name)

    def _build_nomenclature(self, data: dict) -> object:
        from src.models.nomenclature_model import nomenclature_model
        from src.models.nomenclature_group_model import nomenclature_group_model
        from src.models.range_model import range_model
        from src.models.recipe_model import recipe_model
        name = data.get("name", "")
        full_name = data.get("full_name", "")

        group_data = data.get("group")
        group = None
        if isinstance(group_data, dict) and self.__factory:
            group = self.__factory.deserialize_value(group_data, nomenclature_group_model)
        elif isinstance(group_data, nomenclature_group_model):
            group = group_data

        range_data = data.get("range")
        range_val = None
        if isinstance(range_data, dict) and self.__factory:
            range_val = self.__factory.deserialize_value(range_data, range_model)
        elif isinstance(range_data, range_model):
            range_val = range_data

        recipe_data = data.get("recipe")
        recipe_val = None
        if isinstance(recipe_data, dict) and self.__factory:
            recipe_val = self.__factory.deserialize_value(recipe_data, recipe_model)
        elif isinstance(recipe_data, recipe_model):
            recipe_val = recipe_data

        return nomenclature_model(name=name, full_name=full_name, group=group, range=range_val, recipe=recipe_val)

    def _build_storage(self, data: dict) -> object:
        from src.models.storage_model import storage_model
        name = data.get("name", "")
        address = data.get("address", "")
        return storage_model(name=name, address=address)

    def _build_organization(self, data: dict) -> object:
        from src.models.organization_model import organization_model
        name = data.get("name")
        inn = data.get("inn", "")
        bik = data.get("bik", "")
        account = data.get("account", "")
        ownership_form = data.get("ownership_form", "")
        corr_account = data.get("corr_account", "")
        return organization_model(
            name=name,
            inn=inn,
            bik=bik,
            account=account,
            ownership_form=ownership_form,
            corr_account=corr_account,
        )

    def _build_settings(self, data: dict) -> object:
        from src.models.settings_model import settings_model
        from src.models.organization_model import organization_model
        from src.dtos.report_type_enum import report_type_enum
        name = data.get("name")
        instance = settings_model(name=name)
        instance.boss_name = data.get("boss_name", "")
        instance.account_name = data.get("account_name", "")

        company_data = data.get("company")
        if isinstance(company_data, dict) and self.__factory:
            instance.company = self.__factory.deserialize_value(company_data, organization_model)
        elif isinstance(company_data, organization_model):
            instance.company = company_data

        resp_format = data.get("response_format")
        if resp_format is not None:
            if isinstance(resp_format, int):
                instance.response_format = report_type_enum(resp_format)
            elif isinstance(resp_format, str):
                instance.response_format = report_type_enum.from_string(resp_format)
            elif isinstance(resp_format, report_type_enum):
                instance.response_format = resp_format

        return instance

    def _build_recipe_step(self, data: dict) -> object:
        from src.models.recipe_step_model import recipe_step_model
        step_number = data.get("step_number", 1)
        name = data.get("name", "")
        description = data.get("description", "")
        time_minutes = data.get("time_minutes", 0.0)
        return recipe_step_model(
            step_number=int(step_number),
            name=name,
            description=description,
            time_minutes=float(time_minutes),
        )

    def _build_recipe_row(self, data: dict) -> object:
        from src.models.recipe_row_model import recipe_row_model
        from src.models.nomenclature_model import nomenclature_model
        from src.models.range_model import range_model
        nom_data = data.get("nomenclature")
        nomenclature = None
        if isinstance(nom_data, dict) and self.__factory:
            nomenclature = self.__factory.deserialize_value(nom_data, nomenclature_model)
        elif isinstance(nom_data, nomenclature_model):
            nomenclature = nom_data

        range_data = data.get("range")
        row_range = None
        if isinstance(range_data, dict) and self.__factory:
            row_range = self.__factory.deserialize_value(range_data, range_model)
        elif isinstance(range_data, range_model):
            row_range = range_data

        brutto = float(data.get("brutto", 0.0))
        netto = float(data.get("netto", 0.0))
        name = data.get("name")
        return recipe_row_model(
            nomenclature=nomenclature,
            brutto=brutto,
            netto=netto,
            range=row_range,
            name=name,
        )

    def _build_recipe(self, data: dict) -> object:
        from src.models.recipe_model import recipe_model
        from src.models.nomenclature_model import nomenclature_model
        from src.models.recipe_row_model import recipe_row_model
        from src.models.recipe_step_model import recipe_step_model
        name = data.get("name", "")
        category = data.get("category", "")
        output = data.get("output", "")
        standard = data.get("standard", "")
        cooking_time = float(data.get("cooking_time", 0.0))
        description = data.get("description", "")

        target_nom_data = data.get("target_nomenclature")
        target_nom = None
        if isinstance(target_nom_data, dict) and self.__factory:
            target_nom = self.__factory.deserialize_value(target_nom_data, nomenclature_model)
        elif isinstance(target_nom_data, nomenclature_model):
            target_nom = target_nom_data

        instance = recipe_model(
            name=name,
            category=category,
            output=output,
            standard=standard,
            cooking_time=cooking_time,
            description=description,
            target_nomenclature=target_nom,
        )

        rows_data = data.get("rows")
        if isinstance(rows_data, list):
            for r_item in rows_data:
                if isinstance(r_item, dict) and self.__factory:
                    row_obj = self.__factory.deserialize_value(r_item, recipe_row_model)
                    if row_obj:
                        instance.add_row(row_obj)
                elif isinstance(r_item, recipe_row_model):
                    instance.add_row(r_item)

        steps_data = data.get("steps")
        if isinstance(steps_data, list):
            for s_item in steps_data:
                if isinstance(s_item, dict) and self.__factory:
                    step_obj = self.__factory.deserialize_value(s_item, recipe_step_model)
                    if step_obj:
                        instance.add_step(step_obj)
                elif isinstance(s_item, recipe_step_model):
                    instance.add_step(s_item)

        return instance

    def deserialize(self, data: object, target_type: type = None) -> object:
        """
        Десериализует словарь в экземпляр доменной модели через сборку с использованием конструкторов.

        :param data: Исходные данные (словарь)
        :param target_type: Ожидаемый класс доменной модели
        :return: Экземпляр доменной модели
        """
        if data is None:
            return None

        if not isinstance(data, dict):
            raise arguments_exception(
                "data",
                f"Ожидается словарь данных для десериализации модели, получено: {type(data)}"
            )

        model_cls = self._resolve_target_type(data, target_type)
        if model_cls is None:
            raise arguments_exception(
                "target_type",
                "Не удалось определить целевой класс для десериализации словаря"
            )

        entity_id = self._extract_id(data)
        if entity_id:
            cached_instance = self.__context.get(entity_id)
            if cached_instance is not None:
                return cached_instance

        resolved_data = self._resolve_references(data, model_cls)

        builder = self.__model_builders.get(model_cls.__name__)
        if builder is not None:
            instance = builder(resolved_data)
        else:
            instance = model_cls()

        if entity_id and hasattr(instance, "id"):
            instance.id = entity_id
            self.__context.register(instance)

        return instance

    def _extract_id(self, data: dict) -> str:
        """
        Извлекает строковый идентификатор из словаря.
        """
        raw_id = data.get("id")
        if raw_id is not None and str(raw_id).strip():
            return str(raw_id).strip()
        return ""

    def _resolve_target_type(self, data: dict, target_type: type = None) -> type:
        """
        Определяет целевой класс модели динамически по полю 'type' или переданному типу.
        """
        if target_type is not None and isinstance(target_type, type):
            return target_type

        if isinstance(target_type, str):
            resolved = self._resolve_class_from_string(target_type)
            if resolved is not None:
                return resolved

        type_indicator = data.get("type")
        if type_indicator and isinstance(type_indicator, str):
            resolved = self._resolve_class_from_string(type_indicator)
            if resolved is not None:
                return resolved

        return None

    @staticmethod
    def _resolve_class_from_string(name: str) -> type | None:
        """
        Динамически импортирует и возвращает класс по его полному имени или краткому названию.
        """
        clean_name = name.strip()
        if not clean_name:
            return None

        if "." in clean_name:
            try:
                module_name, class_name = clean_name.rsplit(".", 1)
                module = importlib.import_module(module_name)
                return getattr(module, class_name, None)
            except (ImportError, AttributeError):
                pass

        try:
            module = importlib.import_module(f"src.models.{clean_name}")
            return getattr(module, clean_name, None)
        except (ImportError, AttributeError):
            pass

        return None
