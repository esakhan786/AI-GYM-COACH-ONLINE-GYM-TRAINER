import base64
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


def find_landing_dir() -> Path:
    current_dir = Path(__file__).resolve().parent
    # Check directly inside app/LandingPage
    app_landing = current_dir.parent.parent / "LandingPage"
    if (app_landing / "index.html").exists():
        return app_landing

    # Search upwards for LandingPage or docs
    check_dir = current_dir
    for _ in range(5):
        for candidate in ["LandingPage", "docs"]:
            p = check_dir / candidate
            if (p / "index.html").exists():
                return p
        check_dir = check_dir.parent

    # Check cwd
    cwd = Path.cwd()
    for candidate in ["LandingPage", "app/LandingPage", "docs", "."]:
        p = cwd / candidate
        if (p / "index.html").exists():
            return p

    return Path("LandingPage").resolve()


def get_compiled_landing_page() -> str:
    landing_dir = find_landing_dir()
    html_file = landing_dir / "index.html"
    css_file = landing_dir / "style.css"

    if not html_file.exists():
        return "<h2 style='color:white;text-align:center;'>Landing page not found</h2>"

    html = html_file.read_text(encoding="utf-8")
    css = css_file.read_text(encoding="utf-8") if css_file.exists() else ""

    # Inline style.css
    if css:
        html = re.sub(
            r'<link\s+rel=["\']stylesheet["\']\s+href=["\']style\.css["\']\s*/?>',
            f"<style>\n{css}\n</style>",
            html,
        )

    # Inline Averta font as base64 data URI
    font_file = landing_dir / "fonts" / "Averta.woff2"
    if not font_file.exists():
        font_file = landing_dir.parent / "LandingPage" / "fonts" / "Averta.woff2"

    if font_file.exists():
        try:
            with open(font_file, "rb") as ff:
                font_b64 = base64.b64encode(ff.read()).decode("utf-8")
            font_uri = f"data:font/woff2;charset=utf-8;base64,{font_b64}"
            html = re.sub(
                r'url\(["\']fonts/Averta\.woff2["\']\)',
                f'url("{font_uri}")',
                html,
            )
        except Exception:
            pass

    # Inline all 5 preview images and any other PNG/JPG images as base64 data URIs
    def replace_image_source(match):
        raw_src = match.group(1)
        clean_name = raw_src.replace("./", "").replace("../", "").replace("images/", "").replace("LandingPage/", "")
        
        candidates = [
            landing_dir / "images" / clean_name,
            landing_dir / clean_name,
            landing_dir.parent / "LandingPage" / "images" / clean_name,
            landing_dir.parent / "docs" / "images" / clean_name,
        ]

        for cand in candidates:
            if cand.exists():
                ext = cand.suffix.lower()
                mime = "image/png" if ext == ".png" else "image/jpeg" if ext in (".jpg", ".jpeg") else "image/svg+xml"
                try:
                    with open(cand, "rb") as im:
                        b64_str = base64.b64encode(im.read()).decode("utf-8")
                    return f'src="data:{mime};base64,{b64_str}"'
                except Exception:
                    pass
        return match.group(0)

    html = re.sub(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|svg))["\']', replace_image_source, html)

    # Preserve working openDemoModal modal popup
    custom_script = """
    <script>

      function notifyParentHeight() {
        try {
          var body = document.body;
          var html = document.documentElement;
          var height = Math.max(
            body.scrollHeight, body.offsetHeight,
            html.clientHeight, html.scrollHeight, html.offsetHeight
          );
          window.parent.postMessage({
            type: 'streamlit:setFrameHeight',
            height: height
          }, '*');
        } catch (e) {}
      }

      window.addEventListener('load', notifyParentHeight);
      window.addEventListener('resize', notifyParentHeight);
      setTimeout(notifyParentHeight, 400);
      setTimeout(notifyParentHeight, 1200);
      setTimeout(notifyParentHeight, 2500);
    </script>
    """

    # Inject script right before closing </body>
    if "</body>" in html:
        html = html.replace("</body>", f"{custom_script}\n</body>")
    else:
        html += custom_script

    return html


def render_landing_page():
    # Style to make the landing page 100% full-screen fixed viewport, exactly like localhost:8080
    st.markdown(
        """
        <style>
        /* Hide all Streamlit UI elements */
        #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stBottom"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        html, body, [data-testid="stApp"], .main, .block-container, [data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"] {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
            width: 100vw !important;
            height: 100vh !important;
            max-height: 100vh !important;
            overflow: hidden !important;
            background: #0a0a0a !important;
        }
        div[data-testid="stCustomComponentV1"], div[data-testid="stCustomComponentV1"] > iframe, iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 999999 !important;
            display: block !important;
            background: #0a0a0a !important;
        }
        /* Floating native Streamlit TRY IT LIVE button with top z-index */
        div.st-key-st_native_try_live_btn, div:has(> button[data-testid*="st_native_try_live_btn"]) {
            position: fixed !important;
            top: 16px !important;
            right: 32px !important;
            z-index: 10000000 !important;
            display: block !important;
        }
        div.st-key-st_native_try_live_btn button {
            background: #f5a623 !important;
            color: #000000 !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            border: none !important;
            padding: 10px 24px !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 25px rgba(245, 166, 35, 0.6) !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }
        div.st-key-st_native_try_live_btn button:hover {
            background: #ffb84d !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 35px rgba(245, 166, 35, 0.9) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("⚡ TRY IT LIVE (LOGIN)", key="st_native_try_live_btn", type="primary"):
        st.session_state["entered_app"] = True
        st.query_params["start"] = "true"
        st.rerun()

    compiled_html = get_compiled_landing_page()
    components.html(compiled_html, height=1200, scrolling=True)

