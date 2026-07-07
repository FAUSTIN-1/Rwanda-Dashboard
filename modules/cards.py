"""
cards.py
--------
Renders the five headline KPI cards: Family Planning, Child Nutrition,
HIV Tested, Health Insurance, and Fertility.
Author: Faustin NIZEYIMANA
"""
import streamlit as st
from modules.helpers import fmt_pct, fmt_number
CARD_SPECS = [
    {
        "key": "family_planning",
        "icon": "🗓️",
        "color": "#00205B",
        "bg": "rgba(0,32,91,0.08)",
        "label": "Family Planning",
        "subtitle": "Modern contraceptive use",
        "is_pct": True,
    },
    {
        "key": "child_nutrition",
        "icon": "⚖️",
        "color": "#C0392B",
        "bg": "rgba(192,57,43,0.08)",
        "label": "Child Nutrition",
        "subtitle": "Children stunted (under 5)",
        "is_pct": True,
    },
    {
        "key": "hiv_tested",
        "icon": "🧪",
        "color": "#1B9E77",
        "bg": "rgba(27,158,119,0.08)",
        "label": "HIV Tested",
        "subtitle": "Women ever tested for HIV",
        "is_pct": True,
    },
    {
        "key": "health_insurance",
        "icon": "🛡️",
        "color": "#2E86C1",
        "bg": "rgba(46,134,193,0.08)",
        "label": "Health Insurance",
        "subtitle": "Women with health coverage",
        "is_pct": True,
    },
    {
        "key": "fertility",
        "icon": "👨‍👩‍👧",
        "color": "#FDB813",
        "bg": "rgba(253,184,19,0.14)",
        "label": "Fertility",
        "subtitle": "Mean children ever born",
        "is_pct": False,
    },
]
def render_kpi_cards(kpis: dict) -> None:
    cols = st.columns(5)
    for col, spec in zip(cols, CARD_SPECS):
        data = kpis[spec["key"]]
        value_str = fmt_pct(data["value"]) if spec["is_pct"] else fmt_number(data["value"], decimals=2)
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon" style="background:{spec['bg']}; color:{spec['color']};">{spec['icon']}</div>
                    <div class="kpi-value">{value_str}</div>
                    <div class="kpi-label">{spec['label']}</div>
                    <div class="kpi-subtitle">{spec['subtitle']} &nbsp;·&nbsp; n={data['n']:,}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
