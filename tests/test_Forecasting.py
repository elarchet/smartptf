from datetime import date

import polars as pl
import pytest

from src.config.logging_config import configure_logging
from src.models.Forecasting import Forecast

configure_logging()


@pytest.fixture
def predictor():
    dates = [date(2023, m, 28) for m in range(1, 13)] + [date(2024, m, 28) for m in range(1, 13)]
    data = pl.DataFrame({
        "Date": dates,
        "AAA_logR": [0.001 * i for i in range(24)],
        "BBB_logR": [0.0005 * i for i in range(24)],
        "GSPC.INDX_logR": [0.0008 * i for i in range(24)],
    })
    return Forecast(data=data, index_ticker="GSPC.INDX")


def test_moving_average(predictor: Forecast):
    predictions = predictor.moving_average(window=5)
    assert "AAA" in predictions
    assert "BBB" in predictions
    assert "GSPC.INDX" not in predictions
    assert predictions["AAA"] == 0.001 * (19 + 20 + 21 + 22 + 23) / 5
    assert predictions["BBB"] == 0.0005 * (19 + 20 + 21 + 22 + 23) / 5

    # Test polars output
    pred_df = predictor.moving_average(window=5, output="polars")
    assert isinstance(pred_df, pl.DataFrame)
    assert "AAA" in pred_df.columns
    assert pred_df.item(0, "AAA") == predictions["AAA"]


def test_arima(predictor):
    predictions = predictor.arima(approximation=True)
    assert predictions is not None, "ARIMA prediction should be calculated successfully"
    assert "AAA" in predictions
    assert "BBB" in predictions

    # Test polars output
    pred_df = predictor.arima(approximation=True, output="polars")
    assert isinstance(pred_df, pl.DataFrame)
    assert "AAA" in pred_df.columns

    # Test explicit order not implemented
    with pytest.raises(NotImplementedError):
        predictor.arima(auto=False)


def test_unimplemented_forecasts(predictor):
    with pytest.raises(NotImplementedError):
        predictor.exponential_smoothing()
        
    with pytest.raises(NotImplementedError):
        predictor.lstm()
