import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

# =========================================================
# DRUGXPERT AI - COMPLETE APPLICATION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"
DB_FILE = "drugxpert_db.json"

# =========================================================
# DEFAULT DATABASE
# =========================================================

DEFAULT_DATA = {
    "title": "DrugXpert AI",
    "subtitle": "Integrated Computational Platform for Drug–Excipient Compatibility, Solubility Prediction and Solvent Selection",
    "welcome": "WELCOME TO DRUGXPERT AI",
    "about": "DrugXpert AI is an integrated computational platform designed for drug–excipient compatibility assessment, solubility prediction, Hansen Solubility Parameter analysis and rational excipient selection.",
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "developer_info": "Researcher working in pharmaceutics, computational drug delivery, AI/ML-assisted excipient selection and cyclodextrin-based drug delivery systems.",
    "guide_name": "Guide Name",
    "guide_role": "Professor / Research Guide",
    "guide_info": "Research guide working in pharmaceutics, formulation development and advanced drug delivery research.",
    "logo": "",
    "developer_photo": "",
    "guide_photo": "",
    "drugs": {
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
    },
    "excipients": {
        "PVP K30": {
            "dD": 18.8,
            "dP": 10.2,
            "dH": 11.5,
            "solvents": [
                "Water",
                "Ethanol",
                "Methanol",
                "Dichloromethane"
            ]
        },
        "Soluplus": {
            "dD": 18.1,
            "dP": 8.6,
            "dH": 9.8,
            "solvents": [
                "Ethanol",
                "Acetone",
                "Methanol",
                "Dimethylformamide"
            ]
        },
        "PEG 6000": {
            "dD": 17.9,
            "dP": 9.1,
            "dH": 11.0,
            "solvents": [
                "Water",
                "Ethanol",
                "Chloroform",
                "Acetonitrile"
            ]
        },
        "Poloxamer 188": {
            "dD": 17.5,
            "dP": 7.4,
            "dH": 9.5,
            "solvents": [
                "Water",
                "Ethanol",
                "Isopropanol"
            ]
        },
        "Poloxamer 407": {
            "dD": 17.6,
            "dP": 7.2,
            "dH": 9.1,
            "solvents": [
                "Water",
                "Ethanol",
                "Methanol"
            ]
        },
        "HPMC": {
            "dD": 18.4,
            "dP": 9.5,
            "dH": 13.2,
            "solvents": [
                "Water",
                "Ethanol-Water Mixture",
                "Dichloromethane-Methanol"
            ]
        }
    },
    "logs": []
}

