import streamlit as st
import cv2
import time

st.set_page_config(page_title="ICU Monitor AI — Camera Test", layout="centered")
st.title("🏥 ICU Monitor AI — Stage 1: Camera Test")
st.caption("Just capturing and displaying frames — no AI yet")

# Session state to control loop and camera hardware
if "running" not in st.session_state:
    st.session_state.running = False
if "camera" not in st.session_state:
    st.session_state.camera = None

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Camera"):
        st.session_state.running = True
        if st.session_state.camera is None:
            st.session_state.camera = cv2.VideoCapture(0)
with col2:
    if st.button("⏹️ Stop Camera"):
        st.session_state.running = False
        if st.session_state.camera is not None:
            st.session_state.camera.release()
            st.session_state.camera = None

# Settings
interval = st.slider("Capture Interval (seconds)", 1, 30, 3)

# Display placeholders
status_placeholder = st.empty()
image_placeholder = st.empty()

# The "Loop" (using rerun instead of a while loop)
if st.session_state.running and st.session_state.camera is not None:
    ret, frame = st.session_state.camera.read()

    if ret:
        cv2.imwrite("frame.jpg", frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_placeholder.image(frame_rgb, caption=f"Live Capture — {time.strftime('%H:%M:%S')}", width="stretch")
        status_placeholder.success(f"Frame captured at {time.strftime('%H:%M:%S')}")
    else:
        status_placeholder.error("Failed to read frame")

    time.sleep(interval)
    st.rerun()

elif not st.session_state.running:
    status_placeholder.warning("Camera stopped. Click Start to begin.")