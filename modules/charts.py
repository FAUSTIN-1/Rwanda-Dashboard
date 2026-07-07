"""
charts.py
---------
Full suite of publication-quality statistical visualizations for the
analytics section of the Rwanda DHS 2019-20 Dashboard: population pyramid,
age histogram, fertility trend, maternal care cascade, child nutrition,
wealth distribution, education x wealth heatmap, household infrastructure,
province comparison, lollipop, radar, donut, treemap, funnel, slope, and
ranked horizontal bar charts.

Every chart function renders itself directly into the Streamlit app inside
a styled panel, following one consistent visual language (font, palette,
hover behaviour) so the dashboard feels cohesive.

Author: Faustin NIZEYIMANA
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from modules.helpers import COLORS, CATEGORICAL_SCALE
from modules import calculations as calc

PLOTLY_FONT = dict(family="Inter, sans-serif", size=12, color=COLORS["text"])
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=PLOTLY_FONT,
    margin=dict(l=10, r=10, t=30, b=10),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
)


def _panel_start(title: str, caption: str = "") -> None:
    st.markdown('<div class="dhs-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="dhs-panel-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="dhs-panel-caption">{caption}</div>', unsafe_allow_html=True)


def _panel_end() -> None:
    st.markdown('</div>', unsafe_allow_html=True)


def _render(fig, height=340):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# --------------------------------------------------------------------------
# 1. Population pyramid (women age-group structure)
# --------------------------------------------------------------------------

def population_pyramid(women: pd.DataFrame) -> None:
    _panel_start("👥 Women's Age Structure (Population Pyramid)",
                  "Distribution of surveyed women aged 15–49 across five-year age groups.")
    df = calc.population_pyramid_data(women, None)
    fig = go.Figure(go.Bar(
        y=df["Age Group"], x=-df["Women"], orientation="h",
        marker_color=COLORS["primary"], name="Women",
        hovertemplate="%{y}: %{customdata:,} women<extra></extra>",
        customdata=df["Women"],
    ))
    fig.update_layout(
        xaxis=dict(title="Number of women", tickvals=None, showgrid=True, gridcolor=COLORS["bg"]),
        yaxis=dict(title=""),
        showlegend=False,
    )
    fig.update_xaxes(tickformat=",")
    _render(fig)
    _panel_end()


# --------------------------------------------------------------------------
# 2. Age distribution histogram
# --------------------------------------------------------------------------

def age_histogram(women: pd.DataFrame) -> None:
    _panel_start("📊 Age Distribution", "Histogram of individual ages among surveyed women.")
    ages = calc.age_distribution(women)
    fig = px.histogram(ages, nbins=25, color_discrete_sequence=[COLORS["info"]])
    fig.update_layout(xaxis_title="Age (years)", yaxis_title="Count", showlegend=False, bargap=0.05)
    _render(fig)
    _panel_end()


# --------------------------------------------------------------------------
# 3. Fertility trend by age group
# --------------------------------------------------------------------------

def fertility_trend(women: pd.DataFrame) -> None:
    _panel_start("📈 Fertility Trend by Age Group", "Mean number of children ever born, by five-year age group.")
    df = calc.fertility_by_age_group(women)
    fig = px.line(df, x="Age Group", y="Mean Children Born", markers=True,
                  color_discrete_sequence=[COLORS["secondary"]])
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_layout(xaxis_title="", yaxis_title="Mean children ever born")
    _render(fig)
    _panel_end()


# --------------------------------------------------------------------------
# 4. Maternal care cascade (funnel)
# --------------------------------------------------------------------------

def maternal_care_funnel(women: pd.DataFrame, children: pd.DataFrame) -> None:
    _panel_start("🏥 Maternal Care Cascade", "Share of women/births reaching each stage of maternal care.")
    df = calc.maternal_care_cascade(women, children)
    fig = go.Figure(go.Funnel(
        y=df["Stage"], x=df["Percent"],
        marker=dict(color=CATEGORICAL_SCALE[:len(df)]),
        textinfo="value+percent initial",
        texttemplate="%{value:.1f}%",
    ))
    _render(fig)
    _panel_end()


# --------------------------------------------------------------------------
# 5. Child nutrition analysis
# --------------------------------------------------------------------------

def child_nutrition_chart(children: pd.DataFrame) -> None:
    _panel_start("🍼 Child Nutrition Indicators", "Share of children under 5 classified as stunted, underweight, or wasted.")
    df = calc.child_nutrition_breakdown(children)
    fig = px.bar(df, x="Indicator", y="Percent", color="Indicator",
                 color_discrete_sequence=CATEGORICAL_SCALE, text="Percent")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Percent of children (%)")
    _render(fig)
    _panel_end()


# --------------------------------------------------------------------------
# 6. Wealth distribution (donut)
# --------------------------------------------------------------------------

def wealth_donut(df: pd.DataFrame, title_scope: str = "Women") -> None:
    _panel_start("💰 Wealth Quintile Distribution", f"Distribution of {title_scope.lower()} across household wealth quintiles.")
    data = calc.wealth_distribution(df)
    fig = px.pie(data, names="Wealth Quintile", values="Count", hole=0.55,
                 color_discrete_sequence=CATEGORICAL_SCALE)
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    _render(fig, height=360)
    _panel_end()


# --------------------------------------------------------------------------
# 7. Education x Wealth heatmap
# --------------------------------------------------------------------------

def education_wealth_heatmap(women: pd.DataFrame) -> None:
    _panel_start("🎓 Education × Wealth: Modern Contraceptive Use",
                  "Cross-tabulation of modern contraceptive prevalence (%) by education level and wealth quintile.")
    pivot = calc.education_wealth_heatmap(women)
    fig = px.imshow(
        pivot, text_auto=".1f", aspect="auto",
        color_continuous_scale=["#EAF4FF", "#9CC7E8", "#4E92C9", "#1D5B9E", "#00205B"],
        labels=dict(color="% Modern FP"),
    )
    fig.update_layout(xaxis_title="Wealth Quintile", yaxis_title="Education Level")
    _render(fig, height=360)
    _panel_end()


# --------------------------------------------------------------------------
# 8. Household infrastructure (ranked horizontal bar)
# --------------------------------------------------------------------------

def household_infrastructure_chart(households: pd.DataFrame) -> None:
    _panel_start("🏠 Household Infrastructure & Assets", "Share of households with access to key assets and services, ranked.")
    df = calc.household_infrastructure(households)
    fig = px.bar(df, x="Percent", y="Indicator", orientation="h",
                 color="Percent", color_continuous_scale=["#EAF4FF", "#00205B"],
                 text="Percent")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), xaxis_title="Percent of households (%)",
                       yaxis_title="", coloraxis_showscale=False)
    _render(fig, height=380)
    _panel_end()


# --------------------------------------------------------------------------
# 9. Province comparison (grouped bar)
# --------------------------------------------------------------------------

def province_comparison_chart(data: dict) -> None:
    _panel_start("📊 Province Comparison: Key Health Indicators",
                  "Comparing modern contraceptive use, HIV testing, and health insurance coverage across provinces.")
    indicators = ["Modern Contraceptive Prevalence", "HIV Testing", "Health Insurance Coverage"]
    df = calc.province_comparison_table(data, indicators)
    df_melt = df.melt(id_vars="Province", var_name="Indicator", value_name="Percent")
    fig = px.bar(df_melt, x="Province", y="Percent", color="Indicator", barmode="group",
                 color_discrete_sequence=CATEGORICAL_SCALE)
    fig.update_layout(xaxis_title="", yaxis_title="Percent (%)", legend_title="")
    _render(fig, height=380)
    _panel_end()


# --------------------------------------------------------------------------
# 10. Lollipop chart — province ranking on one indicator
# --------------------------------------------------------------------------

def lollipop_chart(data: dict, indicator: str = "Modern Contraceptive Prevalence") -> None:
    _panel_start("🍭 Province Ranking — Modern Contraceptive Prevalence", "Provinces ranked from lowest to highest.")
    df = calc.province_indicator_table(data, indicator).sort_values("Value")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Value"], y=df["Province"], mode="markers",
        marker=dict(size=14, color=COLORS["primary"]),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    for _, row in df.iterrows():
        fig.add_shape(type="line", x0=0, x1=row["Value"], y0=row["Province"], y1=row["Province"],
                      line=dict(color=COLORS["muted"], width=2))
    fig.update_layout(xaxis_title="Modern contraceptive use (%)", yaxis_title="")
    _render(fig, height=340)
    _panel_end()


# --------------------------------------------------------------------------
# 11. Radar chart — multi-indicator province profile
# --------------------------------------------------------------------------

def radar_chart(data: dict, province: str) -> None:
    _panel_start("🕸️ Health Indicator Profile", f"Multi-indicator radar profile for {province}.")
    indicators = list(calc.MAP_INDICATORS.keys())
    indicators = [i for i in indicators if i != "Fertility Rate"]  # keep percentages on one scale
    values = []
    for ind in indicators:
        t = calc.province_indicator_table(data, ind)
        if province == "National":
            values.append(t["Value"].mean())
        else:
            row = t[t["Province"] == province]
            values.append(row["Value"].values[0] if len(row) else 0)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], theta=indicators + [indicators[0]],
        fill="toself", line_color=COLORS["primary"], fillcolor="rgba(0,32,91,0.18)",
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    _render(fig, height=400)
    _panel_end()


# --------------------------------------------------------------------------
# 12. Donut — education distribution
# --------------------------------------------------------------------------

def education_donut(women: pd.DataFrame) -> None:
    _panel_start("🎓 Education Level Distribution", "Share of women by highest education level attained.")
    df = calc.education_distribution(women)
    fig = px.pie(df, names="Education Level", values="Count", hole=0.55,
                 color_discrete_sequence=CATEGORICAL_SCALE)
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    _render(fig, height=360)
    _panel_end()


# --------------------------------------------------------------------------
# 13. Treemap — wealth x residence composition
# --------------------------------------------------------------------------

def wealth_residence_treemap(women: pd.DataFrame) -> None:
    _panel_start("🌳 Sample Composition: Residence × Wealth Quintile", "Hierarchical view of the surveyed sample.")
    df = women.dropna(subset=["Residence", "Wealth Index"])
    grouped = df.groupby(["Residence", "Wealth Index"], observed=True).size().reset_index(name="Count")
    fig = px.treemap(grouped, path=["Residence", "Wealth Index"], values="Count",
                      color="Count", color_continuous_scale=["#EAF4FF", "#00205B"])
    fig.update_layout(coloraxis_showscale=False)
    _render(fig, height=380)
    _panel_end()


# --------------------------------------------------------------------------
# 14. Funnel — already covered by maternal_care_funnel (reused pattern);
#     additional funnel: family planning awareness cascade
# --------------------------------------------------------------------------

def family_planning_funnel(women: pd.DataFrame) -> None:
    _panel_start("🔻 Family Planning Awareness Cascade", "From radio/TV exposure to awareness and use of family planning.")
    heard_radio = women["Heard Family Planning Radio"].dropna()
    heard_tv = women["Heard Family Planning Tv"].dropna()
    uses_modern = women["Contraceptive Use"].dropna()

    from modules.helpers import share_of
    stages = [
        ("Heard FP on radio", share_of(heard_radio, "Yes") if len(heard_radio) else 0),
        ("Heard FP on TV", share_of(heard_tv, "Yes") if len(heard_tv) else 0),
        ("Currently using modern method", share_of(uses_modern, "Modern")),
    ]
    df = pd.DataFrame(stages, columns=["Stage", "Percent"])
    fig = go.Figure(go.Funnel(
        y=df["Stage"], x=df["Percent"],
        marker=dict(color=[COLORS["accent"], COLORS["info"], COLORS["primary"]]),
        texttemplate="%{value:.1f}%",
    ))
    _render(fig, height=320)
    _panel_end()


# --------------------------------------------------------------------------
# 15. Slope chart — urban vs rural comparison
# --------------------------------------------------------------------------

def slope_chart(data: dict, indicator: str = "Skilled Antenatal Care") -> None:
    _panel_start("📐 Urban vs Rural Gap", f"{indicator}: comparing urban and rural residence.")
    df = calc.slope_chart_data(data, indicator)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=["Rural", "Urban"],
        y=[df[df["Residence"] == "Rural"]["Value"].values[0], df[df["Residence"] == "Urban"]["Value"].values[0]],
        mode="lines+markers+text",
        line=dict(color=COLORS["secondary"], width=4),
        marker=dict(size=14, color=[COLORS["muted"], COLORS["primary"]]),
        text=[f"{v:.1f}%" for v in [df[df['Residence']=='Rural']['Value'].values[0], df[df['Residence']=='Urban']['Value'].values[0]]],
        textposition="top center",
    ))
    fig.update_layout(xaxis_title="", yaxis_title="Percent (%)", showlegend=False)
    _render(fig, height=320)
    _panel_end()


# --------------------------------------------------------------------------
# 16. Ranked horizontal bar — provinces on stunting
# --------------------------------------------------------------------------

def ranked_bar_chart(data: dict, indicator: str = "Child Stunting") -> None:
    _panel_start(f"📶 Ranked Provinces — {indicator}", "Provinces ranked from highest to lowest.")
    df = calc.province_indicator_table(data, indicator).sort_values("Value", ascending=True)
    fig = px.bar(df, x="Value", y="Province", orientation="h", text="Value",
                 color="Value", color_continuous_scale=["#EAF4FF", "#C0392B"])
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(xaxis_title="Percent (%)", yaxis_title="", coloraxis_showscale=False)
    _render(fig, height=340)
    _panel_end()
