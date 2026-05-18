import datetime

import polars as pl
import pytest

from src.utils.polars import TimesSeriesPolars, sliding_window


def test_times_series_polars_get():
    # Setup mock data
    df = pl.DataFrame({
        "Date": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)],
        "AAPL_Close": [150.0, 152.0],
        "AAPL_Volume": [1000, 1100],
        "SPY_Close": [400.0, 405.0]
    })
    
    ts = TimesSeriesPolars(data=df, index_ticker="SPY")
    
    # Test getting Close prices without index
    res = ts.get(cat="Close", include_index=False, include_date=True, rename=True)
    assert res.columns == ["Date", "AAPL"]
    assert res["AAPL"].to_list() == [150.0, 152.0]
    
    # Test include_index=True
    res_idx = ts.get(cat="Close", include_index=True, include_date=True, rename=True)
    assert "SPY" in res_idx.columns
    
    # Test without renaming
    res_no_rename = ts.get(cat="Close", include_index=False, rename=False)
    assert "AAPL_Close" in res_no_rename.columns
    assert "AAPL" not in res_no_rename.columns
    
def test_times_series_polars_calculate_logR():
    df = pl.DataFrame({
        "Date": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)],
        "AAPL_Close": [100.0, 110.0]
    })
    
    ts = TimesSeriesPolars(data=df)
    ts.calculate_logR()
    
    assert "AAPL_Close_logR" in ts.data.columns
    # log(110) - log(100) ≈ 0.0953
    # First value should be null or ignored
    log_returns = ts.data["AAPL_Close_logR"].to_list()
    assert log_returns[0] is None
    assert abs(log_returns[1] - 0.0953) < 0.001

def test_times_series_polars_calculate_logR_early_return():
    df = pl.DataFrame({
        "Date": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)],
        "AAPL_logR": [0.01, 0.02]
    })
    
    ts = TimesSeriesPolars(data=df)
    # This should return early and not duplicate or fail
    ts.calculate_logR()
    assert "AAPL_logR" in ts.data.columns

def test_times_series_polars_get_no_date():
    df = pl.DataFrame({
        "Date": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)],
        "AAPL_Close": [150.0, 152.0]
    })
    
    ts = TimesSeriesPolars(data=df)
    res = ts.get(cat="Close", include_date=False)
    assert "Date" not in res.columns
    assert "AAPL" in res.columns

def test_sliding_window():
    df = pl.DataFrame({
        "Date": [datetime.date(2023, 1, i) for i in range(1, 11)],
        "Value": list(range(10))
    })
    
    # Test normal iteration
    windows = list(sliding_window(df, first_date_limit=datetime.date(2023, 1, 5), window_length=3))
    assert len(windows) == 6
    assert len(windows[0]) == 3
    assert windows[0]["Value"].to_list() == [2, 3, 4]
    assert windows[-1]["Value"].to_list() == [7, 8, 9]

    # Test error condition
    with pytest.raises(ValueError, match="Missing"):
        list(sliding_window(df, first_date_limit=datetime.date(2023, 1, 3), window_length=5))
