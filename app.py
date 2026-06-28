import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

# Page Configuration for Premium, Mobile-Friendly UI
st.set_page_config(
    page_title="VeriRank AI v3.5 - Local SEO Review Agent",
    page_icon="🎯",
    layout="centered"
)

# Custom Styling for modern premium SaaS look and mobile optimization
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
    color: #f3f4f6;
}

/* Glassmorphism card wrappers */
.glass-container {
    background: rgba(31, 41, 55, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.3);
}

/* Accent texts */
.gradient-text {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Button aesthetics */
div.stButton > button {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# Main Title & Subheading
st.markdown('<h1>🎯 VeriRank <span class="gradient-text">AI v3.5</span></h1>', unsafe_allow_html=True)
st.subheader("Enterprise Local SEO Review Agent")
st.write("Convert raw customer feedback (Roman Urdu, Pashto, or English) into genuine, keyword-rich Google Reviews optimized for Local Google Maps ranking.")

st.write("---")

# Sidebar Configuration for API Key
st.sidebar.markdown("### 🔑 Authentication")
env_api_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Gemini API Key:",
    value=env_api_key if env_api_key else "",
    type="password",
    help="Enter your Gemini API key or save it in a .env file as GEMINI_API_KEY."
)

if not api_key:
    st.info("Aage barhne ke liye sidebar mein Gemini API Key darj karein.", icon="🔑")
    st.stop()

# Form UI
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown("### 🏬 Business Context")

shop_name = st.text_input("Business Name / Dukan Ka Naam:", placeholder="Eg: Bilal Laptops Peshawar")
category = st.text_input("Product Category / Service:", placeholder="Eg: Core i7 Laptops, Wholesale Photocopiers")

st.markdown("### 🧑‍💻 Customer Feedback")
user_input = st.text_area(
    "Customer feedback / comments (Roman Urdu, Pashto mix, or English):",
    placeholder="Eg: hum shopkeeper ko bahuth daad day rahay hai laptop custom build kia tha, pricing reasonable hai, gul haji plaza me best hai..."
)
st.markdown('</div>', unsafe_allow_html=True)

# Strict System Instructions for Local SEO (targeting Peshawar/Gul Haji Plaza tech hubs and Roman Urdu/Pashto-mix translation)
SYSTEM_INSTRUCTION = f"""
You are "VeriRank AI v3.5", an elite Enterprise Local SEO Architect. Your goal is to transform informal, raw customer feedback (often provided in Roman Urdu, Pashto-mix, or simple English) into a professional, engaging, and keyword-rich English Google Review.

TARGET BUSINESS & GEOGRAPHY:
- Target Business Name: {shop_name if shop_name else "the shop"}
- Product Category: {category if category else "electronics/laptops"}
- Target Location Focus: Peshawar tech hubs, particularly Gul Haji Plaza, University Road Peshawar, and surrounding local markets.

STRICT COMPLIANCE DIRECTIVES:
1. ZERO HALLUCINATION: Depend strictly on facts provided by the customer. If they highlight any issues or neutral points, do not hide them; represent them constructively.
2. NATURAL SEO INJECTION: Weave in high-intent keywords naturally (e.g., "best laptop shop in Peshawar", "Gul Haji Plaza laptop prices", "trusted computer dealer in Peshawar").
3. OUTPUT FORMAT: Return ONLY the final optimized review text. Do not include markdown headers, quotes, introductory phrases, or extra notes.
"""

if st.button("Generate Optimized SEO Review 🚀"):
    if not user_input.strip():
        st.warning("Meharbani kar ke customer ka feedback type karein.")
    elif not shop_name.strip() or not category.strip():
        st.warning("Meharbani kar ke Business Name aur Product Category enter karein.")
    else:
        with st.spinner("Processing feedback through VeriRank Multi-Engine Pipeline..."):
            
            response = None
            last_error = ""
            # Fallback models as requested (including the 'gemiash' test and preview models)
            models_to_try = ["gemiash", "gemini-3-flash-preview", "gemini-1.5-flash"]
            successful_model = None
            
            # Setup GenAI Client
            try:
                client = genai.Client(api_key=api_key)
                
                # Try models sequentially
                for model_name in models_to_try:
                    try:
                        st.caption(f"Trying model target: `{model_name}`...")
                        res = client.models.generate_content(
                            model=model_name,
                            contents=user_input,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.3
                            )
                        )
                        if res and res.text:
                            response = res
                            successful_model = model_name
                            break
                    except Exception as model_err:
                        last_error = str(model_err)
                        st.caption(f"⚠️ Model `{model_name}` failed: {last_error[:100]}...")
                        continue
                        
            except Exception as client_err:
                st.error(f"Client setup failed: {client_err}")
            
            # Final output display
            if response and response.text:
                st.success(f"Review generated successfully using `{successful_model}`! 🎉")
                st.markdown("#### 📋 Final Optimized Review (Copy this):")
                st.code(response.text.strip(), language="")
                st.markdown("💡 **Next Step:** Customer can copy this text and paste it directly onto your Google Business Profile.")
            else:
                st.error("Model fallback pipeline failed. Please verify your API Key and network connection.")
                with st.expander("Technical Error Log"):
                    st.write(last_error)

st.write("---")
st.caption("VeriRank AI v3.5 | Powered by Google GenAI 2026 SDK | Peshawar Enterprise Edition")