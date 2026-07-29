import streamlit as st
import numpy as np
import re
import string
import joblib

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
def load_models():
    """Load the trained ML models."""
    import os
    current_folder = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_folder, 'sms_fraud_model.pkl')
    vectorizer_path = os.path.join(current_folder, 'sms_vectorizer.pkl')
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    except Exception as e:
        st.error(f"❌ Failed to load models. Error: {e}")
        return None, None

model, vectorizer = load_models()

if model is None:
    st.stop()

# ==========================================
# 3. HELPER FUNCTIONS
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
                     'dollars', 'help me', 'dear friend', 'foreign', 'whatsapp',
                     'telegram', 'join', 'earn', 'minutes', 'payment']
    
    matched_keywords = [k for k in scam_keywords if k in text_lower]
    
    if (has_phone and len(matched_keywords) >= 1) or (len(matched_keywords) >= 3):
        return True, matched_keywords
    return False, []

# ==========================================
# 4. MAIN APP UI
# ==========================================
st.title("🛡️ NIGERIAN SMS FRAUD CLASSIFIER 🛡️")
st.markdown("<p style='text-align: center; color: #e0e0e0;'>Powered by Machine Learning | Built by Opeyemi Adeshina<br>AI & Machine Learning NextGen Cohort</p>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("📱 How to Use")
    st.markdown("""
    1. Copy the suspicious SMS message.
    2. Paste it into the text box below.
    3. Click **Analyze Message**.
    
    ---
    
    **Features:**
    - ✅ Hybrid AI Detection
    - ✅ Keyword Insights
    - ✅ Confidence Scoring
    - ✅ Nigerian Context Aware
    """)

st.subheader("🔽 Input Your Message")
message_text = st.text_area(
    "Paste SMS message here:", 
    value=st.session_state.message_text,
    placeholder="Example: Dear, do you need a part-time job? You don't need to invest...",
    height=150,
    key="sms_input"  
)

analyze_btn = st.button(" Analyze Message", use_container_width=True)

# ==========================================
# 4. INPUT & EXAMPLES SECTION
# ==========================================

# Initialize the text in the session state so it can be updated by buttons
if 'message_text' not in st.session_state:
    st.session_state.message_text = ""

st.subheader("🔽 Input Your Message")

# Link the text area to the session state
message_text = st.text_area(
    "Paste SMS message here:", 
    value=st.session_state.message_text,
    placeholder="Example: Dear, do you need a part-time job? You don't need to invest...",
    height=150
)

# Example Buttons
st.markdown("---")
st.subheader("📋 Try These Examples:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💼 Job Scam", use_container_width=True):
        st.session_state.message_text = "Dear, do you need a part-time job? You don't need to invest. Our work is very simple. You only need to spend 10-30 minutes and pay your salary immediately after completing your mobile phone. Earn 60000NGN every day. If you want to join, please add us through WhatsApp."
        st.rerun()

with col2:
    if st.button("🎁 APC Reward", use_container_width=True):
        st.session_state.message_text = "Your new reward is at congratulation to APC member you are just be Rewarded a token of 91,000 call Emma for your payment(08163700328)"
        st.rerun()

with col3:
    if st.button("🏦 Bank Manager", use_container_width=True):
        st.session_state.message_text = "Dear friend, I am a bank manager in Nigeria. We have unclaimed funds. Help me transfer and get 20% commission."
        st.rerun()

with col4:
    if st.button("✅ Safe Message", use_container_width=True):
        st.session_state.message_text = "Hey, are we still meeting for the project review at 2pm today? Let me know if you're coming."
        st.rerun()

# ==========================================
# 5. ANALYSIS LOGIC
# ==========================================
analyze_btn = st.button("🔍 Analyze Message", use_container_width=True)

if analyze_btn:
    if not message_text or len(message_text.strip()) == 0:
        st.warning("⚠️ Please enter a message first!")
        st.stop()

    with st.spinner("🧠 Analyzing message patterns..."):
        # (Keep your existing analysis logic here...)
        cleaned_msg = clean_text(message_text)
        msg_vec = vectorizer.transform([cleaned_msg])
        
        ml_pred = model.predict(msg_vec)[0]
        ml_conf = max(model.predict_proba(msg_vec)[0]) * 100
        
        is_rule_spam, matched_kw = rule_based_scam_check(message_text)
        
        if ml_pred.lower() == 'ham' and is_rule_spam:
            final_pred = 'spam'
            override_note = "️ **AI Override:** Flagged by Security Rules!"
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

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ using Streamlit2026</p>", unsafe_allow_html=True)
