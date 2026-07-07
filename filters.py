"""
filters.py
----------
Province filter system that replaces default Streamlit tab navigation.
A single source of truth for the selected province is kept in
st.session_state so every component of the dashboard stays in sync.

Author: Faustin NIZEYIMANA
"""

import streamlit as st

from modules.helpers import PROVINCES


def render_province_filter() -> str:
    """Render the province filter bar and return the selected province."""
    st.markdown('<div class="dhs-filter-bar">', unsafe_allow_html=True)
    col_label, col_select, col_note = st.columns([1, 2, 3])

    with col_label:
        st.markdown('<div class="dhs-filter-label">🗺️ Province</div>', unsafe_allow_html=True)

    with col_select:
        province = st.selectbox(
            "Select province",
            PROVINCES,
            index=0,
            label_visibility="collapsed",
            key="selected_province",
        )

    with col_note:
        if province == "National":
            note = "Showing indicators aggregated across all five provinces of Rwanda."
        else:
            note = f"Showing indicators for **{province}** Province only. All charts, maps and tables update dynamically."
        st.markdown(f"<div style='padding-top:6px; color:#6B7280; font-size:0.85rem;'>{note}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return province
