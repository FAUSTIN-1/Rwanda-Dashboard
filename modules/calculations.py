"""
calculations.py
----------------
All statistical computation logic for the Rwanda DHS 2019-20 Dashboard.
Every function here is pure: it takes DataFrames (already filtered by
province if needed) and returns numbers, Series or small DataFrames.
Keeping calculations separate from rendering makes the app testable and
avoids duplicated logic across chart/card modules.

Author: Faustin NIZEYIMANA
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from modules.helpers import pct, share_of


# --------------------------------------------------------------------------
# Filtering
# --------------------------------------------------------------------------

def filter_by_province(df: pd.DataFrame, province: str) -> pd.DataFrame:
    """Return rows for the selected province, or the whole DataFrame for
    'National'. Safe against missing 'Province' column."""
    if province == "National" or "Province" not in df.columns:
        return df
    return df[df["Province"] == province]


# --------------------------------------------------------------------------
# KPI card calculations
# --------------------------------------------------------------------------

def kpi_family_planning(women: pd.DataFrame) -> dict:
    total = women["Contraceptive Use"].dropna()
    value = share_of(total, "Modern")
    return {"value": value, "n": len(total)}


def kpi_child_nutrition(children: pd.DataFrame) -> dict:
    total = children["Stunted"].dropna()
    value = share_of(total, "Stunted")
    return {"value": value, "n": len(total)}


def kpi_hiv_tested(women: pd.DataFrame) -> dict:
    total = women["Ever Tested Hiv"].dropna()
    value = share_of(total, "Yes")
    return {"value": value, "n": len(total)}


def kpi_health_insurance(women: pd.DataFrame) -> dict:
    total = women["Has Health Insurance"].dropna()
    value = share_of(total, "Yes")
    return {"value": value, "n": len(total)}


def kpi_fertility(women: pd.DataFrame) -> dict:
    series = women["Num Children Ever Born"].dropna()
    value = round(series.mean(), 2) if len(series) else 0.0
    return {"value": value, "n": len(series)}


def compute_all_kpis(women: pd.DataFrame, children: pd.DataFrame) -> dict:
    return {
        "family_planning": kpi_family_planning(women),
        "child_nutrition": kpi_child_nutrition(children),
        "hiv_tested": kpi_hiv_tested(women),
        "health_insurance": kpi_health_insurance(women),
        "fertility": kpi_fertility(women),
    }


# --------------------------------------------------------------------------
# Map / indicator calculations (province-level)
# --------------------------------------------------------------------------

MAP_INDICATORS = {
    "Modern Contraceptive Prevalence": {
        "source": "women", "column": "Contraceptive Use", "match": "Modern", "unit": "%",
    },
    "Child Stunting": {
        "source": "children", "column": "Stunted", "match": "Stunted", "unit": "%",
    },
    "Health Insurance Coverage": {
        "source": "women", "column": "Has Health Insurance", "match": "Yes", "unit": "%",
    },
    "HIV Testing": {
        "source": "women", "column": "Ever Tested Hiv", "match": "Yes", "unit": "%",
    },
    "Fertility Rate": {
        "source": "women", "column": "Num Children Ever Born", "match": None, "unit": "children",
    },
    "Skilled Antenatal Care": {
        "source": "women", "column": "Skilled Antenatal", "match": "Yes", "unit": "%",
    },
}


def province_indicator_table(data: dict, indicator_name: str) -> pd.DataFrame:
    """Build a province x indicator-value table for the choropleth map."""
    spec = MAP_INDICATORS[indicator_name]
    df = data[spec["source"]]
    provinces = [p for p in df["Province"].dropna().unique() if p]

    rows = []
    for prov in provinces:
        sub = df[df["Province"] == prov]
        col = sub[spec["column"]].dropna()
        if spec["match"] is None:
            value = round(col.mean(), 2) if len(col) else np.nan
        else:
            value = share_of(col, spec["match"])
        rows.append({"Province": prov, "Value": value, "Sample Size": len(col)})

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Analytics-section calculations
# --------------------------------------------------------------------------

def population_pyramid_data(women: pd.DataFrame, households: pd.DataFrame) -> pd.DataFrame:
    """Approximate a population pyramid using women's age groups as the
    female side. Since the dataset only truly samples women 15-49, we
    frame this transparently as a 'Women 15-49 age structure' pyramid."""
    order = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
    counts = women["Age Group"].value_counts().reindex(order).fillna(0)
    return pd.DataFrame({"Age Group": order, "Women": counts.values})


def age_distribution(women: pd.DataFrame) -> pd.Series:
    return women["Age"].dropna()


def fertility_by_age_group(women: pd.DataFrame) -> pd.DataFrame:
    grp = women.groupby("Age Group", observed=True)["Num Children Ever Born"].mean().round(2)
    order = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
    grp = grp.reindex(order)
    return grp.reset_index().rename(columns={"Num Children Ever Born": "Mean Children Born"})


def maternal_care_cascade(women: pd.DataFrame, children: pd.DataFrame) -> pd.DataFrame:
    """Funnel: Skilled ANC -> Facility Delivery -> Skilled Birth Attendant."""
    anc_visits = women["Antenatal Visits"].dropna() if "Antenatal Visits" in women.columns else pd.Series(dtype=float)
    anc_any = pct((anc_visits > 0).sum(), len(anc_visits)) if len(anc_visits) else 0.0
    skilled_anc = share_of(women["Skilled Antenatal"].dropna(), "Yes")
    facility_col = children["Delivery In Facility"].dropna() if "Delivery In Facility" in children.columns else pd.Series(dtype=object)
    facility_delivery = share_of(facility_col, "Yes") if len(facility_col) else 0.0
    skilled_delivery = share_of(children["Delivery By Skilled"].dropna(), "Yes")

    stages = [
        ("Any ANC visit", anc_any),
        ("Skilled ANC provider", skilled_anc),
        ("Delivered in facility", facility_delivery),
        ("Skilled birth attendant", skilled_delivery),
    ]
    return pd.DataFrame(stages, columns=["Stage", "Percent"])


def child_nutrition_breakdown(children: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Stunted", share_of(children["Stunted"].dropna(), "Stunted")),
        ("Underweight", share_of(children["Underweight"].dropna(), "Underweight")),
        ("Wasted", share_of(children["Wasted"].dropna(), "Wasted")),
    ]
    return pd.DataFrame(rows, columns=["Indicator", "Percent"])


def wealth_distribution(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Poorest", "Poor", "Middle", "Richer", "Richest"]
    counts = df["Wealth Index"].value_counts().reindex(order).fillna(0)
    return pd.DataFrame({"Wealth Quintile": order, "Count": counts.values})


def education_wealth_heatmap(women: pd.DataFrame, value_col: str = "Contraceptive Use", match: str = "Modern") -> pd.DataFrame:
    edu_order = ["No Education", "Primary", "Secondary", "Higher"]
    wealth_order = ["Poorest", "Poor", "Middle", "Richer", "Richest"]
    pivot = pd.pivot_table(
        women.assign(_flag=(women[value_col] == match)),
        index="Education Level",
        columns="Wealth Index",
        values="_flag",
        aggfunc="mean",
    ) * 100
    pivot = pivot.reindex(index=edu_order, columns=wealth_order)
    return pivot.round(1)


def household_infrastructure(households: pd.DataFrame) -> pd.DataFrame:
    indicators = {
        "Electricity": ("Has Electricity", "Yes"),
        "Mobile Phone": ("Has Mobile Phone", "Yes"),
        "Bank Account": ("Has Bank Account", "Yes"),
        "Mosquito Net": ("Has Mosquito Net", "Yes"),
        "Radio": ("Has Radio", "Yes"),
        "TV": ("Has Tv", "Yes"),
        "Refrigerator": ("Has Refrigerator", "Yes"),
        "Owns Land": ("Owns Land", "Yes"),
    }
    rows = []
    for label, (col, match) in indicators.items():
        if col in households.columns:
            rows.append({"Indicator": label, "Percent": share_of(households[col].dropna(), match)})
    return pd.DataFrame(rows).sort_values("Percent", ascending=False)


def province_comparison_table(data: dict, indicators: list[str]) -> pd.DataFrame:
    """Wide table: rows = provinces, columns = requested indicator names."""
    frames = []
    for ind in indicators:
        t = province_indicator_table(data, ind).set_index("Province")["Value"]
        t.name = ind
        frames.append(t)
    return pd.concat(frames, axis=1).reset_index()


def slope_chart_data(data: dict, indicator: str) -> pd.DataFrame:
    """Compare Urban vs Rural for a given indicator across residence type."""
    spec = MAP_INDICATORS[indicator]
    df = data[spec["source"]]
    rows = []
    for res in ["Urban", "Rural"]:
        sub = df[df["Residence"] == res]
        col = sub[spec["column"]].dropna()
        if spec["match"] is None:
            value = round(col.mean(), 2) if len(col) else np.nan
        else:
            value = share_of(col, spec["match"])
        rows.append({"Residence": res, "Value": value})
    return pd.DataFrame(rows)


def education_distribution(women: pd.DataFrame) -> pd.DataFrame:
    order = ["No Education", "Primary", "Secondary", "Higher"]
    counts = women["Education Level"].value_counts().reindex(order).fillna(0)
    return pd.DataFrame({"Education Level": order, "Count": counts.values})


def sample_sizes(data: dict) -> dict:
    return {
        "women": len(data.get("women", [])),
        "households": len(data.get("households", [])),
        "children": len(data.get("children", [])),
    }
