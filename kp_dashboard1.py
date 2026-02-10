import streamlit as st 
import time 
import cv2
# We import Sant's engine, which already includes Mith's AI 
from sant_engine import get_processed_stream 
st.set_page_config(page_title="Marine Trash Collector", layout="wide") 
# Header Section 
st.title("🌊 Project: Autonomous Marine Trash Collector") 
#st.write("Team Members: Mith (AI), Sant (Integration), KP (UI), MO (Hardware)") 
# Sidebar for Setup 
st.sidebar.header("Connection Setup") 
st.sidebar.info("Enter the IP Address shown on MO's Serial Monitor.") 
# Default value is a placeholder 
esp_ip = st.sidebar.text_input("ESP32 IP Address", "192.168.X.X") 
# Main Display Area 
col1, col2 = st.columns([3, 1]) 
 
with col1: 
    st.subheader("Live AI Vision Feed") 
    # This creates a black box that we will update with video 
    video_placeholder = st.empty() 
 
with col2: 
    _='''# --- MANUAL BOAT CONTROLS ---
    st.markdown("---")
    st.subheader("🎮 Manual Override")

    # Create a 3x3 grid using columns
    # Row 1: Forward
    c1, c2, c3 = st.columns(3)
    with c2:
        st.button("🔼 FRONT", use_container_width=True)

    # Row 2: Left, Stop, Right
    c4, c5, c6 = st.columns(3)
    with c4:
        st.button("◀️ LEFT", use_container_width=True)
    with c5:
        st.button("🛑 STOP", type="primary", use_container_width=True)
    with c6:
        st.button("▶️ RIGHT", use_container_width=True)

    # Row 3: Backward
    c7, c8, c9 = st.columns(3)
    with c8:
        st.button("🔽 BACK", use_container_width=True)

    st.info("Manual mode: Use buttons to steer the boat.")
    # --- MANUAL BOAT CONTROLS ---
    st.markdown("---")
    st.subheader("🎮 Manual Override")

    # Row 1: Forward (Center-aligned using 5 columns)
    _, _, center, _, _ = st.columns([1, 1, 1, 1, 1])
    with center:
        st.button("🔼  FRONT", use_container_width=True, key="front")

    # Row 2: Left, Stop, Right (Aligned in a tighter center grid)
    _, left, stop, right, _ = st.columns([1, 1, 1, 1, 1])
    with left:
        st.button("◀️  LEFT", use_container_width=True, key="left")
    with stop:
        st.button("🛑  STOP", type="primary", use_container_width=True, key="stop_boat")
    with right:
        st.button("▶️  RIGHT", use_container_width=True, key="right")

    # Row 3: Backward (Center-aligned)
    _, _, back, _, _ = st.columns([1, 1, 1, 1, 1])
    with back:
        st.button("🔽  BACK", use_container_width=True, key="back")'''
    # --- MANUAL BOAT CONTROLS ---
    st.markdown("---")
    st.subheader("🎮 Manual Override")

    # We create a nested container to limit the width
    # This prevents the vertical text stacking
    control_container = st.container()

    with control_container:
        # Row 1: Forward (Using 3 columns for better spacing)
        _, center_top, _ = st.columns([1, 1, 1])
        with center_top:
            st.button("🔼 FRONT", use_container_width=True, key="btn_f")

        # Row 2: Left, Stop, Right
        left, stop, right = st.columns([1, 1, 1])
        with left:
            st.button("◀️ LEFT", use_container_width=True, key="btn_l")
        with stop:
            st.button("🛑 STOP", type="primary", use_container_width=True, key="btn_s")
        with right:
            st.button("▶️ RIGHT", use_container_width=True, key="btn_r")

        # Row 3: Backward
        _, center_bottom, _ = st.columns([1, 1, 1])
        with center_bottom:
            st.button("🔽 BACK", use_container_width=True, key="btn_b")

    #st.caption("Manual mode active. Controls centered for precision.")

    st.info("Manual mode: D-pad centered for precision control.")
    st.subheader("System Status") 
    status_indicator = st.empty() 
    st.metric(label="System Mode", value="Active Scan") 
    stop_btn = st.button("Stop System") 
 
# The Main Loop 
# Initialize the 'running' state if it doesn't exist
if 'running' not in st.session_state:
    st.session_state.running = False

# Start Button
if st.sidebar.button("🚀 Start Surveillance"):
    st.session_state.running = True

# Stop Button
if stop_btn:
    st.session_state.running = False
    status_indicator.info("System Stopped.")

# The Main Loop logic
if st.session_state.running:
    status_indicator.success("System Active")
    # This loop keeps going until session_state.running is False
    while st.session_state.running:
        final_frame = get_processed_stream(esp_ip)
        
        if final_frame is not None:
            final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(final_frame_rgb, channels="RGB")
        else:
            status_indicator.error("Connection Lost. Checking IP...")
            time.sleep(1) # Don't spam the network if it's down
            
        # This is CRITICAL for Streamlit to check for new button clicks
        time.sleep(0.01)


_='''if st.sidebar.button("🚀 Start Surveillance"): 
    status_indicator.success("System Connecting...") 
     
    while not stop_btn: 
        # 1. Get the AI-processed image from Sant's engine 
        final_frame = get_processed_stream(esp_ip)
        final_frame = None  # Placeholder until sant_engine is available
        
        if final_frame is not None: 
            # 2. Display it! 
            # We convert BGR to RGB because OpenCV and Streamlit disagree on colors 
            final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB) 
            video_placeholder.image(final_frame_rgb, channels="RGB") 
            status_indicator.success("Receiving Data") 
else: 
    status_indicator.error("Connecting...")
    # Wait a bit before trying again to not crash the app 
    time.sleep(0.5)'''