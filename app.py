import streamlit as st
import requests
import os
import time
from PIL import Image

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .generate-box {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">AI Video Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate videos from text prompts and reference images</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Settings")

    video_duration = st.selectbox(
        "Video Duration",
        ["5 seconds", "10 seconds"]
    )

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["16:9", "9:16", "1:1"]
    )

    model = st.selectbox(
        "AI Model",
        [
            "Video Generation Model",
            "Image-to-Video Model"
        ]
    )

    st.divider()

    st.info(
        "Upload a reference image and describe the motion "
        "you want in your video."
    )

# -----------------------------
# Main UI
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("Reference Image")

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:

        image = Image.open(uploaded_image)

        st.image(
            image,
            caption="Reference Image",
            use_container_width=True
        )

with col2:

    st.subheader("Video Prompt")

    prompt = st.text_area(
        "Describe your video",
        placeholder=(
            "Example: A cinematic Pakistani couple walking "
            "together on a beautiful street during sunset, "
            "natural movement, realistic camera motion..."
        ),
        height=220
    )

    negative_prompt = st.text_area(
        "Negative Prompt",
        placeholder="blurry, distorted face, extra fingers, low quality..."
    )

# -----------------------------
# Generate Button
# -----------------------------
st.divider()

generate = st.button(
    "Generate AI Video",
    type="primary",
    use_container_width=True
)

# -----------------------------
# Generation
# -----------------------------
if generate:

    if not prompt.strip():
        st.error("Please enter a video prompt.")
        st.stop()

    if uploaded_image is None:
        st.warning("Please upload a reference image.")
        st.stop()

    os.makedirs("outputs", exist_ok=True)

    progress = st.progress(0)

    status = st.empty()

    status.info("Preparing your video generation...")

    for i in range(1, 101):

        time.sleep(0.03)

        progress.progress(i)

        if i < 30:
            status.info("Analyzing reference image...")

        elif i < 60:
            status.info("Generating video frames...")

        elif i < 90:
            status.info("Applying motion and camera movement...")

        else:
            status.info("Finalizing video...")

    status.success("Video generation completed.")

    st.info(
        "The Streamlit interface is ready. "
        "Next, connect this button to your actual AI video model/API."
    )

    # Demo output placeholder
    st.subheader("Generated Video")

    st.warning(
        "AI model/API is not connected yet. "
        "This section will display the generated MP4 once the model is connected."
    )
