"""
=============================================================================
 Rwanda DHS 2019-20 Dashboard
 National Health and Demographic Intelligence
-----------------------------------------------------------------------------
 A production-grade Streamlit analytics application built entirely from the
 Rwanda DHS 2019-20 survey microdata (Women, Households, Children recodes).

 This file (app.py) is the main entry point. It is intentionally kept as a
 thin orchestration layer: it wires together the reusable, single-purpose
 modules that live under /modules (header, footer, cards, filters, map,
 charts, tables, calculations, helpers) rather than embedding business
 logic directly here. This separation of concerns keeps the codebase
 maintainable, testable and easy to extend with new indicators or charts.

 Run locally:
     streamlit run app.py

 Author : Faustin NIZEYIMANA — Statistician and Data Analyst
 Source : National Institute of Statistics of Rwanda (NISR), Rwanda DHS 2019-20
=============================================================================
"""

from __future__ import annotations

import streamlit as st

from modules.helpers import load_all_data, load_css, DATA_PATH
from modules.calculations import (
    filter_by_province,
    compute_all_kpis,
    sample_sizes,
)
from modules.header import render_header
from modules.footer import render_footer
from modules.filters import render_province_filter
from modules.cards import render_kpi_cards
from modules import charts
from modules.map import render_map
from modules.tables import render_data_table


# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Rwanda DHS 2019–20 Dashboard | National Health & Demographic Intelligence",
    page_icon="🇷🇼",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# 2. GLOBAL STYLING
# =============================================================================

load_css("style.css")


# =============================================================================
# 3. DATA LOADING (cached — see modules/helpers.py::load_all_data)
# =============================================================================

@st.cache_data(show_spinner="Loading Rwanda DHS 2019–20 microdata…")
def get_data():
    return load_all_data(DATA_PATH)


try:
    raw_data = get_data()
except FileNotFoundError:
    st.error(
        "The Rwanda DHS 2019–20 dataset could not be found at "
        f"`{DATA_PATH}`. Please make sure the Excel workbook is present "
        "under the `data/` folder before running the dashboard."
    )
    st.stop()

REQUIRED_SHEETS = ["women", "households", "children"]
missing = [s for s in REQUIRED_SHEETS if s not in raw_data or raw_data[s].empty]
if missing:
    st.error(f"The following required data sheets are missing or empty: {missing}")
    st.stop()


# =============================================================================
# 4. HEADER
# =============================================================================

render_header()


# =============================================================================
# 5. PROVINCE FILTER (replaces all tab-based navigation)
# =============================================================================

selected_province = render_province_filter()

women_all = raw_data["women"]
households_all = raw_data["households"]
children_all = raw_data["children"]

women = filter_by_province(women_all, selected_province)
households = filter_by_province(households_all, selected_province)
children = filter_by_province(children_all, selected_province)

filtered_data = {
    "women": women,
    "households": households,
    "children": children,
}

# The choropleth map and province-comparison views always need the FULL,
# unfiltered dataset (they compare provinces against one another), while
# every other component reacts to the province filter.
national_data = {
    "women": women_all,
    "households": households_all,
    "children": children_all,
}


# =============================================================================
# 6. KPI CARDS
# =============================================================================

kpis = compute_all_kpis(women, children)
render_kpi_cards(kpis)


# =============================================================================
# 7. CHOROPLETH MAP
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">🗺️ Geographic Intelligence</div>'
    '<div class="dhs-section-sub">Interactive province-level map of Rwanda\'s core health and demographic indicators.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
render_map(national_data)


# =============================================================================
# 8. DEMOGRAPHIC OVERVIEW
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">👥 Demographic Overview</div>'
    f'<div class="dhs-section-sub">Age structure and demographic composition — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
demo_col1, demo_col2 = st.columns(2)
with demo_col1:
    charts.population_pyramid(women)
with demo_col2:
    charts.age_histogram(women)


# =============================================================================
# 9. FERTILITY & FAMILY PLANNING
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">👶 Fertility & Family Planning</div>'
    f'<div class="dhs-section-sub">Reproductive behaviour and family planning uptake — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
fp_col1, fp_col2 = st.columns(2)
with fp_col1:
    charts.fertility_trend(women)
with fp_col2:
    charts.family_planning_funnel(women)


# =============================================================================
# 10. MATERNAL & CHILD HEALTH
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">🏥 Maternal & Child Health</div>'
    f'<div class="dhs-section-sub">Antenatal care, delivery care, and child nutrition outcomes — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
mch_col1, mch_col2 = st.columns(2)
with mch_col1:
    charts.maternal_care_funnel(women, children)
with mch_col2:
    charts.child_nutrition_chart(children)


# =============================================================================
# 11. WEALTH, EDUCATION & EQUITY
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">🎓 Wealth, Education & Equity</div>'
    f'<div class="dhs-section-sub">Socioeconomic composition and its relationship with health outcomes — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
we_col1, we_col2, we_col3 = st.columns(3)
with we_col1:
    charts.wealth_donut(women)
with we_col2:
    charts.education_donut(women)
with we_col3:
    charts.wealth_residence_treemap(women)

st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
charts.education_wealth_heatmap(women)


# =============================================================================
# 12. HOUSEHOLD INFRASTRUCTURE
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">🏠 Household Infrastructure</div>'
    f'<div class="dhs-section-sub">Access to assets, utilities and services at the household level — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
charts.household_infrastructure_chart(households)


# =============================================================================
# 13. PROVINCIAL COMPARISON & RANKINGS
# (always uses the national dataset — comparing provinces requires all of them)
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">📊 Provincial Comparison & Rankings</div>'
    '<div class="dhs-section-sub">How Rwanda\'s five provinces compare on core health indicators.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)
pc_col1, pc_col2 = st.columns(2)
with pc_col1:
    charts.lollipop_chart(national_data)
with pc_col2:
    charts.radar_chart(national_data, selected_province)

charts.province_comparison_chart(national_data)

rank_col1, rank_col2 = st.columns(2)
with rank_col1:
    charts.ranked_bar_chart(national_data, "Child Stunting")
with rank_col2:
    charts.slope_chart(national_data, "Skilled Antenatal Care")


# =============================================================================
# 14. EXPLORE THE DATA (searchable / sortable / paginated tables)
# =============================================================================

st.markdown(
    '<div class="dhs-section-title">📋 Explore the Data</div>'
    f'<div class="dhs-section-sub">Browse, search, sort, and export the underlying microdata — {selected_province}.</div>'
    '<div class="dhs-divider"></div>',
    unsafe_allow_html=True,
)

table_tab1, table_tab2, table_tab3 = st.tabs(["👩 Women", "🏠 Households", "👶 Children"])
with table_tab1:
    render_data_table(women, "women_table", "Women (Individual Recode)", "rwanda_dhs_women.csv")
with table_tab2:
    render_data_table(households, "hh_table", "Households (Household Recode)", "rwanda_dhs_households.csv")
with table_tab3:
    render_data_table(children, "children_table", "Children (Children Recode)", "rwanda_dhs_children.csv")


# =============================================================================
# 15. FOOTER
# =============================================================================

render_footer(sample_sizes(national_data))
