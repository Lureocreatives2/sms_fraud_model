# Save this as app.py
import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import joblib
import easyocr
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Nigerian SMS Fraud Classifier",
    page_icon="️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (Dark Purple Theme)
# ==========================================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a0f2e 0%, #2d1b4e 50%, #0a0514 100%);
        min-height: 100vh;
    }
    .stTextInput>div>div>input {
        background-color: rgba(45, 27, 78, 0.8);
        color: white;
        border: 2px solid #ba55d3;
        border-radius: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff00ff 0%, #ff1493 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 10px 30px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.6);
    }
    h1 {
        color: white;
        text-align: center;
        text-shadow: 0 0 20px rgba(186, 85, 211, 0.5);
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
    .info-box {
        background: rgba(45, 27, 78, 0.6);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ba55d3;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODELS & OCR
# ==========================================
@st.cache_resource
def load_models():
    """Load models and OCR engine"""
    try:
        model = joblib.load('sms_fraud_model.pkl')
        vectorizer = joblib.load('sms_vectorizer.pkl')
        reader = easyocr.Reader(['en'], gpu=False)
        return model, vectorizer, reader
    except:
        return None, None, None

model, vectorizer, reader = load_models()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def rule_based_scam_check(text):
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
    if image is None:
        return ""
    image_np = np.array(image)
    results = reader.readtext(image_np)
    return " ".join([result[1] for result in results]).strip()

# ==========================================
# MAIN APP
# ==========================================
st.title("🛡️ NIGERIAN SMS FRAUD CLASSIFIER 🛡️")
st.markdown("<p style='text-align: center; color: #e0e0e0;'>Powered by Machine Learning | Built by Opeyemi Adeshina<br>AI & Machine Learning NextGen Cohort</p>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
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
    
    ---
    
    **Features:**
    - ✅ Text or screenshot input
    - ✅ Real-time spam detection
    - ✅ Keyword analysis
    - ✅ Confidence scoring
    - ✅ Safety recommendations
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔽 Input Your Message")
    
    input_method = st.radio("Choose input method:", ["Paste Text", "Upload Screenshot"])
    
    message = ""
    uploaded_image = None
    
    if input_method == "Paste Text":
        message = st.text_area("Paste SMS message here:", 
                               placeholder="Example: Congratulations! You have won 1,000,000 Naira...",
                               height=150)
    else:
        uploaded_image = st.file_uploader("Upload screenshot of SMS", 
                                          type=['png', 'jpg', 'jpeg'])
    
    analyze_btn = st.button("🔍 Analyze Message", use_container_width=True)
    
    if analyze_btn:
        if model is None:
            st.error("️ Models not found! Please upload sms_fraud_model.pkl and sms_vectorizer.pkl files.")
        else:
            with st.spinner("Analyzing message..."):
                # Get message from text or image
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)
                    message = extract_text_from_image(image, reader)
                    source = "📸 Analyzed from screenshot"
                elif message:
                    source = " Analyzed from pasted text"
                else:
                    st.warning("⚠️ Please enter a message or upload a screenshot!")
                    st.stop()
                
                # Clean and predict
                cleaned_msg = clean_text(message)
                msg_vec = vectorizer.transform([cleaned_msg])
                
                ml_pred = model.predict(msg_vec)[0]
                ml_conf = max(model.predict_proba(msg_vec)[0]) * 100
                
                # Rule-based check
                is_rule_spam, matched_kw = rule_based_scam_check(message)
                
                # Hybrid override
                if ml_pred.lower() == 'ham' and is_rule_spam:
                    final_pred = 'spam'
                    override_note = "⚠️ AI Override: Flagged by Security Rules!"
                else:
                    final_pred = ml_pred
                    override_note = ""
                
                # Display results
                st.markdown("---")
                st.subheader(" Analysis Results")
                
                if override_note:
                    st.warning(override_note)
                
                if final_pred.lower() == 'spam':
                    st.markdown(f'<div class="danger-box">🚨 FRAUD DETECTED! 🚨</div>', 
                               unsafe_allow_html=True)
                    st.metric("Confidence", f"{ml_conf:.2f}%")
                    
                    if matched_kw:
                        st.markdown("### 🔍 Triggered Keywords:")
                        for i, kw in enumerate(matched_kw, 1):
                            st.markdown(f"{i}. **{kw.upper()}**")
                    
                    st.markdown("""
                    ### ⚠️ Safety Recommendations:
                    - Do NOT click any links in this message
                    - Do NOT share personal information or bank details
                    - Do NOT send money or make payments
                    - Report this number to your network provider
                    - Delete this message immediately
                    """)
                else:
                    st.markdown(f'<div class="success-box">✅ MESSAGE IS SAFE ✅</div>', 
                               unsafe_allow_html=True)
                    st.metric("Confidence", f"{ml_conf:.2f}%")
                    st.success("No high-risk keywords or suspicious patterns detected.")
                
                st.info(f"Source: {source}")

with col2:
    st.markdown("### 📋 Try These Examples:")
    
    examples = [
        "Hello! You can work from home, Only need a mobile phone GET daily salary 60000NGN-80000NGN",
        "Your new reward is at congratulation to APC member you are just be Rewarded a token of 91,000 call Emma",
        "Hey, are we still meeting for the project review at 2pm today?",
        "Dear friend, I am a bank manager in Nigeria. We have unclaimed funds. Help me transfer",
    ]
    
    for i, ex in enumerate(examples, 1):
        if st.button(f"Example {i}", key=f"ex_{i}", use_container_width=True):
            st.session_state.example_text = ex
            st.rerun()

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ using Streamlit</p>", 
           unsafe_allow_html=True)