"""
helpers.py
----------
Core data-loading, cleaning and generic utility functions shared across the
Rwanda DHS 2019-20 Dashboard. All Excel parsing lives here so that every other
module works with clean, ready-to-use pandas DataFrames.

Author: Faustin NIZEYIMANA
"""

from __future__ import annotations

import base64
import os
from typing import Dict

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "rwanda_dhs_2019_20.xlsx")
GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rwanda.geojson")

PROVINCES = ["National", "Kigali City", "Southern", "Eastern", "Northern", "Western"]

# Rwanda-inspired professional palette (deep blue, sunny yellow, green, muted teal)
COLORS = {
    "primary": "#00205B",     # deep national blue
    "secondary": "#1B9E77",   # green
    "accent": "#FDB813",      # sunny yellow
    "danger": "#C0392B",
    "info": "#2E86C1",
    "muted": "#6B7280",
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text": "#1F2933",
}

SEQUENTIAL_SCALE = ["#EAF4FF", "#9CC7E8", "#4E92C9", "#1D5B9E", "#00205B"]
CATEGORICAL_SCALE = ["#00205B", "#1B9E77", "#FDB813", "#2E86C1", "#C0392B", "#6B7280"]


# --------------------------------------------------------------------------
# Sheet loading helpers
# --------------------------------------------------------------------------

def _clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Drop trailing footer / blank rows that trail the real microdata rows.

    The source workbook appends notes such as '© Faustin 2026 | Source: ...'
    below the data. Any row whose 'SN' (serial number) column is not a valid
    integer is considered a non-data row and is dropped.
    """
    if "SN" not in df.columns:
        return df.dropna(how="all")

    def _is_valid_sn(v):
        try:
            if pd.isna(v):
                return False
            float(v)
            return True
        except (ValueError, TypeError):
            return False

    mask = df["SN"].apply(_is_valid_sn)
    cleaned = df.loc[mask].copy()
    return cleaned.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_all_data(path: str = DATA_PATH) -> Dict[str, pd.DataFrame]:
    """Load and clean every sheet of the Rwanda DHS workbook.

    Returns a dict of DataFrames keyed by a short logical name:
    women, households, children, summary, province_table, edu_wealth
    """
    xls = pd.ExcelFile(path)
    sheet_map = {
        "women": "👩 Women (IR)",
        "households": "🏠 Households (HR)",
        "children": "👶 Children (KR)",
        "summary": "📊 Summary Stats",
        "province_table": "📈 Province Table",
        "edu_wealth": "🎓 Edu × Wealth",
    }

    data: Dict[str, pd.DataFrame] = {}
    for key, sheet_name in sheet_map.items():
        if sheet_name not in xls.sheet_names:
            continue
        header_row = 3 if key == "summary" else 4
        df = pd.read_excel(path, sheet_name=sheet_name, header=header_row)
        data[key] = _clean_frame(df)

    # Normalize province labels so filters line up everywhere
    for key in ("women", "households", "children"):
        if key in data and "Province" in data[key].columns:
            data[key]["Province"] = data[key]["Province"].astype(str).str.strip()

    return data


# --------------------------------------------------------------------------
# Generic numeric / formatting helpers
# --------------------------------------------------------------------------

def pct(numerator: float, denominator: float, decimals: int = 1) -> float:
    """Safe percentage calculation that never raises on zero denominators."""
    if not denominator:
        return 0.0
    return round(100.0 * numerator / denominator, decimals)


def share_of(series: pd.Series, value_or_values) -> float:
    """Return the percentage share of rows in `series` matching value(s)."""
    if series.empty:
        return 0.0
    if isinstance(value_or_values, (list, tuple, set)):
        mask = series.isin(value_or_values)
    else:
        mask = series == value_or_values
    valid = series.dropna()
    if valid.empty:
        return 0.0
    return pct(mask.sum(), len(valid))


def fmt_number(value: float, decimals: int = 0, suffix: str = "") -> str:
    """Human friendly number formatting with thousands separators."""
    if pd.isna(value):
        return "N/A"
    if decimals == 0:
        return f"{value:,.0f}{suffix}"
    return f"{value:,.{decimals}f}{suffix}"


def fmt_pct(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"


def df_to_csv_download(df: pd.DataFrame, filename: str, label: str = "Download CSV") -> None:
    """Render a Streamlit download button for a DataFrame as CSV."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇ {label}",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
        use_container_width=False,
    )


def load_css(css_path: str) -> None:
    """Inject a local CSS file into the Streamlit app."""
    if not os.path.exists(css_path):
        return
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_geojson(path: str = GEOJSON_PATH) -> dict:
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def image_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
