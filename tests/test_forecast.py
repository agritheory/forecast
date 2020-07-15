from decimal import Decimal

import pytest

from forecast import Forecast


@pytest.mark.skip
@pytest.mark.parametrize("method", [
    'percent_over_previous_period',
    'calculated_percent_over_previous_period',
    'last_year_to_this_year',
    'moving_average',
    'linear_approximiation',
    'least_squares_regression',
    'second_degree_approximiation',
    'flexible_method',
    'weighted_moving_average',
    'linear_smoothing',
    'expotential_smoothing',
    'exponential_smoothing_with_trend_and_seasonality'
])
def test_validate_forecast_method(method, dataset):
    assert Forecast(data=dataset, method=method)


def test_percent_over_previous_period():
    dataset = [128, 117, 115, 125, 122, 137, 140, 129, 131, 114, 119, 137]
    output = [141, 129, 127, 138, 134, 151, 154, 142, 144, 125, 131, 151]
    f = Forecast(data=dataset, method='percent_over_last_year', percent=110.0)
    for index, period in enumerate(f):
        assert period == Decimal(output[index])


def test_calculated_percent_over_previous_period():
    dataset = [None, None, None, None, None, None, None, None, 118, 123, 139, 133, 128, 117, 115, 125, 122, 137, 140, 129, 131, 114, 119, 137]
