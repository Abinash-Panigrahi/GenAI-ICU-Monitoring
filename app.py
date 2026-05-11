import streamlit as st
import cv2
import time
from extract import extract_vitals
from validate import validate_vitals ,save_to_file
from report import generate_report, generate_quick_status   

st.set_page_config(page_title="ICU Monitor AI", layout="wide")
st.title("🏥 ICU Monitor AI — Stage 3: Extraction + Validation")
st.caption("Capturing frames, extracting and validating vitals using Gemini Vision")

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
            st.session_state.camera = cv2.VideoCapture(0, cv2.CAP_ANY)
            st.session_state.camera.set(cv2.CAP_PROP_AUTO_WB, 1)

with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.running = False
        if st.session_state.camera is not None:
            st.session_state.camera.release()
            st.session_state.camera = None

if st.button("📋 Generate Report"):
    with st.spinner("Generating report..."):

        # Quick status — always on top
        quick = generate_quick_status()
        st.subheader("⚡ Quick Status")
        st.info(quick)

        # Full report — expandable
        with st.expander("📄 View Full Clinical Report"):
            report = generate_report()
            st.markdown(report)

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
            vitals = validate_vitals(vitals)
            save_to_file(vitals) 
            status_placeholder.success(f"Vitals extracted and validated at {time.strftime('%H:%M:%S')}")

            with vitals_placeholder.container():

                st.subheader("🫀 Core Vitals")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("Heart Rate", f"{vitals.get('heart_rate', '--')} {vitals.get('heart_rate_unit', '')}")
                with c2:
                    st.metric("SpO2", f"{vitals.get('spo2', '--')} {vitals.get('spo2_unit', '')}")
                with c3:
                    st.metric("Pulse Rate", f"{vitals.get('pulse_rate', '--')} {vitals.get('pulse_rate_unit', '')}")
                with c4:
                    st.metric("PI", f"{vitals.get('pi', '--')} {vitals.get('pi_unit', '')}")

                st.subheader("🩸 Blood Pressure")
                c1, c2, c3 = st.columns(3)
                with c1:
                    bp_sys = vitals.get('nibp_systolic', '--')
                    bp_dia = vitals.get('nibp_diastolic', '--')
                    st.metric("NIBP", f"{bp_sys} / {bp_dia} {vitals.get('nibp_unit', '')}")
                with c2:
                    st.metric("NIBP Status", vitals.get('nibp_status', '--'))

                st.subheader("🌡️ Temperature")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("T1", f"{vitals.get('temperature_t1', '--')} {vitals.get('temperature_t1_unit', '')}")
                with c2:
                    st.metric("T2", f"{vitals.get('temperature_t2', '--')} {vitals.get('temperature_t2_unit', '')}")

                st.subheader("📋 Monitor Info")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("ECG Status", vitals.get('ecg_status', '--'))
                with c2:
                    st.metric("Patient Mode", vitals.get('patient_mode', '--'))
                with c3:
                    st.metric("Device", vitals.get('device_name', '--'))
                with c4:
                    st.metric("Timestamp", vitals.get('timestamp', '--'))

                st.subheader("⚠️ Alerts")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Alarm Status", vitals.get('alarm_status', '--'))
                with c2:
                    st.metric("Other Data", vitals.get('any_other_visible_data', '--'))

            with st.expander("Raw JSON Output"):
                json_placeholder.json(vitals)

        except Exception as e:
            status_placeholder.error(f"Extraction failed: {e}")

    else:
        status_placeholder.error("Failed to read frame")

    time.sleep(interval)
    st.rerun()

elif not st.session_state.running:
    status_placeholder.warning("Monitoring stopped. Click Start to begin.")