# =========================================================
# DATABASE
# =========================================================

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(
                DB_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                saved = json.load(f)

            data = json.loads(
                json.dumps(DEFAULT_DATA)
            )

            data.update(saved)

            return data

        except Exception:
            pass

    return json.loads(
        json.dumps(DEFAULT_DATA)
    )


def save_db(data):
    with open(
        DB_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# HELPERS
# =========================================================

def file_to_b64(uploaded_file):

    if uploaded_file is None:
        return ""

    raw = uploaded_file.getvalue()

    mime = uploaded_file.type or "image/png"

    return (
        "data:"
        + mime
        + ";base64,"
        + base64.b64encode(raw).decode("utf-8")
    )


def image_html(
    data_uri,
    width=120,
    height=120
):

    if not data_uri:
        return ""

    return (
        '<img src="' + data_uri + '" '
        'style="width:' + str(width) +
        'px;height:' + str(height) +
        'px;object-fit:cover;'
        'border-radius:50%;'
        'border:4px solid white;'
        'box-shadow:0 8px 25px '
        'rgba(15,23,42,.18);">'
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


def screening_log_s(drug, excipient, ra):
    base = 1.0 / (1.0 + ra)
    return round(-2.0 + (base * 4.0), 3)

        ) ** 2# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":

    st.title(
        "AI/ML Solubility Screening"
    )

    st.write(
        "Descriptor-based screening estimate for drug-excipient systems."
    )

    st.warning(
        "This built-in calculation is a screening estimator, "
        "not a validated clinical model. Replace it with your "
        "trained XGBoost model and validated dataset when deploying "
        "a research model."
    )

    drug_list = (
        ["Select drug"]
        + list(db["drugs"].keys())
    )

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    if drug != "Select drug":

        exc_list = (
            ["Select excipient"]
            + list(db["excipients"].keys())
        )

        exc = st.selectbox(
            "Select Excipient",
            exc_list
        )

        if exc != "Select excipient":

            d = db["drugs"][drug]
            e = db["excipients"][exc]

            ra = hsp_distance(
                d,
                e
            )

            log_s = screening_log_s(
                d,
                ra
            )

            ug_ml = (
                (10 ** log_s)
                * d["mw"]
                * 1000
            )

            a, b, c = st.columns(3)

            a.metric(
                "Estimated logS",
                f"{log_s:.3f}"
            )

            b.metric(
                "Estimated Solubility",
                f"{ug_ml:.3f} µg/mL"
            )

            c.metric(
                "HSP Ra",
                f"{ra:.3f}"
            )

            st.markdown(
                "### Input Descriptors"
            )

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

            st.dataframe(
                descriptor_data,
                use_container_width=True
            )


# =========================================================
# SOLVENT LOOKUP
# =========================================================

elif page == "Solvent Lookup":

    st.title(
        "Solvent Lookup"
    )

    st.write(
        "Lookup solvents listed for the selected excipient."
    )

    exc_list = (
        ["Select excipient"]
        + list(db["excipients"].keys())
    )

    exc = st.selectbox(
        "Select Excipient / Polymer",
        exc_list
    )

    if exc != "Select excipient":

        solvents = db["excipients"][exc].get(
            "solvents",
            []
        )

        if solvents:

            st.success(
                "Available solvents found: "
                + str(len(solvents))
            )

            for solvent in solvents:

                st.markdown(
                    '<div class="card" '
                    'style="min-height:0;margin-bottom:10px;">'
                    '<h3>'
                    + solvent
                    + '</h3>'
                    '</div>',
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No solvent data is currently stored "
                "for this excipient."
            )


# =========================================================
# INTEGRATED SCREENING
# =========================================================

elif page == "Integrated Screening":

    st.title(
        "Integrated Screening"
    )

    st.write(
        "Combine HSP compatibility, descriptor screening "
        "and solvent information."
    )

    drug_list = (
        ["Select drug"]
        + list(db["drugs"].keys())
    )

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    if drug != "Select drug":

        exc_list = (
            ["Select excipient"]
            + list(db["excipients"].keys())
        )

        exc = st.selectbox(
            "Select Excipient",
            exc_list
        )

        if exc != "Select excipient":

            d = db["drugs"][drug]
            e = db["excipients"][exc]

            ra = hsp_distance(
                d,
                e
            )

            log_s = screening_log_s(
                d,
                ra
            )

            ug_ml = (
                (10 ** log_s)
                * d["mw"]
                * 1000
            )

            st.markdown(
                "### Integrated Result"
            )

            a, b, c, dcol = st.columns(4)

            a.metric(
                "Drug",
                drug
            )

            b.metric(
                "Excipient",
                exc
            )

            c.metric(
                "HSP Ra",
                f"{ra:.2f}"
            )

            dcol.metric(
                "Estimated µg/mL",
                f"{ug_ml:.2f}"
            )

            st.markdown(
                "### Recommendation"
            )

            if ra <= 3:

                st.success(
                    "High compatibility by HSP screening. "
                    "This pair can be prioritized for further "
                    "experimental validation."
                )

            elif ra <= 5:

                st.info(
                    "Good compatibility by HSP screening. "
                    "Consider this pair for further screening "
                    "and formulation studies."
                )

            else:

                st.warning(
                    "Lower HSP compatibility. "
                    "Consider other excipients or confirm "
                    "experimentally."
                )

            st.markdown(
                "### Solvent Information"
            )

            solvents = e.get(
                "solvents",
                []
            )

            if solvents:

                st.write(
                    ", ".join(solvents)
                )

            else:

                st.write(
                    "No solvent information stored."
                )


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.title(
        "About DrugXpert AI"
    )

    st.markdown(
        '<div class="card">'
        '<h2>About the Software</h2>'
        '<p>'
        + db.get("about", "")
        + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "## Research Team"
    )

    c1, c2 = st.columns(2)

    with c1:

        photo = db.get(
            "developer_photo",
            ""
        )

        if photo:

            photo_html = image_html(
                photo,
                120,
                120
            )

        else:

            photo_html = ""

        st.markdown(
            '<div class="profile-card">'
            + photo_html
            + '<h3>'
            + db.get(
                "developer_name",
                ""
            )
            + '</h3>'
            + '<p><b>'
            + db.get(
                "developer_role",
                ""
            )
            + '</b></p>'
            + '<p>'
            + db.get(
                "developer_info",
                ""
            )
            + '</p>'
            + '</div>',
            unsafe_allow_html=True
        )

    with c2:

        photo = db.get(
            "guide_photo",
            ""
        )

        if photo:

            photo_html = image_html(
                photo,
                120,
                120
            )

        else:

            photo_html = ""

        st.markdown(
            '<div class="profile-card">'
            + photo_html
            + '<h3>'
            + db.get(
                "guide_name",
                ""
            )
            + '</h3>'
            + '<p><b>'
            + db.get(
                "guide_role",
                ""
            )
            + '</b></p>'
            + '<p>'
            + db.get(
                "guide_info",
                ""
            )
            + '</p>'
            + '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# ADMIN CONTROL PANEL
# =========================================================

elif page == "AI/ML Solubility":
