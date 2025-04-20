import streamlit as st
import pandas as pd
import ast
import os

# ------------------ Page Configuration ------------------
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide", page_icon="🔍")

# ------------------ Session State Setup ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "users" not in st.session_state:
    st.session_state.users = {
        "gokul@example.com": "test123",
        "user2@example.com": "pass456"
    }
if "page" not in st.session_state:
    st.session_state.page = "login"
if "forgot_password_email" not in st.session_state:
    st.session_state.forgot_password_email = ""

# ------------------ Logo Check ------------------
logo_path = "logo.png"
logo_exists = os.path.exists(logo_path)

# ------------------ Global Professional CSS ------------------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Proxima Nova', 'Helvetica Neue', sans-serif;
    }

    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(to right, #56C5FF, #3BADE0);
        color: white;
        padding: 0.6em 1.4em;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(86, 197, 255, 0.3);
    }

    .stButton > button:hover {
        transform: scale(1.03);
        background: linear-gradient(to right, #3BADE0, #56C5FF);
    }

    .stTextInput input,
    .stSelectbox div div,
    .stSlider > div > div {
        border-radius: 10px;
        padding: 0.2em;
    }

    /* 🔥 Dropdown fix: adjust font and background */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e1e1e !important; /* Dark background */
        color: #ffffff !important; /* White text */
        border-radius: 10px;
    }

    .stSelectbox div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    h1, h2, h3 {
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Login Page ------------------
def login_page():
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        if logo_exists:
            st.image(logo_path, use_container_width=True)
        st.markdown("<h2 style='color:#56C5FF; text-align:center;'>🔐 Login to SHL Recommender</h2>", unsafe_allow_html=True)
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Password", type="password", key="login_password")

        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")

        col_login, col_forgot = st.columns([1, 1])
        with col_login:
            if st.button("Don't have an account? Sign up here"):
                st.session_state.page = "signup"
                st.rerun()
        with col_forgot:
            if st.button("Forgot Password?"):
                st.session_state.forgot_password_email = email
                st.info("📨 Simulated: A password reset link has been sent.")

# ------------------ Signup Page ------------------
def signup_page():
    if logo_exists:
        st.image(logo_path, use_container_width=True)
    st.markdown("<h2 style='color:#56C5FF;'>📝 Create Your Account</h2>", unsafe_allow_html=True)
    email = st.text_input("📧 Email", key="signup_email")
    password = st.text_input("🔑 Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if email in st.session_state.users:
            st.warning("⚠️ Email already exists. Please log in.")
        else:
            st.session_state.users[email] = password
            st.success("✅ Signup successful! Please log in.")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Already have an account? Login here"):
        st.session_state.page = "login"
        st.rerun()

# ------------------ Recommender Page ------------------
def recommender_page():
    try:
        # ✅ FIX: Read CSV with correct encoding to prevent UnicodeDecodeError
        df = pd.read_csv("shl_product_catalog.csv", encoding="latin1")
        df['ApplicableRoles'] = df['ApplicableRoles'].apply(ast.literal_eval)
    except Exception as e:
        st.error("❌ Failed to load assessment catalog.")
        st.code(str(e))
        return

    if logo_exists:
        st.sidebar.image(logo_path, use_container_width=True)

    # Theme
    theme = st.sidebar.radio("🌓 Select Theme", ["Light", "Dark"])
    bg_color, text_color = ("#F7FBFE", "#000") if theme == "Light" else ("#0E1117", "#FFF")
    st.markdown(f"""<style>.main {{ background-color: {bg_color}; color: {text_color}; }}</style>""", unsafe_allow_html=True)

    # Main UI
    st.markdown("<h1 style='color:#56C5FF;'>🔍 SHL Assessment Recommendation Engine</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px;'>Welcome, <b>{st.session_state.email}</b>! Get your personalized assessment recommendations below.</p>", unsafe_allow_html=True)

    # Sidebar Filters
    st.sidebar.header("🎛️ Customize Filters")
    job_role_input = st.sidebar.text_input("💼 Enter Job Role", value="Software Engineer")
    difficulty_input = st.sidebar.selectbox("📊 Select Difficulty", ["Any", "Easy", "Medium", "Hard"])
    type_input = st.sidebar.selectbox("🧠 Select Assessment Type", ["Any", "Cognitive", "Personality", "Behavioral", "Situational", "Technical"])
    top_n = st.sidebar.slider("📌 Number of Recommendations", 1, 10, 5)

    # Recommendation Logic
    def recommend_assessments(job_role, top_n=5, difficulty=None, assess_type=None):
        filtered_df = df[df['ApplicableRoles'].apply(lambda roles: any(job_role.lower() in r.lower() for r in roles))]
        if difficulty != "Any":
            filtered_df = filtered_df[filtered_df['DifficultyLevel'] == difficulty]
        if assess_type != "Any":
            filtered_df = filtered_df[filtered_df['AssessmentType'] == assess_type]
        return filtered_df.head(top_n)

    # Generate Recommendations
    if st.sidebar.button("🚀 Get Recommendations"):
        recs = recommend_assessments(job_role_input, top_n, difficulty_input, type_input)
        if recs.empty:
            st.warning(f"😕 No recommendations found for role: **{job_role_input}**")
        else:
            st.success(f"✅ Top {top_n} Recommendations for '**{job_role_input}**':")
            st.dataframe(recs[['AssessmentName', 'AssessmentType', 'DifficultyLevel']])

            # CSV Download
            csv = recs.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download as CSV", csv, file_name="recommendations.csv", mime="text/csv")

            # PDF Download
            try:
                import pdfkit
                config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')  # Change this if needed
                html = recs[['AssessmentName', 'AssessmentType', 'DifficultyLevel']].to_html(index=False)
                pdfkit.from_string(html, "recommendations.pdf", configuration=config)
                with open("recommendations.pdf", "rb") as f:
                    st.download_button("📄 Download as PDF", f, file_name="recommendations.pdf", mime="application/pdf")
            except Exception as e:
                st.info("ℹ️ PDF export requires `pdfkit` and `wkhtmltopdf`. Please ensure both are installed.")
                st.code(str(e))

    st.markdown("<hr style='margin-top: 3em;'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:gray;'>✨ Designed by <b>Gokul Gopakumar</b> | SHL UI Pro Edition</div>", unsafe_allow_html=True)

# ------------------ Page Routing ------------------
if not st.session_state.logged_in:
    login_page() if st.session_state.page == "login" else signup_page()
else:
    recommender_page()
