import streamlit as st
import json
import os
import base64
from datetime import datetime

# =========================================================
# DRUGXPERT AI - ADMIN & CONTENT MANAGEMENT MODULE
# =========================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"

DB_FILE = "drugxpert_db.json"
CONTENT_FILE = "site_content.json"
ASSET_DIR = "assets"

# ---------------------------------------------------------
# DEFAULT DATABASE
# ---------------------------------------------------------

DEFAULT_DB = {
    "custom_drugs": {},
    "custom_excipients": {},
    "logs": []
}

# ---------------------------------------------------------
# DEFAULT WEBSITE CONTENT
# ---------------------------------------------------------

DEFAULT_CONTENT = {
    "welcome_title": "WELCOME TO DRUGXPERT AI",
    "welcome_subtitle": (
        "AI-Assisted Computational Platform for Rational "
        "Drug Formulation Development"
    ),
    "about_title": "About DrugXpert AI",
    "about_text": (
        "DrugXpert AI is an integrated computational platform "
        "designed to support rational drug formulation development "
        "through computational screening, molecular descriptors, "
        "machine learning, Hansen Solubility Parameter analysis, "
        "solubility prediction and solvent compatibility analysis."
    ),
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Researcher",
    "developer_bio": (
        "Researcher working in pharmaceutics, computational drug "
        "formulation, AI/ML-assisted excipient selection and "
        "cyclodextrin-based drug delivery systems."
    ),
    "guide_name": "Guide Name",
    "guide_role": "Research Guide / Professor",
    "guide_bio": (
        "Research guide providing scientific guidance and supervision "
        "for computational pharmaceutics and drug delivery research."
    ),
    "software_features": (
        "HSP Compatibility\n"
        "AI/ML Solubility Prediction\n"
        "Solvent Lookup\n"
        "Integrated Computational Screening"
    ),
    "logo_file": "",
    "developer_photo": "",
    "guide_photo": ""
}


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def load_custom_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = json.loads(json.dumps(DEFAULT_DB))
            if isinstance(data, dict):
                merged.update(data)
            return merged
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_DB))


def save_custom_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================================================
# CONTENT FUNCTIONS
# =========================================================

def load_site_content():
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = DEFAULT_CONTENT.copy()
            if isinstance(data, dict):
                merged.update(data)
            return merged
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_CONTENT))


def save_site_content(data):
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================================================
# FILE / IMAGE FUNCTIONS
# =========================================================

def save_uploaded_file(uploaded_file, filename):
    if uploaded_file is None:
        return ""
    os.makedirs(ASSET_DIR, exist_ok=True)
    file_path = os.path.join(ASSET_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def image_to_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        return ""
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = image_path.lower().split(".")[-1]
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return ""


# =========================================================
# PREMIUM DRUGXPERT AI THEME
# =========================================================

def apply_premium_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background:
            radial-gradient(circle at 10% 10%, rgba(0, 188, 212, 0.10), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(255, 80, 120, 0.08), transparent 30%),
            linear-gradient(135deg, #07121f 0%, #0a1928 50%, #07111d 100%);
            color: #f5f9ff;
        }
        .main .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #06101c 0%, #091c2b 100%);
            border-right: 1px solid rgba(0, 210, 230, 0.18);
        }
        section[data-testid="stSidebar"] * {
            color: #eaf7ff !important;
        }
        h1, h2, h3 {
            color: #ffffff !important;
            letter-spacing: -0.3px;
        }
        .dx-card, .card {
            background: linear-gradient(145deg, rgba(17, 38, 58, 0.92), rgba(7, 22, 36, 0.88));
            border: 1px solid rgba(65, 220, 235, 0.18);
            border-radius: 20px;
            padding: 25px;
            margin: 12px 0;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.28);
        }
        .profile-card {
            background: linear-gradient(145deg, rgba(17, 38, 58, 0.92), rgba(7, 22, 36, 0.88));
            border: 1px solid rgba(65, 220, 235, 0.22);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.28);
        }
        .dx-hero {
            padding: 45px 35px;
            border-radius: 28px;
            text-align: center;
            background:
            radial-gradient(circle at 20% 20%, rgba(0, 210, 230, 0.18), transparent 35%),
            linear-gradient(135deg, rgba(8, 48, 72, 0.96), rgba(12, 28, 47, 0.96));
            border: 1px solid rgba(50, 220, 235, 0.25);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
        }
        .dx-hero-title {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #55e6ee, #ff7c96);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .dx-hero-subtitle {
            color: #b9d9e8;
            font-size: 17px;
            line-height: 1.6;
        }
        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid rgba(50, 220, 235, 0.30) !important;
            background: linear-gradient(135deg, #087f91, #0aa6ad) !important;
            color: white !important;
            font-weight: 700 !important;
            min-height: 45px;
            transition: 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(0, 200, 220, 0.25);
        }
        input, textarea {
            background-color: rgba(5, 17, 29, 0.85) !important;
            color: white !important;
            border: 1px solid rgba(100, 210, 230, 0.20) !important;
            border-radius: 10px !important;
        }
        div[data-testid="stExpander"] {
            background: rgba(8, 25, 40, 0.78);
            border: 1px solid rgba(80, 210, 230, 0.16);
            border-radius: 15px;
        }
        button[data-baseweb="tab"] {
            color: #a9cbd8 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #55e6ee !important;
        }
        div[data-testid="stMetric"] {
            background: rgba(12, 35, 52, 0.8);
            border: 1px solid rgba(50, 220, 235, 0.15);
            padding: 15px;
            border-radius: 15px;
        }
        .dx-watermark {
            position: fixed;
            bottom: 25px;
            right: 30px;
            font-size: 52px;
            font-weight: 900;
            color: rgba(80, 220, 235, 0.035);
            transform: rotate(-12deg);
            pointer-events: none;
            z-index: 0;
            letter-spacing: 3px;
        }
        </style>
        <div class="dx-watermark">DRUGXPERT AI</div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INITIALIZE AUTHENTICATION
# =========================================================

def init_auth_and_sidebar():
    apply_premium_theme()

    if "custom_db" not in st.session_state:
        st.session_state.custom_db = load_custom_db()

    if "site_content" not in st.session_state:
        st.session_state.site_content = load_site_content()

    if "role" not in st.session_state:
        st.session_state.role = None
        st.session_state.username = ""

    db = st.session_state.custom_db
    content = st.session_state.site_content

    if st.session_state.role is None:
        logo_b64 = image_to_base64(content.get("logo_file", ""))
        logo_tag = (
            f'<img src="{logo_b64}" style="width:90px;height:90px;object-fit:contain;margin-bottom:10px;">'
            if logo_b64 else ""
        )
        st.markdown(
            f"""
            <div class="dx-hero">
                {logo_tag}
