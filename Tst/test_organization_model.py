import pytest
from src.core.exception import arguments_exception
from src.models.organization_model import organization_model


def test_organization_legal_entity_10_digit_inn_success():
    """
    Проверка создания юрлица с 10-значным ИНН и валидными банковскими реквизитами.
    """
    company = organization_model(
        name="АО Вектор",
        inn="7701987654",
        bik="044525999",
        account="40702810938000005678",
        ownership_form="ЗАО"
    )

    assert company.name == "АО Вектор"
    assert company.inn == "7701987654"
    assert company.bik == "044525999"
    assert company.account == "40702810938000005678"
    assert company.ownership_form == "ЗАО"


def test_organization_individual_entrepreneur_12_digit_inn_success():
    """
    Проверка корректной инициализации ИП с 12-значным ИНН.
    """
    entrepreneur = organization_model(
        name="ИП Сидоров",
        inn="500100123456",
        bik="044525999",
        account="40802810938000005678",
        ownership_form="ИП"
    )

    assert entrepreneur.inn == "500100123456"
    assert entrepreneur.ownership_form == "ИП"


def test_organization_invalid_inn_length_raises():
    """
    Выброс arguments_exception при некорректной длине ИНН (например, 9 цифр).
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "987654321", "044525999", "40702810938000005678", "ЗАО")


def test_organization_inn_containing_letters_raises():
    """
    Выброс arguments_exception при попытке передать символы вместо цифр в ИНН.
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "770198765X", "044525999", "40702810938000005678", "ЗАО")


def test_organization_inn_non_string_type_raises():
    """
    Выброс arguments_exception при передаче ИНН в виде целочисленного типа (int).
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", 7701987654, "044525999", "40702810938000005678", "ЗАО")


def test_organization_bik_invalid_length_raises():
    """
    Проверка валидации длины БИК (должно быть строго 9 цифр).
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", "044525", "40702810938000005678", "ЗАО")


def test_organization_account_invalid_length_raises():
    """
    Проверка валидации длины расчетного счета (должно быть строго 20 цифр).
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", "044525999", "407028101234", "ЗАО")


def test_organization_ownership_form_length_exceeded_raises():
    """
    Ограничение на длину формы собственности (не более 5 символов).
    """
    with pytest.raises(arguments_exception):
        organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", "ХОЛДИНГ")


def test_organization_bik_setter_validation():
    """
    Проверка срабатывания валидации при изменении БИК через сеттер у созданного объекта.
    """
    company = organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", "ЗАО")

    with pytest.raises(arguments_exception):
        company.bik = "044"