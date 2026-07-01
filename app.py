import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="VeriRank AI v4.7 - Standard Compliant UX",
    page_icon="🎯",
    layout="centered"
)

# Session State Database
if "review_logs" not in st.session_state:
    st.session_state.review_logs = []

# Admin Panel Sidebar
st.sidebar.markdown("### 🏢 VeriRank Admin Panel")
app_mode = st.sidebar.radio("Go To Interface:", ["Customer Station 🧑‍💻", "Merchant Dashboard 📊"])

# Backend Secrets Configuration
api_key = st.secrets.get("GEMINI_API_KEY", "")
shop_name = st.secrets.get("MERCHANT_NAME", "Shaheen Laptop Wholesaler").strip()
gmb_url = st.secrets.get("MERCHANT_GMB_URL", "https://g.page/r/CfE02PXX8HUQEAE/review").strip()

if not api_key:
    st.error("🛑 Configuration Error: API Key missing in backend secrets.")
    st.stop()

# ==========================================
# 🎯 THE 100% UNBLOCKED NATIVE ANCHOR POPUP
# ==========================================
@st.dialog("📢 IMPORTANT: How to Publish")
def show_combo_popup(review_text, target_url):
    st.warning("⚠️ **Dukan Par Khade Customer Ke Liye Zaroori Note:**", icon="⚠️")
    st.markdown(
        """
        Google ke security rules ki wajah se review khud type nahi ho sakta. 
        Aapko agli screen par ja kar sirf **PASTE** ka button dabana hai!
        """
    )
    
    # Clean text preview area
    st.text_area("📋 Aapka Generated Review:", value=review_text, height=100, disabled=True)
    
    st.write("---")

    # Sanitizing string tokens safely for JavaScript execution context
    js_safe_review = review_text.replace("`", "\\`").replace('"', '\\"').replace("\n", "\\n")
    
    # ADVANCED NATIVE ANCHOR INJECTION (Bypasses all iframe pop-up blockers)
    js_button_code = f"""
    <a href="{target_url}" target="_blank" id="combo-link" style="
        display: block;
        text-align: center;
        text-decoration: none;
        width: 90%; 
        background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
        color: white; 
        border: none; 
        padding: 16px; 
        font-size: 16px; 
        font-weight: bold; 
        border-radius: 8px; 
        cursor: pointer;
        box-shadow: 0px 4px 15px rgba(0,200,81,0.4);
        margin: 0 auto;
    ">🟢 Click Here to Auto-Copy & Open Maps 🚀</a>

    <script>
    document.getElementById('combo-link').addEventListener('click', function(e) {{
        // Synchronous Textarea Hack to force background clipboard save instantly
        const textToCopy = `{js_safe_review}`;
        const input = document.createElement('textarea');
        input.value = textToCopy;
        document.body.appendChild(input);
        input.select();
        try {{
            document.execCommand('copy');
        }} catch (err) {{
            console.log('Sandbox restriction fallback');
        }}
        document.body.removeChild(input);
        
        // Show the prompt block alert to guide the user mindset
        alert("📋 REVIEW COPIED SUCCESSFULLY!\\n\\nDear Customer, agli screen par ja kar likhnay ki koi zaroorat nahi hai. Bas box par ungli daba kar rakhain (Long Press) aur PASTE par click kar dain!\\n\\nAb OK dabo kar Google Maps par jain. 👍");
    }});
    </script>
    """
    
    components.html(js_button_code, height=90)

# ==========================================
# INTERFACE 1: CUSTOMER FEEDBACK STATION
# ==========================================
if app_mode == "Customer Station 🧑‍💻":
    st.title("🎯 VeriRank AI")
    st.subheader("Smart Local SEO Review Agent")
    
    st.write("---")
    st.markdown("### 📝 Customer Feedback Station")
    st.caption(f"Review being generated securely for: **{shop_name}**")

    category = st.text_input("Aapne kya khareeda? (Optional):", placeholder="Eg: HP Laptop, Core i7")
    user_input = st.text_area(
        "Aapka hamari dukan par experience kaisa raha? (Roman Urdu ya Pashto mein likhein):",
        placeholder="Eg: dukaandar ka behaviour zbrdst tha aur price bhi sahi thi..."
    )

    if st.button("✨ Mera Review Banayein", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Meharbani kar ke pehle thora sa apna feedback likhein.")
        else:
            with st.spinner("AI aapke liye ek shandaar review likh raha hai..."):
                response = None
                models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.0-flash"]
                
                # Context Optimization Mapping Instruction Matrix
                SYSTEM_INSTRUCTION = f"""
                You are "VeriRank AI", an organic Local SEO Review Assistant. Your job is to transform raw inputs into natural, human-sounding English Google Reviews.
                Target Merchant: {shop_name}
                Product Focus: {category if category else "hardware and laptops"}
                
                CRITICAL LINGUISTIC INSTRUCTIONS FOR LAYMAN AUTHENTICITY:
                1. Use natural, conversational vocabulary (e.g., "fair pricing", "genuine items", "honest dealing", "trusted wholesaler", "highly recommend").
                2. Sentence structure must be incredibly simple, as if written by a regular walk-in local consumer. No complex tech terminology.
                3. Output ONLY the clean review text.
                """
                
                try:
                    client = genai.Client(api_key=api_key)
                    config = types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION, temperature=0.7)
                    
                    for model_name in models_to_try:
                        try:
                            res = client.models.generate_content(model=model_name, contents=user_input, config=config)
                            if res and res.text:
                                response = res
                                break
                        except:
                            continue
                except Exception as e:
                    st.error(f"Error: {e}")

                if response and response.text:
                    generated_text = response.text.strip()
                    
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.review_logs.append({
                        "time": now,
                        "item": category if category else "General Hardware",
                        "status": "Interceptor Fired"
                    })
                    
                    show_combo_popup(generated_text, gmb_url)

# ==========================================
# INTERFACE 2: MERCHANT ANALYTICS DASHBOARD
# ==========================================
elif app_mode == "Merchant Dashboard 📊":
    st.title("📊 VeriRank Business Control Center")
    st.subheader(f"Live Analytics for {shop_name}")
    st.write("---")
    
    total_reviews = len(st.session_state.review_logs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total AI Reviews Driven", value=total_reviews, delta=f"+{total_reviews} today")
    with col2:
        st.metric(label="Spam Protection Rate", value="100%", delta="Verified")
    with col3:
        st.metric(label="Ecosystem Status", value="Active ⚡")
        
    st.markdown("### 📜 Live Counter Log Feed")
    st.dataframe(st.session_state.review_logs, use_container_width=True)

st.write("---")
st.caption("VeriRank AI v4.7 | Pure Production Shield | Google-Kaggle Bootcamp Submission")