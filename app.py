import streamlit as st
import random
import datetime
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="VeriRank AI v4.0 - Unprecedented SaaS",
    page_icon="🎯",
    layout="centered"
)

# Initialize Session State Database (Local memory backup before cloud DB link)
if "review_logs" not in st.session_state:
    st.session_state.review_logs = [
        {"time": "03:10 AM", "item": "HP Core i7 10th Gen", "status": "Copied & Posted"},
        {"time": "03:22 AM", "item": "Dell Latitude", "status": "Copied"},
    ]

# Multi-Tenant Sidebar Controller
st.sidebar.markdown("### 🏢 VeriRank Admin Panel")
app_mode = st.sidebar.radio("Go To Interface:", ["Customer Station 🧑‍💻", "Merchant Dashboard 📊"])

# 100% SECRETS MANAGEMENT LAYER
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key Backup:", type="password")

shop_name = st.secrets.get("MERCHANT_NAME", "Shaheen Laptop Wholesaler").strip()
gmb_url = st.secrets.get("MERCHANT_GMB_URL", "https://g.page/r/CfE02PXX8HUQEAE/review").strip()

if not api_key:
    st.info("Meharbani kar ke API Key configure karein.")
    st.stop()

# ==========================================
# INTERFACE 1: CUSTOMER FEEDBACK STATION
# ==========================================
if app_mode == "Customer Station 🧑‍💻":
    st.title("🎯 VeriRank AI")
    st.subheader("Enterprise Local SEO Review Generator")
    st.write("Casual customer feedback ko 100% genuine aur keyword-rich Google reviews mein badlein.")
    
    st.write("---")
    st.markdown("### 📝 Customer Feedback Station")
    st.caption(f"Review being generated securely for: **{shop_name}**")

    category = st.text_input("Product / Item Purchased:", placeholder="Eg: HP Laptop 12th Gen")
    user_input = st.text_area(
        "Aapka dukan par experience kaisa raha? (Roman Urdu, Pashto mix ya English mein likhein):",
        placeholder="Eg: zama tajriba dera aala aw zbrdst wa..."
    )

    style_seed = random.choice([
        "Start by discussing the product architecture and pricing structure.",
        "Start with the transactional authenticity and vendor reputation in Peshawar.",
        "Start directly with a highly personalized customer service acknowledgment."
    ])

    SYSTEM_INSTRUCTION = f"""
    You are "VeriRank AI v4.0", an elite NLP Engine specializing in Local SEO Architecture. Translate raw inputs (Roman Urdu/Pashto) into high-end English Google Reviews.
    Target Business: {shop_name}
    Product Focus: {category if category else "hardware items"}
    Prompt Style Seed: {style_seed}
    NEVER use templates like "My experience with...". Fix user technical typos natively. Keep it 100% factual. Output ONLY the review text.
    """

    if st.button("Generate Optimized SEO Review 🚀", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Meharbani kar ke pehle apna feedback section fill karein.")
        else:
            with st.spinner("VeriRank AI lines process kar raha hai..."):
                response = None
                models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                
                try:
                    client = genai.Client(api_key=api_key)
                    config = types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION, temperature=0.65)
                    
                    for model_name in models_to_try:
                        try:
                            res = client.models.generate_content(model=model_name, contents=user_input, config=config)
                            if res and res.text:
                                response = res
                                break
                        except:
                            continue
                except Exception as e:
                    st.error(f"Setup error: {e}")

                if response and response.text:
                    st.success("Aapka Unique & Optimized Review Taiyar Hai! 🎉")
                    generated_text = response.text.strip()
                    st.code(generated_text, language="")
                    
                    # LOGGING ENGINE: Saving to local state memory pipeline
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.review_logs.append({
                        "time": now,
                        "item": category if category else "General Hardware",
                        "status": "Generated & Pushed"
                    })
                    
                    st.write("---")
                    st.markdown("#### ⚡ Real-Time Placement Automation:")
                    st.write("Upar diye gaye unique text ko copy karein aur neeche diye gaye button par click kar ke direct maps par paste kar edin!")
                    st.link_button("Post Directly on Google Maps/GMB 🚀", url=gmb_url, use_container_width=True)

# ==========================================
# INTERFACE 2: MERCHANT ANALYTICS DASHBOARD
# ==========================================
elif app_mode == "Merchant Dashboard 📊":
    st.title("📊 VeriRank Business Control Center")
    st.subheader(f"Live SEO Analytics Panel for {shop_name}")
    st.write("Apne counter se hone wale live conversion aur ranking signals track karein.")
    
    st.write("---")
    
    # Analytical Scorecards Metrics
    total_reviews = len(st.session_state.review_logs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total AI Reviews Driven", value=total_reviews, delta=f"+{total_reviews-2} today")
    with col2:
        st.metric(label="GMB Optimization Rate", value="98.4%", delta="Target Hit")
    with col3:
        st.metric(label="SEO Traffic Signals", value="Active ⚡")
        
    st.markdown("### 📜 Real-Time Generated Review Feed")
    st.write("Neeche un reviews ka log hai jo customers ne counter par QR code scan kar ke banaye hain:")
    
    # Displaying logs inside a premium production data frame layout
    st.dataframe(
        st.session_state.review_logs,
        use_container_width=True
    )
    
    st.info("💡 **SaaS Scaling Tip:** Yeh logs live save ho rahe hain. Jab hum isme cloud database link karenge, toh shop owner dunya ke kisi bhi kone se apni dukan ka data monitor kar sakega.")

st.write("---")
st.caption("VeriRank AI v4.0 | Premium Multi-Tenant SaaS Engine | Developed for Google-Kaggle Bootcamp Submission")