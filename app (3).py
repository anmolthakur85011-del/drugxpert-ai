import streamlit as st
import json
import math
from pathlib import Path

# =========================================================
# DRUGXPERT AI - SINGLE FILE STREAMLIT APPLICATION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DATABASE
# =========================================================

DB_FILE = Path("drugxpert_db.json")

DEFAULT_DB = {
    "users": {
        "admin": {
            "password": "drugxpert123",
            "role": "admin",
        },
        "user": {
            "password": "user123",
            "role": "user",
        },
    },
    "drugs": {
        "Deflazacort": {"dD": 18.2, "dP": 8.1, "dH": 10.4},
        "Artemether": {"dD": 18.0, "dP": 6.5, "dH": 8.0},
        "Curcumin": {"dD": 18.1, "dP": 7.2, "dH": 10.3},
    },
    "excipients": {
        "PVP K30": {"dD": 17.8, "dP": 12.5, "dH": 8.0},
        "Soluplus": {"dD": 17.0, "dP": 10.5, "dH": 7.5},
        "PEG 6000": {"dD": 16.8, "dP": 8.0, "dH": 6.0},
        "Poloxamer 188": {"dD": 16.2, "dP": 7.0, "dH": 8.0},
        "Poloxamer 407": {"dD": 16.0, "dP": 6.8, "dH": 8.5},
        "HPMC": {"dD": 17.0, "dP": 9.0, "dH": 10.0},
    },
    "solvents": {
        "PVP K30": ["Water", "Ethanol", "Methanol"],
        "Soluplus": ["Water", "Ethanol"],
        "PEG 6000": ["Water", "Ethanol"],
        "Poloxamer 188": ["Water", "Ethanol"],
        "Poloxamer 407": ["Water", "Ethanol"],
        "HPMC": ["Water", "Ethanol"],
    },
}


def load_db():
    if not DB_FILE.exists():
        return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return json.loads(json.dumps(DEFAULT_DB))


def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


