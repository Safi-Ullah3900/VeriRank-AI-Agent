import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="VeriRank AI v3.6 - Enterprise Local SEO",
    page_icon="🎯",
    layout="centered"
)

# App Title & Branding
st.title("🎯 VeriRank AI")
st.subheader("Smart Local SEO Review Agent")
st.write("Casual customer feedback ko 100% genuine aur keyword-rich Google reviews mein badlein.")

# DYNAMIC SECRETS MANAGER: Baar-baar key daalne ki janjhat khatam!
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Agar local laptop par chalayein toh sidebar backup dikhega
    api_key = st.sidebar.text_input("Gemini API Key darj karein (Local Backup):", type="password")

if not api_key:
    st.info("Meharbani kar ke Streamlit Cloud par Secrets set karein ya local backup key lagayein.", icon="🔑")
    st.stop()

# User Interface (Advanced SaaS Inputs)
st.write("---")
st.markdown("### 🏬 Business & Product Context")

col1, col2 = st.columns(2)
with col1:
    shop_name = st.text_input("Dukan / Business Ka Naam:", placeholder="Eg: Bilal Laptops")
with col2:
    category = st.text_input("Product / Service Category:", placeholder="Eg: Core i7 Laptops")

st.markdown("### 🧑‍💻 Customer Feedback Section")
user_input = st.text_area(
    "Aapka shop par experience kaisa raha? (Roman Urdu, Pashto mix ya English mein likhein):",
    placeholder="Eg: hum shopkeeper ko bahuth daad day rahay hai really appreciate him..."
)

# System Instructions Matrix
SYSTEM_INSTRUCTION = f"""
You are "VeriRank AI v3.6", an elite Enterprise Local SEO Architect. Your objective is to transform raw customer feedback into professional, keyword-rich English Google Reviews.

CONTEXT FOR THIS REVIEW:
- Target Business Name: {shop_name if shop_name else "the store"}
- Product/Service Category: {category if category else "products and services"}

STRICT ETHICAL GUARDRAILS:
1. ZERO HALLUCINATION: Rely ONLY on facts provided in the user's feedback. If they mention a critique, convert it into a constructive, honest point. Authenticity ranks higher on Google.
2. NATURAL SEO INJECTION: Weave in high-intent local search keywords naturally based on the category and location (e.g., "best laptop shop in Peshawar", "wholesale photocopier machine prices", "Gul Haji Plaza tech market").

OUTPUT FORMAT:
Return ONLY the final review text. No markdown explanations, no notes.
"""

if st.button("Generate Optimized SEO Review 🚀", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Meharbani kar ke pehle customer ka raw feedback yahan likhein.")
    elif shop_name.strip() == "" or category.strip() == "":
        st.warning("Meharbani kar ke Business Name aur Category zaroor darj karein.")
    else:
        with st.spinner("VeriRank AI backend tunnel se connect ho raha hai..."):
            
            response = None
            last_error = ""
            models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3-flash-preview", "gemini-1.5-flash"]
            
            try:
                client = genai.Client(api_key=api_key)
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3
                )
                
                # Resilient Fallback Loop
                for model_name in models_to_try:
                    try:
                        res = client.models.generate_content(
                            model=model_name,
                            contents=user_input,
                            config=config
                        )
                        if res and res.text:
                            response = res
                            break
                    except Exception as model_err:
                        last_error = str(model_err)
                        continue
                        
            except Exception as client_err:
                st.error(f"Client setup error: {client_err}")

            # Final Display Layout
            if response and response.text:
                st.success("Aapka Genuine & Optimized Review Taiyar Hai! 🎉")
                st.markdown("#### 📋 Neeche diye gaye review ko Copy karein:")
                st.code(response.text.strip(), language="")
                st.markdown("💡 **Next Step:** Ab customer is text ko copy kar ke seedha aapke Google Business Profile par paste kar sakta hai!")
            else:
                st.error("Server endpoints par temporary load hai. Dubara koshish karein.")

st.write("---")
st.caption("VeriRank AI v3.6 | Powered by Secure Cloud Secrets Pipeline | Google-Kaggle Bootcamp Edition")