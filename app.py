import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

# =========================================================
# DRUGXPERT AI - APPLICATION
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ADMIN LOGIN
# =========================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"

DB_FILE = "drugxpert_db.json"

# =========================================================
# DEFAULT DATABASE
# =========================================================

DEFAULT_DATA = {
    "title": "DrugXpert AI",
    "subtitle": (
        "Integrated Computational Platform for Drug–Excipient "
        "Compatibility, Solubility Prediction and Solvent Selection"
    ),

    "welcome": "WELCOME TO DRUGXPERT AI",

    "about": (
        "DrugXpert AI is an integrated computational platform designed "
        "for drug–excipient compatibility assessment, solubility prediction, "
        "Hansen Solubility Parameter analysis and rational excipient selection."
    ),

    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "developer_info": (
        "Researcher working in pharmaceutics, computational drug delivery, "
        "AI/ML-assisted excipient selection and cyclodextrin-based drug "
        "delivery systems."
    ),

    "guide_name": "Guide Name",
    "guide_role": "Professor / Research Guide",
    "guide_info": (
        "Research guide working in pharmaceutics, formulation development "
        "and advanced drug delivery research."
    ),

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
# DATABASE FUNCTIONS
# =========================================================

def load_db():

    if os.path.exists(DB_FILE):

        try:

            with open(
                DB_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            merged = json.loads(
                json.dumps(DEFAULT_DATA)
            )

            for key, value in data.items():
                merged[key] = value

            return merged

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
# IMAGE FUNCTIONS
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
        '<img src="'
        + data_uri
        + '" style="width:'
        + str(width)
        + 'px;height:'
        + str(height)
        + 'px;object-fit:cover;border-radius:50%;'
        + 'border:4px solid white;'
        + 'box-shadow:0 8px 25px rgba(15,23,42,.18);">'
    )


# =========================================================
# HSP CALCULATION
# =========================================================

def hsp_distance(
    drug,
    excipient
):

    return math.sqrt(
        4 * (
            drug["dD"]
            - excipient["dD"]
        ) ** 2

        + (
            drug["dP"]
            - excipient["dP"]
        ) ** 2

        + (
            drug["dH"]
            - excipient["dH"]
        ) ** 2
    )


def compatibility_label(ra):

    if ra <= 3:
        return "Excellent compatibility"

    elif ra <= 5:
        return "Good compatibility"

    elif ra <= 8:
        return "Moderate compatibility"

    else:
        return "Low compatibility"


# =========================================================
# SESSION STATE
# =========================================================

if "db" not in st.session_state:
    st.session_state.db = load_db()

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

db = st.session_state.db


# =========================================================
# PREMIUM DRUGXPERT AI DESIGN
# =========================================================

st.markdown(
    """
<style>

.stApp {

    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(37,99,235,0.10),
            transparent 30%
        ),

        radial-gradient(
            circle at 95% 10%,
            rgba(6,182,212,0.08),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #F8FAFC 0%,
            #EEF4FF 100%
        );
}


.block-container {

    max-width: 1400px;

    padding-top: 1.4rem;

    padding-bottom: 3rem;
}


#MainMenu {
    visibility: hidden;
}


footer {
    visibility: hidden;
}


header {
    background: transparent !important;
}


/* =================================================
   BUTTONS
================================================= */

.stButton > button {

    border-radius: 12px !important;

    border: 0 !important;

    background:
        linear-gradient(
            90deg,
            #2563EB,
            #0891B2
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    min-height: 42px;

    box-shadow:
        0 8px 20px
        rgba(37,99,235,0.18);
}


.stButton > button:hover {

    transform: translateY(-1px);

}


/* =================================================
   INPUTS
================================================= */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {

    border-radius: 10px !important;

}


/* =================================================
   HERO
================================================= */

.hero {

    padding: 30px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1D4ED8 55%,
            #0891B2
        );

    color: white;

    box-shadow:
        0 18px 45px
        rgba(15,23,42,0.18);

    position: relative;

    overflow: hidden;

}


.hero h1 {

    margin: 0;

    font-size: 40px;

    font-weight: 900;

}


.hero p {

    margin: 8px 0 0 0;

    opacity: 0.92;

    font-size: 15px;

}


/* =================================================
   WELCOME
================================================= */

.dx-welcome {

    margin-top: 20px;

    padding: 32px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(30,64,175,0.98),
            rgba(8,145,178,0.96)
        );

    color: white;

    box-shadow:
        0 18px 45px
        rgba(15,23,42,0.15);

}


.dx-welcome h1 {

    margin: 0;

    font-size: 34px;

    font-weight: 900;

}


.dx-welcome p {

    margin: 10px 0 0 0;

    opacity: 0.92;

}


/* =================================================
   CARDS
================================================= */

.card {

    background:
        rgba(255,255,255,0.92);

    border:
        1px solid
        rgba(148,163,184,0.22);

    border-radius: 20px;

    padding: 22px;

    min-height: 190px;

    box-shadow:
        0 10px 32px
        rgba(15,23,42,0.07);

}


.card h3 {

    margin-top: 0;

    color: #0F172A;

}


.card p {

    color: #475569;

    line-height: 1.55;

}


/* =================================================
   PROFILE CARDS
================================================= */

.profile-card {

    background:
        rgba(255,255,255,0.94);

    border:
        1px solid
        rgba(148,163,184,0.22);

    border-radius: 22px;

    padding: 25px;

    text-align: center;

    box-shadow:
        0 10px 32px
        rgba(15,23,42,0.07);

}


.profile-card h3 {

    margin: 10px 0 4px 0;

}


.profile-card p {

    color: #64748B;

}


/* =================================================
   SECTION TITLE
================================================= */

.section-title {

    color: #0F172A;

    font-weight: 900;

    font-size: 25px;

    margin-top: 20px;

}


/* =================================================
   BACKGROUND WATERMARK
================================================= */

.watermark {

    position: fixed;

    right: 25px;

    bottom: 25px;

    z-index: 0;

    opacity: 0.035;

    pointer-events: none;

    font-size: 110px;

    font-weight: 900;

    transform: rotate(-12deg);

    color: #1D4ED8;

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# GLOBAL WATERMARK
# =========================================================

st.markdown(
    """
<div class="watermark">
    DrugXpert AI
</div>
""",
    unsafe_allow_html=True
)
# =========================================================
# LOGIN SCREEN
# =========================================================

if st.session_state.role is None:

    logo = db.get("logo", "")

    if logo:
        st.markdown(
            '<div style="text-align:center;">' +
            image_html(logo, 100, 100) +
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="hero">'
        '<h1>' + db["title"] + '</h1>'
        '<p>' + db["subtitle"] + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dx-welcome">'
        '<h1>' + db.get("welcome", "WELCOME TO DRUGXPERT AI") + '</h1>'
        '<p>Computational pharmaceutics, rational excipient selection and AI-assisted formulation screening.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.4, 1])

    with center:
        tab_part, tab_admin = st.tabs(
            ["Participant Login", "Admin Login"]
        )

        with tab_part:
            st.subheader("Enter as Participant")

            p_name = st.text_input(
                "Your Full Name",
                placeholder="e.g. Rahul Sharma"
            )

            p_dept = st.text_input(
                "Institution / Department",
                placeholder="e.g. Pharmaceutics Research Lab"
            )

            if st.button(
                "Enter Software",
                type="primary",
                use_container_width=True
            ):
                if p_name.strip():

                    st.session_state.role = "participant"
                    st.session_state.username = p_name.strip()

                    db["logs"].insert(
                        0,
                        {
                            "name": p_name.strip(),
                            "dept": p_dept.strip() or "General",
                            "time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        }
                    )

                    save_db(db)
                    st.rerun()

                else:
                    st.error(
                        "Please enter your name to continue."
                    )

        with tab_admin:
            st.subheader("Administrator Control Login")

            a_user = st.text_input(
                "Admin Username",
                key="login_admin_user"
            )

            a_pass = st.text_input(
                "Admin Password",
                type="password",
                key="login_admin_pass"
            )

            if st.button(
                "Login as Admin",
                type="primary",
                use_container_width=True
            ):

                if (
                    a_user.strip() == ADMIN_USERNAME
                    and a_pass == ADMIN_PASSWORD
                ):

                    st.session_state.role = "admin"
                    st.session_state.username = (
                        "Admin (" + a_user.strip() + ")"
                    )
                    st.session_state.current_page = "Home"

                    st.rerun()

                else:
                    st.error(
                        "Invalid Admin Username or Password."
                    )

    st.stop()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

nav_options = [
    "Home",
    "HSP Compatibility",
    "AI/ML Solubility",
    "Solvent Lookup",
    "Integrated Screening",
    "About"
]

if st.session_state.role == "admin":
    nav_options.append("Admin Control Panel")


with st.sidebar:

    if db.get("logo"):

        st.markdown(
            '<div style="text-align:center;">' +
            image_html(db["logo"], 72, 72) +
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        "## " + db["title"]
    )

    if st.session_state.role == "admin":

        st.success(
            "Logged in as: " +
            st.session_state.username
        )

    else:

        st.info(
            "Participant: " +
            st.session_state.username
        )

    st.markdown("---")

    current = st.session_state.current_page

    selected_nav = st.radio(
        "Navigation",
        nav_options,
        index=(
            nav_options.index(current)
            if current in nav_options
            else 0
        )
    )

    if selected_nav != current:

        st.session_state.current_page = selected_nav
        st.rerun()

    st.markdown("---")

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.role = None
        st.session_state.username = ""
        st.session_state.current_page = "Home"

        st.rerun()

    st.caption(
        "Computational Drug Formulation Platform"
    )


page = st.session_state.current_page


# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown(
        '<div class="hero">'
        '<h1>' + db["title"] + '</h1>'
        '<p>' + db["subtitle"] + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dx-welcome">'
        '<h1>' +
        db.get(
            "welcome",
            "WELCOME TO DRUGXPERT AI"
        ) +
        '</h1>'
        '<p>'
        'Integrated platform for compatibility screening, '
        'solubility prediction and solvent selection.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Core Modules'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="card">'
            '<h3>HSP Compatibility</h3>'
            '<p>'
            'Calculate Hansen distance (Ra) between a selected '
            'drug and excipient and rank compatibility.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Open HSP Compatibility",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "HSP Compatibility"
            )

            st.rerun()

    with c2:

        st.markdown(
            '<div class="card">'
            '<h3>AI/ML Solubility</h3>'
            '<p>'
            'Generate a descriptor-based screening estimate '
            'for logS and solubility using the selected '
            'drug-excipient pair.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Open AI/ML Solubility",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "AI/ML Solubility"
            )

            st.rerun()

    with c3:

        st.markdown(
            '<div class="card">'
            '<h3>Solvent Lookup</h3>'
            '<p>'
            'Find listed solvents for polymers and excipients '
            'and compare the available options.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Open Solvent Lookup",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "Solvent Lookup"
            )

            st.rerun()

    st.markdown("---")

    st.markdown(
        "## Integrated Screening"
    )

    st.info(
        "Drug → Excipient → HSP Compatibility → "
        "Descriptor Analysis → Solubility Screening → "
        "Solvent Selection → Recommendation"
    )

    if st.button(
        "Launch Integrated Screening",
        type="primary"
    ):

        st.session_state.current_page = (
            "Integrated Screening"
        )

        st.rerun()


# =========================================================
# HSP COMPATIBILITY
# =========================================================

elif page == "HSP Compatibility":

    st.title(
        "HSP Compatibility Screening"
    )

    st.write(
        "Screen drug-excipient compatibility using "
        "Hansen Solubility Parameters."
    )

    st.markdown("---")

    drug_list = (
        ["Select drug"] +
        list(db["drugs"].keys())
    )

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    if drug != "Select drug":

        d = db["drugs"][drug]

        st.markdown(
            "### Drug Parameters"
        )

        a, b, c, dcol = st.columns(4)

        a.metric(
            "delta D",
            str(d["dD"])
        )

        b.metric(
            "delta P",
            str(d["dP"])
        )

        c.metric(
            "delta H",
            str(d["dH"])
        )

        dcol.metric(
            "LogP",
            str(d["logP"])
        )

        exc_list = (
            ["Select excipient"] +
            list(db["excipients"].keys())
        )

        exc = st.selectbox(
            "Select Excipient",
            exc_list
        )

        if exc != "Select excipient":

            e = db["excipients"][exc]

            ra = hsp_distance(
                d,
                e
            )

            st.markdown(
                "### Compatibility Result"
            )

            x, y, z = st.columns(3)

            x.metric(
                "Hansen Distance (Ra)",
                f"{ra:.2f}"
            )

            y.metric(
                "Compatibility",
                compatibility_label(ra)
            )

            z.metric(
                "Excipient",
                exc
            )

            st.markdown(
                '<div class="card">'
                '<h3>Interpretation</h3>'
                '<p>'
                'Lower Ra indicates greater similarity between '
                'the Hansen solubility parameter coordinates of '
                'the drug and excipient.'
                '</p>'
                '</div>',
                unsafe_allow_html=True
            )

            ranking = []

            for name, ex in db["excipients"].items():

                value = hsp_distance(
                    d,
                    ex
                )

                ranking.append(
                    {
                        "Excipient": name,
                        "Ra": round(value, 3),
                        "Compatibility":
                            compatibility_label(value)
                    }
                )

            ranking.sort(
                key=lambda item: item["Ra"]
            )

            st.markdown(
                "### Excipient Ranking"
            )

            st.dataframe(
                ranking,
                use_container_width=True
            )


# =========================================================
# AI/ML SOLUBILITY
# =========================================================

elif page == "AI/ML Solubility":

    st.title(
        "AI/ML Solubility Screening"
    )

    st.write(
        "Descriptor-based screening estimate for "
        "drug-excipient systems."
    )

    st.warning(
        "This built-in calculation is a screening estimator, "
        "not a validated clinical model. Replace it with your "
        "trained XGBoost model and validated dataset when "
        "deploying a research model."
    )

    drug_list = (
        ["Select drug"] +
        list(db["drugs"].keys())
    )

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    if drug != "Select drug":

        exc_list = (
            ["Select excipient"] +
            list(db["excipients"].keys())
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

            # Screening estimate only
            log_s = (
                -0.010 * d["mw"]
                + 0.42 * (4.0 - d["logP"])
                - 0.12 * ra
            )

            log_s = max(
                -12.0,
                min(-1.0, log_s)
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
        "Lookup solvents listed for the selected "
        "excipient."
    )

    exc_list = (
        ["Select excipient"] +
        list(db["excipients"].keys())
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
                    '<h3>' +
                    solvent +
                    '</h3>'
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
        ["Select drug"] +
        list(db["drugs"].keys())
    )

    drug = st.selectbox(
        "Select Drug",
        drug_list
    )

    if drug != "Select drug":

        exc_list = (
            ["Select excipient"] +
            list(db["excipients"].keys())
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

            log_s = (
                -0.010 * d["mw"]
                + 0.42 * (4.0 - d["logP"])
                - 0.12 * ra
            )

            log_s = max(
                -12.0,
                min(-1.0, log_s)
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
        '<p>' +
        db.get("about", "") +
        '</p>'
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

        photo_html = (
            image_html(
                photo,
                120,
                120
            )
            if photo
            else ""
        )

        st.markdown(
            '<div class="profile-card">'
            + photo_html +
            '<h3>' +
            db.get(
                "developer_name",
                ""
            ) +
            '</h3>'
            '<p><b>' +
            db.get(
                "developer_role",
                ""
            ) +
            '</b></p>'
            '<p>' +
            db.get(
                "developer_info",
                ""
            ) +
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:

        photo = db.get(
            "guide_photo",
            ""
        )

        photo_html = (
            image_html(
                photo,
                120,
                120
            )
            if photo
            else ""
        )

        st.markdown(
            '<div class="profile-card">'
            + photo_html +
            '<h3>' +
            db.get(
                "guide_name",
                ""
            ) +
            '</h3>'
            '<p><b>' +
            db.get(
                "guide
