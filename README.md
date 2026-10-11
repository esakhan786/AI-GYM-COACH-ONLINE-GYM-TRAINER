# 🏋️‍♂️ AI Real-time GYM Coach

> **Your form. Analyzed. Corrected. In milliseconds.**  
> A full-stack, real-time computer vision fitness trainer with proactive AI voice coaching powered by Google MediaPipe, Streamlit WebRTC, Groq Cloud LLM, and Edge TTS.

---

## ⚡ Overview

**AI Real-time GYM Coach** transforms any laptop webcam or mobile browser into an intelligent personal trainer. It tracks 33 3D body landmarks at 30+ frames per second, analyzes joint angles and biomechanical kinematics, counts completed repetitions and sets, and proactively speaks corrective coaching cues in real time when posture errors are detected.

---

## 🌟 Key Features

- **🎥 Real-Time Computer Vision (WebRTC)**: Zero-lag video streaming in the browser via `streamlit-webrtc` and `OpenCV`.
- **📐 3D Biomechanical Pose Landmarker**: Powered by Google MediaPipe Pose Landmarker model, tracking 33 skeletal points.
- **🏋️‍♂️ 5 Core Exercise Detectors**:
  - **Squats**: Calculates knee flexion and thigh-to-hip depth angles; detects shallow squats and forward torso lean.
  - **Push-ups**: Tracks torso-to-leg line, detects sagging hips and piked hips.
  - **Biceps Curls**: Measures elbow flexion and monitors dumbbell torso swinging or elbow drift.
  - **Shoulder Press**: Monitors overhead arm extension and flags excessive lower-back arching.
  - **Lunges**: Assesses front/back knee flexion and tracks center-of-gravity lateral balance.
