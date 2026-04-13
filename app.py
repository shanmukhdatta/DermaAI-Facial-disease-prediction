"""
DermaAI - Professional Skin Disease Classification System
Main Streamlit Application
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import io
import base64
from datetime import datetime

# Page config MUST be first
st.set_page_config(
    page_title="DermaAI - Skin Disease Classifier",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

from model_loader import ModelManager
from preprocessor import ImagePreprocessor
from predictor import EnsemblePredictor
from disease_info import DISEASE_INFO
from ui_components import (
    inject_custom_css,
    render_header,
    render_validation_badge,
    render_prediction_card,
    render_history_item,
    render_disclaimer,
    render_loading_animation
)

# ─── Initialize session state ────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "model_manager" not in st.session_state:
    st.session_state.model_manager = None
if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False

# ─── Load models (cached) ────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_models():
    manager = ModelManager()
    manager.load_all_models()
    return manager

# ─── Inject CSS ──────────────────────────────────────────────────────────────
inject_custom_css()

# ─── Header ──────────────────────────────────────────────────────────────────
render_header()

# ─── Model Loading ───────────────────────────────────────────────────────────
if not st.session_state.models_loaded:
    with st.spinner(""):
        loading_placeholder = st.empty()
        loading_placeholder.markdown(render_loading_animation("Initializing DermaAI Engine..."), unsafe_allow_html=True)
        try:
            st.session_state.model_manager = load_models()
            st.session_state.models_loaded = True
            loading_placeholder.empty()
            st.success("✅ All models loaded successfully!")
            time.sleep(0.8)
            st.rerun()
        except Exception as e:
            loading_placeholder.empty()
            st.warning(f"⚠️ Some models could not be loaded: {e}\nRunning in demo mode.")
            st.session_state.models_loaded = True

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <span class='brand-icon'>🔬</span>
        <span class='brand-text'>DermaAI</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Capture or Upload** your skin image
    2. Ensure **good lighting** and **clear focus**
    3. Keep the affected area **centered**
    4. Wait for **validation** to pass (green border)
    5. Click **Analyze** to get results
    """)

    st.markdown("---")
    st.markdown("### 🧠 Active Models")
    if st.session_state.model_manager:
        loaded = st.session_state.model_manager.get_loaded_models()
        for model_name, status in loaded.items():
            icon = "✅" if status else "❌"
            st.markdown(f"{icon} `{model_name}`")
    else:
        st.markdown("*Loading...*")

    st.markdown("---")
    render_disclaimer()

# ─── Main Content ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📸 Analyze", "📊 History", "ℹ️ About"])

# ══════════════════════════════════════════════════════════════════
# TAB 1: ANALYZE
# ══════════════════════════════════════════════════════════════════
with tab1:
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 🖼️ Image Input")

        input_mode = st.radio(
            "Choose input method:",
            ["📁 Upload Image", "📷 Camera Capture"],
            horizontal=True,
            label_visibility="collapsed"
        )

        image = None
        preprocessor = ImagePreprocessor()

        if input_mode == "📁 Upload Image":
            uploaded = st.file_uploader(
                "Upload skin image",
                type=["jpg", "jpeg", "png", "bmp", "webp"],
                help="Supported: JPG, PNG, BMP, WebP"
            )
            if uploaded:
                pil_img = Image.open(uploaded).convert("RGB")
                image = np.array(pil_img)

        else:  # Camera
            st.markdown("""
            <div class='camera-guide'>
                <div class='camera-overlay'>
                    <div class='alignment-frame' id='alignFrame'>
                        <div class='corner tl'></div>
                        <div class='corner tr'></div>
                        <div class='corner bl'></div>
                        <div class='corner br'></div>
                        <div class='guide-text'>Align skin area here</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            camera_img = st.camera_input("Capture skin area", label_visibility="collapsed")
            if camera_img:
                pil_img = Image.open(camera_img).convert("RGB")
                image = np.array(pil_img)

        # ── Image Validation ──────────────────────────────────────
        if image is not None:
            validation = preprocessor.validate_image(image)

            # Show image with colored border
            border_color = "#00ff88" if validation["passed"] else "#ff4444"
            status_icon = "✅" if validation["passed"] else "❌"

            st.markdown(f"""
            <div style='border: 3px solid {border_color}; border-radius: 12px; 
                        padding: 4px; margin: 8px 0; transition: all 0.3s ease;
                        box-shadow: 0 0 20px {border_color}44;'>
            """, unsafe_allow_html=True)
            st.image(image, use_container_width=True, caption="Input Image")
            st.markdown("</div>", unsafe_allow_html=True)

            # Validation badges
            render_validation_badge(validation)

            # Analyze button
            if validation["passed"]:
                if st.button("🔬 Analyze Skin Condition", type="primary", use_container_width=True):
                    with col_output:
                        with st.spinner(""):
                            placeholder = st.empty()
                            placeholder.markdown(
                                render_loading_animation("Running ensemble analysis..."),
                                unsafe_allow_html=True
                            )
                            time.sleep(0.5)

                            try:
                                predictor = EnsemblePredictor(st.session_state.model_manager)
                                results = predictor.predict(image)
                                placeholder.empty()

                                # Store in history
                                history_entry = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "image": image.copy(),
                                    "results": results
                                }
                                st.session_state.history.insert(0, history_entry)
                                if len(st.session_state.history) > 10:
                                    st.session_state.history.pop()

                                render_prediction_card(results, DISEASE_INFO)

                            except Exception as e:
                                placeholder.empty()
                                st.error(f"Analysis failed: {str(e)}")
            else:
                st.button(
                    "⚠️ Fix image issues to analyze",
                    disabled=True,
                    use_container_width=True
                )
        else:
            with col_output:
                st.markdown("""
                <div class='empty-state'>
                    <div class='empty-icon'>🔬</div>
                    <div class='empty-title'>Ready to Analyze</div>
                    <div class='empty-sub'>Upload or capture an image to begin</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2: HISTORY
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📊 Prediction History")

    if not st.session_state.history:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-icon'>📋</div>
            <div class='empty-title'>No predictions yet</div>
            <div class='empty-sub'>Your analysis history will appear here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.history = []
            st.rerun()

        for i, entry in enumerate(st.session_state.history):
            render_history_item(entry, i)

# ══════════════════════════════════════════════════════════════════
# TAB 3: ABOUT
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### ℹ️ About DermaAI")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **DermaAI** is a multi-model ensemble skin disease classification system 
        trained to detect 13 different skin conditions from facial/skin images.

        #### 🧠 Ensemble Architecture
        - **Primary**: SVM (highest weighted)
        - **Deep Learning**: MobileNetV2, AlexNet, LeNet
        - **Classical ML**: Random Forest
        - **Fusion**: Weighted probability averaging

        #### 📊 Detectable Conditions
        """)
        from disease_info import DISEASE_INFO
        for cls, info in DISEASE_INFO.items():
            st.markdown(f"- {info['emoji']} {cls.replace('_', ' ')}")

    with col2:
        st.markdown("""
        #### ⚙️ Technical Stack
        - **Framework**: Streamlit
        - **CV**: OpenCV
        - **DL**: TensorFlow / Keras
        - **ML**: scikit-learn (joblib)
        - **Image**: PIL / NumPy

        #### 🛡️ Safety Features
        - Brightness validation
        - Blur detection
        - Skin region verification
        - Confidence thresholding

        #### ⚠️ Disclaimer
        This tool is for **educational purposes only**.
        Always consult a qualified dermatologist for medical advice.
        """)
