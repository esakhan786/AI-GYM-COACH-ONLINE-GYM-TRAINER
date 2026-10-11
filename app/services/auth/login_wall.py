from pathlib import Path
import streamlit as st
from services.persistence.exercise_repository import get_or_create_user

STATIC_IMG = Path(__file__).resolve().parent.parent.parent / "static" / "images"


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

    st.markdown("<div style='margin-top: 38px;'></div>", unsafe_allow_html=True)

    tab_gallery, tab_arch, tab_exercises = st.tabs([
        "📸 Live App Showcase & Previews",
        "🏛️ How It Works & Architecture",
        "🏋️ 5 Target Exercises",
    ])

    with tab_gallery:
        st.markdown("<h4 style='color:#ffffff; margin-bottom:4px; font-weight:700;'>⚡ Real-Time Tracking & AI Coaching in Action</h4>", unsafe_allow_html=True)
        st.caption("Here is how Apna AI Gym Coach tracks your skeletal landmarks, monitors posture angles, and guides your workout in real-time.")

        c1, c2 = st.columns(2)
        with c1:
            st.image(str(STATIC_IMG / "preview-shoulder-press.png"), caption="🏋️ Shoulder Press: Overhead lockout & neutral spine monitoring", use_container_width=True)
            st.image(str(STATIC_IMG / "preview-biceps-curl.png"), caption="💪 Biceps Curl: Elbow hinge isolation & anti-swing detection", use_container_width=True)
        with c2:
            st.image(str(STATIC_IMG / "preview-dashboard.png"), caption="📋 Routine Planner: Custom sets, rep volume & camera device", use_container_width=True)
            st.image(str(STATIC_IMG / "preview-workout.png"), caption="🎙️ Voice Coaching & Workout Completion Summary", use_container_width=True)

        st.image(str(STATIC_IMG / "preview-login.png"), caption="👤 Athlete Portal & Profile Management", use_container_width=True)

    with tab_arch:
        st.markdown("<h4 style='color:#ffffff; margin-bottom:4px; font-weight:700;'>🏛️ Complete System Architecture</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-top: 14px;">
                <div style="background: rgba(18, 22, 34, 0.95); border: 1px solid rgba(245, 166, 35, 0.25); border-radius: 8px; padding: 16px;">
                    <div style="color: #f5a623; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px;">01 / COMPUTER VISION</div>
                    <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-bottom: 8px;">👁️ MediaPipe Vision Engine</div>
                    <p style="color: #9ab0cb; font-size: 12.5px; line-height: 1.5; margin: 0;">
                        Ingests real-time video frames via <strong>Streamlit WebRTC</strong> at 30+ FPS. 
                        Tracks 33 3D skeletal landmarks with zero wearable sensors.
                    </p>
                </div>
                <div style="background: rgba(18, 22, 34, 0.95); border: 1px solid rgba(245, 166, 35, 0.25); border-radius: 8px; padding: 16px;">
                    <div style="color: #f5a623; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px;">02 / BIOMECHANICS</div>
                    <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-bottom: 8px;">📐 Kinematic Form Detectors</div>
                    <p style="color: #9ab0cb; font-size: 12.5px; line-height: 1.5; margin: 0;">
                        Calculates joint angles in real time. Finite state machines count reps and detect form breakdowns (knee collapse, back arching, elbow drift).
                    </p>
                </div>
                <div style="background: rgba(18, 22, 34, 0.95); border: 1px solid rgba(245, 166, 35, 0.25); border-radius: 8px; padding: 16px;">
                    <div style="color: #f5a623; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px;">03 / REAL-TIME AI</div>
                    <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-bottom: 8px;">🎙️ Groq LLM Voice Coach</div>
                    <p style="color: #9ab0cb; font-size: 12.5px; line-height: 1.5; margin: 0;">
                        Ultra-fast sub-second LLM inference via <strong>Groq Cloud</strong>. 
                        Delivers spoken motivational cues and instant form corrections via <strong>Edge TTS</strong>.
                    </p>
                </div>
                <div style="background: rgba(18, 22, 34, 0.95); border: 1px solid rgba(245, 166, 35, 0.25); border-radius: 8px; padding: 16px;">
                    <div style="color: #f5a623; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px;">04 / PERSISTENCE</div>
                    <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-bottom: 8px;">📊 Session Analytics & SQLite</div>
                    <p style="color: #9ab0cb; font-size: 12.5px; line-height: 1.5; margin: 0;">
                        Stores athlete profiles, timestamped sets, completed reps, and duration for progressive overload tracking.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_exercises:
        st.markdown("<h4 style='color:#ffffff; margin-bottom:4px; font-weight:700;'>🏋️ 5 Target Biomechanical Exercises</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 14px;">
                <div style="background: rgba(18, 22, 34, 0.85); border-left: 3px solid #f5a623; padding: 12px 16px; border-radius: 4px;">
                    <strong style="color: #ffffff;">🦵 Squats:</strong> <span style="color: #9ab0cb;">Tracks hip-knee flexion depth, neutral spine angle, and full lockout extension.</span>
                </div>
                <div style="background: rgba(18, 22, 34, 0.85); border-left: 3px solid #00d4ff; padding: 12px 16px; border-radius: 4px;">
                    <strong style="color: #ffffff;">💪 Push-ups:</strong> <span style="color: #9ab0cb;">Checks straight-line torso rigid plank, 90° elbow flexion, and full lockout.</span>
                </div>
                <div style="background: rgba(18, 22, 34, 0.85); border-left: 3px solid #f5a623; padding: 12px 16px; border-radius: 4px;">
                    <strong style="color: #ffffff;">🏋️ Biceps Curls:</strong> <span style="color: #9ab0cb;">Measures elbow flexion/extension and detects torso swinging or momentum cheating.</span>
                </div>
                <div style="background: rgba(18, 22, 34, 0.85); border-left: 3px solid #00d4ff; padding: 12px 16px; border-radius: 4px;">
                    <strong style="color: #ffffff;">⚡ Shoulder Press:</strong> <span style="color: #9ab0cb;">Detects full vertical arm extension overhead while preventing lower-back hyperextension.</span>
                </div>
                <div style="background: rgba(18, 22, 34, 0.85); border-left: 3px solid #f5a623; padding: 12px 16px; border-radius: 4px;">
                    <strong style="color: #ffffff;">🏃 Lunges:</strong> <span style="color: #9ab0cb;">Evaluates 90° knee angle, rear knee drop, and upright balance posture.</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return False