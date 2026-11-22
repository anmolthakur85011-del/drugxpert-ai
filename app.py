import streamlit as st
import math
from admin import (
    init_auth_and_sidebar,
    render_admin_panel,
    image_to_base64
)

# =========================================================
# DRUGXPERT AI - COMPLETE APPLICATION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_auth_and_sidebar()

content = st.session_state.site_content
custom_db = st.session_state.custom_db

# =========================================================
# DEFAULT DRUGS & EXCIPIENTS + CUSTOM MERGE
# =========================================================

DEFAULT_DRUGS = {
    "Deflazacort": {
        "dD": 18.6,
        "dP": 8.4,
        "dH": 9.2,
        "logP": 2.8,
        "mw": 441.5,
        "rot": 4,
        "arom": 0.19
    },
    "Artemether": {
        "dD": 17.4,
        "dP": 5.1,
        "dH": 6.8,
        "logP": 3.1,
        "mw": 298.4,
        "rot": 1,
        "arom": 0.00
    },
    "Curcumin": {
        "dD": 19.2,
        "dP": 9.8,
        "dH": 12.4,
        "logP": 3.2,
        "mw": 368.4,
        "rot": 8,
        "arom": 0.44
    }
}

DEFAULT_EXCIPIENTS = {
    "PVP K30": {
        "dD": 18.8,
        "dP": 10.2,
        "dH": 11.5,
        "solvents": ["Water", "Ethanol", "Methanol", "Dichloromethane"]
    },
    "Soluplus": {
        "dD": 18.1,
        "dP": 8.6,
        "dH": 9.8,
        "solvents": ["Ethanol", "Acetone", "Methanol", "Dimethylformamide"]
    },
    "PEG 6000": {
        "dD": 17.9,
        "dP": 9.1,
        "dH": 11.0,
        "solvents": ["Water", "Ethanol", "Chloroform", "Acetonitrile"]
    },
    "Poloxamer 188": {
        "dD": 17.5,
        "dP": 7.4,
        "dH": 9.5,
        "solvents": ["Water", "Ethanol", "Isopropanol"]
    },
    "Poloxamer 407": {
        "dD": 17.6,
        "dP": 7.2,
        "dH": 9.1,
        "solvents": ["Water", "Ethanol", "Methanol"]
    },
    "HPMC": {
        "dD": 18.4,
        "dP": 9.5,
        "dH": 13.2,
        "solvents": ["Water", "Ethanol-Water Mixture", "Dichloromethane-Methanol"]
    }
}

ALL_DRUGS = {**DEFAULT_DRUGS, **custom_db.get("custom_drugs", {})}
ALL_EXCIPIENTS = {**DEFAULT_EXCIPIENTS, **custom_db.get("custom_excipients", {})}


# =========================================================
# HELPERS
# =========================================================

