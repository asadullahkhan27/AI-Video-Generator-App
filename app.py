import io
import requests
import streamlit as st
from PIL import Image


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">AI Video Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Create AI videos from reference images and text prompts'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Video Settings")

    duration = st.selectbox(
        "Duration",
        [
            "5 seconds",
            "10 seconds"
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
        "Upload a reference image and describe "
        "the motion you want to generate."
    )


# ==========================================
# INPUT SECTION
# ==========================================

left, right = st.columns(2)


with left:

    st.subheader("Reference Image")

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Reference Image",
            use_container_width=True
        )


with right:

    st.subheader("Video Prompt")

    prompt = st.text_area(
        "Describe your video",
        placeholder=(
            "Example: A cinematic couple walking together "
            "during sunset, realistic movement, natural "
            "facial expressions, smooth camera movement, "
            "cinematic lighting."
        ),
        height=200
    )

    negative_prompt = st.text_area(
        "Negative Prompt",
        placeholder=(
            "blurry, distorted face, extra fingers, "
            "deformed body, low quality"
        ),
        height=100
    )


# ==========================================
# GENERATION FUNCTION
# ==========================================

def generate_video(image_bytes, prompt):

    # Hugging Face token stored in Streamlit Secrets
    token = st.secrets.get("HF_TOKEN", "")

    if not token:

        raise Exception(
            "HF_TOKEN is missing from Streamlit Secrets."
        )

    # Model endpoint
    model_url = (
        "https://api-inference.huggingface.co/models/"
        "stabilityai/stable-video-diffusion-img2vid-xt"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        model_url,
        headers=headers,
        data=image_bytes,
        timeout=600
    )

    if response.status_code != 200:

        try:
            error = response.json()
        except Exception:
            error = response.text

        raise Exception(str(error))

    return response.content


# ==========================================
# GENERATE BUTTON
# ==========================================

st.divider()

generate_button = st.button(
    "Generate AI Video",
    type="primary"
)


if generate_button:

    # --------------------------------------
    # Validation
    # --------------------------------------

    if uploaded_file is None:

        st.error(
            "Please upload a reference image."
        )

        st.stop()


    if not prompt.strip():

        st.error(
            "Please enter a video prompt."
        )

        st.stop()


    # --------------------------------------
    # Generation
    # --------------------------------------

    progress = st.progress(0)

    status = st.empty()

    try:

        status.info(
            "Preparing your reference image..."
        )

        progress.progress(15)

        image_bytes = uploaded_file.getvalue()

        status.info(
            "Sending image to the AI video model..."
        )

        progress.progress(30)

        video_bytes = generate_video(
            image_bytes,
            prompt
        )

        progress.progress(90)

        status.info(
            "Preparing generated video..."
        )

        progress.progress(100)

        status.success(
            "Video generated successfully!"
        )

        # ----------------------------------
        # Output
        # ----------------------------------

        st.subheader("Generated Video")

        st.video(video_bytes)

        st.download_button(
            label="Download AI Video",
            data=video_bytes,
            file_name="generated_video.mp4",
            mime="video/mp4",
            use_container_width=True
        )

    except Exception as error:

        progress.empty()

        status.error(
            "Video generation failed."
        )

        st.error(str(error))
