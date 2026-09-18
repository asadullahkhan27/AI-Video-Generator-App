import streamlit as st
from huggingface_hub import InferenceClient


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("AI Video Generator")

st.write(
    "Generate an AI video from a reference image "
    "and a cinematic text prompt."
)

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Video Settings")

    duration = st.selectbox(
        "Video Duration",
        [
            "Short",
            "Medium"
        ]
    )

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        [
            "16:9",
            "9:16",
            "1:1"
        ]
    )

    st.divider()

    st.info(
        "Upload an image and describe the movement, "
        "camera motion and visual style you want."
    )


# ==========================================
# INPUT
# ==========================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("Reference Image")

    uploaded_image = st.file_uploader(
        "Upload your image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Reference Image",
            use_container_width=True
        )


with col2:

    st.subheader("Video Prompt")

    prompt = st.text_area(
        "Describe your video",
        height=220,
        placeholder=(
            "A cinematic Pakistani couple walking "
            "together during sunset, natural body movement, "
            "realistic facial expressions, gentle wind, "
            "smooth camera movement, cinematic lighting, "
            "photorealistic."
        )
    )

    negative_prompt = st.text_area(
        "Negative Prompt",
        height=100,
        value=(
            "blurry, distorted face, deformed body, "
            "extra fingers, extra limbs, low quality, "
            "flickering, unnatural movement"
        )
    )


st.divider()


# ==========================================
# GENERATE VIDEO
# ==========================================

if st.button(
    "Generate AI Video",
    type="primary",
    use_container_width=True
):

    if uploaded_image is None:

        st.error(
            "Please upload a reference image."
        )

        st.stop()


    if not prompt.strip():

        st.error(
            "Please enter a video prompt."
        )

        st.stop()


    # ======================================
    # HF TOKEN
    # ======================================

    try:

        hf_token = st.secrets["HF_TOKEN"]

    except Exception:

        st.error(
            "HF_TOKEN is missing from Streamlit Secrets."
        )

        st.stop()


    # ======================================
    # CREATE CLIENT
    # ======================================

    client = InferenceClient(
        provider="auto",
        api_key=hf_token
    )


    # ======================================
    # GENERATE
    # ======================================

    progress = st.progress(0)

    status = st.empty()

    try:

        status.info(
            "Preparing reference image..."
        )

        progress.progress(15)

        image_bytes = uploaded_image.getvalue()

        status.info(
            "Sending image and prompt to AI video model..."
        )

        progress.progress(30)

        video = client.image_to_video(
            image=image_bytes,
            model="Wan-AI/Wan2.2-I2V-A14B",
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_frames=81,
            num_inference_steps=30
        )

        progress.progress(90)

        status.info(
            "Preparing final MP4..."
        )

        progress.progress(100)

        status.success(
            "AI video generated successfully!"
        )


        # ==================================
        # VIDEO OUTPUT
        # ==================================

        st.subheader("Generated Video")

        st.video(video)


        # ==================================
        # DOWNLOAD
        # ==================================

        st.download_button(
            label="Download AI Video",
            data=video,
            file_name="ai_generated_video.mp4",
            mime="video/mp4",
            use_container_width=True
        )


    except Exception as e:

        progress.empty()

        status.error(
            "Video generation failed."
        )

        st.error(str(e))
