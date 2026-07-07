"""
header.py
---------
Renders the premium landing header for the Rwanda DHS 2019-20 Dashboard.
Author: Faustin NIZEYIMANA
"""
import os
import streamlit as st
from modules.helpers import image_to_base64

AUTHOR_PHOTO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "faustin.jpg")


def render_header() -> None:
    photo_b64 = image_to_base64(AUTHOR_PHOTO_PATH)

    if photo_b64:
        avatar_html = f'<img src="data:image/jpeg;base64,{photo_b64}" class="dhs-author-avatar-img" />'
    else:
        # Falls back to initials if the photo file isn't found, so the app never breaks
        avatar_html = '<div class="dhs-author-avatar">FN</div>'

    st.markdown(
        f"""
        <div class="dhs-header">
            <div class="dhs-header-eyebrow">Republic of Rwanda &nbsp;·&nbsp; NISR &nbsp;·&nbsp; DHS Program</div>
            <div class="dhs-header-title">Rwanda DHS 2019–20 Dashboard</div>
            <div class="dhs-header-subtitle">National Health and Demographic Intelligence</div>
            <div class="dhs-header-author">
                {avatar_html}
                <div>
                    <div class="dhs-author-name">Faustin NIZEYIMANA</div>
                    <div class="dhs-author-role">Statistician and Data Analyst</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
