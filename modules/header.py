"""
header.py
---------
Renders the premium landing header for the Rwanda DHS 2019-20 Dashboard.
Author: Faustin NIZEYIMANA
"""
import os
import streamlit as st
from modules.helpers import image_to_base64

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

# Looks for the logo under any of these common filenames/extensions,
# so it works whether the file is named faustin.jpg, faustin.png, logo.png, etc.
CANDIDATE_FILENAMES = ["faustin.jpg", "faustin.jpeg", "faustin.png", "logo.png", "logo.jpg"]


def _find_author_photo():
    for name in CANDIDATE_FILENAMES:
        path = os.path.join(ASSETS_DIR, name)
        if os.path.exists(path):
            ext = name.rsplit(".", 1)[-1].lower()
            mime = "png" if ext == "png" else "jpeg"
            return path, mime
    return None, None


def render_header() -> None:
    photo_path, mime = _find_author_photo()
    photo_b64 = image_to_base64(photo_path) if photo_path else ""

    if photo_b64:
        avatar_html = (
            f'<div class="dhs-author-avatar-frame">'
            f'<img src="data:image/{mime};base64,{photo_b64}" class="dhs-author-avatar-img" />'
            f'</div>'
        )
    else:
        # Falls back to initials if no photo/logo file is found, so the app never breaks
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
