"""
tables.py
---------
Searchable, sortable, paginated data tables with CSV export, used in the
'Explore the Data' section of the dashboard.

Author: Faustin NIZEYIMANA
"""

import math

import pandas as pd
import streamlit as st

from modules.helpers import df_to_csv_download

PAGE_SIZE_OPTIONS = [10, 25, 50, 100]


def render_data_table(df: pd.DataFrame, key_prefix: str, title: str, filename: str) -> None:
    st.markdown('<div class="dhs-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="dhs-panel-title">📋 {title}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="dhs-panel-caption">{len(df):,} records &nbsp;·&nbsp; searchable, sortable, and exportable.</div>',
        unsafe_allow_html=True,
    )

    top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
    with top_col1:
        search = st.text_input("Search", placeholder="Search across all columns…", key=f"{key_prefix}_search", label_visibility="collapsed")
    with top_col2:
        sort_col = st.selectbox("Sort by", options=["(none)"] + list(df.columns), key=f"{key_prefix}_sort", label_visibility="collapsed")
    with top_col3:
        page_size = st.selectbox("Rows", options=PAGE_SIZE_OPTIONS, index=1, key=f"{key_prefix}_pagesize", label_visibility="collapsed")

    filtered = df
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
        filtered = df[mask]

    if sort_col != "(none)":
        filtered = filtered.sort_values(sort_col)

    total_rows = len(filtered)
    total_pages = max(1, math.ceil(total_rows / page_size))
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1, step=1,
        key=f"{key_prefix}_page", label_visibility="collapsed",
    )

    start = (page - 1) * page_size
    end = start + page_size
    st.dataframe(filtered.iloc[start:end], use_container_width=True, hide_index=True)

    footer_col1, footer_col2 = st.columns([3, 1])
    with footer_col1:
        st.caption(f"Showing rows {start + 1:,}–{min(end, total_rows):,} of {total_rows:,} (page {page} of {total_pages})")
    with footer_col2:
        df_to_csv_download(filtered, filename, label="Export filtered CSV")

    st.markdown('</div>', unsafe_allow_html=True)
