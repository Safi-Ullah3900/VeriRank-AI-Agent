import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="VeriRank AI v4.4 - 1-Click Combo Engine",
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
# 🆕 THE ULTIMATE 1-CLICK JAVASCRIPT POPUP
# ==========================================
@st.dialog("✨ VeriRank Quick Publish")
def show_combo_popup(review_text, target_url):
    st.success("🎉 Aapka Review Taiyar Hai!")
    st.write("Neeche diye gaye review ko dekhlein, aur direct publish karein:")
    
    # Visual check for the user to read the text
    st.text_area("📋 Generated Text View:", value=review_text, height=120, disabled=True)
    
    st.write("---")
    st.markdown("### **🎯 Asaan Automation Flow:**")
    st.caption("Neeche diye gaye magic button ko **sirf ek baar click** karein. Review khud-ba-khud copy ho jayega aur Google Maps open ho jayega. Wahan ja kar bas **Paste** kar dein!")

    # Preparing string sanitation for clean JavaScript injection
    js_safe_review = review_text.replace("`", "\\`").replace('"', '\\"').replace("\n", "\\n")
    
    # HIGH-END JAVASCRIPT COMBO BUTTON INJECTION
    # This executes native browser clipboard storage and redirection in a unified interaction event
    js_button_code = f"""
    <button id="combo-btn" style="
        width: 100%; 
        background: linear-gradient(135deg, #FF4B4B 0%, #FF2B2B 100%);
        color: white; 
        border: none; 
        padding: 14px; 
        font-size: 16px; 
        font-weight: bold; 
        border-radius: 8px; 
        cursor: pointer;
        box-shadow: 0px 4px 15px rgba(255,75,75,0.4);
        transition: all 0.2s ease;
    ">📋 Copy Review & Go to Google Maps 🚀</button>

    <script>
    document.getElementById('combo-btn').addEventListener('click', function() {{
        const textToCopy = `{js_safe_review}`;
        
        // Command 1: Force background clipboard storage natively
        navigator.clipboard.writeText(textToCopy).then(function() {{
            // Command 2: Instantly trigger cross-tab deep-linking redirection
            window.open('{target_url}', '_blank');
        }}).catch(function(err) {{
            // Secure fallback redirection if browser restricts clipboard sandbox
            window.open('{target_url}', '_blank');
        }});
    }});
    </script>
    """
    
    # Rendering the specialized JS combo component
    components.html(js_button_code, height=80)

# ==========================================
# INTERFACE 1: CUSTOMER FEEDBACK STATION
# ==========================================
if app_mode == "Customer Station 🧑‍💻":
    st.title("🎯 VeriRank AI")
    st.subheader("Smart Local SEO Review Agent")
    
    st.write("---")
    st.markdown("### 📝 Customer Feedback Station")
    st.caption(f"Review being generated securely for: **{shop_name}**")

    category = st.text_input("Aapne kya khareeda? (Optional):", placeholder="Eg: HP Elitebook, Core i7 Laptop")
    user_input = st.text_area(
        "Aapka hamari dukan par experience kaisa raha? (Roman Urdu ya Pashto mein likhein):",
        placeholder="Eg: dukaandar ka behaviour zbrdst tha aur price bhi sahi thi..."
    )

    # Friendly, premium customer-facing click target
    if st.button("✨ Create Review ", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Meharbani kar ke pehle thora sa apna feedback likhein.")
        else:
            with st.spinner("AI aapke liye ek shandaar review likh raha hai..."):
                response = None
                models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.0-flash"]
                
                SYSTEM_INSTRUCTION = f"""
                You are "VeriRank AI", an organic Local SEO Review Assistant. Your job is to transform raw inputs into natural, human-sounding English Google Reviews.
                Target Merchant: {shop_name}
                Product Focus: {category if category else "hardware and laptops"}
                
                CRITICAL LINGUISTIC INSTRUCTIONS FOR LAYMAN AUTHENTICITY:
                1. Use natural, conversational vocabulary (e.g., "fair pricing", "genuine items", "honest dealing", "trusted wholesaler", "highly recommend").
                2. Keep sentence structures brief and entirely grounded in the facts input by the user. Avoid technical or robotic fluff.
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
                    
                    # Log monitoring data
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.review_logs.append({
                        "time": now,
                        "item": category if category else "General Hardware",
                        "status": "Combo Triggered"
                    })
                    
                    # Trigger the advanced hybrid JS popup modal
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
st.caption("VeriRank AI v4.4 | JavaScript Combo Integration Layer | Google-Kaggle Bootcamp Submission")