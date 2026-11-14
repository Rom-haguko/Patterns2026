from src.logics.storage_manager import storage_manager


class entity_dependency_validator:
    """
    Валидатор зависимостей доменных сущностей.
    Проверяет, используется ли сущность (по id) в других коллекциях хранилища,
    прежде чем разрешить её удаление.
    """

    @staticmethod
    def validate_delete(entity_id: str, storage: storage_manager) -> list[str]:
        """
        Проверяет наличие ссылок на entity_id во всех коллекциях хранилища.

        Атрибуты, по которым ведётся поиск ссылок, определяются через getattr:
        - nomenclature_model: .group.id, .range.id, .recipe.id
        - recipe_model: .target_nomenclature.id, строки .rows[].nomenclature.id
        - recipe_row_model: .range.id
        - settings_model: .company.id

        :param entity_id: Идентификатор удаляемой сущности.
        :param storage: Экземпляр storage_manager.
        :return: Список описаний найденных зависимостей (пустой — удаление безопасно).
        """
        dependencies = []

        for key in list(storage.data.keys()):
            collection = storage.get(key)
            for item in collection:
                deps = entity_dependency_validator._check_item(item, entity_id)
                dependencies.extend(deps)

        return dependencies

    @staticmethod
    def _check_item(item, entity_id: str) -> list[str]:
        """
        Проверяет один объект хранилища на наличие ссылок на entity_id.
        Использует getattr для обхода проверки типа через isinstance.

        :param item: Объект доменной модели.
        :param entity_id: Искомый идентификатор.
        :return: Список описаний обнаруженных зависимостей.
        """
        found = []
        item_name = getattr(item, "name", str(item))
        item_id = getattr(item, "id", None)

        # Пропускаем саму удаляемую сущность
        if item_id == entity_id:
            return found

        # nomenclature_model: ссылки на group, range и recipe
        group = getattr(item, "group", None)
        if group is not None and getattr(group, "id", None) == entity_id:
            found.append(f"Номенклатура '{item_name}' ссылается на группу с id={entity_id}")

        nom_range = getattr(item, "range", None)
        if nom_range is not None and getattr(nom_range, "id", None) == entity_id:
            found.append(f"Номенклатура '{item_name}' ссылается на единицу измерения с id={entity_id}")

        nom_recipe = getattr(item, "recipe", None)
        if nom_recipe is not None and getattr(nom_recipe, "id", None) == entity_id:
            found.append(f"Номенклатура '{item_name}' ссылается на рецепт с id={entity_id}")

        # range_model: ссылка на базовую единицу измерения
        base_range = getattr(item, "base_range", None)
        if base_range is not None and getattr(base_range, "id", None) == entity_id:
            found.append(f"Единица измерения '{item_name}' ссылается на базовую единицу измерения с id={entity_id}")

        # recipe_model: ссылка на целевую номенклатуру (выходную продукцию)
        target_nom = getattr(item, "target_nomenclature", None)
        if target_nom is not None and getattr(target_nom, "id", None) == entity_id:
            recipe_name = getattr(item, "name", str(item))
            found.append(f"Рецепт '{recipe_name}' ссылается на номенклатуру-результат с id={entity_id}")

        # settings_model: ссылка на организацию (company)
        company = getattr(item, "company", None)
        if company is not None and getattr(company, "id", None) == entity_id:
            settings_name = getattr(item, "name", str(item))
            found.append(f"Настройки '{settings_name}' ссылаются на организацию с id={entity_id}")

        # recipe_model: проверка строк рецепта
        rows = getattr(item, "rows", None)
        if rows is not None:
            for row in rows:
                row_name = getattr(row, "name", str(row))

                row_nom = getattr(row, "nomenclature", None)
                if row_nom is not None and getattr(row_nom, "id", None) == entity_id:
                    recipe_name = getattr(item, "name", str(item))
                    found.append(
                        f"Рецепт '{recipe_name}': строка '{row_name}' ссылается на номенклатуру с id={entity_id}"
                    )

                # recipe_row_model: ссылка на единицу измерения
                row_range = getattr(row, "range", None)
                if row_range is not None and getattr(row_range, "id", None) == entity_id:
                    recipe_name = getattr(item, "name", str(item))
                    found.append(
                        f"Рецепт '{recipe_name}': строка '{row_name}' ссылается на единицу измерения с id={entity_id}"
                    )

        return found