- **🎙️ Proactive AI Voice Coaching**:
  - Ultra-fast sub-second LLM inference via **Groq Cloud** (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`).
  - Converts dynamic coaching advice into crystal-clear voice audio using **Edge TTS**.
  - Speaks only when needed (rate-limited and prioritized for safety and major workout milestones).
- **🛡️ Bulletproof Resilience & Model Fallbacks**:
  - Automatic fallback between Groq models if specific endpoints are retired or unavailable.
  - Fail-safe fallback cues ensure workouts continue smoothly even during offline or network drops.
  - Paste API key directly in the sidebar settings or configure via Streamlit secrets.
- **📊 Session Analytics & SQLite Persistence**:
  - Profile-based session tracking with SQLite storage.
  - Logs completed sets, reps, duration, and exercise date history.
- **🎨 Dark Futuristic Landing Page**:
  - Cyberpunk-inspired showcase with live metrics, app screenshots, and interactive video demo styling.

---

## 🏛️ System Architecture

```text
[Webcam / Browser Video]
         │
         ▼
[Streamlit WebRTC & OpenCV VideoProcessor]
         │
         ▼
[Google MediaPipe Pose Landmarker (33 Landmarks)]
         │
         ▼
[Biomechanical Kinematics Engine (Trigonometry & State Machines)]
 ├── Rep Counter (Down / Up phases)
 └── Form Fault Detection (Angles, Arching, Drift)
         │
         ├──────────────────────────────┐
         ▼                              ▼
[Groq LLM Coach Engine]         [SQLite Repository]
 (openai/gpt-oss-120b/20b)       (Sets, Reps, Time, History)
         │
         ▼
[Edge TTS Audio Synthesizer]
         │
         ▼
[Real-Time Voice Feedback in Browser]
```

---

## 📁 Repository Structure

```text
ai-gym-coach/
├── LandingPage/                     # Standalone landing page
│   ├── index.html                   # Landing page HTML with architecture & showcase
│   ├── style.css                    # Futuristic dark theme styles
│   ├── images/                      # 5 Live application screenshots & assets
│   │   ├── preview-login.png        # Screenshot: Athlete profile login wall
│   │   ├── preview-dashboard.png    # Screenshot: Routine & rep goal setup
│   │   ├── preview-shoulder-press.png # Screenshot: Live shoulder press pose tracking
│   │   ├── preview-biceps-curl.png  # Screenshot: Live biceps curl arm kinematics
│   │   └── preview-workout.png      # Screenshot: Session completion & voice coach log
│   └── fonts/                       # Averta web fonts
│
├── app/                             # Streamlit web application
│   ├── main.py                      # Main application entry point & UI layout
│   ├── requirements.txt             # Python dependencies
│   │
│   ├── core/                        # Base exercise abstract classes
│   │   └── base_exercise.py
│   │
│   ├── detectors/                   # Biomechanical rule engines
│   │   ├── squat.py                 # Squat angle & depth state machine
│   │   ├── pushup.py                # Push-up straight-line & hip state machine
│   │   ├── biceps_curl.py           # Biceps curl angle & swing detector
│   │   ├── shoulder_press.py        # Overhead press & back arch detector
│   │   └── lunges.py                # Lunge balance & knee angle detector
│   │
│   ├── ml_models/                   # Computer vision models
│   │   └── pose_landmarker_full.task# MediaPipe full pose landmarker model
│   │
│   ├── services/                    # Application services
│   │   ├── auth/                    # Login wall & user profile management
│   │   ├── coaching/                # LLM feedback, TTS & voice pipeline
│   │   ├── config/                  # Workout prompts & exercise lists
│   │   ├── persistence/             # SQLite exercise & workout database
│   │   ├── state/                   # Streamlit session state defaults
│   │   ├── tracking/                # Metrics calculation & rep counters
│   │   ├── ui/                      # CSS and custom font loaders
│   │   └── vision/                  # WebRTC video frame processor
│   │
│   └── static/                      # Custom fonts & app styles
│
├── requirements.txt                 # Root Python dependencies for cloud deployment
├── .gitignore                       # Git ignore rules (protects secrets & DB)
└── README.md                        # Project documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10 or 3.11 installed
- A modern webcam or camera device
- A free API key from [Groq Console](https://console.groq.com)

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/esakhan786/AI-GYM-COACH-ONLINE-GYM-TRAINER.git
cd AI-GYM-COACH-ONLINE-GYM-TRAINER

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Your Groq API Key

Create a `.streamlit/secrets.toml` file inside `app/` (or repository root):

```toml
# app/.streamlit/secrets.toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"
```

*(Alternatively, you can paste your key directly in the sidebar **"🔑 AI Coach Settings"** when the app runs.)*

### 4. Run the Main Application

```bash
streamlit run app/main.py
```

Open your browser at **[http://localhost:8501](http://localhost:8501)**.

### 5. Run the Landing Page

```bash
# In a separate terminal:
cd LandingPage
python -m http.server 8080
```

Open your browser at **[http://localhost:8080](http://localhost:8080)**.

---

## ☁️ Deployment on Streamlit Cloud

1. Push your repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app.
3. Set **Main file path** to: `app/main.py`.
4. Under **Advanced settings** -> **Python version**, select **3.11**.
5. Under **Secrets**, add your Groq API key:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```
6. Deploy! Streamlit will automatically read `requirements.txt` and build the application cleanly.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend & UI** | [Streamlit](https://streamlit.io/) | Interactive dashboard, controls, WebRTC integration |
| **Computer Vision** | [MediaPipe](https://developers.google.com/mediapipe) & [OpenCV](https://opencv.org/) | 3D body landmarks, frame analysis, posture angles |
| **Video Streaming** | [Streamlit WebRTC](https://github.com/whitphx/streamlit-webrtc) | Ultra-low latency webcam ingestion in browser |
| **LLM Inference** | [Groq Cloud](https://groq.com/) | Real-time coaching prompts (`openai/gpt-oss-120b`, `gpt-oss-20b`) |
| **Voice Synthesis** | [Edge TTS](https://github.com/rany2/edge-tts) | Natural audio generation for spoken form cues |
| **Persistence** | [SQLite3](https://www.sqlite.org/) | Athlete logs, timestamps, reps, and set completion |

---

## 👨‍💻 Author & Acknowledgements

- **Developer**: Esa Khan ([GitHub](https://github.com/esakhan786) · [LinkedIn](https://www.linkedin.com/in/esa-khan-1b4941385/))
- **Original Base**: Shradha Khapra

---

## 📄 License

This project is licensed under the MIT License - feel free to build, expand, and train with it!