def image_html(data_uri, width=120, height=120):
    if not data_uri:
        return ""
    return (
        '<img src="' + data_uri + '" '
        'style="width:' + str(width) +
        'px;height:' + str(height) +
        'px;object-fit:cover;'
        'border-radius:50%;'
        'border:4px solid white;'
        'box-shadow:0 8px 25px rgba(15,23,42,.18);margin-bottom:10px;">'
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


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    logo_uri = image_to_base64(content.get("logo_file", ""))
    logo_html = (
        f'<img src="{logo_uri}" style="width:72px;height:72px;object-fit:contain;margin-bottom:6px;">'
        if logo_uri else ""
    )
    st.markdown(
        f"""
        <div style="text-align:center;padding:12px;font-size:25px;font-weight:800;color:#55e6ee;">
            {logo_html}<div>💊 DrugXpert AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    if st.session_state.role == "admin":
        st.success(f"🛡️ {st.session_state.username}")
    else:
        st.info(f"👤 {st.session_state.username}")

    menu = [
        "Home",
        "HSP Compatibility",
        "AI/ML Solubility",
        "Solvent Lookup",
        "Integrated Screening",
        "About"
    ]
    if st.session_state.role == "admin":
        menu.append("Admin Control Panel")

    page = st.radio("Navigation", menu, label_visibility="collapsed")
    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()


# =========================================================
# HOME
# =========================================================

if page == "Home":
    logo_uri = image_to_base64(content.get("logo_file", ""))
    logo_tag = (
        f'<img src="{logo_uri}" style="width:95px;height:95px;object-fit:contain;margin-bottom:10px;">'
        if logo_uri else ""
    )
    st.markdown(
        f"""
        <div class="dx-hero">
            {logo_tag}
            <div class="dx-hero-title">{content.get("welcome_title", "WELCOME TO DRUGXPERT AI")}</div>
            <div class="dx-hero-subtitle">{content.get("welcome_subtitle", "")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">'
        '<h2>' + content.get("about_title", "About DrugXpert AI") + '</h2>'
        '<p>' + content.get("about_text", "") + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Research Team")
    c1, c2 = st.columns(2)
    with c1:
        photo = image_to_base64(content.get("developer_photo", ""))
        photo_html = image_html(photo, 120, 120) if photo else ""
        st.markdown(
            '<div class="profile-card">'
            + photo_html
            + '<h3>' + content.get("developer_name", "") + '</h3>'
            + '<p><b>' + content.get("developer_role", "") + '</b></p>'
            + '<p>' + content.get("developer_bio", "") + '</p>'
            + '</div>',
            unsafe_allow_html=True
        )
    with c2:
        photo = image_to_base64(content.get("guide_photo", ""))
        photo_html = image_html(photo, 120, 120) if photo else ""
        st.markdown(
            '<div class="profile-card">'
            + photo_html
            + '<h3>' + content.get("guide_name", "") + '</h3>'
            + '<p><b>' + content.get("guide_role", "") + '</b></p>'
            + '<p>' + content.get("guide_bio", "") + '</p>'
            + '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# HSP COMPATIBILITY
# =========================================================

elif page == "HSP Compatibility":
    st.title("HSP Compatibility")
    st.write("Calculate Hansen Solubility Parameter distance (Ra) between drug and excipient.")

    drug = st.selectbox("Select Drug", ["Select drug"] + list(ALL_DRUGS.keys()))
    if drug != "Select drug":
        exc = st.selectbox("Select Excipient", ["Select excipient"] + list(ALL_EXCIPIENTS.keys()))
        if exc != "Select excipient":
            d = ALL_DRUGS[drug]
            e = ALL_EXCIPIENTS[exc]
            ra = hsp_distance(d, e)
            label = compatibility_label(ra)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("HSP Ra", f"{ra:.3f}")
            c2.metric("ΔδD", f"{abs(d['dD'] - e['dD']):.2f}")
            c3.metric("ΔδP", f"{abs(d['dP'] - e['dP']):.2f}")
            c4.metric("ΔδH", f"{abs(d['dH'] - e['dH']):.2f}")

            if ra <= 3:
                st.success(label)
            elif ra <= 5:
                st.info(label)
            elif ra <= 7:
                st.warning(label)
            else:
                st.error(label)


# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":
    st.title("AI/ML Solubility Screening")
    st.write("Descriptor-based screening estimate for drug-excipient systems.")
    st.warning(
        "This built-in calculation is a screening estimator, "
        "not a validated clinical model. Replace it with your "
        "trained XGBoost model and validated dataset when deploying "
        "a research model."
    )

    drug_list = ["Select drug"] + list(ALL_DRUGS.keys())
    drug = st.selectbox("Select Drug", drug_list)

    if drug != "Select drug":
        exc_list = ["Select excipient"] + list(ALL_EXCIPIENTS.keys())
        exc = st.selectbox("Select Excipient", exc_list)

        if exc != "Select excipient":
            d = ALL_DRUGS[drug]
            e = ALL_EXCIPIENTS[exc]
            ra = hsp_distance(d, e)
            log_s = screening_log_s(d, ra)
            ug_ml = (10 ** log_s) * d["mw"] * 1000

            a, b, c = st.columns(3)
            a.metric("Estimated logS", f"{log_s:.3f}")
            b.metric("Estimated Solubility", f"{ug_ml:.3f} µg/mL")
            c.metric("HSP Ra", f"{ra:.3f}")

            st.markdown("### Input Descriptors")
            descriptor_data = {
                "Descriptor": [
                    "Molecular Weight",
                    "LogP",
                    "Rotatable Bonds",
                    "Aromatic Proportion"
                ],
                "Value": [
                    d["mw"],
                    d["logP"],
                    d["rot"],
                    d["arom"]
                ]
            }
            st.dataframe(descriptor_data, use_container_width=True)


# =========================================================
# SOLVENT LOOKUP
# =========================================================

elif page == "Solvent Lookup":
    st.title("Solvent Lookup")
    st.write("Lookup solvents listed for the selected excipient.")

    exc_list = ["Select excipient"] + list(ALL_EXCIPIENTS.keys())
