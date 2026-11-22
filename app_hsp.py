import streamlit as st

# =========================================================
# DRUGXPERT AI - CONNECTED APP
# Existing app.py remains untouched.
# HSP Compatibility is connected through hsp_compatibility.py
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# IMPORT NEW HSP MODULE
# ---------------------------------------------------------
from hsp_compatibility import run_hsp_compatibility

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
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
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 💊 DrugXpert AI")
    st.markdown("---")

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
    st.caption("Computational Drug Formulation Platform")

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>💊 DrugXpert AI</h1>
        <p>
        Integrated Computational Platform for Drug–Excipient Compatibility,
        Solubility Prediction and Solvent Selection
        </p>
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
            <p>
            Hansen Solubility Parameter based screening of
            drug–excipient compatibility using δD, δP, δH
            and Hansen distance (Ra).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>🤖 AI/ML Solubility</h3>
            <p>
            Molecular descriptor-based prediction of LogS
            and solubility for drug–excipient systems using
            machine learning models.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🧴 Solvent Lookup</h3>
            <p>
            Computational lookup and ranking of suitable
            solvents for selected polymers and excipients.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🔗 Integrated Screening")
    st.info(
        "Drug → Excipient → HSP Compatibility → Molecular Descriptor Analysis "
        "→ AI/ML Solubility Prediction → Solvent Selection → Final Recommendation"
    )

# ---------------------------------------------------------
# HSP MODULE - CONNECTED NEW MODULE
# ---------------------------------------------------------
elif page == "HSP Compatibility":

    st.title("🧪 HSP Compatibility Screening")

    st.write(
        "Admin-controlled HSP database with automatic Hansen distance (Ra) "
        "calculation and polymer compatibility ranking."
    )

    st.markdown("---")

    # Admin control for this new HSP module.
    # This does not modify the old app.py.
    is_admin = st.checkbox(
        "🔐 Admin Mode",
        value=False,
        help="Enable this only when you need to add or update HSP values."
    )

    run_hsp_compatibility(is_admin=is_admin)

# ---------------------------------------------------------
# AI/ML SOLUBILITY MODULE
# ---------------------------------------------------------
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
            ["Select drug", "Deflazacort", "Artemether", "Curcumin"]
        )

    with col2:
        excipient = st.selectbox(
            "Select Excipient",
            ["Select excipient", "PVP K30", "Soluplus", "PEG 6000"]
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

    if st.button("Predict Solubility"):
        st.info(
            "ML model will be connected here. "
            "The trained model will generate the predicted LogS "
            "and corresponding solubility value."
        )

# ---------------------------------------------------------
# SOLVENT LOOKUP
# ---------------------------------------------------------
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
        ]
    )

    if polymer != "Select polymer":
        st.success(f"Selected: {polymer}")
        st.info(
            "Solvent database will be connected here. "
            "Compatible solvents will be retrieved and ranked."
        )

# ---------------------------------------------------------
# INTEGRATED SCREENING
# ---------------------------------------------------------
elif page == "Integrated Screening":

    st.title("🔗 Integrated Drug–Excipient Screening")

    st.write(
        "Combine HSP compatibility, AI/ML solubility prediction "
        "and solvent selection in a single workflow."
    )

    st.markdown("---")

    drug = st.selectbox(
        "Select Drug",
        ["Select drug", "Deflazacort", "Artemether", "Curcumin"]
    )

    excipient = st.selectbox(
        "Select Excipient",
        ["Select excipient", "PVP K30", "Soluplus", "PEG 6000"]
    )

    if st.button("Run Integrated Screening"):
        st.info(
            "Integrated computational workflow will be activated "
            "after the HSP database, molecular descriptor dataset, "
            "ML model and solvent database are connected."
        )

        st.markdown("### Screening Workflow")
        st.write("1️⃣ HSP compatibility analysis")
        st.write("2️⃣ Molecular descriptor analysis")
        st.write("3️⃣ AI/ML solubility prediction")
        st.write("4️⃣ Solvent compatibility lookup")
        st.write("5️⃣ Final candidate recommendation")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
© 2026 DrugXpert AI | Integrated Computational Drug Formulation Platform
</div>
""", unsafe_allow_html=True)
