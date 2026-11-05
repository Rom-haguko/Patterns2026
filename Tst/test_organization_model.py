import pytest
from src.core.exception import arguments_exception
from src.models.organization_model import organization_model


def test_organization_legal_entity_10_digit_inn_success():
    """
    Проверка создания юрлица с 10-значным ИНН и валидными банковскими реквизитами.
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

    # Проверки
    assert company.name == org_name
    assert company.inn == org_inn
    assert company.bik == org_bik
    assert company.account == org_account
    assert company.ownership_form == org_ownership_form


def test_organization_individual_entrepreneur_12_digit_inn_success():
    """
    Проверка корректной инициализации ИП с 12-значным ИНН.
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

    # Проверки
    assert entrepreneur.inn == org_inn
    assert entrepreneur.ownership_form == org_ownership_form


def test_organization_invalid_inn_length_raises():
    """
    Выброс arguments_exception при некорректной длине ИНН (например, 9 цифр).
    """
    # Подготовка
    invalid_inn = "987654321"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")

    # Проверки
    assert exc_info.value is not None


def test_organization_inn_containing_letters_raises():
    """
    Выброс arguments_exception при попытке передать символы вместо цифр в ИНН.
    """
    # Подготовка
    invalid_inn = "770198765X"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")

    # Проверки
    assert exc_info.value is not None


def test_organization_inn_non_string_type_raises():
    """
    Выброс arguments_exception при передаче ИНН в виде целочисленного типа (int).
    """
    # Подготовка
    invalid_inn = 7701987654

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", invalid_inn, "044525999", "40702810938000005678", "ЗАО")

    # Проверки
    assert exc_info.value is not None


def test_organization_bik_invalid_length_raises():
    """
    Проверка валидации длины БИК (должно быть строго 9 цифр).
    """
    # Подготовка
    invalid_bik = "044525"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", "7701987654", invalid_bik, "40702810938000005678", "ЗАО")

    # Проверки
    assert exc_info.value is not None


def test_organization_account_invalid_length_raises():
    """
    Проверка валидации длины расчетного счета (должно быть строго 20 цифр).
    """
    # Подготовка
    invalid_account = "407028101234"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", "7701987654", "044525999", invalid_account, "ЗАО")

    # Проверки
    assert exc_info.value is not None


def test_organization_corr_account_valid():
    """
    Проверка установки и чтения корректного корр. счета.
    """
    # Подготовка
    corr = "30101810200000000999"

    # Действие
    org = organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", "ЗАО", corr)

    # Проверки
    assert org.corr_account == corr


def test_organization_corr_account_none_resets_to_empty():
    """
    Проверка: передача None сбрасывает корр. счет в пустую строку.
    """
    # Подготовка
    org = organization_model()

    # Действие
    org.corr_account = None

    # Проверки
    assert org.corr_account == ""


def test_organization_corr_account_invalid_letters_raises():
    """
    Проверка: буквы в корр. счете вызывают arguments_exception.
    """
    # Подготовка
    org = organization_model()
    invalid_corr = "301018102ABC"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        org.corr_account = invalid_corr

    # Проверки
    assert exc_info.value is not None


def test_organization_corr_account_invalid_type_raises():
    """
    Проверка: передача неподдерживаемого типа (список) в корр. счет вызывает arguments_exception.
    """
    # Подготовка
    org = organization_model()
    invalid_corr = ["12345"]

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        org.corr_account = invalid_corr

    # Проверки
    assert exc_info.value is not None


def test_organization_ownership_form_length_exceeded_raises():
    """
    Ограничение на длину формы собственности (не более 5 символов).
    """
    # Подготовка
    invalid_ownership_form = "ХОЛДИНГ"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", invalid_ownership_form)

    # Проверки
    assert exc_info.value is not None


def test_organization_bik_setter_validation():
    """
    Проверка срабатывания валидации при изменении БИК через сеттер у созданного объекта.
    """
    # Подготовка
    company = organization_model("АО Вектор", "7701987654", "044525999", "40702810938000005678", "ЗАО")
    invalid_bik = "044"

    # Действие
    with pytest.raises(arguments_exception) as exc_info:
        company.bik = invalid_bik

    # Проверки
    assert exc_info.value is not None
