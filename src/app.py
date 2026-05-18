import streamlit as st
from dotenv import load_dotenv

from src.config.logging_config import configure_logging

load_dotenv("src/config/.env")
configure_logging()


# --- PAGE SETUP ---
page_import = st.Page("views/page_import.py", title="Import", default=True)
page_export = st.Page("views/page_export.py", title="Export")
page_fourier = st.Page("views/page_fourier_analysis.py", title="Fourier Analysis")
page_forecasting = st.Page("views/page_forecasting.py", title="Forecasting")
page_solver = st.Page("views/page_solver.py", title="Solve")

pg = st.navigation({"Settings": [page_import, page_export], "DPT": [page_fourier, page_forecasting, page_solver]})
pg.run()
