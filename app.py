import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

st.set_page_config(page_title="DrugXpert AI", page_icon="💊", layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = "drugxpert123"
DB_FILE = "drugxpert_db.json"

DEFAULT_DB = {
    "title": "DrugXpert AI",
    "welcome": "WELCOME TO DRUGXPERT AI",
    "subtitle": "Integrated Computational Platform for Drug-Excipient Compatibility, Solubility Prediction and Solvent Selection",
    "about": "DrugXpert AI is an integrated computational platform for pharmaceutical research including drug-excipient compatibility, Hansen Solubility Parameter (HSP) analysis, AI/ML solubility prediction, excipient and solvent selection, and integrated screening.",
    "dev_name": "Anmol Rajan",
    "dev_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "dev_bio": "Researcher working in computational pharmaceutics, AI/ML-assisted excipient selection and drug delivery systems.",
    "guide_name": "Research Guide",
    "guide_role": "Professor / Research Supervisor",
    "guide_bio": "Research guide supervising formulation development and computational pharmaceutics research.",
    "logo": "",
    "dev_photo": "",
    "guide_photo": "",
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
    data = json.loads(json.dumps(DEFAULT_DB))
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                data.update(saved)
        except Exception:
            pass
    return data

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def to_b64(up):
    if up is None:
        return ""
    return f"data:{up.type or 'image/png'};base64,{base64.b64encode(up.getvalue()).decode()}"

def calc_ra(d1, d2):
    return math.sqrt(4 * (d1["dD"] - d2["dD"]) ** 2 + (d1["dP"] - d2["dP"]) ** 2 + (d1["dH"] - d2["dH"]) ** 2)

def calc_logs(ra):
    return round(-2.0 + (4.0 / (1.0 + ra)), 3)

if "db" not in st.session_state:
    st.session_state.db = load_db()
if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.user = ""

db = st.session_state.db

st.markdown("""
<style>
.stApp {background-color: #07121f; color: #ffffff;}
.box {background: #0e253d; border: 1px solid #2ccce4; border-radius: 14px; padding: 20px; margin-bottom: 14px;}
.wm {position: fixed; bottom: 16px; right: 24px; font-size: 40px; font-weight: 900; color: rgba(85,230,238,0.06); pointer-events: none;}
</style><div class="wm">DRUGXPERT AI</div>
""", unsafe_allow_html=True)

if st.session_state.role is None:
    if db.get("logo"):
        st.image(db["logo"], width=100)
    st.title(f"💊 {db['welcome']}")
    st.write(db["subtitle"])
    t1, t2 = st.tabs(["👤 Participant Login", "🛡️ Admin Login"])
    with t1:
        name = st.text_input("Full Name *")
        dept = st.text_input("Department / Lab")
        if st.button("Enter Software", type="primary"):
            if name.strip():
                st.session_state.role = "participant"
                st.session_state.user = name.strip()
                db["logs"].insert(0, {"Name": name.strip(), "Dept": dept.strip() or "General", "Time": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_db(db)
                st.rerun()
            else:
                st.error("Enter your name.")
    with t2:
        u = st.text_input("Admin Username")
        p = st.text_input("Admin Password", type="password")
        if st.button("Login as Admin", type="primary"):
            if u.strip() == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.role = "admin"
                st.session_state.user = "Admin"
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

pages = ["Home", "HSP Compatibility", "AI/ML Solubility", "Solvent Lookup", "Integrated Screening", "About"]
if st.session_state.role == "admin":
    pages.append("Admin Panel")

st.sidebar.title(f"💊 {db['title']}")
st.sidebar.write(f"Logged in: **{st.session_state.user}**")
page = st.sidebar.radio("Go to", pages)
if st.sidebar.button("Logout"):
    st.session_state.role = None
    st.rerun()

if page == "Home":
    if db.get("logo"):
        st.image(db["logo"], width=110)
    st.title(db["welcome"])
    st.write(db["subtitle"])
    st.markdown(f"<div class='box'><h3>About the Software</h3><p>{db['about']}</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='box'><h4>Developer: {db['dev_name']}</h4><p><b>{db['dev_role']}</b></p><p>{db['dev_bio']}</p></div>", unsafe_allow_html=True)
        if db.get("dev_photo"):
            st.image(db["dev_photo"], width=120)
    with c2:
        st.markdown(f"<div class='box'><h4>Guide: {db['guide_name']}</h4><p><b>{db['guide_role']}</b></p><p>{db['guide_bio']}</p></div>", unsafe_allow_html=True)
        if db.get("guide_photo"):
            st.image(db["guide_photo"], width=120)

elif page == "HSP Compatibility":
    st.header("🧪 HSP Compatibility & Ra Calculation")
    drug = st.selectbox("Select Drug", list(db["drugs"].keys()))
    exc = st.selectbox("Select Excipient", list(db["excipients"].keys()))
    d, e = db["drugs"][drug], db["excipients"][exc]
    ra = calc_ra(d, e)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("HSP Ra", f"{ra:.3f}")
    c2.metric("ΔδD", f"{abs(d['dD']-e['dD']):.2f}")
    c3.metric("ΔδP", f"{abs(d['dP']-e['dP']):.2f}")
    c4.metric("ΔδH", f"{abs(d['dH']-e['dH']):.2f}")
    st.success("Excellent Compatibility" if ra <= 3 else ("Good Compatibility" if ra <= 5 else "Moderate/Poor Compatibility"))

elif page == "AI/ML Solubility":
    st.header("🤖 AI/ML Solubility Screening (logS)")
    drug = st.selectbox("Select Drug", list(db["drugs"].keys()))
    exc = st.selectbox("Select Excipient", list(db["excipients"].keys()))
    d, e = db["drugs"][drug], db["excipients"][exc]
    ra = calc_ra(d, e)
    logs = calc_logs(ra)
    ug = (10 ** logs) * d["mw"] * 1000
    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated logS", f"{logs:.3f}")
    c2.metric("Solubility (µg/mL)", f"{ug:.2f}")
    c3.metric("HSP Ra", f"{ra:.3f}")
    st.dataframe({"Descriptor": ["MW", "LogP", "Rotatable Bonds", "Aromatic Prop"], "Value": [d["mw"], d["logP"], d["rot"], d["arom"]]})

elif page == "Solvent Lookup":
    st.header("💧 Solvent Lookup")
    exc = st.selectbox("Select Excipient", list(db["excipients"].keys()))
    solvs = db["excipients"][exc].get("solvents", [])
    st.success(f"Solvents ({len(solvs)}): " + ", ".join(solvs))

elif page == "Integrated Screening":
    st.header("🧬 Integrated Screening")
    drug = st.selectbox("Select Drug", list(db["drugs"].keys()))
    exc = st.selectbox("Select Excipient", list(db["excipients"].keys()))
    d, e = db["drugs"][drug], db["excipients"][exc]
    ra = calc_ra(d, e)
    logs = calc_logs(ra)
    ug = (10 ** logs) * d["mw"] * 1000
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Drug", drug)
    c2.metric("Excipient", exc)
    c3.metric("HSP Ra", f"{ra:.2f}")
    c4.metric("Est. µg/mL", f"{ug:.2f}")
    st.info("Recommended Solvents: " + ", ".join(e.get("solvents", [])))

elif page == "About":
    st.header("📖 About DrugXpert AI")
    st.write(db["about"])
    st.subheader(f"Developer: {db['dev_name']} ({db['dev_role']})")
    st.write(db["dev_bio"])
    st.subheader(f"Guide: {db['guide_name']} ({db['guide_role']})")
    st.write(db["guide_bio"])

elif page == "Admin Panel":
    st.header("🛡️ Admin Control Panel")
    t1, t2, t3, t4, t5 = st.tabs(["Branding & Logo", "Developer & Guide", "Drugs", "Excipients", "Logs"])
    with t1:
        db["title"] = st.text_input("App Title", db["title"])
        db["welcome"] = st.text_input("Welcome Heading", db["welcome"])
        db["subtitle"] = st.text_area("Subtitle", db["subtitle"])
        db["about"] = st.text_area("About Text", db["about"])
        up_l = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
        if up_l:
            db["logo"] = to_b64(up_l)
        if st.button("Save Branding"):
            save_db(db)
            st.success("Saved!")
    with t2:
        db["dev_name"] = st.text_input("Developer Name", db["dev_name"])
        db["dev_role"] = st.text_input("Developer Role", db["dev_role"])
        db["dev_bio"] = st.text_area("Developer Bio", db["dev_bio"])
        up_d = st.file_uploader("Developer Photo", type=["png", "jpg", "jpeg"])
        if up_d:
            db["dev_photo"] = to_b64(up_d)
        db["guide_name"] = st.text_input("Guide Name", db["guide_name"])
        db["guide_role"] = st.text_input("Guide Role", db["guide_role"])
        db["guide_bio"] = st.text_area("Guide Bio", db["guide_bio"])
        up_g = st.file_uploader("Guide Photo", type=["png", "jpg", "jpeg"])
        if up_g:
