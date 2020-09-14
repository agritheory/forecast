import typing
from inspect import getmembers, ismethod
from decimal import Decimal
import pandas as pd
from scipy import stats
import numpy as np


class Forecast:
    data: typing.Optional[typing.List] = None
    forecast: typing.Optional[typing.List] = None

    def __init__(self, **kwargs):
        self._idx = 1
        self(**kwargs)

    def __call__(
        self,
        data: typing.Optional[
            typing.Sequence[typing.Sequence[typing.Union[Decimal, int, float]]]
        ],
        **kwargs
    ) -> 'Forecast':
        if not self.data and not data:
            raise Exception("Cannot forecast without data")
        self.data = data if data else []
        return self

    def percent_over_previous_period(
        self, percent: typing.Union[float, Decimal]
    ) -> 'Forecast':
        percent = Decimal(percent)
        self.forecast = [
            Decimal(period) * (1 + percent / 100) for period in self.data[-1]
        ]
        return self

    def calculated_percent_over_previous_period(self) -> 'Forecast':
        n_minus_2_data = Decimal(sum(self.data[-2]))
        n_minus_1_data = Decimal(sum(self.data[-1]))
        percent = Decimal((n_minus_1_data / n_minus_2_data - 1) * 100)
        self.forecast = [Decimal(n) * (1 + percent / 100) for n in self.data[-1]]
        return self

    def previous_period_to_current_period(self) -> 'Forecast':
        self.forecast = self.data[-1]  # type: ignore
        return self

    def moving_average(self, periods: int) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(self._flat_data):
            raise Exception("Cannot forecast for more periods than data exists")
        moving_average = _data
        for i in range(periods):
            moving_average.append(Decimal(np.mean(moving_average[-periods:])))
        del moving_average[:periods]
        self.forecast = moving_average
        return self

    def linear_approximiation(self, periods: int) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        print(len(_data))
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        slope = Decimal((_data[-1] - _data[-periods + 1]) / periods)
        self.forecast = [Decimal(_data[-1]) + (slope * (i + 1)) for i in range(periods)]
        return self

    def least_squares_regression(self, periods: int) -> 'Forecast':
        x = range(1, periods + 1)
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        y = _data[-periods:]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        self.forecast = [
            Decimal(i * slope + intercept) for i in range(periods + 1, periods + 13)
        ]
        return self

    def second_degree_approximiation(self, periods: int) -> 'Forecast':
        x = range(1, periods + 1)
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        y = _data[-periods:]
        c, b, a = np.polyfit(x, y, deg=2)
        self.forecast = [
            Decimal(a + b * x + c * x ** 2) for x in range(periods + 1, periods + 13)
        ]
        return self

    def flexible_method(
        self, percent: typing.Union[float, Decimal], periods: int
    ) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        flexible_method = _data
        for i in range(periods):
            flexible_method.append(
                Decimal(flexible_method[i] * Decimal(1 + percent / 100))
            )
        del flexible_method[:periods]
        self.forecast = flexible_method
        return self

    def weighted_moving_average(
        self, periods: int, weights: typing.Union[list, tuple, np.array]
    ) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        if sum(weights) != 1:
            raise Exception("Total of weights must be exactly 1")
        if len(weights) != periods:
            raise Exception(
                "Weights must have as many elements as periods. Weights: {} Periods: {}".format(
                    len(weights), periods
                )
            )

        weighted_moving_average = _data[-periods:]

        for i in range(periods):
            weighted_moving_average.append(
                sum(weights * np.array(weighted_moving_average[i : i + periods]))
            )
        # Remove the historical data needed for the first several forecast period calcs
        del weighted_moving_average[:periods]
        self.forecast = [Decimal(n) for n in weighted_moving_average]
        return self

    def linear_smoothing(self, periods: int) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        W = (periods ** 2 + periods) / 2
        weights = np.array([n / W for n in range(1, periods + 1)])
        linear_smoothing = _data[-periods:]

        for i in range(12):
            linear_smoothing.append(
                sum(weights * np.array(linear_smoothing[i : i + periods]))
            )
        del linear_smoothing[:periods]

        self.forecast = [Decimal(n) for n in linear_smoothing]
        return self

    def exponential_smoothing(
        self, periods: int, alpha: typing.Union[float, Decimal]
    ) -> 'Forecast':
        _data = self._flat_data if periods > len(self.data[-1]) else self.data[-1]
        if periods - 1 > len(_data):
            raise Exception("Cannot forecast for more periods than data exists")
        smoothed = [_data[-periods]]
        tmp = _data[-periods + 1 :]

        for i, data in enumerate(tmp):
            smoothed.append(alpha * data + (1 - alpha) * smoothed[i])
        self.forecast = [Decimal(smoothed[-1])] * 12
        return self

    def exponential_smoothing_with_trend_and_seasonality(
        self,
        season: int,
        periods: int,
        alpha: typing.Union[float, Decimal],
        beta: typing.Union[float, Decimal],
    ) -> 'Forecast':
        alpha = Decimal(alpha)
        beta = Decimal(beta)

        # Calculate seasonality indices
        total_units = sum(self.data[-2]) + sum(self.data[-1])
        seasonality = [
            Decimal((data_n_minus_1 + self.data[-2][i]) / total_units * periods)
            for i, data_n_minus_1 in enumerate(self.data[-1])
        ]

        averages = [self.data[-1][0] / seasonality[0]]
        trends = [Decimal("0")]

        for i in range(periods):
            A_t = alpha * (self.data[-1][i] / seasonality[i]) + (1 - alpha) * (
                averages[i - 1] + trends[i - 1]
            )
            T_t = beta * (A_t - averages[i - 1]) + (1 - beta) * (trends[i - 1])
            averages.append(A_t)
            trends.append(T_t)
        exponential_smoothing_trend_seasonality = []

        for m in range(periods):
            F = (averages[-1] + trends[-1] * m) * seasonality[m - 1]
            exponential_smoothing_trend_seasonality.append(Decimal(F))
        self.forecast = exponential_smoothing_trend_seasonality
        return self

    @property
    def _flat_data(self):
        return [item for sublist in self.data for item in sublist]
