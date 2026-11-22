import streamlit as st
import json
import os
import math
from datetime import datetime

# -------------------------------------------------
# ADMIN CREDENTIALS (Yahan se apna username/password badal sakte hain)
# -------------------------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"

DB_FILE = "drugxpert_db.json"
# =========================================================
# DRUGXPERT AI - BRANDING & ABOUT DATA
# =========================================================

BRAND_NAME = "DrugXpert AI"
WELCOME_TEXT = "Welcome to DrugXpert AI"

ABOUT_DEFAULT = {
    "software_name": "DrugXpert AI",
    "description": (
        "DrugXpert AI is an integrated computational platform designed "
        "for drug–excipient compatibility assessment, solubility prediction, "
        "Hansen Solubility Parameter analysis and rational excipient selection."
    ),
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "developer_bio": (
        "Researcher working in pharmaceutics, computational drug delivery, "
        "AI/ML-assisted excipient selection and cyclodextrin-based drug delivery systems."
    ),
    "guide_name": "Guide Name",
    "guide_role": "Professor / Research Guide",
    "guide_bio": (
        "Research guide working in pharmaceutics, formulation development "
        "and advanced drug delivery research."
    )
}

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# DEFAULT DATABASE & STORAGE FUNCTIONS
# -------------------------------------------------
DEFAULT_DATA = {
    "title": "💊 DrugXpert AI",
    "subtitle": "Integrated Computational Platform for Drug–Excipient Compatibility, Solubility Prediction and Solvent Selection",
    "drugs": {
        "Deflazacort": {"dD": 18.6, "dP": 8.4, "dH": 9.2, "logP": 2.8, "mw": 441.5, "rot": 4, "arom": 0.19},
        "Artemether": {"dD": 17.4, "dP": 5.1, "dH": 6.8, "logP": 3.1, "mw": 298.4, "rot": 1, "arom": 0.00},
        "Curcumin": {"dD": 19.2, "dP": 9.8, "dH": 12.4, "logP": 3.2, "mw": 368.4, "rot": 8, "arom": 0.44}
    },
    "excipients": {
        "PVP K30": {"dD": 18.8, "dP": 10.2, "dH": 11.5, "solvents": ["Water", "Ethanol", "Methanol", "Dichloromethane"]},
        "Soluplus": {"dD": 18.1, "dP": 8.6, "dH": 9.8, "solvents": ["Ethanol", "Acetone", "Methanol", "Dimethylformamide"]},
        "PEG 6000": {"dD": 17.9, "dP": 9.1, "dH": 11.0, "solvents": ["Water", "Ethanol", "Chloroform", "Acetonitrile"]},
        "Poloxamer 188": {"dD": 17.5, "dP": 7.4, "dH": 9.5, "solvents": ["Water", "Ethanol", "Isopropanol"]},
        "Poloxamer 407": {"dD": 17.6, "dP": 7.2, "dH": 9.1, "solvents": ["Water", "Ethanol", "Methanol"]},
        "HPMC": {"dD": 18.4, "dP": 9.5, "dH": 13.2, "solvents": ["Water", "Ethanol-Water Mixture", "Dichloromethane-Methanol"]}
    },
    "logs": []
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_DATA))

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state.db = load_db()

if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.username = ""

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

