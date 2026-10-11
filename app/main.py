import streamlit as st
import os
import time
import pandas as pd
from pathlib import Path
from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
from services.persistence.exercise_repository import init_db
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from services.persistence.exercise_repository import get_users_exercises
from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio
from services.ui.landing_page_renderer import render_landing_page

APP_DIR = Path(__file__).resolve().parent


def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="Real-time AI GYM Trainer",
        initial_sidebar_state="collapsed",
        layout="wide"
    )

    start_param = st.query_params.get("start")
    if start_param in ("true", "1", "yes"):
        st.session_state["entered_app"] = True

    entered_app = st.session_state.get("entered_app", False)

    if not entered_app:
        render_landing_page()
        return

    load_css(str(APP_DIR / "static" / "style.css"))
    inject_local_font(str(APP_DIR / "static" / "AdobeClean.otf"), "AdobeClean")

    init_db()

    with st.sidebar:
        if st.button("🏠 Landing Page / Overview", key="back_to_landing_nav"):
            st.session_state["entered_app"] = False
            if "start" in st.query_params:
                del st.query_params["start"]
            st.rerun()

    if not render_login_wall():
        return 

    initial_session_defaults()

    env_key = os.environ.get("GROQ_API_KEY", "")
    if not env_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        env_key = st.secrets["GROQ_API_KEY"]

    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = env_key

    def setup_voice_pipeline(key):
        try:
            groq_client = Groq(api_key=key) if key else None
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            return VoicePipeline(llm_coach, tts)
        except Exception:
            return None

    if "voice_pipeline" not in st.session_state or st.session_state.voice_pipeline is None:
        st.session_state.voice_pipeline = setup_voice_pipeline(st.session_state.groq_api_key)

    workout_started = st.session_state.get("workout_started", False)
    
    with st.sidebar:
        st.title("🏋️‍♂️ Apna AI Coach")

        if st.session_state.username:
            st.caption(f"👤 Login as {st.session_state.username}")

        with st.expander("🔑 AI Coach Settings", expanded=not bool(st.session_state.groq_api_key)):
            pasted_key = st.text_input(
                "Groq API Key",
                value=st.session_state.groq_api_key,
                type="password",
                help="Paste your Groq API key here (get one free at console.groq.com)",
                placeholder="gsk_..."
            )
            if pasted_key != st.session_state.groq_api_key:
                st.session_state.groq_api_key = pasted_key
                st.session_state.voice_pipeline = setup_voice_pipeline(pasted_key)
                st.rerun()

            if st.session_state.groq_api_key:
                st.caption("🟢 Voice Coach: Connected")
            else:
                st.caption("🟡 Paste Groq key above for live voice coaching")

        st.divider()

        st.subheader("Workout Plan")

        if not workout_started:
            plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")

            plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)

            plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)

            st.markdown("")

            start_session_button = st.button("Start Workout", width="stretch", key="start_session_button")

            if start_session_button:
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_started",
                        exercise=plan_exercise,
                        metrics={}
                    )
                    
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False
                st.rerun()
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets")
            reps = st.session_state.get("reps_per_set")

            st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")

            end_session_button = st.button("End Workout", key="end_session_button", width="stretch")

            if end_session_button:
                st.session_state.workout_started = False
                
                sets_completed = st.session_state.get("sets_completed", 0)
                target_sets = st.session_state.get("target_sets", 0)
                total_reps = st.session_state.get("reps", 0)
                is_completed = (target_sets > 0 and sets_completed >= target_sets)

                if st.session_state.voice_pipeline:
                    if is_completed:
                        event = "workout_completed"
                        metrics_payload = {}
                    else:
                        event = "workout_ended_early"
                        metrics_payload = {
                            "issue": (
                                f"The user ended the workout early! Completed only {sets_completed} of {target_sets} sets "
                                f"({total_reps} total reps). Tell them clearly that they did not finish the full workout, "
                                f"and push them to complete all planned sets next time."
                            )
                        }

                    result = st.session_state.voice_pipeline.process_event(
                        event=event,
                        exercise=exercise,
                        metrics=metrics_payload
                    )
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.rerun()

        if workout_started:
            st.divider()

            exercise = st.session_state.get("exercise_type")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")
            reps_per_set = st.session_state.get("reps_per_set")
            sets_completed = st.session_state.get("sets_completed")
            target_sets = st.session_state.get("target_sets")

            st.subheader("Progress")

            st.metric("Total Reps", f"{total_reps}")
            st.metric("Current Set Reps", f"{current_set_reps} / {reps_per_set}")
            st.metric("Sets Completed", f"{sets_completed} / {target_sets}")

            st.divider()

            if exercise == "Squats":
                st.subheader("Squat Metrics")
                st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
                st.metric("Back Angle", f"{st.session_state.back_angle}°")
                st.metric("Depth Status", st.session_state.depth_status)

            elif exercise == "Push-ups":
                st.subheader("Push-up Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Body Alignment", st.session_state.body_alignment)
                st.metric("Hip Position", st.session_state.hip_status)

            elif exercise == "Biceps Curls (Dumbbell)":
                st.subheader("Curl Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Shoulder Stability", st.session_state.shoulder_status)
                st.metric("Swing Detection", st.session_state.swing_status)

            elif exercise == "Shoulder Press":
                st.subheader("Shoulder Press Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Arm Extension", st.session_state.extension_status)
                st.metric("Back Arch", st.session_state.back_arch_status)

            elif exercise == "Lunges":
                st.subheader("Lunge Metrics")
                st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
                st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
                st.metric("Balance Status", st.session_state.balance_status)

    st.title("AI Real-time GYM Coach")
    st.markdown("#### Real-time pose detection with proactive AI voice coaching")
 
    if st.session_state.get("audio_to_play"):
        autoplay_audio(st.session_state.audio_to_play)

    if st.session_state.get("coach_feedback"):
        st.markdown("")
        st.success(f"🤖 **Coach:** {st.session_state.coach_feedback}")

    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 10px dashed #444;
                border-radius: 0px;
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
                margin-bottom: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,<br>
                    then click <strong>Start Workout</strong> to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )

        sync_metrics_update(context)

        if context.state.playing:
            time.sleep(0.25)
            st.rerun()

        inject_webrtc_styles()

    st.divider()

    st.markdown("#### Workout History")

    user_id = st.session_state.get("user_id", 0)

    if isinstance(user_id, int):
        history_rows = get_users_exercises(user_id)

        arr = [
            {
                "Exercise": row['exercise_name'],
                "Reps": row['reps'],
                "Sets": row['sets'],
                "Time (sec)": row['time'],
                "Date": row['created_at']
            }
            for row in history_rows
        ]

        df = pd.DataFrame(arr)

        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            agg_df = df.groupby(["Exercise", "Date"]).agg({
                "Reps": 'sum',
                "Sets": "sum",
                "Time (sec)": "sum"
            }).reset_index()
            agg_df.index += 1
            st.table(agg_df, border="horizontal")
        else:
            st.info("No workout history found.")


if __name__ == "__main__":
    main()
    