import streamlit as st
from admin_module import init_auth_and_sidebar, render_admin_panel

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# AUTHENTICATION
# =========================================================

init_auth_and_sidebar()

# =========================================================
# ADMIN ACCESS
# =========================================================

if st.session_state.get("role") == "admin":

    render_admin_panel()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#777;
            padding:30px 0 10px 0;
            font-size:13px;
        ">
        DrugXpert AI | Administrator Control Panel
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# =========================================================
# CUSTOM CSS
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
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD ADMIN DATABASE
# =========================================================

db = st.session_state.get("custom_db", {})

custom_drugs = db.get("custom_drugs", {})
custom_excipients = db.get("custom_excipients", {})

# =========================================================
# BUILD DRUG LIST
# =========================================================

default_drugs = [
    "Deflazacort",
    "Artemether",
    "Curcumin"
]

drug_list = default_drugs.copy()

for drug_name in custom_drugs.keys():
    if drug_name not in drug_list:
        drug_list.append(drug_name)

# =========================================================
# BUILD EXCIPIENT LIST
# =========================================================

default_excipients = [
    "PVP K30",
    "Soluplus",
    "PEG 6000"
]

excipient_list = default_excipients.copy()

for excipient_name in custom_excipients.keys():
    if excipient_name not in excipient_list:
        excipient_list.append(excipient_name)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 💊 DrugXpert AI")

    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:10px;
            background:#eaf6f8;
            margin-bottom:15px;
        ">
        👤 <b>User:</b> {st.session_state.get("username", "User")}
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Home",
            "HSP Compatibility",
            "AI/ML Solubility",
            "Solvent Lookup",
            "Integrated Screening"
        ]
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
        unsafe_allow_html=True
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
            unsafe_allow_html=True
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
            unsafe_allow_html=True
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
            unsafe_allow_html=True
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

    st.subheader("Drug Selection")

    drug = st.selectbox(
        "Select Drug",
        ["Select drug"] + drug_list
    )

    if drug != "Select drug":

        st.success(f"Selected Drug: {drug}")

        drug_data = custom_drugs.get(drug)

        if drug_data:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "δD",
                    f'{drug_data.get("dD", "—")}'
                )

            with col2:
                st.metric(
                    "δP",
                    f'{drug_data.get("dP", "—")}'
                )

            with col3:
                st.metric(
                    "δH",
                    f'{drug_data.get("dH", "—")}'
                )

            st.success(
                "HSP values loaded from the Admin database."
            )

        else:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("δD", "—")

            with col2:
                st.metric("δP", "—")

            with col3:
                st.metric("δH", "—")

            st.info(
                "HSP values for this built-in drug will be connected "
                "to the scientific database."
            )

        st.markdown("### Compatibility Analysis")

        st.info(
            "The HSP engine will calculate Hansen distance (Ra) "
            "and rank compatible excipients."
        )

# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":

    st.title("🤖 AI/ML Solubility Prediction")

    st.write(
        "Predict LogS and solubility using molecular descriptors "
        "and the trained machine learning model."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        drug = st.selectbox(
            "Select Drug",
            ["Select drug"] + drug_list,
            key="ml_drug"
        )

    with col2:

        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + excipient_list,
            key="ml_excipient"
        )

    st.markdown("### Molecular Descriptors")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("LogP", "—")

    with col2:
        st.metric("Molecular Weight", "—")

    with col3:
        st.metric("Rotatable Bonds", "—")

    with col4:
        st.metric("Aromatic Proportion", "—")

    if st.button(
        "Predict Solubility",
        type="primary"
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
                "ML model will be connected here. "
                "The trained model will generate predicted LogS "
                "and corresponding solubility."
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
        [
            "Select polymer",
            "PVP K30",
            "Soluplus",
            "PEG 6000",
            "Poloxamer 188",
            "Poloxamer 407",
            "HPMC"
        ] + [
            x for x in custom_excipients.keys()
            if x not in [
                "PVP K30",
                "Soluplus",
                "PEG 6000",
                "Poloxamer 188",
                "Poloxamer 407",
                "HPMC"
            ]
        ]
    )

    if polymer != "Select polymer":

        st.success(f"Selected: {polymer}")

        st.info(
            "Solvent database will be connected here. "
            "Compatible solvents will be retrieved and ranked."
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

    col1, col2 = st.columns(2)

    with col1:

        drug = st.selectbox(
            "Select Drug",
            ["Select drug"] + drug_list,
            key="integrated_drug"
        )

    with col2:

        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient"] + excipient_list,
            key="integrated_excipient"
        )

    if st.button(
        "Run Integrated Screening",
        type="primary"
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

            st.write("1️⃣ HSP