db = st.session_state.db

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left,
        rgba(37,99,235,0.10),
        transparent 35%),
        linear-gradient(135deg, #F8FAFC 0%, #EEF4FF 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* DRUGXPERT AI BRANDING */

.dx-brand {
    text-align: center;
    padding: 18px 10px 8px 10px;
}

.dx-logo {
    width: 78px;
    height: 78px;
    margin: auto;
    border-radius: 22px;

    background:
        linear-gradient(135deg,
        #2563EB 0%,
        #06B6D4 50%,
        #7C3AED 100%);

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;
    font-size: 38px;
    font-weight: 900;

    box-shadow:
        0 12px 35px rgba(37,99,235,0.30);
}

.dx-brand-title {
    font-size: 38px;
    font-weight: 900;
    margin-top: 12px;

    background:
        linear-gradient(90deg,
        #1D4ED8,
        #0891B2,
        #7C3AED);

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.dx-brand-subtitle {
    color: #64748B;
    font-size: 15px;
    margin-top: 4px;
}

/* WELCOME */

.dx-welcome {
    position: relative;
    overflow: hidden;

    margin-top: 22px;
    padding: 38px 30px;

    border-radius: 26px;

    background:
        linear-gradient(
        135deg,
        rgba(15,23,42,0.98),
        rgba(30,64,175,0.96),
        rgba(8,145,178,0.94)
        );

    color: white;

    box-shadow:
        0 20px 50px rgba(15,23,42,0.20);
}

.dx-welcome h1 {
    font-size: 36px;
    margin: 0;
    font-weight: 900;
}

.dx-welcome p {
    font-size: 16px;
    opacity: 0.90;
    margin-top: 10px;
}

/* CARDS */

.dx-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(148,163,184,0.20);
    border-radius: 20px;
    padding: 24px;
    box

# -------------------------------------------------
# LOGIN SCREEN (IF NOT LOGGED IN)
# -------------------------------------------------
if st.session_state.role is None:
    st.markdown(f"""
    <div class="hero" style="text-align:center;">
        <h1>{db['title']}</h1>
        <p>{db['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        tab_part, tab_admin = st.tabs(["👤 Participant Login", "🛡️ Admin Login"])

        with tab_part:
            st.subheader("Enter as Participant")
            p_name = st.text_input("Your Full Name *", placeholder="e.g. Rahul Sharma")
            p_dept = st.text_input("Institution / Department (Optional)", placeholder="e.g. Pharmaceutics Research Lab")
            if st.button("Enter Software →", type="primary", use_container_width=True):
                if p_name.strip():
                    st.session_state.role = "participant"
                    st.session_state.username = p_name.strip()
                    db["logs"].insert(0, {
                        "name": p_name.strip(),
                        "dept": p_dept.strip() if p_dept.strip() else "General",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_db(db)
                    st.rerun()
                else:
                    st.error("Please enter your name to continue.")

        with tab_admin:
            st.subheader("Administrator Control Login")
            a_user = st.text_input("Admin Username", placeholder="Enter admin username")
            a_pass = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
            if st.button("Login as Admin 🔒", type="primary", use_container_width=True):
                if a_user.strip() == ADMIN_USERNAME and a_pass == ADMIN_PASSWORD:
                    st.session_state.role = "admin"
                    st.session_state.username = f"Admin ({a_user.strip()})"
                    st.rerun()
                else:
                    st.error("❌ Invalid Admin Username or Password!")

    st.stop()

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
nav_options = [
    "Home",
    "HSP Compatibility",
    "AI/ML Solubility",
    "Solvent Lookup",
    "Integrated Screening"
]
if st.session_state.role == "admin":
    nav_options.append("⚙️ Admin Control Panel")

with st.sidebar:
    st.markdown(f"## {db['title']}")
    if st.session_state.role == "admin":
        st.success(f"🛡️ Logged in as: **{st.session_state.username}**")
    else:
        st.info(f"👤 Participant: **{st.session_state.username}**")

    st.markdown("---")

    selected_nav = st.radio(
        "Navigation",
        nav_options,
        index=nav_options.index(st.session_state.current_page) if st.session_state.current_page in nav_options else 0
    )
    if selected_nav != st.session_state.current_page:
        st.session_state.current_page = selected_nav
        st.rerun()

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.role = None
        st.session_state.username = ""
        st.session_state.current_page = "Home"
        st.rerun()

    st.caption("Computational Drug Formulation Platform")

page = st.session_state.current_page

# -------------------------------------------------
# 1. HOME PAGE
# -------------------------------------------------
if page == "Home":
    st.markdown(f"""
    <div class="hero">
        <h1>{db['title']}</h1>
        <p>{db['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Welcome to DrugXpert AI")
    st.write(
        "DrugXpert AI is designed to support rational drug formulation "
        "development using computational screening, molecular descriptors, "
        "machine learning and solvent compatibility analysis."
    )

    st.markdown("### 🔬 Three Core Modules")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>🧪 HSP Compatibility</h3>
            <p>Hansen Solubility Parameter based screening of drug–excipient compatibility using δD, δP, δH and Hansen distance (Ra).</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open HSP Compatibility →", use_container_width=True):
            st.session_state.current_page = "HSP Compatibility"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <h3>🤖 AI/ML Solubility</h3>
            <p>Molecular descriptor-based prediction of LogS and solubility for drug–excipient systems using machine learning models.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI/ML Solubility →", use_container_width=True):
            st.session_state.current_page = "AI/ML Solubility"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🧴 Solvent Lookup</h3>
            <p>Computational lookup and ranking of suitable solvents for selected polymers and excipients.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Solvent Lookup →", use_container_width=True):
            st.session_state.current_page = "Solvent Lookup"
            st.rerun()

    st.markdown("---")
    st.markdown("## 🔗 Integrated Screening")
    st.info(
        "Drug → Excipient → HSP Compatibility → Molecular Descriptor Analysis "
        "→ AI/ML Solubility Prediction → Solvent Selection → Final Recommendation"
    )
    if st.button("Launch Integrated Screening →", type="primary"):
        st.session_state.current_page = "Integrated Screening"
        st.rerun()

# -------------------------------------------------
# 2. HSP MODULE
# -------------------------------------------------
elif page == "HSP Compatibility":
    st.title("🧪 HSP Compatibility Screening")
    st.write("Screen drug–excipient compatibility using Hansen Solubility Parameters.")
    st.markdown("---")

    drug_list = ["Select drug"] + list(db["drugs"].keys())
    drug = st.selectbox("Select Drug", drug_list)

    if drug != "Select drug":
        d = db["drugs"][drug]
