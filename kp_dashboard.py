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
    st.subheader("System Status") 
    status_indicator = st.empty() 
    st.metric(label="System Mode", value="Active Scan") 
    stop_btn = st.button("Stop System") 
 
# The Main Loop 
if st.sidebar.button("🚀 Start Surveillance"): 
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
    time.sleep(0.5)