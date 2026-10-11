import base64
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
LANDING_DIR = ROOT_DIR / "LandingPage"


@st.cache_data(show_spinner=False)
def get_compiled_landing_page() -> str:
    html_path = LANDING_DIR / "index.html"
    css_path = LANDING_DIR / "style.css"

    if not html_path.exists():
        # Fallback if LandingPage is in app/ or docs/
        if (ROOT_DIR / "docs" / "index.html").exists():
            html_path = ROOT_DIR / "docs" / "index.html"
            css_path = ROOT_DIR / "docs" / "style.css"

    if not html_path.exists():
        return "<h2 style='color:white;text-align:center;'>Landing page not found</h2>"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    css_content = ""
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # Inline style.css
    if css_content:
        html = re.sub(
            r'<link\s+rel=["\']stylesheet["\']\s+href=["\']style\.css["\']\s*/?>',
            f"<style>\n{css_content}\n</style>",
            html,
        )

    # Helper to encode local images to base64 data URIs
    def encode_image(match):
        raw_src = match.group(1)
        clean = raw_src.lstrip("./").replace("LandingPage/", "")
        img_file = LANDING_DIR / clean
        if not img_file.exists():
            img_file = ROOT_DIR / clean

        if img_file.exists():
            ext = img_file.suffix.lower()
            mime = "image/svg+xml" if ext == ".svg" else "image/png" if ext == ".png" else "image/jpeg"
            try:
                with open(img_file, "rb") as im:
                    b64 = base64.b64encode(im.read()).decode("utf-8")
                return f'src="data:{mime};base64,{b64}"'
            except Exception:
                return match.group(0)
        return match.group(0)

    # Replace relative image sources with data URIs
    html = re.sub(r'src=["\'](\.?/?images/[^"\']+)["\']', encode_image, html)
    html = re.sub(r'src=["\'](\.?/?IMGs/[^"\']+)["\']', encode_image, html)

    # Replace CTA button link with ?start=true target=_top so clicking it inside iframe navigates Streamlit
    html = re.sub(
        r'<a\s+[^>]*id=["\']cta-button["\'][^>]*>',
        '<a href="?start=true" target="_top" class="btn-primary" id="cta-button">',
        html,
        flags=re.DOTALL,
    )
    # Also handle if id is after
    html = re.sub(
        r'<a\s+href=["\'][^"\']*streamlit\.app[^"\']*["\'][^>]*>',
        '<a href="?start=true" target="_top" class="btn-primary" id="cta-button">',
        html,
        flags=re.DOTALL,
    )
    # Also handle generic #cta-button
    html = re.sub(
        r'<a\s+href=["\']#visuals["\']\s+class=["\']btn-ghost["\']',
        '<a href="#visuals" target="_self" class="btn-ghost"',
        html,
    )

    return html


def render_landing_page():
    # Sticky Action Bar at the top of Streamlit
    st.markdown(
        """
        <style>
        .stApp [data-testid="stHeader"] {
            display: none !important;
        }
        .live-top-banner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(90deg, #0e111a 0%, #151a26 100%);
            border: 1px solid rgba(245, 166, 35, 0.35);
            border-radius: 10px;
            padding: 12px 20px;
            margin-bottom: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }
        .banner-text {
            color: #ffffff;
            font-size: 15px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .banner-tag {
            color: #f5a623;
            background: rgba(245, 166, 35, 0.15);
            border: 1px solid rgba(245, 166, 35, 0.4);
            border-radius: 4px;
            font-size: 11px;
            padding: 2px 8px;
            font-weight: 800;
            letter-spacing: 0.1em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            """
            <div class="live-top-banner">
                <div class="banner-text">
                    <span class="banner-tag">LIVE DEMO READY</span>
                    <span>🏋️ Apna AI Real-Time Gym Coach</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("🚀 TRY IT LIVE", type="primary", use_container_width=True, key="top_try_it_live"):
            st.session_state["entered_app"] = True
            st.query_params["start"] = "true"
            st.rerun()

    # Render the full HTML Landing Page in full fidelity
    compiled_html = get_compiled_landing_page()
    components.html(compiled_html, height=2700, scrolling=False)
