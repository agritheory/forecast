# Forecast

## A brief example

```python
>>> fc = Forecast(
        data=[
            [128, 117, 115, 125, 122, 137, 140, 129, 131, 114, 119, 137],
            [125, 123, 115, 137, 122, 130, 141, 128, 118, 123, 139, 133],
        ]
    )
>>> fc.percent_over_previous_period(10).forecast

[Decimal('137.5'), Decimal('135.3'), Decimal('126.5'), Decimal('150.7'), Decimal('134.2'), Decimal('143.0'), Decimal('155.1'), Decimal('140.8'), Decimal('129.8'), Decimal('135.3'), Decimal('152.9'), Decimal('146.3')]

```

## Running Tests

To run pytest:
```bash
python -m pytest
```


To run mypy
```bash 
python -m pytest --mypy -m mypy forecast/ tests/
```