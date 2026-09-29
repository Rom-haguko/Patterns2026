import pytest
from src.core.exception import arguments_exception
from src.models.organization_model import organization_model


def test_organization_legal_entity_10_digit_inn_success():
    """
    <summary>
    Проверка создания юрлица с 10-значным ИНН и валидными банковскими реквизитами.
    </summary>
    """
    # Подготовка
    org_name = "АО Вектор"
    org_inn = "7701987654"
    org_bik = "044525999"
    org_account = "40702810938000005678"
    org_ownership_form = "ЗАО"

    # Действие
    company = organization_model(
        name=org_name,
        inn=org_inn,
        bik=org_bik,
        account=org_account,
        ownership_form=org_ownership_form
    )

    # Проверка
    assert company.name == org_name
    assert company.inn == org_inn
    assert company.bik == org_bik
    assert company.account == org_account
    assert company.ownership_form == org_ownership_form


def test_organization_individual_entrepreneur_12_digit_inn_success():
    """
    <summary>
    Проверка корректной инициализации ИП с 12-значным ИНН.
    </summary>
    """
    # Подготовка
    org_name = "ИП Сидоров"
    org_inn = "500100123456"
    org_bik = "044525999"
    org_account = "40802810938000005678"
    org_ownership_form = "ИП"

    # Действие
    entrepreneur = organization_model(
        name=org_name,
        inn=org_inn,
        bik=org_bik,
        account=org_account,
        ownership_form=org_ownership_form
    )

    # Проверка
    assert entrepreneur.inn == org_inn
    assert entrepreneur.ownership_form == org_ownership_form


def test_organization_invalid_inn_length_raises():
    """
    <summary>
    Выброс arguments_exception при некорректной длине ИНН (например, 9 цифр).
    </summary>
    """
    # Подготовка
    invalid_inn = "987654321"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")


def test_organization_inn_containing_letters_raises():
    """
    <summary>
    Выброс arguments_exception при попытке передать символы вместо цифр в ИНН.
    </summary>
    """
    # Подготовка
    invalid_inn = "770198765X"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")


def test_organization_inn_non_string_type_raises():
    """
    <summary>
    Выброс arguments_exception при передаче ИНН в виде целочисленного типа (int).
    </summary>
    """
    # Подготовка
    invalid_inn = 7701987654

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")


def test_organization_bik_invalid_length_raises():
    """
    <summary>
    Проверка валидации длины БИК (должно быть строго 9 цифр).
    </summary>
    """
    # Подготовка
    invalid_bik = "044525"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", invalid_bik, "40702810938000005678", "ЗАО")


def test_organization_account_invalid_length_raises():
    """
    <summary>
    Проверка валидации длины расчетного счета (должно быть строго 20 цифр).
    </summary>
    """
    # Подготовка
    invalid_account = "407028101234"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", "044525999", invalid_account, "ЗАО")


def test_organization_ownership_form_length_exceeded_raises():
    """
    <summary>
    Ограничение на длину формы собственности (не более 5 символов).
    </summary>
    """
    # Подготовка
    invalid_ownership_form = "ХОЛДИНГ"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", invalid_ownership_form)


def test_organization_bik_setter_validation():
    """
    <summary>
    Проверка срабатывания валидации при изменении БИК через сеттер у созданного объекта.
    </summary>
    """
    # Подготовка
    company = organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", "ЗАО")
    invalid_bik = "044"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        company.bik = invalid_bik