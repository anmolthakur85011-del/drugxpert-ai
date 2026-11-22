import streamlit as st
import json
import math
import os

HSP_DB_FILE = "hsp_database.json"

DEFAULT_HSP_DATABASE = {
    "drugs": {
        "Deflazacort": {"dD": 18.6, "dP": 8.4, "dH": 9.2},
        "Artemether": {"dD": 17.4, "dP": 5.1, "dH": 6.8},
        "Curcumin": {"dD": 19.2, "dP": 9.8, "dH": 12.4},
    },
    "polymers": {
        "PVP K30": {"dD": 18.8, "dP": 10.2, "dH": 11.5},
        "Soluplus": {"dD": 18.1, "dP": 8.6, "dH": 9.8},
        "PEG 6000": {"dD": 17.9, "dP": 9.1, "dH": 11.0},
        "Poloxamer 188": {"dD": 17.5, "dP": 7.4, "dH": 9.5},
        "Poloxamer 407": {"dD": 17.6, "dP": 7.2, "dH": 9.1},
        "HPMC": {"dD": 18.4, "dP": 9.5, "dH": 13.2},
    },
}

def load_hsp_database():
    if not os.path.exists(HSP_DB_FILE):
        save_hsp_database(DEFAULT_HSP_DATABASE)
    try:
        with open(HSP_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_HSP_DATABASE.copy()

def save_hsp_database(db):
    with open(HSP_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

def calculate_ra(drug, polymer):
    return math.sqrt(
        4 * (drug["dD"] - polymer["dD"]) ** 2
        + (drug["dP"] - polymer["dP"]) ** 2
        + (drug["dH"] - polymer["dH"]) ** 2
    )

def compatibility_label(ra):
    if ra <= 3:
        return "Excellent"
    if ra <= 5:
        return "Good"
    if ra <= 7:
        return "Moderate"
    return "Poor"

def run_hsp_compatibility(is_admin=False):
    db = load_hsp_database()

    st.markdown(
        "<h1>HSP Compatibility</h1>"
        "<p>Hansen Solubility Parameter based drug–polymer compatibility screening</p>",
        unsafe_allow_html=True,
    )

    if is_admin:
        st.subheader("🔐 HSP Database – Admin Control")
        tab1, tab2, tab3 = st.tabs(
            ["➕ Add / Update Drug", "➕ Add / Update Polymer", "🗂️ Database"]
        )

        with tab1:
            st.markdown("### Drug HSP Values")
            drug_name = st.text_input(
                "Drug Name", placeholder="e.g. Deflazacort", key="hsp_drug_name"
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                drug_d = st.number_input("δD (d value)", value=0.0, format="%.4f", key="hsp_drug_d")
            with c2:
                drug_p = st.number_input("δP (p value)", value=0.0, format="%.4f", key="hsp_drug_p")
            with c3:
                drug_h = st.number_input("δH (h value)", value=0.0, format="%.4f", key="hsp_drug_h")

            if st.button("💾 Save / Update Drug", use_container_width=True):
                if not drug_name.strip():
                    st.error("Please enter the drug name.")
                elif drug_d == 0 and drug_p == 0 and drug_h == 0:
                    st.error("Please enter valid HSP values.")
                else:
                    db["drugs"][drug_name.strip()] = {"dD": drug_d, "dP": drug_p, "dH": drug_h}
                    save_hsp_database(db)
                    st.success(f"{drug_name.strip()} saved successfully.")
                    st.rerun()

        with tab2:
            st.markdown("### Polymer / Excipient HSP Values")
            polymer_name = st.text_input(
                "Polymer / Excipient Name", placeholder="e.g. PVP K30", key="hsp_polymer_name"
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                polymer_d = st.number_input("δD (d value)", value=0.0, format="%.4f", key="hsp_polymer_d")
            with c2:
                polymer_p = st.number_input("δP (p value)", value=0.0, format="%.4f", key="hsp_polymer_p")
            with c3:
                polymer_h = st.number_input("δH (h value)", value=0.0, format="%.4f", key="hsp_polymer_h")

            if st.button("💾 Save / Update Polymer", use_container_width=True):
                if not polymer_name.strip():
                    st.error("Please enter the polymer/excipient name.")
                elif polymer_d == 0 and polymer_p == 0 and polymer_h == 0:
                    st.error("Please enter valid HSP values.")
                else:
                    db["polymers"][polymer_name.strip()] = {
                        "dD": polymer_d, "dP": polymer_p, "dH": polymer_h
                    }
                    save_hsp_database(db)
                    st.success(f"{polymer_name.strip()} saved successfully.")
                    st.rerun()

        with tab3:
            st.markdown("### Current HSP Database")
            st.markdown("#### Drugs")
            st.dataframe(
                [
                    {"Drug": n, "δD": v["dD"], "δP": v["dP"], "δH": v["dH"]}
                    for n, v in db["drugs"].items()
                ],
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("#### Polymers / Excipients")
            st.dataframe(
                [
                    {"Polymer / Excipient": n, "δD": v["dD"], "δP": v["dP"], "δH": v["dH"]}
                    for n, v in db["polymers"].items()
                ],
                use_container_width=True,
                hide_index=True,
            )

    st.markdown("## 🔎 Search Drug")
    if not db["drugs"]:
        st.warning("No drug HSP data is available.")
        return

    selected_drug = st.selectbox(
        "Select / Search Drug", sorted(db["drugs"].keys()), key="hsp_user_drug"
    )
    drug = db["drugs"][selected_drug]

    st.markdown("### Drug HSP Parameters")
    d1, d2, d3 = st.columns(3)
    d1.metric("δD", f'{drug["dD"]:.4f}')
    d2.metric("δP", f'{drug["dP"]:.4f}')
    d3.metric("δH", f'{drug["dH"]:.4f}')

    results = []
    for polymer_name, polymer in db["polymers"].items():
        ra = calculate_ra(drug, polymer)
        results.append({
            "Polymer / Excipient": polymer_name,
            "δD": polymer["dD"],
            "δP": polymer["dP"],
            "δH": polymer["dH"],
            "Ra": ra,
            "Compatibility": compatibility_label(ra),
        })

    results.sort(key=lambda x: x["Ra"])
    for rank, item in enumerate(results, start=1):
        item["Rank"] = rank

    display_results = [
        {
            "Rank": item["Rank"],
            "Polymer / Excipient": item["Polymer / Excipient"],
            "δD": round(item["δD"], 4),
            "δP": round(item["δP"], 4),
            "δH": round(item["δH"], 4),
            "Ra": round(item["Ra"], 4),
            "Compatibility": item["Compatibility"],
        }
        for item in results
    ]

    st.markdown("### 🏆 Polymer Compatibility Ranking")
    st.dataframe(display_results, use_container_width=True, hide_index=True)

    if display_results:
        best = display_results[0]
        st.success(
            f'🥇 Rank 1: {best["Polymer / Excipient"]} — Lowest Ra = {best["Ra"]:.4f}'
        )

if __name__ == "__main__":
    st.set_page_config(
        page_title="DrugXpert AI - HSP Compatibility",
        page_icon="🧪",
        layout="wide",
    )
    st.title("DrugXpert AI")
    st.caption("HSP Compatibility Module")
    admin_mode = st.checkbox("Admin Mode", value=False)
    run_hsp_compatibility(is_admin=admin_mode)
