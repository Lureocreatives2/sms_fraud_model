import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import joblib
import easyocr
from PIL import Image
import os

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Nigerian SMS Fraud Classifier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(ellipse at center, #2d1b4e 0%, #1a0f2e 40%, #0a0514 100%);
        color: white;
    }
    h1 {
        color: white !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(186, 85, 211, 0.5);
        font-size: 2.5rem;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(45, 27, 78, 0.8) !important;
        color: white !important;
        border: 2px solid #ba55d3 !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff00ff 0%, #ff1493 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        padding: 10px 30px !important;
        width: 100%;
    }
    .danger-box {
        background: linear-gradient(135deg, #ff00ff 0%, #ff1493 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #00e676 0%, #00c853 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD MODELS
# ==========================================
@st.cache_resource
@st.cache_resource
def load_models():
    """Load the trained ML models and OCR engine."""
    import os
    
    # Get the exact folder where app.py is located
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full paths to the files
    model_path = os.path.join(current_folder, 'sms_fraud_model.pkl')
    vectorizer_path = os.path.join(current_folder, 'sms_vectorizer.pkl')
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        reader = easyocr.Reader(['en'], gpu=False)
        return model, vectorizer, reader
    except Exception as e:
        st.error(f"❌ Failed to load models. Looking in: {current_folder}. Error: {e}")
        return None, None, None
# ==========================================
# 4. MAIN APP UI
# ==========================================
st.title("🛡️ NIGERIAN SMS FRAUD CLASSIFIER 🛡️")
st.markdown("<p style='text-align: center; color: #e0e0e0;'>Powered by Machine Learning | Built by Opeyemi Adeshina<br>AI & Machine Learning NextGen Cohort</p>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("📱 How to Use")
    st.markdown("""
    **Option 1: Paste Text**
    1. Copy the SMS message
    2. Paste in the text box
    3. Click Analyze
    
    **Option 2: Upload Screenshot**
    1. Take screenshot
    2. Upload the image
    3. Click Analyze
    """)

st.subheader("🔽 Input Your Message")
input_method = st.radio("Choose input method:", ["Paste Text", "Upload Screenshot"], horizontal=True)

message_text = ""
uploaded_image = None

if input_method == "Paste Text":
    message_text = st.text_area("Paste SMS message here:", 
                           placeholder="Example: Congratulations! You have won 1,000,000 Naira...",
                           height=150)
else:
    uploaded_image = st.file_uploader("Upload screenshot of SMS", type=['png', 'jpg', 'jpeg'])

analyze_btn = st.button("🔍 Analyze Message", use_container_width=True)

# ==========================================
# 5. ANALYSIS LOGIC
# ==========================================
if analyze_btn:
    final_message = ""
    source = ""
    
    if input_method == "Upload Screenshot" and uploaded_image is not None:
        with st.spinner("📸 Extracting text from image..."):
            image = Image.open(uploaded_image)
            final_message = extract_text_from_image(image, reader)
            source = "Analyzed from screenshot"
            if not final_message:
                st.warning("⚠️ Could not extract text from this image.")
                st.stop()
    elif input_method == "Paste Text" and message_text:
        final_message = message_text
        source = "Analyzed from pasted text"
    else:
        st.warning("⚠️ Please enter a message or upload a screenshot first!")
        st.stop()

    with st.spinner("🧠 Analyzing message..."):
        cleaned_msg = clean_text(final_message)
        msg_vec = vectorizer.transform([cleaned_msg])
        
        ml_pred = model.predict(msg_vec)[0]
        ml_conf = max(model.predict_proba(msg_vec)[0]) * 100
        
        is_rule_spam, matched_kw = rule_based_scam_check(final_message)
        
        if ml_pred.lower() == 'ham' and is_rule_spam:
            final_pred = 'spam'
            override_note = "⚠️ **AI Override:** Flagged by Security Rules!"
        else:
            final_pred = ml_pred
            override_note = ""
        
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        if override_note:
            st.warning(override_note)
            
        if final_pred.lower() == 'spam':
            st.markdown(f'<div class="danger-box">🚨 FRAUD DETECTED! 🚨</div>', unsafe_allow_html=True)
            st.metric("Confidence", f"{ml_conf:.2f}%")
            
            if matched_kw:
                st.markdown("### 🔍 Triggered Keywords:")
                for i, kw in enumerate(matched_kw, 1):
                    st.markdown(f"{i}. **{kw.upper()}**")
            
            st.markdown("### ⚠️ Safety Recommendations:\n- Do NOT click links\n- Do NOT share BVN or bank details\n- Report and delete immediately")
        else:
            st.markdown(f'<div class="success-box">✅ MESSAGE IS SAFE ✅</div>', unsafe_allow_html=True)
            st.metric("Confidence", f"{ml_conf:.2f}%")
            st.success("No high-risk patterns detected.")
            
        st.info(f"Source: {source}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
