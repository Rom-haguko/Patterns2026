import pytest
from src.core.exception import arguments_exception
from src.models.range_model import range_model


def test_range_model_base_unit_initialization():
    """
    Проверка успешного создания базовой единицы измерения (без указания родительской).
    """
    base_unit = range_model("миллилитр", 1)

    assert base_unit.name == "миллилитр"
    assert base_unit.conversion_factor == 1
    assert base_unit.coefficient == 1
    assert base_unit.base_range is None
    assert base_unit.base is None


def test_range_model_derived_unit_initialization():
    """
    Проверка создания производной единицы с привязкой к базовой единице измерения.
    """
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)

    assert liter_unit.name == "литр"
    assert liter_unit.conversion_factor == 1000
    assert liter_unit.base_range is ml_unit
    assert liter_unit.base.name == "миллилитр"


def test_range_model_conversion_factor_calculation():
    """
    Проверка корректности расчёта пересчёта количества объёма через коэффициент.
    """
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)
    volume_liters = 3.5

    volume_ml = volume_liters * liter_unit.conversion_factor

    assert volume_ml == 3500


def test_range_model_multilevel_conversion():
    """
    Проверка последовательного пересчёта величин по цепочке производных единиц (куб. м -> литр -> мл).
    """
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)
    cubic_m_unit = range_model("куб. м", 1000, liter_unit)

    total_ml = 1.5 * cubic_m_unit.conversion_factor * liter_unit.conversion_factor

    assert total_ml == 1_500_000


def test_range_model_fractional_factor_support():
    """
    Проверка работы с дробными значениями коэффициентов пересчёта.
    """
    ml_unit = range_model("миллилитр", 1)
    drop_unit = range_model("капля", 0.05, ml_unit)

    assert drop_unit.conversion_factor == 0.05
    assert drop_unit.base_range is ml_unit


def test_range_model_zero_conversion_factor_raises():
    """
    Проверка выброса arguments_exception при попытке установить нулевой коэффициент пересчёта.
    """
    with pytest.raises(arguments_exception):
        range_model("ошибка", 0)


def test_range_model_negative_conversion_factor_raises():
    """
    Проверка выброса arguments_exception при отрицательном коэффициенте пересчёта.
    """
    with pytest.raises(arguments_exception):
        range_model("ошибка", -12.5)


def test_range_model_non_numeric_factor_raises():
    """
    Передача строкового типа в качестве коэффициента должна вызывать arguments_exception.
    """
    with pytest.raises(arguments_exception):
        range_model("ошибка", "100")


def test_range_model_invalid_base_range_type_raises():
    """
    Проверка валидации типа для базовой единицы (должен передаваться объект range_model).
    """
    with pytest.raises(arguments_exception):
        range_model("литр", 1000, "миллилитр")