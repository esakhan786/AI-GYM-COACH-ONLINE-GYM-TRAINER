import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown(
        """
        <style>
        .login-hero-card {
            background: linear-gradient(145deg, #121622 0%, #181e2e 100%);
            border: 1px solid rgba(245, 166, 35, 0.28);
            border-radius: 12px;
            padding: 38px 32px 28px;
            margin: 10px auto 28px auto;
            text-align: center;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65), 0 0 40px rgba(245, 166, 35, 0.1);
            position: relative;
            overflow: hidden;
        }
        .login-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 10px;
            letter-spacing: 0.18em;
            color: #f5a623;
            background: rgba(245, 166, 35, 0.12);
            border: 1px solid rgba(245, 166, 35, 0.35);
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .login-hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
            line-height: 1.15;
        }
        .login-hero-title span {
            background: linear-gradient(135deg, #f5a623 30%, #00d4ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-hero-sub {
            font-size: 0.98rem;
            color: #9ab0cb;
            line-height: 1.6;
            max-width: 540px;
            margin: 0 auto 24px;
        }
        .login-feature-strip {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }
        .login-pill {
            font-size: 11px;
            color: #d0e0f5;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.09);
            padding: 6px 14px;
            border-radius: 6px;
            letter-spacing: 0.03em;
        }
        div[data-testid="stForm"] {
            background: #111522 !important;
            border: 1px solid rgba(245, 166, 35, 0.25) !important;
            border-radius: 10px !important;
            padding: 24px 28px !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.4) !important;
        }
        div[data-testid="stForm"] button {
            background: #f5a623 !important;
            color: #000000 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            border: none !important;
            padding: 12px 24px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 20px rgba(245, 166, 35, 0.3) !important;
        }
        div[data-testid="stForm"] button:hover {
            background: #ffb84d !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(245, 166, 35, 0.5) !important;
        }
        </style>

        <div class="login-hero-card">
            <div class="login-badge">⚡ ATHLETE PORTAL · REAL-TIME AI</div>
            <div class="login-hero-title">Apna <span>AI Gym Coach</span></div>
            <div class="login-hero-sub">
                Computer vision posture tracking & proactive voice coaching.<br>
                Enter your unique athlete handle to start your session.
            </div>
            <div class="login-feature-strip">
                <span class="login-pill">🎯 33 3D Pose Landmarks</span>
                <span class="login-pill">🎙️ Instant Voice Cues</span>
                <span class="login-pill">📈 Session History</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        st.markdown("<p style='font-size:13px; color:#f5a623; letter-spacing:0.1em; font-weight:600; text-transform:uppercase; margin-bottom:4px;'>👤 Athlete Handle</p>", unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            label_visibility="collapsed",
            placeholder="Enter unique athlete name (e.g. esakhan)",
        )
        submit_button = st.form_submit_button("🚀 Start Workout Session", width="stretch")

    if submit_button:
        cleaned_username = username.strip() if username else ""
        if not cleaned_username:
            st.error("⚠️ Please enter a username to begin.")
            return False

        user = get_or_create_user(cleaned_username)

        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("← Back to Landing Page", key="back_to_landing_login", use_container_width=True):
            st.session_state["entered_app"] = False
            if "start" in st.query_params:
                del st.query_params["start"]
            st.rerun()

    return False