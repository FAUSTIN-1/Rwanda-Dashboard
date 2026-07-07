"""
header.py
---------
Renders the premium landing header for the Rwanda DHS 2019-20 Dashboard.

Author: Faustin NIZEYIMANA
"""

import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <div class="dhs-header">
            <div class="dhs-header-eyebrow">Republic of Rwanda &nbsp;·&nbsp; NISR &nbsp;·&nbsp; DHS Program</div>
            <div class="dhs-header-title">Rwanda DHS 2019–20 Dashboard</div>
            <div class="dhs-header-subtitle">National Health and Demographic Intelligence</div>
            <div class="dhs-header-author">
                <div class="dhs-author-avatar">FN</div>
                <div>
                    <div class="dhs-author-name">Faustin NIZEYIMANA</div>
                    <div class="dhs-author-role">Statistician and Data Analyst</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
