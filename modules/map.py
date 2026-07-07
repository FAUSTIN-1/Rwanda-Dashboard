"""
map.py
------
Interactive Rwanda choropleth map. Lets the user pick an indicator from a
dropdown and colors the five provinces accordingly, with rich hover
tooltips (province, value, unit, sample size).

Author: Faustin NIZEYIMANA
"""

import streamlit as st
import plotly.graph_objects as go

from modules.calculations import MAP_INDICATORS, province_indicator_table
from modules.helpers import load_geojson, COLORS


def render_map(data: dict) -> None:
    st.markdown('<div class="dhs-panel">', unsafe_allow_html=True)
    st.markdown('<div class="dhs-panel-title">🗺️ Provincial Indicator Map</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dhs-panel-caption">Select an indicator to explore its geographic distribution across Rwanda\'s five provinces.</div>',
        unsafe_allow_html=True,
    )

    indicator = st.selectbox(
        "Indicator",
        list(MAP_INDICATORS.keys()),
        label_visibility="collapsed",
        key="map_indicator",
    )

    table = province_indicator_table(data, indicator)
    geojson = load_geojson()
    unit = MAP_INDICATORS[indicator]["unit"]

    # Build a lookup so hover text and z-values align with geojson features
    values_by_province = table.set_index("Province")["Value"].to_dict()
    n_by_province = table.set_index("Province")["Sample Size"].to_dict()

    feature_provinces = [f["properties"]["province"] for f in geojson["features"]]
    z = [values_by_province.get(p, None) for p in feature_provinces]
    n = [n_by_province.get(p, 0) for p in feature_provinces]

    hover_text = [
        f"<b>{p}</b><br>{indicator}: {v:.1f}{' ' + unit if unit != '%' else '%'}<br>Sample size: n={int(nn):,}"
        if v is not None else f"<b>{p}</b><br>No data"
        for p, v, nn in zip(feature_provinces, z, n)
    ]

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            featureidkey="properties.province",
            locations=feature_provinces,
            z=z,
            text=hover_text,
            hoverinfo="text",
            colorscale=[
                [0.0, "#EAF4FF"],
                [0.25, "#9CC7E8"],
                [0.5, "#4E92C9"],
                [0.75, "#1D5B9E"],
                [1.0, "#00205B"],
            ],
            marker_line_color="white",
            marker_line_width=1.5,
            colorbar=dict(
                title=dict(text=unit if unit != "%" else "%", font=dict(size=11)),
                thickness=14,
                len=0.75,
                tickfont=dict(size=10),
            ),
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=460,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLORS["text"]),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with st.expander("View underlying province data"):
        st.dataframe(table.rename(columns={"Value": f"{indicator} ({unit})"}), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)
