import streamlit as st
import random
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="VeriRank AI v3.9 - Enterprise SaaS Edition",
    page_icon="🎯",
    layout="centered"
)

# App Title & Branding
st.title("🎯 VeriRank AI")
st.subheader("Enterprise Local SEO Review Generator")
st.write("Casual customer feedback ko 100% genuine aur keyword-rich Google reviews mein badlein.")

# 100% B2B SAAS SECRETS MANAGEMENT LAYER
# Hiding core configurations from end-users entirely
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("🛑 **Configuration Error:** API Key missing hai backend secrets mein.")
    st.stop()

# Auto-locking merchant profiles natively from cloud environment settings
shop_name = st.secrets.get("MERCHANT_NAME", "Shaheen Laptop Wholesaler").strip()
gmb_url = st.secrets.get("MERCHANT_GMB_URL", "https://g.page/r/CfE02PXX8HUQEAE/review").strip()

# User Interface (Ultra Clean Customer-First Layout)
st.write("---")
st.markdown("### 📝 Customer Feedback Station")
st.caption(f"Review being generated securely for: **{shop_name}**")

# Only dynamic inputs relevant to the walk-in consumer are exposed
category = st.text_input("Product / Item Purchased:", placeholder="Eg: HP EliteBook Core i7, Dell Laptop")

user_input = st.text_area(
    "Aapka dukan par experience kaisa raha? (Roman Urdu, Pashto mix ya English mein likhein):",
    placeholder="Eg: bahuth hi barhia experience raha, pricing achi thi..."
)

# ADVANCED NLP STRUCTURAL VARIATION ENGINE (Breaking the AI footprint)
# Generating a runtime random seed to shuffle text generation patterns dynamically
style_seed = random.choice([
    "Start by discussing the product architecture and pricing structure.",
    "Start with the transactional authenticity and vendor reputation in Peshawar.",
    "Start directly with a highly personalized customer service acknowledgment."
])

SYSTEM_INSTRUCTION = f"""
You are "VeriRank AI v3.9", an advanced NLP Engine specializing in Local SEO Architecture. Your objective is to translate casual, raw customer feedback into professional, natural English Google Reviews.

TARGET MERCHANT DATA:
- Business Name: {shop_name}
- Specific Product Focus: {category if category else "high-quality computers and laptops"}
- Runtime Prompt Seed Structure: {style_seed}

STRICT NLP ANTI-SPAM & REPETITION BAN RULES:
1. NEVER start the review with generic template structures like "My experience with...", "I recently bought...", or "Highly recommend this place". 
2. SYNONYM DIVERSITY: Actively cycle between different high-level vocabularies. Replace overused terms like "excellent" or "good" with words like "seamless dealing", "authentic setup", "competitive market rates", "robust inventory infrastructure".
3. TYPO CORRECTION CORRIDOR: Autonomously detect and correct technical user typos (e.g., if user inputs "cope i8", elegantly transform it into realistic tech phrases like "Intel Core series setup" or "high-spec processing machine").
4. ZERO HALLUCINATION: Build the review solely upon the facts mentioned by the customer. Keep it 100% true to the operational context.

OUTPUT FORMAT:
Return ONLY the clean final review text. No formatting, no markdown headers, no introductory sentences.
"""

if st.button("Generate Optimized SEO Review 🚀", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Meharbani kar ke pehle apna feedback section fill karein.")
    else:
        with st.spinner("VeriRank AI dynamic pipelines par secure data processing chal rahi hai..."):
            
            response = None
            last_error = ""
            models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
            
            try:
                client = genai.Client(api_key=api_key)
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.65 # Slight increase to boost organic vocabulary variety
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
                st.success("Aapka Unique & Optimized Review Taiyar Hai! 🎉")
                
                generated_text = response.text.strip()
                st.code(generated_text, language="")
                
                # Direct GMB Pipeline Link Activation
                st.write("---")
                st.markdown("#### ⚡ Real-Time Placement Automation:")
                st.write("Upar diye gaye unique text ko copy karein aur neeche diye gaye button par click kar ke direct maps par paste kar dein!")
                st.link_button("Post Directly on Google Maps/GMB 🚀", url=gmb_url, use_container_width=True)
            else:
                st.error("Server endpoints par temporary load hai. Dubara koshish karein.")

st.write("---")
st.caption("VeriRank AI v3.9 | Pure SaaS Architectural Edition | Developed for Google-Kaggle Bootcamp Submission")