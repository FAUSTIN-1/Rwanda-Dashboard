"""
footer.py
---------
Renders the dashboard footer: sample sizes, methodological note, source
citation and author credit.

Author: Faustin NIZEYIMANA
"""

import streamlit as st

from modules.helpers import fmt_number


def render_footer(sample_sizes: dict) -> None:
    women_n = fmt_number(sample_sizes.get("women", 0))
    hh_n = fmt_number(sample_sizes.get("households", 0))
    children_n = fmt_number(sample_sizes.get("children", 0))

    st.markdown(
        f"""
        <div class="dhs-footer">
            <div class="dhs-footer-stats">
                <div>
                    <div class="dhs-footer-stat-value">{women_n}</div>
                    <div class="dhs-footer-stat-label">Women (15–49) surveyed</div>
                </div>
                <div>
                    <div class="dhs-footer-stat-value">{hh_n}</div>
                    <div class="dhs-footer-stat-label">Households surveyed</div>
                </div>
                <div>
                    <div class="dhs-footer-stat-value">{children_n}</div>
                    <div class="dhs-footer-stat-label">Children under 5</div>
                </div>
            </div>
            <div class="dhs-footer-desc">
                Interactive dashboard built from Rwanda DHS 2019–20 survey microdata.
                Results are intended for exploratory analysis and visualization.
                Official published estimates are available from NISR and the DHS Program.
            </div>
            <div class="dhs-footer-source">
                Source: National Institute of Statistics of Rwanda (NISR), Rwanda DHS 2019–20 &nbsp;·&nbsp;
                Dashboard by Faustin NIZEYIMANA, Statistician &amp; Data Analyst &nbsp;·&nbsp;
                © 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
