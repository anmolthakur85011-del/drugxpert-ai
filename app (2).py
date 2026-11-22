import streamlit as st
import json
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# DRUGXPERT AI — SINGLE FILE VERSION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_FILE = Path("drugxpert_db.json")

DEFAULT_DB = {
    "drugs": {
        "Deflazacort": {},
        "Artemether": {},
        "Curcumin": {},
    },
    "excipients": {
        "PVP K30": {},
        "Soluplus": {},
        "PEG 6000": {},
        "Poloxamer 188": {},
        "Poloxamer 407": {},
        "HPMC": {},
    },
    "users": [],
}


def load_db():
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in DEFAULT_DB.items():
                if key not in data:
                    data[key] = value.copy()
            return data
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_DB))


def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Database save error: {e}")
        return False


def calculate_ra(drug, excipient):
    try:
        dd = float(drug.get("dD"))
        dp = float(drug.get("dP"))
        dh = float(drug.get("dH"))
        ed = float(excipient.get("dD"))
        ep = float(excipient.get("dP"))
        eh = float(excipient.get("dH"))

        return math.sqrt(
            4 * (dd - ed) ** 2
            + (dp - ep) ** 2
            + (dh - eh) ** 2
        )
    except Exception:
        return None


def logout():
    for key in ["role", "username"]:
        st.session_state.pop(key, None)
    st.rerun()


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
        padding: 35px;
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
        min-height: 210px;
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
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION / DATABASE
# =========================================================

if "db" not in st.session_state:
    st.session_state.db = load_db()

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================================================
# LOGIN SCREEN
# =========================================================

