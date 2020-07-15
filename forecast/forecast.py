from __future__ import annotations

import typing
from inspect import getmembers, ismethod
from decimal import Decimal


class Forecast:
    data: typing.Optional[typing.List] = None
    forecast: typing.Optional[typing.List] = None
    periods: typing.Optional[int] = 12
    methods: typing.Optional[str] = None

    def __init__(self, **kwargs):
        self._idx = 1
        self(**kwargs)

    @property
    def percent_of_accuracy(self):
        pass

    @property
    def mean_absolute_deviation(self):
        pass

    @property
    def best_fit(self):
        pass

    def __call__(
        self,
        data,
        method,
        periods=12,
        **kwargs
    ) -> Forecast:
        if not self.data and not data:
            raise Exception("Cannot forecast without data")
        self.data = data if data else []
        self.validate_data()
        if method and self.validate_forecast_method(method):
            raise Exception("'{}'' is not an available forecast method".format(method))
        if method is not None:
            self.forecast = getattr(self, method)(**kwargs)
        return self

    def validate_forecast_method(self, method: str) -> typing.NoReturn:
        methods = [
            m[0] for m in getmembers(self) if not m[0].startswith("_") and ismethod(m[1])
        ]
        if method not in methods:
            raise Exception("'{}'' is not an available forecast method".format(method))

    def validate_data(self) -> typing.NoReturn:
        if not self.data:
            raise Exception("Data is required to forecast".format(method))

    def __iter__(self):
        return self

    def __next__(self):
        self._idx += 1
        try:
            return self.data[self._idx - 1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    def __repr__(self):
        return ",".join([str(Decimal(i)) for i in self.forecast])

    def percent_over_previous_period(self, **kwargs) -> Forecast:
        if not kwargs.get('percent'):
            raise Exception(
                "'Percent' is required for 'Percent Over Last Year' forecast method"
            )
        percent = Decimal(kwargs.get('percent'))
        periods = min(len(self.data) - 1, self.periods)
        last_year = self.data[-periods:]  # slice off last X periods
        self.forecast = [Decimal(i * (percent / 100)) for i in last_year]
        return self

    def calculated_percent_over_previous_period(self, **kwargs) -> Forecast:
        if not kwargs.get('percent'):
            raise Exception(
                "'Percent' is required for 'Percent Over Last Year' forecast method"
            )
        # len has to be >= periods + 1
        # default percentage is 100
        percent = Decimal(kwargs.get('percent'))
        periods = min(len(self.data) - 1, self.periods)
        last_year = self.data[-periods:]  # slice off last X periods
        self.forecast = [Decimal(i * (percent / 100)) for i in last_year]
        return self

    def previous_period_to_current_period(self, **kwargs):
        pass

    def moving_average(self):
        pass

    def linear_approximiation(self):
        pass

    def least_squares_regression(self):
        pass

    def second_degree_approximiation(self):
        pass

    def flexible_method(self):
        pass

    def weighted_moving_average(self):
        pass

    def linear_smoothing(self):
        pass

    def expotential_smoothing(self):
        pass

    def exponential_smoothing_with_trend_and_seasonality(self):
        pass
