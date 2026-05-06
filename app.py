import streamlit as st
import cv2
import time
from extract import extract_vitals

st.set_page_config(page_title="ICU Monitor AI", layout="centered")
st.title("🏥 ICU Monitor AI — Stage 2: Vitals Extraction")
st.caption("Capturing frames and extracting vitals using Gemini Vision")

# Session state
if "running" not in st.session_state:
    st.session_state.running = False
if "camera" not in st.session_state:
    st.session_state.camera = None

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Monitoring"):
        st.session_state.running = True
        if st.session_state.camera is None:
            st.session_state.camera = cv2.VideoCapture(1, cv2.CAP_ANY)
            st.session_state.camera.set(cv2.CAP_PROP_AUTO_WB, 1)
with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.running = False
        if st.session_state.camera is not None:
            st.session_state.camera.release()
            st.session_state.camera = None

# Settings
interval = st.slider("Capture Interval (seconds)", 5, 60, 25)

# Placeholders
status_placeholder = st.empty()
image_placeholder = st.empty()
vitals_placeholder = st.empty()
json_placeholder = st.empty()

# Loop
if st.session_state.running and st.session_state.camera is not None:
    ret, frame = st.session_state.camera.read()

    if ret:
        cv2.imwrite("frame.jpg", frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_placeholder.image(frame_rgb, caption=f"Live Capture — {time.strftime('%H:%M:%S')}", width="stretch")

        status_placeholder.info("Extracting vitals from image...")

        try:
            vitals = extract_vitals("frame.jpg")
            status_placeholder.success(f"Vitals extracted at {time.strftime('%H:%M:%S')}")

            with vitals_placeholder.container():
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Heart Rate", f"{vitals.get('heart_rate', '--')} bpm")
                    st.metric("SpO2", f"{vitals.get('spo2', '--')} %")
                with c2:
                    bp_sys = vitals.get('blood_pressure_systolic', '--')
                    bp_dia = vitals.get('blood_pressure_diastolic', '--')
                    st.metric("Blood Pressure", f"{bp_sys}/{bp_dia}")
                    st.metric("Resp Rate", f"{vitals.get('respiratory_rate', '--')}")
                with c3:
                    st.metric("Temperature", f"{vitals.get('temperature', '--')} °C")

            json_placeholder.json(vitals)

        except Exception as e:
            status_placeholder.error(f"Extraction failed: {e}")

    else:
        status_placeholder.error("Failed to read frame")

    time.sleep(interval)
    st.rerun()

elif not st.session_state.running:
    status_placeholder.warning("Monitoring stopped. Click Start to begin.")