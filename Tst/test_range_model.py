import pytest
from src.core.exception import arguments_exception
from src.models.range_model import range_model


def test_range_model_base_unit_initialization():
    """
    <summary>
    Проверка успешного создания базовой единицы измерения (без указания родительской).
    </summary>
    """
    # Подготовка
    unit_name = "миллилитр"
    factor = 1

    # Действие
    base_unit = range_model(unit_name, factor)

    # Проверка
    assert base_unit.name == unit_name
    assert base_unit.conversion_factor == factor
    assert base_unit.coefficient == factor
    assert base_unit.base_range is None
    assert base_unit.base is None


def test_range_model_derived_unit_initialization():
    """
    <summary>
    Проверка создания производной единицы с привязкой к базовой единице измерения.
    </summary>
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    derived_name = "литр"
    derived_factor = 1000

    # Действие
    liter_unit = range_model(derived_name, derived_factor, ml_unit)

    # Проверка
    assert liter_unit.name == derived_name
    assert liter_unit.conversion_factor == derived_factor
    assert liter_unit.base_range is ml_unit
    assert liter_unit.base.name == "миллилитр"


def test_range_model_conversion_factor_calculation():
    """
    <summary>
    Проверка корректности расчёта пересчёта количества объёма через коэффициент.
    </summary>
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)
    volume_liters = 3.5

    # Действие
    volume_ml = volume_liters * liter_unit.conversion_factor

    # Проверка
    assert volume_ml == 3500


def test_range_model_multilevel_conversion():
    """
    <summary>
    Проверка последовательного пересчёта величин по цепочке производных единиц (куб. м -> литр -> мл).
    </summary>
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)
    cubic_m_unit = range_model("куб. м", 1000, liter_unit)
    volume_cubic_m = 1.5

    # Действие
    total_ml = volume_cubic_m * cubic_m_unit.conversion_factor * liter_unit.conversion_factor

    # Проверка
    assert total_ml == 1_500_000


def test_range_model_fractional_factor_support():
    """
    <summary>
    Проверка работы с дробными значениями коэффициентов пересчёта.
    </summary>
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    unit_name = "капля"
    fractional_factor = 0.05

    # Действие
    drop_unit = range_model(unit_name, fractional_factor, ml_unit)

    # Проверка
    assert drop_unit.conversion_factor == fractional_factor
    assert drop_unit.base_range is ml_unit


def test_range_model_zero_conversion_factor_raises():
    """
    <summary>
    Проверка выброса arguments_exception при попытке установить нулевой коэффициент пересчёта.
    </summary>
    """
    # Подготовка
    unit_name = "ошибка"
    zero_factor = 0

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        range_model(unit_name, zero_factor)


def test_range_model_negative_conversion_factor_raises():
    """
    <summary>
    Проверка выброса arguments_exception при отрицательном коэффициенте пересчёта.
    </summary>
    """
    # Подготовка
    unit_name = "ошибка"
    negative_factor = -12.5

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        range_model(unit_name, negative_factor)


def test_range_model_non_numeric_factor_raises():
    """
    <summary>
    Передача строкового типа в качестве коэффициента должна вызывать arguments_exception.
    </summary>
    """
    # Подготовка
    unit_name = "ошибка"
    invalid_factor = "100"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        range_model(unit_name, invalid_factor)


def test_range_model_invalid_base_range_type_raises():
    """
    <summary>
    Проверка валидации типа для базовой единицы (должен передаваться объект range_model).
    </summary>
    """
    # Подготовка
    unit_name = "литр"
    factor = 1000
    invalid_base_range = "миллилитр"

    # Действие & Проверка
    with pytest.raises(arguments_exception):
        range_model(unit_name, factor, invalid_base_range)