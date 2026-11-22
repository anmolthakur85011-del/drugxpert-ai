import streamlit as st
import json
import os
from datetime import datetime

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"
DB_FILE = "drugxpert_db.json"

DEFAULT_DB = {
    "custom_drugs": {},
    "custom_excipients": {},
    "logs": []
}

def load_custom_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_DB))

def save_custom_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def init_auth_and_sidebar():
    if "custom_db" not in st.session_state:
        st.session_state.custom_db = load_custom_db()
    if "role" not in st.session_state:
        st.session_state.role = None
        st.session_state.username = ""

    db = st.session_state.custom_db

    # LOGIN SCREEN
    if st.session_state.role is None:
        st.markdown("""
        <div style="padding:28px;border-radius:16px;background:linear-gradient(135deg,#0b4f6c,#087f8c);color:white;text-align:center;margin-bottom:20px;">
            <h1>💊 DrugXpert AI</h1>
            <p>Integrated Computational Platform for Drug–Excipient Compatibility, Solubility Prediction and Solvent Selection</p>
        </div>
        """, unsafe_allow_html=True)

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
                        db["logs"].insert(0, {
                            "Name": p_name.strip(),
                            "Department": p_dept.strip() or "General",
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        save_custom_db(db)
                        st.rerun()
                    else:
                        st.error("Please enter your name!")

            with t2:
                u = st.text_input("Admin Username", placeholder="admin")
                p = st.text_input("Admin Password", type="password", placeholder="drugxpert123")
                if st.button("Login as Admin 🔒", type="primary", use_container_width=True):
                    if u.strip() == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                        st.session_state.role = "admin"
                        st.session_state.username = f"Admin ({u.strip()})"
                        st.rerun()
                    else:
                        st.error("❌ Wrong Username or Password!")
        st.stop()

    # SIDEBAR USER INFO & LOGOUT
    with st.sidebar:
        if st.session_state.role == "admin":
            st.success(f"🛡️ {st.session_state.username}")
        else:
            st.info(f"👤 {st.session_state.username}")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None
            st.session_state.username = ""
            st.rerun()

def render_admin_panel():
    st.title("⚙️ Admin Control Panel")
    st.write("Yahan se aap naye Drugs, Excipients aur Participants ka record manage kar sakte hain.")
    st.markdown("---")
    db = st.session_state.custom_db

    with st.expander("➕ Add Custom Drug", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        dn = c1.text_input("Drug Name", placeholder="e.g. Ibuprofen")
        dd = c2.number_input("δD", value=18.0, step=0.1)
        dp = c3.number_input("δP", value=7.0, step=0.1)
        dh = c4.number_input("δH", value=8.0, step=0.1)
        if st.button("Save Drug"):
            if dn.strip():
                db["custom_drugs"][dn.strip()] = {"dD": dd, "dP": dp, "dH": dh}
                save_custom_db(db)
                st.success(f"✅ {dn} added!")
                st.rerun()

        if db["custom_drugs"]:
            st.write("**Added Drugs:**", db["custom_drugs"])

    with st.expander("➕ Add Custom Excipient", expanded=True):
        e1, e2, e3, e4 = st.columns(4)
        en = e1.text_input("Excipient Name", placeholder="e.g. Eudragit")
        ed = e2.number_input("Exc. δD", value=18.0, step=0.1)
        ep = e3.number_input("Exc. δP", value=8.0, step=0.1)
        eh = e4.number_input("Exc. δH", value=10.0, step=0.1)
        if st.button("Save Excipient"):
            if en.strip():
                db["custom_excipients"][en.strip()] = {"dD": ed, "dP": ep, "dH": eh}
                save_custom_db(db)
                st.success(f"✅ {en} added!")
                st.rerun()

        if db["custom_excipients"]:
            st.write("**Added Excipients:**", db["custom_excipients"])

    with st.expander("📋 Participant Login Logs", expanded=True):
        if db["logs"]:
            st.table(db["logs"])
            if st.button("Clear Logs"):
                db["logs"] = []
                save_custom_db(db)
                st.rerun()
        else:
            st.info("No participant logins yet.")
