import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import joblib
import easyocr
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Nigerian SMS Fraud Classifier",
    page_icon="️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for the dark purple/magenta theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: radial-gradient(ellipse at center, #2d1b4e 0%, #1a0f2e 40%, #0a0514 100%);
        color: white;
    }
    
    /* Headers */
    h1 {
        color: white !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(186, 85, 211, 0.5);
        font-size: 2.5rem;
    }
    h2, h3, h4 {
        color: #e0e0e0 !important;
    }
    
    /* Text inputs and text areas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(45, 27, 78, 0.8) !important;
        color: white !important;
        border: 2px solid #ba55d3 !important;
        border-radius: 10px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.3) !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff00ff 0%, #ff1493 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        padding: 10px 30px !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Custom Result Cards */
    .danger-box {
        background: linear-gradient(135deg, #ff00ff 0%, #ff1493 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(255, 0, 255, 0.4);
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
        box-shadow: 0 4px 20px rgba(0, 230, 118, 0.4);
    }
    .info-box {
        background: rgba(45, 27, 78, 0.6);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ba55d3;
        margin: 10px 0;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a0f2e;
    }
    .sidebar .sidebar-content {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD MODELS & OCR ENGINE
# ==========================================
@st.cache_resource
@st.cache_resource
def load_models():
    """Load the trained ML models and OCR engine."""
    try:
        model = joblib.load('sms_fraud_model.pkl')
        vectorizer = joblib.load('sms_vectorizer.pkl')
        reader = easyocr.Reader(['en'], gpu=False)
        return model, vectorizer, reader
    except Exception as e:
        st.error(f"❌ Failed to load models. Error: {e}")
        return None, None, None

# Load the models
model, vectorizer, reader = load_models()

# Check if models loaded successfully
if model is None:
    st.stop()  # Stop execution if models failed to load

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def clean_text(text):
    """Cleans text and separates mashed words."""
    text = str(text).lower()
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text
    # ... rest of your helper functions

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def clean_text(text):
    """Cleans text and separates mashed words (e.g., salary60000 -> salary 60000)."""
    text = str(text).lower()
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def rule_based_scam_check(text):
    """Safety net to catch scams the AI might miss."""
    text_lower = text.lower()
    phone_pattern = r'(\+234|0)[789][01]\d{8}'
    has_phone = bool(re.search(phone_pattern, text))
    
    scam_keywords = ['reward', 'token', 'congratulation', 'apc', 'salary', 'ngn', 
                     'naira', 'winner', 'claim', 'prize', 'urgent', 'bvn', 'atm', 
                     'pin', 'transfer', 'inheritance', 'beneficiary', 'work', 
                     'home', 'mobile', 'daily', 'part-time', 'invest',
                     'bank', 'manager', 'unclaimed', 'funds', 'million', 
                     'dollars', 'help me', 'dear friend', 'foreign']
    
    matched_keywords = [k for k in scam_keywords if k in text_lower]
    
    if (has_phone and len(matched_keywords) >= 1) or (len(matched_keywords) >= 3):
        return True, matched_keywords
    return False, []

def extract_text_from_image(image, reader):
    """Extracts text from an uploaded screenshot using OCR."""
    if image is None:
        return ""
    image_np = np.array(image)
    results = reader.readtext(image_np)
    return " ".join([result[1] for result in results]).strip()

# ==========================================
# 4. MAIN APP UI
# ==========================================
st.title("🛡️ NIGERIAN SMS FRAUD CLASSIFIER 🛡️")
st.markdown("<p style='text-align: center; color: #e0e0e0; font-size: 1.1em;'>Powered by Machine Learning | Built by Opeyemi Adeshina<br>AI & Machine Learning NextGen Cohort</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Instructions
with st.sidebar:
    st.header("📱 How to Use")
    st.markdown("""
    **Option 1: Paste Text**
    1. Copy the SMS message
    2. Paste in the text box
    3. Click Analyze
    
    **Option 2: Upload Screenshot**
    1. Take/capture screenshot
    2. Upload the image
    3. Click Analyze
    
    ---
    
    **Features:**
    - ✅ Text or screenshot input
    - ✅ Hybrid AI Detection
    - ✅ Keyword Insights
    - ✅ Confidence Scoring
    - ✅ Nigerian Context Aware
    """)

# Main Content Area
   model, vectorizer, reader = load_models()
if model is None:
    st.stop() # Stop execution if models failed to load

# Input Section
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

# Analyze Button
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
                st.warning("⚠️ Could not extract text from this image. Please try a clearer screenshot or paste the text manually.")
                st.stop()
    elif input_method == "Paste Text" and message_text:
        final_message = message_text
        source = "Analyzed from pasted text"
    else:
        st.warning("⚠️ Please enter a message or upload a screenshot first!")
        st.stop()

    with st.spinner("🧠 Analyzing message patterns..."):
        # Clean and predict
        cleaned_msg = clean_text(final_message)
        msg_vec = vectorizer.transform([cleaned_msg])
        
        ml_pred = model.predict(msg_vec)[0]
        ml_conf = max(model.predict_proba(msg_vec)[0]) * 100
        
        # Rule-based check
        is_rule_spam, matched_kw = rule_based_scam_check(final_message)
        
        # Hybrid override
        if ml_pred.lower() == 'ham' and is_rule_spam:
            final_pred = 'spam'
            override_note = "⚠️ **AI Override:** Flagged by Security Rules (Phone + Keywords) despite messy text."
        else:
            final_pred = ml_pred
            override_note = ""
        
        # Display Results
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        if override_note:
            st.warning(override_note)
            
        if final_pred.lower() == 'spam':
            st.markdown(f'<div class="danger-box">🚨 FRAUD DETECTED! 🚨</div>', unsafe_allow_html=True)
            st.metric("Confidence Score", f"{ml_conf:.2f}%")
            
            if matched_kw:
                st.markdown("### 🔍 Triggered Keywords:")
                for i, kw in enumerate(matched_kw, 1):
                    st.markdown(f"{i}. **{kw.upper()}**")
            
            st.markdown("""
            ### ⚠️ Safety Recommendations:
            - Do NOT click any links in this message.
            - Do NOT share personal information, BVN, or bank details.
            - Do NOT send money or make payments.
            - Report this number to your network provider and delete the message.
            """)
        else:
            st.markdown(f'<div class="success-box">✅ MESSAGE IS SAFE ✅</div>', unsafe_allow_html=True)
            st.metric("Confidence Score", f"{ml_conf:.2f}%")
            st.success("No high-risk keywords or suspicious patterns detected.")
            
        st.info(f"Source: {source}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ using Streamlit & Scikit-Learn</p>", unsafe_allow_html=True)