db = load_db()

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 35px 35px 30px 35px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0b4f6c, #087f8c);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        margin-bottom: 0;
    }

    .card {
        padding: 25px;
        border-radius: 16px;
        background-color: white;
        border: 1px solid #e5e9f0;
        min-height: 190px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .card h3 {
        color: #0b4f6c;
    }

    .card p {
        color: #555;
        line-height: 1.6;
    }

    .footer {
        text-align: center;
        color: #777;
        padding: 30px 0 10px 0;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="hero">
            <h1>💊 DrugXpert AI</h1>
            <p>Computational Drug Formulation Research Platform</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🔐 Login")

    login_type = st.radio(
        "Login as",
        ["User", "Admin"],
        horizontal=True,
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary", use_container_width=True):

        user_record = db["users"].get(username)

        if user_record and user_record["password"] == password:

            required_role = "admin" if login_type == "Admin" else "user"

            if user_record["role"] == required_role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = required_role
                st.rerun()
            else:
                st.error("This account does not have the selected access level.")

        else:
            st.error("Invalid username or password.")

    st.info(
        "Demo accounts: Admin → admin / drugxpert123 | "
        "User → user / user123"
    )

    st.markdown(
        '<div class="footer">DrugXpert AI | Secure Access</div>',
        unsafe_allow_html=True,
    )

    st.stop()

# =========================================================
# LOGOUT
# =========================================================

with st.sidebar:
    st.markdown("## 💊 DrugXpert AI")
    st.markdown("---")
    st.write(f"👤 **{st.session_state.username}**")
    st.write(f"🔑 **Role:** {st.session_state.role.title()}")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

# =========================================================
# ADMIN PANEL
# =========================================================

if st.session_state.role == "admin":

    st.title("🛡️ Administrator Control Panel")
    st.write("Manage the DrugXpert AI database without editing the Python code.")

    tabs = st.tabs(
        [
            "📊 Dashboard",
            "💊 Drugs",
            "🧪 Excipients",
            "🧴 Solvents",
            "👥 Users",
        ]
    )

    with tabs[0]:
        st.metric("Drugs", len(db["drugs"]))
        st.metric("Excipients", len(db["excipients"]))
        st.metric("Users", len(db["users"]))

    with tabs[1]:
        st.subheader("Drug Database")

        drug_names = list(db["drugs"].keys())

        if drug_names:
            selected_drug = st.selectbox("Select drug", drug_names)

            d = db["drugs"][selected_drug]

            c1, c2, c3 = st.columns(3)
            with c1:
                new_dD = st.number_input(
                    "δD",
                    value=float(d.get("dD", 0)),
                    key="drug_dD",
                )
            with c2:
                new_dP = st.number_input(
                    "δP",
                    value=float(d.get("dP", 0)),
                    key="drug_dP",
                )
            with c3:
                new_dH = st.number_input(
                    "δH",
                    value=float(d.get("dH", 0)),
                    key="drug_dH",
                )

            c1, c2 = st.columns(2)

            with c1:
                if st.button("💾 Update Drug", use_container_width=True):
                    db["drugs"][selected_drug] = {
                        "dD": new_dD,
                        "dP": new_dP,
                        "dH": new_dH,
                    }
                    save_db(db)
                    st.success("Drug updated successfully.")
                    st.rerun()

            with c2:
                if st.button("🗑️ Delete Drug", use_container_width=True):
                    del db["drugs"][selected_drug]
                    save_db(db)
                    st.success("Drug deleted.")
                    st.rerun()

        st.markdown("---")
        st.subheader("➕ Add New Drug")

        new_drug_name = st.text_input("Drug name", key="new_drug_name")

        c1, c2, c3 = st.columns(3)
        with c1:
            add_dD = st.number_input("δD", value=0.0, key="add_dD")
        with c2:
            add_dP = st.number_input("δP", value=0.0, key="add_dP")
        with c3:
            add_dH = st.number_input("δH", value=0.0, key="add_dH")

        if st.button("➕ Add Drug", type="primary"):
            if not new_drug_name.strip():
                st.warning("Enter a drug name.")
            elif new_drug_name in db["drugs"]:
                st.warning("Drug already exists.")
            else:
                db["drugs"][new_drug_name.strip()] = {
                    "dD": add_dD,
                    "dP": add_dP,
                    "dH": add_dH,
                }
                save_db(db)
                st.success("Drug added successfully.")
                st.rerun()

    with tabs[2]:
        st.subheader("Excipient / Polymer Database")

        exc_names = list(db["excipients"].keys())

        if exc_names:
            selected_exc = st.selectbox(
                "Select excipient/polymer",
                exc_names,
            )

            e = db["excipients"][selected_exc]

            c1, c2, c3 = st.columns(3)
            with c1:
                e_dD = st.number_input(
                    "δD",
                    value=float(e.get("dD", 0)),
                    key="exc_dD",
                )
            with c2:
                e_dP = st.number_input(
                    "δP",
                    value=float(e.get("dP", 0)),
                    key="exc_dP",
                )
            with c3:
                e_dH = st.number_input(
                    "δH",
                    value=float(e.get("dH", 0)),
                    key="exc_dH",
                )

            c1, c2 = st.columns(2)

            with c1:
                if st.button(
                    "💾 Update Excipient",
                    use_container_width=True,
                ):
                    db["excipients"][selected_exc] = {
                        "dD": e_dD,
                        "dP": e_dP,
                        "dH": e_dH,
                    }
                    save_db(db)
                    st.success("Excipient updated.")
                    st.rerun()

            with c2:
                if st.button(
                    "🗑️ Delete Excipient",
                    use_container_width=True,
                ):
                    del db["excipients"][selected_exc]
                    save_db(db)
                    st.success("Excipient deleted.")
                    st.rerun()

        st.markdown("---")
        st.subheader("➕ Add New Excipient / Polymer")

        new_exc_name = st.text_input(
            "Excipient / polymer name",
            key="new_exc_name",
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            add_e_dD = st.number_input(
                "δD",
                value=0.0,
                key="add_e_dD",
            )
        with c2:
            add_e_dP = st.number_input(
                "δP",
                value=0.0,
                key="add_e_dP",
            )
        with c3:
            add_e_dH = st.number_input(
                "δH",
                value=0.0,
                key="add_e_dH",
            )

        if st.button("➕ Add Excipient", type="primary"):
            if not new_exc_name.strip():
                st.warning("Enter an excipient/polymer name.")
            elif new_exc_name in db["excipients"]:
                st.warning("Excipient already exists.")
            else:
                db["excipients"][new_exc_name.strip()] = {
                    "dD": add_e_dD,
                    "dP": add_e_dP,
                    "dH": add_e_dH,
                }
                save_db(db)
                st.success("Excipient added successfully.")
                st.rerun()

    with tabs[3]:
        st.subheader("🧴 Solvent Database")

        solvent_target = st.selectbox(
            "Select polymer/excipient",
            list(db["excipients"].keys()),
        )

        current_solvents = db["solvents"].get(solvent_target, [])

        st.write("Current solvents:")
        if current_solvents:
            st.write(", ".join(current_solvents))
        else:
            st.write("No solvents added.")

        solvent_to_add = st.text_input(
            "Add solvent",
            key="solvent_to_add",
        )

        if st.button("➕ Add Solvent"):
            if solvent_to_add.strip():
                db["solvents"].setdefault(solvent_target, [])
                if solvent_to_add.strip() not in db["solvents"][solvent_target]:
                    db["solvents"][solvent_target].append(
                        solvent_to_add.strip()
                    )
                    save_db(db)
                    st.success("Solvent added.")
                    st.rerun()
                else:
                    st.warning("Solvent already exists.")

        if current_solvents:
            solvent_to_delete = st.selectbox(
                "Remove solvent",
                current_solvents,
                key="remove_solvent",
            )

            if st.button("🗑️ Remove Solvent"):
                db["solvents"][solvent_target].remove(solvent_to_delete)
                save_db(db)
                st.success("Solvent removed.")
                st.rerun()

    with tabs[4]:
        st.subheader("👥 User Accounts")

        st.write("Existing usernames:")
        for name, record in db["users"].items():
            st.write(
                f"• **{name}** — {record.get('role', 'user').title()}"
            )

        st.markdown("---")
        st.subheader("➕ Add User")

        new_username = st.text_input("Username", key="new_username")
        new_password = st.text_input(
            "Password",
            type="password",
            key="new_password",
        )
        new_role = st.selectbox(
            "Role",
            ["user", "admin"],
            key="new_role",
        )

        if st.button("➕ Add User", type="primary"):
            if not new_username.strip() or not new_password:
                st.warning("Enter both username and password.")
            elif new_username in db["users"]:
                st.warning("Username already exists.")
            else:
                db["users"][new_username.strip()] = {
                    "password": new_password,
                    "role": new_role,
                }
                save_db(db)
                st.success("User created successfully.")
                st.rerun()

    st.markdown(
        '<div class="footer">DrugXpert AI | Administrator Control Panel</div>',
        unsafe_allow_html=True,
    )

    st.stop()

# =========================================================
# USER SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Home",
            "HSP Compatibility",
            "AI/ML Solubility",
            "Solvent Lookup",
            "Integrated Screening",
        ],
    )

    st.markdown("---")
    st.caption("Computational Drug Formulation Platform")

# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>💊 DrugXpert AI</h1>
            <p>
            Integrated Computational Platform for Drug–Excipient
            Compatibility, Solubility Prediction and Solvent Selection
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Welcome to DrugXpert AI")

    st.write(
        "DrugXpert AI is designed to support rational drug formulation "
        "development using computational screening, molecular descriptors, "
        "machine learning and solvent compatibility analysis."
    )

    st.markdown("### 🔬 Core Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>🧪 HSP Compatibility</h3>
                <p>
                Hansen Solubility Parameter based screening of
                drug–excipient compatibility using δD, δP, δH
                and Hansen distance (Ra).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>🤖 AI/ML Solubility</h3>
                <p>
                Molecular descriptor-based prediction of LogS
                and solubility for drug–excipient systems using
                machine learning models.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>🧴 Solvent Lookup</h3>
                <p>
                Computational lookup and ranking of suitable
                solvents for selected polymers and excipients.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("## 🔗 Integrated Screening")

    st.info(
        "Drug → Excipient → HSP Compatibility → Molecular Descriptor "
        "Analysis → AI/ML Solubility Prediction → Solvent Selection "
        "→ Final Recommendation"
    )

# =========================================================
# HSP COMPATIBILITY
# =========================================================

elif page == "HSP Compatibility":

    st.title("🧪 HSP Compatibility Screening")

    st.write(
        "Calculate Hansen distance (Ra) between a selected drug "
        "and the available excipients/polymers."
    )

    st.markdown("---")

    drug = st.selectbox(
        "Select Drug",
        ["Select drug"] + list(db["drugs"].keys()),
    )

    if drug != "Select drug":

        drug_data = db["drugs"][drug]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("δD", drug_data["dD"])

        with c2:
            st.metric("δP", drug_data["dP"])

        with c3:
            st.metric("δH", drug_data["dH"])

        results = []

        for excipient, data in db["excipients"].items():

            delta_d = drug_data["dD"] - data["dD"]
            delta_p = drug_data["dP"] - data["dP"]
            delta_h = drug_data["dH"] - data["dH"]

            ra = math.sqrt(
                4 * (delta_d ** 2)
                + (delta_p ** 2)
                + (delta_h ** 2)
            )

            results.append(
                {
                    "Excipient / Polymer": excipient,
                    "δD": data["dD"],
                    "δP": data["dP"],
                    "δH": data["dH"],
                    "Ra": round(ra, 3),
                }
            )

        results.sort(key=lambda x: x["Ra"])

        st.markdown("### Compatibility Ranking")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True,
        )

        if results:
            best = results[0]

            st.success(
                f"Lowest predicted Hansen distance: "
                f"{best['Excipient / Polymer']} "
                f"(Ra = {best['Ra']})"
            )

        st.caption(
            "Lower Ra indicates closer Hansen parameter proximity. "
            "Ra is a screening metric and should be experimentally validated."
        )

# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":

    st.title("🤖 AI/ML Solubility Prediction")

    st.write(
        "This interface is prepared for connection to your trained "
        "machine-learning model and molecular descriptor dataset."
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        drug = st.selectbox(
            "Select Drug",
            ["Select drug"] + list(db["drugs"].keys()),
            key="ml_drug",
        )

    with c2:
        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + list(db["excipients"].keys()),
            key="ml_excipient",
        )

    st.markdown("### Molecular Descriptors")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("LogP", "—")

    with c2:
        st.metric("Molecular Weight", "—")

    with c3:
        st.metric("Rotatable Bonds", "—")

    with c4:
        st.metric("Aromatic Proportion", "—")

    if st.button("Predict Solubility", type="primary"):

        if drug == "Select drug" or excipient == "Select excipient":
            st.warning("Please select both Drug and Excipient.")
        else:
            st.info(
                "ML model integration point. Connect your trained "
                "XGBoost/model pipeline here to generate LogS and "
                "solubility predictions."
            )

# =========================================================
# SOLVENT LOOKUP
# =========================================================

elif page == "Solvent Lookup":

    st.title("🧴 Solvent Lookup")

    st.write(
        "Find solvents currently stored in the DrugXpert AI database."
    )

    st.markdown("---")

    polymer = st.selectbox(
        "Select Polymer / Excipient",
        ["Select polymer"] + list(db["excipients"].keys()),
    )

    if polymer != "Select polymer":

        solvents = db["solvents"].get(polymer, [])

        if solvents:
            st.success(f"Solvents listed for {polymer}:")
            for solvent in solvents:
                st.write(f"• {solvent}")
        else:
            st.info("No solvent entries are currently available.")

# =========================================================
# INTEGRATED SCREENING
# =========================================================

elif page == "Integrated Screening":

    st.title("🔗 Integrated Drug–Excipient Screening")

    st.write(
        "Combine HSP compatibility, AI/ML solubility prediction "
        "and solvent selection in a single workflow."
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        drug = st.selectbox(
            "Select Drug",
            ["Select drug"] + list(db["drugs"].keys()),
            key="integrated_drug",
        )

    with c2:
        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + list(db["excipients"].keys()),
            key="integrated_excipient",
        )

    if st.button("Run Integrated Screening", type="primary"):

        if drug == "Select drug" or excipient == "Select excipient":
            st.warning("Please select both Drug and Excipient.")
        else:

            st.success(
                f"Screening initiated for {drug} + {excipient}"
            )

            drug_data = db["drugs"][drug]
            exc_data = db["excipients"][excipient]

            delta_d = drug_data["dD"] - exc_data["dD"]
            delta_p = drug_data["dP"] - exc_data["dP"]
            delta_h = drug_data["dH"] - exc_data["dH"]

            ra = math.sqrt(
                4 * (delta_d ** 2)
                + (delta_p ** 2)
                + (delta_h ** 2)
            )

            st.markdown("### HSP Screening")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Drug δD", drug_data["dD"])
            with c2:
                st.metric("Drug δP", drug_data["dP"])
            with c3:
                st.metric("Drug δH", drug_data["dH"])
            with c4:
                st.metric("Hansen Ra", round(ra, 3))

            st.markdown("### Screening Workflow")

            st.write("1️⃣ HSP compatibility analysis")
            st.write("2️⃣ Molecular descriptor analysis")
            st.write("3️⃣ AI/ML solubility prediction")
            st.write("4️⃣ Solvent compatibility lookup")
            st.write("5️⃣ Final candidate recommendation")

            st.info(
                "The HSP calculation is active in this version. "
                "The AI/ML prediction stage requires your trained "
                "model and descriptor dataset to be connected."
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    © 2026 DrugXpert AI | Integrated Computational Drug Formulation Platform
    </div>
    """,
    unsafe_allow_html=True,
)
