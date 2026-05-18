from datetime import date

import pandas as pd
import polars as pl
import pytest

from src.config.logging_config import configure_logging
from src.models.Load import MarketIndex, MarkKetIndexComponents

configure_logging()


CSV_COMPO_PATH = "data/index_compo/sp500_compo_until_2025-03-10.csv"


@pytest.fixture
def sp500():
    components = MarkKetIndexComponents(csv_path=CSV_COMPO_PATH)
    compo = components.get_composition(date_ref=date(2024, 12, 31))
    return MarketIndex(name="SP500", compo=compo, date_end=date(2024, 12, 31), period="20y")


@pytest.fixture
def components():
    return MarkKetIndexComponents(csv_path=CSV_COMPO_PATH)


def test_load_from_yahoo(sp500, monkeypatch):
    dates = pd.to_datetime(["2024-10-31", "2024-11-30", "2024-12-31"])
    columns = pd.MultiIndex.from_tuples(
        [
            ("AAPL", "Open"),
            ("AAPL", "High"),
            ("AAPL", "Low"),
            ("AAPL", "Close"),
            ("AAPL", "Volume"),
            ("GSPC.INDX", "Open"),
            ("GSPC.INDX", "High"),
            ("GSPC.INDX", "Low"),
            ("GSPC.INDX", "Close"),
            ("GSPC.INDX", "Volume"),
        ]
    )
    fake_df = pd.DataFrame(
        [
            [100, 101, 99, 100, 1000, 4000, 4050, 3980, 4020, 1000000],
            [101, 102, 100, 101, 1100, 4020, 4060, 4010, 4040, 1050000],
            [102, 103, 101, 102, 1200, 4040, 4070, 4030, 4060, 1100000],
        ],
        index=dates,
        columns=columns,
    )

    monkeypatch.setattr("src.models.Load.yf.download", lambda *args, **kwargs: fake_df)
    sp500.load_from_yahoo()
    assert sp500.data is not None, "Data should be loaded successfully"
    assert len(sp500.data) > 0, "Data should not be empty"
    assert len(sp500.close) > 0, "Close data should not be empty"


def test_load_from_csv(sp500):
    sp500.load_from_csv()
    assert sp500.data is not None, "Data should be loaded successfully from CSV"
    assert len(sp500.data) > 0, "Data should not be empty after loading from CSV"
    assert len(sp500.open) > 0, "Open data should not be empty"


def test_load_from_eodhd(sp500):
    class DummyEodhd:
        def get_historical(self, tickers, from_date, to_date, display_progress=True):
            del tickers, from_date, to_date, display_progress
            return pl.DataFrame(
                {
                    "Date": [date(2024, 10, 31), date(2024, 11, 30), date(2024, 12, 31)],
                    "AAPL_Open": [100.0, 101.0, 102.0],
                    "AAPL_High": [101.0, 102.0, 103.0],
                    "AAPL_Low": [99.0, 100.0, 101.0],
                    "AAPL_Close": [100.0, 101.0, 102.0],
                    "AAPL_Volume": [1000.0, 1100.0, 1200.0],
                    "GSPC.INDX_Open": [4000.0, 4020.0, 4040.0],
                    "GSPC.INDX_High": [4050.0, 4060.0, 4070.0],
                    "GSPC.INDX_Low": [3980.0, 4010.0, 4030.0],
                    "GSPC.INDX_Close": [4020.0, 4040.0, 4060.0],
                    "GSPC.INDX_Volume": [1000000.0, 1050000.0, 1100000.0],
                }
            )

    sp500._eodhd_client = DummyEodhd()
    sp500.load_from_eodhd(display_progress=False)
    assert sp500.data is not None, "Data should be loaded successfully from EODHD"
    assert len(sp500.data) > 0, "Data should not be empty after loading from EODHD"
    assert len(sp500.high) > 0, "High data should not be empty"


def test_get_composition(components):
    compo = components.get_composition(date_ref=date(2025, 3, 10))
    assert compo is not None, "Composition should be retrieved successfully"
    assert len(compo) > 0, "Composition should not be empty"


def test_to_csv(sp500, tmp_path):
    sp500.load_from_csv()
    sp500.to_csv(directory=tmp_path)
    assert sp500.csv_data_path.exists(), "CSV file should be created"