if st.session_state.role is None:

    st.markdown(
        """
        <div class="hero" style="text-align:center;">
            <h1>💊 DrugXpert AI</h1>
            <p>
            Integrated Computational Platform for Drug–Excipient
            Compatibility, Solubility Prediction and Solvent Selection
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown("## 🔐 Login")

        tab_user, tab_admin = st.tabs(
            ["👤 User Login", "🛡️ Admin Login"]
        )

        # -------------------------------------------------
        # USER LOGIN
        # -------------------------------------------------

        with tab_user:

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="user_name",
            )

            department = st.text_input(
                "Department / Lab",
                placeholder="e.g. Pharmaceutics",
                key="user_department",
            )

            if st.button(
                "Enter Software →",
                type="primary",
                use_container_width=True,
                key="user_login",
            ):

                if not name.strip():
                    st.error("Please enter your name.")

                else:

                    st.session_state.role = "user"
                    st.session_state.username = name.strip()

                    st.session_state.db["users"].append(
                        {
                            "Name": name.strip(),
                            "Department": department.strip() or "General",
                            "Login Time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    )

                    save_db(st.session_state.db)
                    st.rerun()

        # -------------------------------------------------
        # ADMIN LOGIN
        # -------------------------------------------------

        with tab_admin:

            st.warning(
                "Admin access is restricted to the software owner."
            )

            admin_username = st.text_input(
                "Admin Username",
                key="admin_username",
            )

            admin_password = st.text_input(
                "Admin Password",
                type="password",
                key="admin_password",
            )

            if st.button(
                "Login as Admin 🔒",
                type="primary",
                use_container_width=True,
                key="admin_login",
            ):

                # Change these credentials before public production use.
                if (
                    admin_username == "admin"
                    and admin_password == "drugxpert123"
                ):

                    st.session_state.role = "admin"
                    st.session_state.username = "Administrator"
                    st.rerun()

                else:
                    st.error("Incorrect admin username or password.")

    st.stop()


# =========================================================
# ADMIN PANEL
# =========================================================

if st.session_state.role == "admin":

    st.title("🛡️ DrugXpert AI — Admin Control Panel")

    st.success(
        "You are logged in as Administrator. "
        "Changes made here are used by the current software session."
    )

    if st.button("🚪 Logout"):
        logout()

    db = st.session_state.db

    st.markdown("---")

    # -----------------------------------------------------
    # ADMIN TABS
    # -----------------------------------------------------

    t1, t2, t3, t4 = st.tabs(
        [
            "💊 Drugs",
            "🧪 Excipients",
            "👥 Users",
            "⚙️ Database",
        ]
    )

    # -----------------------------------------------------
    # DRUG MANAGEMENT
    # -----------------------------------------------------

    with t1:

        st.subheader("Add / Edit Drug")

        drug_name = st.text_input(
            "Drug Name",
            placeholder="e.g. Mycophenolate mofetil",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            drug_dd = st.number_input(
                "δD",
                value=0.0,
                step=0.1,
                format="%.3f",
            )

        with c2:
            drug_dp = st.number_input(
                "δP",
                value=0.0,
                step=0.1,
                format="%.3f",
            )

        with c3:
            drug_dh = st.number_input(
                "δH",
                value=0.0,
                step=0.1,
                format="%.3f",
            )

        if st.button(
            "➕ Save / Update Drug",
            type="primary",
            key="save_drug",
        ):

            if not drug_name.strip():
                st.error("Enter a drug name.")

            else:

                db["drugs"][drug_name.strip()] = {
                    "dD": drug_dd,
                    "dP": drug_dp,
                    "dH": drug_dh,
                }

                save_db(db)

                st.success(
                    f"{drug_name.strip()} saved successfully."
                )

                st.rerun()

        st.markdown("### Current Drugs")

        if db["drugs"]:

            for name, data in list(db["drugs"].items()):

                c1, c2 = st.columns([5, 1])

                with c1:
                    st.write(f"**{name}**")

                    if data:
                        st.caption(
                            f"δD={data.get('dD', '—')} | "
                            f"δP={data.get('dP', '—')} | "
                            f"δH={data.get('dH', '—')}"
                        )

                with c2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_drug_{name}",
                    ):

                        del db["drugs"][name]
                        save_db(db)
                        st.rerun()

    # -----------------------------------------------------
    # EXCIPIENT MANAGEMENT
    # -----------------------------------------------------

    with t2:

        st.subheader("Add / Edit Excipient / Polymer")

        excipient_name = st.text_input(
            "Excipient / Polymer Name",
            placeholder="e.g. Eudragit L100",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            exc_dd = st.number_input(
                "δD",
                value=0.0,
                step=0.1,
                format="%.3f",
                key="exc_dd",
            )

        with c2:
            exc_dp = st.number_input(
                "δP",
                value=0.0,
                step=0.1,
                format="%.3f",
                key="exc_dp",
            )

        with c3:
            exc_dh = st.number_input(
                "δH",
                value=0.0,
                step=0.1,
                format="%.3f",
                key="exc_dh",
            )

        if st.button(
            "➕ Save / Update Excipient",
            type="primary",
            key="save_excipient",
        ):

            if not excipient_name.strip():
                st.error("Enter an excipient/polymer name.")

            else:

                db["excipients"][excipient_name.strip()] = {
                    "dD": exc_dd,
                    "dP": exc_dp,
                    "dH": exc_dh,
                }

                save_db(db)

                st.success(
                    f"{excipient_name.strip()} saved successfully."
                )

                st.rerun()

        st.markdown("### Current Excipients / Polymers")

        for name, data in list(db["excipients"].items()):

            c1, c2 = st.columns([5, 1])

            with c1:

                st.write(f"**{name}**")

                if data:
                    st.caption(
                        f"δD={data.get('dD', '—')} | "
                        f"δP={data.get('dP', '—')} | "
                        f"δH={data.get('dH', '—')}"
                    )

            with c2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_excipient_{name}",
                ):

                    del db["excipients"][name]
                    save_db(db)
                    st.rerun()

    # -----------------------------------------------------
    # USER LOGS
    # -----------------------------------------------------

    with t3:

        st.subheader("👥 User Login Records")

        if db["users"]:

            st.dataframe(
                db["users"],
                use_container_width=True,
                hide_index=True,
            )

            if st.button(
                "🗑️ Clear User Records",
                key="clear_users",
            ):

                db["users"] = []
                save_db(db)
                st.rerun()

        else:

            st.info("No user login records available.")

    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    with t4:

        st.subheader("⚙️ Database Management")

        st.write(
            "The current database contains the drugs, excipients "
            "and user records managed from this panel."
        )

        st.metric(
            "Drugs",
            len(db["drugs"]),
        )

        st.metric(
            "Excipients / Polymers",
            len(db["excipients"]),
        )

        st.metric(
            "Users",
            len(db["users"]),
        )

        if st.button(
            "🔄 Reload Database",
            key="reload_database",
        ):

            st.session_state.db = load_db()
            st.success("Database reloaded.")
            st.rerun()

    st.markdown("---")

    st.info(
        "Admin changes are saved to drugxpert_db.json. "
        "For reliable permanent cloud persistence, a hosted database "
        "should be connected in a later production version."
    )

    st.stop()


# =========================================================
# USER APPLICATION
# =========================================================

db = st.session_state.db

drug_list = list(db["drugs"].keys())
excipient_list = list(db["excipients"].keys())

with st.sidebar:

    st.markdown("## 💊 DrugXpert AI")

    st.markdown("---")

    st.info(
        f"👤 User: {st.session_state.username}"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):
        logout()

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

    st.caption(
        "Computational Drug Formulation Platform"
    )


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

    c1, c2, c3 = st.columns(3)

    with c1:
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

    with c2:
        st.markdown(
            """
            <div class="card">
                <h3>🤖 AI/ML Solubility</h3>
                <p>
                Molecular descriptor-based prediction of LogS
                and solubility for drug–excipient systems.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
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
        "Screen drug–excipient compatibility using Hansen Solubility Parameters."
    )

    st.markdown("---")

    drug_name = st.selectbox(
        "Select Drug",
        ["Select drug"] + drug_list,
    )

    if drug_name != "Select drug":

        drug = db["drugs"].get(drug_name, {})

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("δD", drug.get("dD", "—"))

        with c2:
            st.metric("δP", drug.get("dP", "—"))

        with c3:
            st.metric("δH", drug.get("dH", "—"))

        st.markdown("### Excipient Compatibility Ranking")

        rows = []

        for exc_name, exc_data in db["excipients"].items():

            ra = calculate_ra(drug, exc_data)

            if ra is not None:
                rows.append(
                    {
                        "Excipient / Polymer": exc_name,
                        "δD": exc_data.get("dD"),
                        "δP": exc_data.get("dP"),
                        "δH": exc_data.get("dH"),
                        "Ra": round(ra, 4),
                    }
                )

        if rows:

            rows.sort(key=lambda x: x["Ra"])

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )

            best = rows[0]

            st.success(
                f"Lowest calculated Ra: {best['Excipient / Polymer']} "
                f"(Ra = {best['Ra']})"
            )

        else:

            st.warning(
                "Add HSP values for both the selected drug and "
                "excipients from the Admin Panel."
            )


# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":

    st.title("🤖 AI/ML Solubility Prediction")

    st.write(
        "Select a drug and excipient for the future trained ML model."
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        drug = st.selectbox(
            "Select Drug",
            ["Select drug"] + drug_list,
            key="ml_drug",
        )

    with c2:
        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + excipient_list,
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

    if st.button(
        "Predict Solubility",
        type="primary",
    ):

        if (
            drug == "Select drug"
            or excipient == "Select excipient"
        ):

            st.warning(
                "Please select both Drug and Excipient."
            )

        else:

            st.info(
                "The ML prediction engine is not connected yet. "
                "This interface is ready for your trained model."
            )


# =========================================================
# SOLVENT LOOKUP
# =========================================================

elif page == "Solvent Lookup":

    st.title("🧴 Solvent Lookup")

    st.write(
        "Find suitable solvents for selected polymers and excipients."
    )

    st.markdown("---")

    polymer = st.selectbox(
        "Select Polymer / Excipient",
        ["Select polymer"] + excipient_list,
    )

    if polymer != "Select polymer":

        st.success(f"Selected: {polymer}")

        st.info(
            "The solvent database can be connected to this module."
        )


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
            ["Select drug"] + drug_list,
            key="integrated_drug",
        )

    with c2:
        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + excipient_list,
            key="integrated_excipient",
        )

    if st.button(
        "Run Integrated Screening",
        type="primary",
    ):

        if (
            drug == "Select drug"
            or excipient == "Select excipient"
        ):

            st.warning(
                "Please select both Drug and Excipient."
            )

        else:

            st.success(
                f"Screening initiated for {drug} + {excipient}"
            )

            st.markdown("### Screening Workflow")

            st.write("1️⃣ HSP compatibility analysis")
            st.write("2️⃣ Molecular descriptor analysis")
            st.write("3️⃣ AI/ML solubility prediction")
            st.write("4️⃣ Solvent compatibility lookup")
            st.write("5️⃣ Final candidate recommendation")


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
