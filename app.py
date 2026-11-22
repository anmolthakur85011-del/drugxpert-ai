import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"
DB_FILE = "drugxpert_db.json"
CONTENT_FILE = "site_content.json"
ASSET_DIR = "assets"

DEFAULT_DB = {
    "custom_drugs": {},
    "custom_excipients": {},
    "logs": []
}

DEFAULT_CONTENT = {
    "welcome_title": "WELCOME TO DRUGXPERT AI",
    "welcome_subtitle": "AI-Assisted Computational Platform for Rational Drug Formulation Development",
    "about_title": "About DrugXpert AI",
    "about_text": "DrugXpert AI is an integrated computational platform designed to support rational drug formulation development through computational screening, molecular descriptors, machine learning, Hansen Solubility Parameter analysis, solubility prediction and solvent compatibility analysis.",
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Researcher",
    "developer_bio": "Researcher working in pharmaceutics, computational drug formulation, AI/ML-assisted excipient selection and cyclodextrin-based drug delivery systems.",
    "guide_name": "Guide Name",
    "guide_role": "Research Guide / Professor",
    "guide_bio": "Research guide providing scientific guidance and supervision for computational pharmaceutics and drug delivery research.",
    "software_features": "HSP Compatibility\nAI/ML Solubility Prediction\nSolvent Lookup\nIntegrated Computational Screening",
    "logo_file": "",
    "developer_photo": "",
    "guide_photo": ""
}

DEFAULT_DRUGS = {
    "Deflazacort": {"dD": 18.6, "dP": 8.4, "dH": 9.2, "logP": 2.8, "mw": 441.5, "rot": 4, "arom": 0.19},
    "Artemether": {"dD": 17.4, "dP": 5.1, "dH": 6.8, "logP": 3.1, "mw": 298.4, "rot": 1, "arom": 0.00},
    "Curcumin": {"dD": 19.2, "dP": 9.8, "dH": 12.4, "logP": 3.2, "mw": 368.4, "rot": 8, "arom": 0.44}
}

DEFAULT_EXCIPIENTS = {
    "PVP K30": {"dD": 18.8, "dP": 10.2, "dH": 11.5, "solvents": ["Water", "Ethanol", "Methanol", "Dichloromethane"]},
    "Soluplus": {"dD": 18.1, "dP": 8.6, "dH": 9.8, "solvents": ["Ethanol", "Acetone", "Methanol", "Dimethylformamide"]},
    "PEG 6000": {"dD": 17.9, "dP": 9.1, "dH": 11.0, "solvents": ["Water", "Ethanol", "Chloroform", "Acetonitrile"]},
    "Poloxamer 188": {"dD": 17.5, "dP": 7.4, "dH": 9.5, "solvents": ["Water", "Ethanol", "Isopropanol"]},
    "Poloxamer 407": {"dD": 17.6, "dP": 7.2, "dH": 9.1, "solvents": ["Water", "Ethanol", "Methanol"]},
    "HPMC": {"dD": 18.4, "dP": 9.5, "dH": 13.2, "solvents": ["Water", "Ethanol-Water Mixture", "Dichloromethane-Methanol"]}
}


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


def image_html(data_uri, width=120, height=120):
    if not data_uri:
        return ""
    return (
        f'<img src="{data_uri}" style="width:{width}px;height:{height}px;'
        f'object-fit:cover;border-radius:50%;border:4px solid white;'
        f'box-shadow:0 8px 25px rgba(15,23,42,.18);margin-bottom:10px;">'
    )


def hsp_distance(d1, d2):
    return math.sqrt(
        4 * (d1["dD"] - d2["dD"]) ** 2
        + (d1["dP"] - d2["dP"]) ** 2
        + (d1["dH"] - d2["dH"]) ** 2
    )


def compatibility_label(ra):
    if ra <= 3:
        return "Excellent Compatibility"
    elif ra <= 5:
        return "Good Compatibility"
    elif ra <= 7:
        return "Moderate Compatibility"
    else:
        return "Poor Compatibility"


def screening_log_s(drug, ra):
    base = 1.0 / (1.0 + ra)
    return round(-2.0 + (base * 4.0), 3)


