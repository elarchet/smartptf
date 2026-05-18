from datetime import date

import pytest

from src.config.logging_config import configure_logging
from src.models.dpt.dpt_cls import DPT
from src.models.forecasting import Forecast
from src.models.load import MarketIndex, MarkKetIndexComponents

configure_logging()


@pytest.fixture
def sp500_close_subset():
    components = MarkKetIndexComponents(csv_path="data/index_compo/sp500_compo_until_2025-03-10.csv")
    compo = components.get_composition(date_ref=date(2024, 12, 31))
    sp500 = MarketIndex(name="SP500", compo=compo, date_end=date(2024, 12, 31), period="20y")
    sp500.load_from_csv()
    close = sp500.close
    non_index_cols = [col for col in close.columns if col not in {"Date", "GSPC.INDX"}]
    subset_cols = ["Date", "GSPC.INDX", *non_index_cols[:8]]
    return close.select(subset_cols)


def test_init(sp500_close_subset):
    dpt = DPT(data=sp500_close_subset, index_ticker="GSPC.INDX")
    dpt.calculate_signals()  # TODO add a control sin_theta**2 + cos_theta**2 = 1.0
    assert dpt.logR is not None, "Log returns should be calculated successfully"
    assert len(dpt.logR) > 0, "Log returns DataFrame should not be empty"

    val = (dpt.cos_theta.to_numpy() ** 2 + dpt.sin_theta.to_numpy() ** 2).flatten().sum()
    assert round(val, 3) == float(dpt.theta.shape[0] * dpt.theta.shape[1])


def test_solver(sp500_close_subset):
    dpt = DPT(data=sp500_close_subset, index_ticker="GSPC.INDX")
    dpt.calculate_signals()
    predictor = Forecast(data=dpt.data, index_ticker="GSPC.INDX")
    forecasts = predictor.moving_average(window=12)
    optimalpdf = dpt.solve(forecasts, S=5, C_alphas=0.8, C_betas=1.6)

    assert (optimalpdf.weights is not None) or (len(optimalpdf.weights) > 0)
    assert (optimalpdf.returns is not None )or (len(optimalpdf.returns) > 0)
    assert (optimalpdf.betas is not None) or (len(optimalpdf.betas) > 0)
    assert (optimalpdf.alphas is not None) or (len(optimalpdf.alphas) > 0)
    assert (optimalpdf.R is not None) or (len(optimalpdf.R) > 0)
    assert (optimalpdf.ptf_return is not None) or (len(optimalpdf.ptf_return) > 0)
    assert (optimalpdf.ptf_betas is not None) or (len(optimalpdf.ptf_betas) > 0)
    assert (optimalpdf.ptf_alphas is not None) or (len(optimalpdf.ptf_alphas) > 0)

def test_dpt_only_returns():
    # Test DPT initialization when only logR is provided
    # Should trigger the `if len(self.logR) == 0:` code block
    import polars as pl
    data = pl.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "AAPL_logR": [0.01, -0.02, 0.03],
        "GSPC.INDX_logR": [0.005, -0.01, 0.015]
    })
    dpt = DPT(data=data, index_ticker="GSPC.INDX")
    assert dpt.logR is not None
    assert len(dpt.logR) == 3

