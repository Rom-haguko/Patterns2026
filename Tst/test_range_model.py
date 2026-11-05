import pytest
from src.core.exception import arguments_exception
from src.models.range_model import range_model


def test_range_model_base_unit_initialization():
    """
    Проверка успешного создания базовой единицы измерения.
    """
    # Подготовка
    unit_name = "миллилитр"
    factor = 1

    # Действие
    base_unit = range_model(unit_name, factor)

    # Проверки
    assert base_unit.name == unit_name
    assert base_unit.conversion_factor == factor
    assert base_unit.base_range is None


def test_range_model_derived_unit_initialization():
    """
    Проверка создания производной единицы с привязкой к базовой единице измерения.
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    derived_name = "литр"
    derived_factor = 1000

    # Действие
    liter_unit = range_model(derived_name, derived_factor, ml_unit)

    # Проверки
    assert liter_unit.name == derived_name
    assert liter_unit.conversion_factor == derived_factor
    assert liter_unit.base_range is ml_unit


def test_range_model_conversion_factor_calculation():
    """
    Проверка корректности коэффициента пересчёта и привязки базовой единицы.
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)

    # Действие
    liter_unit = range_model("литр", 1000, ml_unit)

    # Проверки
    assert liter_unit.conversion_factor == 1000
    assert liter_unit.base_range is ml_unit


def test_range_model_multilevel_conversion():
    """
    Проверка последовательной цепочки производных единиц (куб. м -> литр -> мл).
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    liter_unit = range_model("литр", 1000, ml_unit)

    # Действие
    cubic_m_unit = range_model("куб. м", 1000, liter_unit)

    # Проверки
    assert cubic_m_unit.base_range is liter_unit
    assert cubic_m_unit.base_range.base_range is ml_unit
    assert cubic_m_unit.total_conversion_factor == 1000000.0


def test_range_model_to_base_calculation():
    """
    Проверка расчёта пересчёта значения в базовые единицы измерения.
    """
    # Подготовка
    gram = range_model("грамм", 1)
    kg = range_model("килограмм", 1000, gram)
    ton = range_model("тонна", 1000, kg)

    # Действие
    result_kg_to_gram = kg.to_base(2.5)
    result_ton_to_gram = ton.to_base(0.5)

    # Проверки
    assert result_kg_to_gram == 2500.0
    assert result_ton_to_gram == 500000.0


def test_range_model_factory_methods():
    """
    Проверка фабричных методов создания стандартных единиц измерения.
    """
    # Подготовка
    # Действие
    gram = range_model.create_gram()
    kg = range_model.create_kilogram()
    ml = range_model.create_milliliter()
    liter = range_model.create_liter()
    piece = range_model.create_piece()

    # Проверки
    assert gram.name == "грамм"
    assert gram.conversion_factor == 1
    assert kg.name == "килограмм"
    assert kg.conversion_factor == 1000
    assert kg.base_range.name == "грамм"
    assert ml.name == "миллилитр"
    assert liter.name == "литр"
    assert liter.conversion_factor == 1000
    assert liter.base_range.name == "миллилитр"
    assert piece.name == "штука"
    assert piece.conversion_factor == 1


def test_range_model_fractional_factor_support():
    """
    Проверка работы с дробными значениями коэффициентов пересчёта.
    """
    # Подготовка
    ml_unit = range_model("миллилитр", 1)
    unit_name = "капля"
    fractional_factor = 0.05

    # Действие
    drop_unit = range_model(unit_name, fractional_factor, ml_unit)

    # Проверки
    assert drop_unit.conversion_factor == fractional_factor
    assert drop_unit.base_range is ml_unit
    assert drop_unit.to_base(10) == 0.5


def test_range_model_zero_conversion_factor_raises():
    """
    Проверка выброса arguments_exception при попытке установить нулевой коэффициент пересчёта.
    """
    # Подготовка
    unit_name = "ошибка"
    zero_factor = 0

    # Действие & Проверки
    # Действие
    with pytest.raises(arguments_exception):
        range_model(unit_name, zero_factor)

    # Проверки
    assert True


def test_range_model_negative_conversion_factor_raises():
    """
    Проверка выброса arguments_exception при отрицательном коэффициенте пересчёта.
    """
    # Подготовка
    unit_name = "ошибка"
    negative_factor = -12.5

    # Действие
    with pytest.raises(arguments_exception):
        range_model(unit_name, negative_factor)

    # Проверки
    assert True


def test_range_model_non_numeric_factor_raises():
    """
    Передача строкового типа в качестве коэффициента должна вызывать arguments_exception.
    """
    # Подготовка
    unit_name = "ошибка"
    invalid_factor = "100"

    # Действие
    with pytest.raises(arguments_exception):
        range_model(unit_name, invalid_factor)

    # Проверки
    assert True


def test_range_model_invalid_base_range_type_raises():
    """
    Проверка валидации типа для базовой единицы (должен передаваться объект range_model).
    """
    # Подготовка
    unit_name = "литр"
    factor = 1000
    invalid_base_range = "миллилитр"

    # Действие
    with pytest.raises(arguments_exception):
        range_model(unit_name, factor, invalid_base_range)

    # Проверки
    assert True
