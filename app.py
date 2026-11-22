import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

st.set_page_config(page_title="DrugXpert AI", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"
DB_FILE = "drugxpert_db.json"
CONTENT_FILE = "site_content.json"
ASSET_DIR = "assets"

DEFAULT_DB = {"custom_drugs": {}, "custom_excipients": {}, "logs": []}

DEFAULT_CONTENT = {
    "welcome_title": "WELCOME TO DRUGXPERT AI",
    "welcome_subtitle": "Integrated Computational Platform for Drug-Excipient Compatibility, Solubility Prediction and Solvent Selection",
    "about_title": "About DrugXpert AI",
    "about_text": "DrugXpert AI is an integrated computational platform designed for drug-excipient compatibility assessment, solubility prediction, Hansen Solubility Parameter analysis, AI/ML-assisted prediction, excipient selection, solvent selection, integrated screening and computational drug-delivery research.",
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "developer_bio": "Researcher working in pharmaceutics, computational drug formulation, AI/ML-assisted excipient selection and cyclodextrin-based drug delivery systems.",
    "developer_interests": "Computational Pharmaceutics, Hansen Solubility Parameters, AI/ML Drug Delivery, Cyclodextrins",
    "guide_name": "Guide Name",
    "guide_role": "Professor / Research Guide",
    "guide_bio": "Research guide providing scientific guidance and supervision for computational pharmaceutics and drug delivery research.",
    "guide_interests": "Novel Drug Delivery Systems, Formulation Development, Preformulation Science",
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

DEFAULT_SVG = (
    '<svg xmlns="http://w3.org" viewBox="0 0 200 200" width="200" height="200">'
    '<polygon points="100,10 180,55 180,145 100,190 20,145 20,55" fill="#0d263d" stroke="#55e6ee" stroke-width="5"/>'
    '<circle cx="100" cy="100" r="62" fill="none" stroke="#ff7c96" stroke-width="2" stroke-dasharray="6 4"/>'
    '<polygon points="72,72 92,60 112,72 112,95 92,107 72,95" fill="none" stroke="#55e6ee" stroke-width="3"/>'
    '<circle cx="92" cy="60" r="4" fill="#ffffff"/><circle cx="112" cy="95" r="4" fill="#ff7c96"/>'
    '<text x="100" y="160" text-anchor="middle" fill="#eaf7ff" font-family="sans-serif" font-size="16" font-weight="800">DX-AI</text>'
    '</svg>'
)
DEFAULT_LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(DEFAULT_SVG.encode("utf-8")).decode("utf-8")


def load_json_file(filepath, default_dict):
    data = json.loads(json.dumps(default_dict))
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                data.update(saved)
        except Exception:
            pass
    return data


def save_json_file(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
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
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = image_path.lower().split(".")[-1]
        if ext == "jpg":
            ext = "jpeg"
        if ext == "svg":
            ext = "svg+xml"
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return ""


def get_active_logo(content):
    saved = image_to_base64(content.get("logo_file", ""))
    return saved if saved else DEFAULT_LOGO_URI


def image_html(data_uri, width=120, height=120):
    if not data_uri:
        return ""
    return f'<img src="{data_uri}" style="width:{width}px;height:{height}px;object-fit:cover;border-radius:50%;border:3px solid #55e6ee;box-shadow:0 8px 25px rgba(0,0,0,0.3);margin-bottom:10px;">'


def hsp_distance(d1, d2):
    return math.sqrt(4 * (d1["dD"] - d2["dD"]) ** 2 + (d1["dP"] - d2["dP"]) ** 2 + (d1["dH"] - d2["dH"]) ** 2)


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


def apply_premium_theme(logo_uri):
    css = (
        "<style>"
        ".stApp{background:linear-gradient(135deg,#07121f 0%,#0a1928 50%,#07111d 100%);color:#f5f9ff;}"
        f'.stApp::before{{content:"";position:fixed;top:52%;left:54%;transform:translate(-50%,-50%);width:420px;height:420px;background-image:url("{logo_uri}");background-repeat:no-repeat;background-position:center;background-size:contain;opacity:0.045;pointer-events:none;z-index:0;}}'
        'section[data-testid="stSidebar"]{background:linear-gradient(180deg,#06101c 0%,#091c2b 100%);border-right:1px solid rgba(0,210,230,0.18);}'
        'section[data-testid="stSidebar"] *{color:#eaf7ff !important;}'
        "h1,h2,h3{color:#ffffff !important;}"
        ".dx-card,.card{background:linear-gradient(145deg,rgba(17,38,58,0.92),rgba(7,22,36,0.88));border:1px solid rgba(65,220,235,0.18);border-radius:20px;padding:24px;margin:12px 0;box-shadow:0 15px 40px rgba(0,0,0,0.28);}"
        ".profile-card{background:linear-gradient(145deg,rgba(17,38,58,0.92),rgba(7,22,36,0.88));border:1px solid rgba(65,220,235,0.22);border-radius:20px;padding:24px;text-align:center;box-shadow:0 15px 40px rgba(0,0,0,0.28);}"
        ".dx-hero{padding:40px 30px;border-radius:26px;text-align:center;background:linear-gradient(135deg,rgba(8,48,72,0.96),rgba(12,28,47,0.96));border:1px solid rgba(50,220,235,0.25);box-shadow:0 20px 50px rgba(0,0,0,0.35);margin-bottom:16px;}"
        ".dx-hero-title{font-size:40px;font-weight:800;background:linear-gradient(90deg,#ffffff,#55e6ee,#ff7c96);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;}"
        ".dx-hero-subtitle{color:#b9d9e8;font-size:17px;line-height:1.6;}"
        ".stButton>button{border-radius:12px !important;border:1px solid rgba(50,220,235,0.30) !important;background:linear-gradient(135deg,#087f91,#0aa6ad) !important;color:white !important;font-weight:700 !important;min-height:44px;}"
        'div[data-testid="stMetric"]{background:rgba(12,35,52,0.8);border:1px solid rgba(50,220,235,0.15);padding:15px;border-radius:15px;}'
        ".dx-watermark{position:fixed;bottom:22px;right:28px;font-size:46px;font-weight:900;color:rgba(80,220,235,0.04);transform:rotate(-12deg);pointer-events:none;z-index:0;letter-spacing:3px;}"
        '</style><div class="dx-watermark">DRUGXPERT AI</div>'
    )
    st.markdown(css, unsafe_allow_html=True)


if "custom_db" not in st.session_state:
    st.session_state.custom_db = load_json_file(DB_FILE, DEFAULT_DB)

if "site_content" not in st.session_state:
    st.session_state.site_content = load_json_file(CONTENT_FILE, DEFAULT_CONTENT)

if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.username = ""

custom_db = st.session_state.custom_db
content = st.session_state.site_content
active_logo = get_active_logo(content)
apply_premium_theme(active_logo)

if st.session_state.role is None:
    st.markdown(
        f'<div class="dx-hero"><img src="{active_logo}" style="width:92px;height:92px;object-fit:contain;margin-bottom:10px;">'
        f'<div class="dx-hero-title">{content.get("welcome_title", "WELCOME TO DRUGXPERT AI")}</div>'
        f'<div class="dx-hero-subtitle">{content.get("welcome_subtitle", "")}</div></div>',
        unsafe_allow_html=True
    )
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
                    custom_db["logs"].insert(0, {"Name": p_name.strip(), "Department": p_dept.strip() or "General", "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    save_json_file(DB_FILE, custom_db)
                    st.rerun()
