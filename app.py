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

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 32px 32px 28px 32px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0b4f6c, #087f8c);
    color: white;
    margin-bottom: 22px;
}
.hero h1 {
    font-size: 38px;
    margin-bottom: 8px;
}
.hero p {
    font-size: 17px;
    margin-bottom: 0;
}
.card {
    padding: 22px;
    border-radius: 16px;
    background-color: white;
    border: 1px solid #e5e9f0;
    min-height: 185px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.card h3 {
    color: #0b4f6c;
    margin-bottom: 8px;
}
.card p {
    color: #555;
    line-height: 1.5;
}
.footer {
    text-align: center;
    color: #777;
    padding: 30px 0 10px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

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