def apply_premium_theme():
    css = (
        "<style>"
        ".stApp { background: linear-gradient(135deg, #07121f 0%, #0a1928 50%, #07111d 100%); color: #f5f9ff; }"
        ".main .block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem; }"
        "section[data-testid='stSidebar'] { background: linear-gradient(180deg, #06101c 0%, #091c2b 100%); border-right: 1px solid rgba(0, 210, 230, 0.18); }"
        "section[data-testid='stSidebar'] * { color: #eaf7ff !important; }"
        "h1, h2, h3 { color: #ffffff !important; letter-spacing: -0.3px; }"
        ".dx-card, .card { background: linear-gradient(145deg, rgba(17, 38, 58, 0.92), rgba(7, 22, 36, 0.88)); border: 1px solid rgba(65, 220, 235, 0.18); border-radius: 20px; padding: 25px; margin: 12px 0; box-shadow: 0 15px 40px rgba(0, 0, 0, 0.28); }"
        ".profile-card { background: linear-gradient(145deg, rgba(17, 38, 58, 0.92), rgba(7, 22, 36, 0.88)); border: 1px solid rgba(65, 220, 235, 0.22); border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 15px 40px rgba(0, 0, 0, 0.28); }"
        ".dx-hero { padding: 45px 35px; border-radius: 28px; text-align: center; background: linear-gradient(135deg, rgba(8, 48, 72, 0.96), rgba(12, 28, 47, 0.96)); border: 1px solid rgba(50, 220, 235, 0.25); box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35); }"
        ".dx-hero-title { font-size: 42px; font-weight: 800; background: linear-gradient(90deg, #ffffff, #55e6ee, #ff7c96); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }"
        ".dx-hero-subtitle { color: #b9d9e8; font-size: 17px; line-height: 1.6; }"
        ".stButton > button { border-radius: 12px !important; border: 1px solid rgba(50, 220, 235, 0.30) !important; background: linear-gradient(135deg, #087f91, #0aa6ad) !important; color: white !important; font-weight: 700 !important; min-height: 45px; }"
        "input, textarea { background-color: rgba(5, 17, 29, 0.85) !important; color: white !important; border: 1px solid rgba(100, 210, 230, 0.20) !important; border-radius: 10px !important; }"
        "div[data-testid='stMetric'] { background: rgba(12, 35, 52, 0.8); border: 1px solid rgba(50, 220, 235, 0.15); padding: 15px; border-radius: 15px; }"
        ".dx-watermark { position: fixed; bottom: 25px; right: 30px; font-size: 52px; font-weight: 900; color: rgba(80, 220, 235, 0.035); transform: rotate(-12deg); pointer-events: none; z-index: 0; letter-spacing: 3px; }"
        "</style><div class='dx-watermark'>DRUGXPERT AI</div>"
    )
    st.markdown(css, unsafe_allow_html=True)


apply_premium_theme()

if "custom_db" not in st.session_state:
    st.session_state.custom_db = load_custom_db()
if "site_content" not in st.session_state:
    st.session_state.site_content = load_site_content()
if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.username = ""

custom_db = st.session_state.custom_db
content = st.session_state.site_content

if st.session_state.role is None:
    logo_b64 = image_to_base64(content.get("logo_file", ""))
    logo_tag = f'<img src="{logo_b64}" style="width:90px;height:90px;object-fit:contain;margin-bottom:10px;">' if logo_b64 else ""
    st.markdown(
        f'<div class="dx-hero">{logo_tag}'
        f'<div class="dx-hero-title">{content.get("welcome_title", "WELCOME TO DRUGXPERT AI")}</div>'
        f'<div class="dx-hero-subtitle">{content.get("welcome_subtitle", "")}</div></div>',
        unsafe_allow_html=True
    )
    st.write("")
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        t1, t2 = st.tabs(["👤 Participant Login", "🛡️ Admin Login"])
        with t1:
            p_name = st.text_input("Enter Your Full Name *", placeholder="e.g. Rahul Sharma")
            p_dept = st.text_input("Department / Lab (Optional)", placeholder="e.g. Pharmaceutics")
            if st.button("Enter Software →", type="primary", use_container_width=True):
                if p_name.strip():
                    st.session_state.role = "participant"
                    st.session_state.username = p_name.strip()
                    custom_db["logs"].insert(0, {
                        "Name": p_name.strip(),
                        "Department": p_dept.strip() or "General",
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_custom_db(custom_db)
                    st.rerun()
                else:
                    st.error("Please enter your name!")
        with t2:
