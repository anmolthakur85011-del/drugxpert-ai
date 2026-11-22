import streamlit as st
import json
import os
import math
import base64
from datetime import datetime

# =========================================================
# DRUGXPERT AI - COMPLETE INTEGRATED PLATFORM
# =========================================================

st.set_page_config(
    page_title="DrugXpert AI | Computational Pharmaceutics Platform",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "drugxpert123"
DB_FILE = "drugxpert_db.json"

# =========================================================
# DEFAULT SCIENTIFIC SVG LOGO (PHARMA + AI + MOLECULE)
# =========================================================

DEFAULT_SVG_LOGO = """
<svg xmlns="http://w3.org" viewBox="0 0 220 220" width="220" height="220">
  <defs>
    <linearGradient id="dxGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00e5ff"/>
      <stop offset="55%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#ff6b8b"/>
    </linearGradient>
    <linearGradient id="dxGrad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f2942"/>
      <stop offset="100%" stop-color="#163b5c"/>
    </linearGradient>
  </defs>
  <!-- Outer AI Hexagonal Ring -->
  <polygon points="110,12 195,61 195,159 110,208 25,159 25,61"
           fill="url(#dxGrad2)" stroke="url(#dxGrad1)" stroke-width="5"/>
  <!-- Inner Neural Orbit -->
  <circle cx="110" cy="110" r="68" fill="none" stroke="#55e6ee" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.7"/>
  <!-- Molecular Benzene Ring Left -->
  <polygon points="78,76 98,64 118,76 118,99 98,111 78,99"
           fill="none" stroke="#55e6ee" stroke-width="3"/>
  <!-- Pharmaceutical Capsule Right -->
  <g transform="translate(128,118) rotate(-38)">
    <rect x="-28" y="-13" width="56" height="26" rx="13" fill="none" stroke="#ff7c96" stroke-width="3.5"/>
    <path d="M 0,-13 L 15,-13 A 13,13 0 0 1 15,13 L 0,13 Z" fill="#ff7c96" opacity="0.85"/>
  </g>
  <!-- AI Neural Nodes -->
  <circle cx="78" cy="76" r="4.5" fill="#ffffff"/>
  <circle cx="98" cy="64" r="4.5" fill="#55e6ee"/>
  <circle cx="118" cy="76" r="4.5" fill="#55e6ee"/>
  <circle cx="78" cy="99" r="4.5" fill="#55e6ee"/>
  <circle cx="98" cy="111" r="5" fill="#ff7c96"/>
  <line x1="98" y1="111" x2="116" y2="118" stroke="#ffffff" stroke-width="2" stroke-dasharray="3 2"/>
  <!-- Monogram -->
  <text x="110" y="176" text-anchor="middle" fill="#eaf7ff" font-family="sans-serif" font-size="16" font-weight="800" letter-spacing="2">DX·AI</text>
</svg>
""".strip()

DEFAULT_LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(
    DEFAULT_SVG_LOGO.encode("utf-8")
).decode("utf-8")

# =========================================================
# DEFAULT DATABASE & CONTENT
# =========================================================

DEFAULT_DATA = {
    "title": "DrugXpert AI",
    "welcome": "WELCOME TO DRUGXPERT AI",
    "subtitle": (
        "Integrated Computational Platform for Drug–Excipient Compatibility, "
        "Hansen Solubility Parameter (HSP) Analysis, AI/ML Solubility Prediction "
        "and Rational Solvent Selection"
    ),
    "about": (
        "DrugXpert AI is an integrated computational platform developed for advanced "
        "pharmaceutical research and rational formulation design. It unifies "
        "drug–excipient compatibility screening, Hansen Solubility Parameter (HSP) "
        "distance (Ra) modeling, AI/ML-assisted aqueous and polymer-mediated solubility "
        "prediction, systematic excipient selection, solvent lookup, and multi-parameter "
        "integrated screening to accelerate computational drug-delivery research."
    ),
    "software_features": (
        "HSP Compatibility & Ra Distance Modeling\n"
        "AI/ML-Assisted Solubility Screening\n"
        "Polymer & Excipient Solvent Lookup\n"
        "Multi-Parameter Integrated Formulation Screening"
    ),
    "developer_name": "Anmol Rajan",
    "developer_role": "M.Pharm (Pharmaceutics) Research Scholar",
    "developer_info": (
        "Pharmaceutical researcher specializing in computational pharmaceutics, "
        "AI/ML-assisted excipient selection, solid dispersion modeling, and "
        "cyclodextrin-based drug delivery systems."
    ),
    "developer_interests": (
        "Computational Pharmaceutics, Hansen Solubility Parameters, AI/ML Drug Delivery, "
        "Amorphous Solid Dispersions, Cyclodextrin Complexation"
    ),
    "guide_name": "Prof. (Dr.) Research Guide",
    "guide_role": "Professor & Research Supervisor (Pharmaceutics)",
    "guide_info": (
        "Academic research supervisor mentoring formulation development, "
        "preformulation science, novel drug delivery systems, and computational "
        "pharmaceutical modeling."
    ),
    "guide_interests": (
        "Novel Drug Delivery Systems, Preformulation & Compatibility, "
        "Solubility Enhancement, Quality by Design (QbD)"
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
# DATABASE PERSISTENCE
# =========================================================

def load_db():
    data = json.loads(json.dumps(DEFAULT_DATA))
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                for key, val in saved.items():
                    if key in ("drugs", "excipients") and isinstance(val, dict):
                        data[key].update(val)
                    else:
                        data[key] = val
        except Exception:
            pass
    return data


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================================================
# IMAGE & SCIENTIFIC CALCULATION HELPERS
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


def get_active_logo(db):
    custom_logo = db.get("logo", "").strip()
    return custom_logo if custom_logo else DEFAULT_LOGO_URI


def avatar_html(data_uri, fallback_initials="DX", size=115):
    if data_uri:
        return (
            f'<img src="{data_uri}" '
            f'style="width:{size}px;height:{size}px;object-fit:cover;'
            f'border-radius:50%;border:3px solid #55e6ee;'
            f'box-shadow:0 8px 25px rgba(0,229,255,0.25);margin-bottom:14px;">'
        )
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'margin:0 auto 14px auto;display:flex;align-items:center;'
        f'justify-content:center;font-size:32px;font-weight:800;'
        f'color:#55e6ee;background:linear-gradient(135deg,#0c2d48,#144266);'
        f'border:3px solid rgba(85,230,238,0.45);'
        f'box-shadow:0 8px 25px rgba(0,0,0,0.3);">{fallback_initials}</div>'
    )


def hsp_distance(d1, d2):
    return math.sqrt(
        4.0 * (float(d1["dD"]) - float(d2["dD"])) ** 2
        + (float(d1["dP"]) - float(d2["dP"])) ** 2
        + (float(d1["dH"]) - float(d2["dH"])) ** 2
    )


def compatibility_label(ra):
    if ra <= 3.0:
        return "Excellent Compatibility (Miscible / High Affinity)"
    elif ra <= 5.0:
        return "Good Compatibility (Favorable Interaction)"
    elif ra <= 7.0:
        return "Moderate Compatibility (Borderline / Screen Further)"
    else:
        return "Poor Compatibility (Immiscible / Low Affinity)"
        


