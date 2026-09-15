import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# SHIPPING COMPANY
# HEALTH, SAFETY, SECURITY & ENVIRONMENTAL
# OPERATIONS CONTROL CENTRE
# ============================================================

st.set_page_config(
    page_title="SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MASTER DATA - 21 VESSELS
# ============================================================

VESSELS = [
    "ASL MANTRUS",
    "ASL MULIA",
    "ASL SENTOSA",
    "ASL VICTORY",
    "ASL INTAN",
    "ASL GEMINI",
    "ASL BEAVER",
    "ASL CRESST",
    "ASL CALYPSO",
    "ASL PHOENIX",
    "ASL MARINE 8",
    "AST LEGEND",
    "TERAS HYDRA",
    "AST MAJU",
    "KARYA ABADI 8",
    "NUSANTARA ABADI 1",
    "CAPITOL T2002",
    "CAPITOL T2001",
    "TB1000-06",
    "TB1000-07",
    "WHALE 3",
]

# ============================================================
# SESSION STATE
# ============================================================

if "incidents" not in st.session_state:
    st.session_state.incidents = []

if "near_misses" not in st.session_state:
    st.session_state.near_misses = []

if "actions" not in st.session_state:
    st.session_state.actions = []

if "risk_register" not in st.session_state:
    st.session_state.risk_register = []

# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 30px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .company-box {
        padding: 15px;
        border: 1px solid #cccccc;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        padding: 25px 5px 10px 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚓ SHIPPING COMPANY HSSE")
st.sidebar.caption("Operations Control Centre")

menu = st.sidebar.radio(
    "CONTROL CENTRE",
    [
        "📊 Executive Dashboard",
        "🏢 Company & Shore HSSE",
        "🚢 Fleet HSSE",
        "🦺 Safety Management",
        "❤️ Health Management",
        "🔐 Security Management",
        "🌱 Environmental Management",
        "⚠️ Incident & Near Miss",
        "🧭 Risk Management",
        "🚨 Emergency Response",
        "📋 Compliance & Audit",
        "✅ Corrective Actions",
        "📈 HSSE KPI",
        "🤖 AI HSSE Intelligence",
    ]
)

st.sidebar.divider()

selected_vessel = st.sidebar.selectbox(
    "Selected Vessel",
    ["ALL VESSELS"] + VESSELS
)

st.sidebar.write("Fleet size:", len(VESSELS))
st.sidebar.write("System:", "ONLINE")
st.sidebar.write("Updated:", datetime.now().strftime("%d-%m-%Y %H:%M"))

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
    ⚓ SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL
    OPERATIONS CONTROL CENTRE
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
    Company • Shore Office • Fleet • Vessel • Personnel • Contractors •
    Risk • Compliance • Emergency Response • HSSE Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if menu == "📊 Executive Dashboard":

    st.header("📊 HSSE Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Fleet", len(VESSELS))
    col2.metric("Active Vessels", len(VESSELS))
    col3.metric("Open HSSE Actions", len(st.session_state.actions))
    col4.metric("Critical Events", 0)

    st.divider()

    st.subheader("🏢 Company HSSE Status")

    company_status = pd.DataFrame(
        {
            "Area": [
                "Health",
                "Safety",
                "Security",
                "Environment",
                "Emergency Preparedness",
                "Compliance",
            ],
            "Status": [
                "MONITORING",
                "MONITORING",
                "MONITORING",
                "MONITORING",
                "READY",
                "MONITORING",
            ],
        }
    )

    st.dataframe(
        company_status,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🚢 Fleet HSSE Overview")

    fleet_data = pd.DataFrame(
        {
            "Vessel": VESSELS,
            "HSSE Status": ["MONITORING"] * len(VESSELS),
            "Open Incident": [0] * len(VESSELS),
            "Near Miss": [0] * len(VESSELS),
            "Open Actions": [0] * len(VESSELS),
        }
    )

    st.dataframe(
        fleet_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# COMPANY & SHORE HSSE
# ============================================================

elif menu == "🏢 Company & Shore HSSE":

    st.header("🏢 Company & Shore HSSE Management")

    st.info(
        "Central HSSE control for shipping company management, "
        "shore office, marine operations, technical department, "
        "crewing, contractors and fleet."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Company HSSE Functions")
        st.write("• HSSE Policy & Objectives")
        st.write("• Management Review")
        st.write("• Safety Management System")
        st.write("• Management of Change")
        st.write("• Contractor HSSE")
        st.write("• Training & Competency")

    with col2:
        st.subheader("Shore Management")
        st.write("• Marine Operations")
        st.write("• Technical Department")
        st.write("• Crewing Department")
        st.write("• DPA / Safety Department")
        st.write("• Emergency Response Team")
        st.write("• Senior Management")

# ============================================================
# FLEET HSSE
# ============================================================

elif menu == "🚢 Fleet HSSE":

    st.header("🚢 Fleet HSSE Control")

    vessel = st.selectbox(
        "Select Vessel",
        VESSELS,
        key="fleet_vessel"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("HSSE Status", "MONITORING")
    col2.metric("Open Incident", 0)
    col3.metric("Near Miss", 0)
    col4.metric("Open Actions", 0)

    st.success(f"{vessel} is under HSSE monitoring.")

    st.subheader("Fleet Monitoring Areas")

    monitoring = pd.DataFrame(
        {
            "Category": [
                "Safety",
                "Health",
                "Security",
                "Environment",
                "Emergency Preparedness",
                "Compliance",
            ],
            "Status": ["MONITORING"] * 6,
        }
    )

    st.dataframe(
        monitoring,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# SAFETY
# ============================================================

elif menu == "🦺 Safety Management":

    st.header("🦺 Safety Management")

    st.write("Control and monitoring of:")

    st.write("• Permit to Work")
    st.write("• Toolbox Meeting")
    st.write("• Job Safety Analysis")
    st.write("• PPE Compliance")
    st.write("• Safe Working Practices")
    st.write("• Lifting Operations")
    st.write("• Working Aloft")
    st.write("• Enclosed Space Entry")
    st.write("• Hot Work")
    st.write("• Safety Observation")

# ============================================================
# HEALTH
# ============================================================

elif menu == "❤️ Health Management":

    st.header("❤️ Occupational Health Management")

    st.write("• Crew medical fitness")
    st.write("• Occupational health monitoring")
    st.write("• Fatigue management")
    st.write("• Hours of rest monitoring")
    st.write("• Hygiene and sanitation")
    st.write("• Heat stress")
    st.write("• Noise exposure")
    st.write("• Health campaigns")

# ============================================================
# SECURITY
# ============================================================

elif menu == "🔐 Security Management":

    st.header("🔐 Maritime Security Management")

    st.write("• Ship Security Plan")
    st.write("• Security Level Monitoring")
    st.write("• Access Control")
    st.write("• Visitor Management")
    st.write("• Security Drills")
    st.write("• Suspicious Activity Reporting")
    st.write("• Cyber Security Awareness")
    st.write("• ISPS Monitoring")

# ============================================================
# ENVIRONMENT
# ============================================================

elif menu == "🌱 Environmental Management":

    st.header("🌱 Environmental Management")

    st.write("• MARPOL compliance")
    st.write("• Oil pollution prevention")
    st.write("• Garbage management")
    st.write("• Sewage management")
    st.write("• Air emissions")
    st.write("• Ballast water")
    st.write("• Spill prevention")
    st.write("• Environmental incidents")

# ============================================================
# INCIDENT & NEAR MISS
# ============================================================

elif menu == "⚠️ Incident & Near Miss":

    st.header("⚠️ Incident & Near Miss Management")

    with st.form("incident_form"):

        source = st.selectbox(
            "Source",
            ["SHORE OFFICE"] + VESSELS
        )

        event_type = st.selectbox(
            "Event Type",
            [
                "Incident",
                "Near Miss",
                "Unsafe Act",
                "Unsafe Condition",
                "Environmental Event",
                "Security Event",
            ]
        )

        description = st.text_area("Description")

        severity = st.selectbox(
            "Severity",
            ["Low", "Medium", "High", "Critical"]
        )

        submitted = st.form_submit_button("Save HSSE Event")

        if submitted:

            if description.strip():

                st.session_state.incidents.append(
                    {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Source": source,
                        "Type": event_type,
                        "Description": description,
                        "Severity": severity,
                    }
                )

                st.success("HSSE event recorded successfully.")

            else:
                st.warning("Please enter event description.")

    if st.session_state.incidents:

        st.subheader("HSSE Event Register")

        st.dataframe(
            pd.DataFrame(st.session_state.incidents),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# RISK MANAGEMENT
# ============================================================

elif menu == "🧭 Risk Management":

    st.header("🧭 HSSE Risk Management")

    with st.form("risk_form"):

        hazard = st.text_input("Hazard")

        likelihood = st.selectbox(
            "Likelihood",
            [1, 2, 3, 4, 5]
        )

        consequence = st.selectbox(
            "Consequence",
            [1, 2, 3, 4, 5]
        )

        mitigation = st.text_area("Control / Mitigation")

        save_risk = st.form_submit_button("Add Risk")

        if save_risk and hazard.strip():

            score = likelihood * consequence

            st.session_state.risk_register.append(
                {
                    "Hazard": hazard,
                    "Likelihood": likelihood,
                    "Consequence": consequence,
                    "Risk Score": score,
                    "Mitigation": mitigation,
                }
            )

            st.success("Risk added to HSSE Risk Register.")

    if st.session_state.risk_register:

        st.dataframe(
            pd.DataFrame(st.session_state.risk_register),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# EMERGENCY RESPONSE
# ============================================================

elif menu == "🚨 Emergency Response":

    st.header("🚨 Emergency Response Centre")

    st.warning("Emergency Response Readiness")

    emergency_data = pd.DataFrame(
        {
            "Emergency Scenario": [
                "Fire / Explosion",
                "Collision",
                "Grounding",
                "Oil Spill",
                "Man Overboard",
                "Medical Emergency",
                "Security Threat",
                "Abandon Ship",
            ],
            "Status": ["READY"] * 8,
        }
    )

    st.dataframe(
        emergency_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# COMPLIANCE & AUDIT
# ============================================================

elif menu == "📋 Compliance & Audit":

    st.header("📋 HSSE Compliance & Audit")

    compliance = pd.DataFrame(
        {
            "Framework": [
                "ISM Code",
                "ISPS Code",
                "MARPOL",
                "SOLAS",
                "MLC",
                "Company SMS",
                "Internal Audit",
                "External Audit",
            ],
            "Status": ["MONITORING"] * 8,
        }
    )

    st.dataframe(
        compliance,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# CORRECTIVE ACTIONS
# ============================================================

elif menu == "✅ Corrective Actions":

    st.header("✅ Corrective & Preventive Action Tracker")

    with st.form("action_form"):

        action_source = st.selectbox(
            "Source",
            [
                "Incident",
                "Near Miss",
                "Audit",
                "Inspection",
                "Risk Assessment",
                "Management Review",
            ]
        )

        action = st.text_area("Required Action")

        responsible = st.text_input("Responsible Person / Department")

        target_date = st.date_input("Target Date")

        save_action = st.form_submit_button("Create Action")

        if save_action and action.strip():

            st.session_state.actions.append(
                {
                    "Source": action_source,
                    "Action": action,
                    "Responsible": responsible,
                    "Target Date": str(target_date),
                    "Status": "OPEN",
                }
            )

            st.success("Corrective action created.")

    if st.session_state.actions:

        st.dataframe(
            pd.DataFrame(st.session_state.actions),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# HSSE KPI
# ============================================================

elif menu == "📈 HSSE KPI":

    st.header("📈 HSSE Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Fatality", "0")
    col2.metric("LTI", "0")
    col3.metric("Environmental Spill", "0")
    col4.metric("Security Incident", "0")

    st.divider()

    kpi = pd.DataFrame(
        {
            "KPI": [
                "Lost Time Injury",
                "Medical Treatment Case",
                "First Aid Case",
                "Near Miss",
                "Safety Observation",
                "Environmental Incident",
                "Security Incident",
                "Open Corrective Actions",
            ],
            "Current": [0, 0, 0, 0, 0, 0, 0, len(st.session_state.actions)],
            "Target": [0, 0, 0, "Monitor", "Increase", 0, 0, 0],
        }
    )

    st.dataframe(
        kpi,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# AI HSSE INTELLIGENCE
# ============================================================

elif menu == "🤖 AI HSSE Intelligence":

    st.header("🤖 AI HSSE Intelligence Centre")

    st.info(
        "HSSE intelligence workspace for company, shore management "
        "and fleet operational decision support."
    )

    question = st.text_area(
        "Ask HSSE Co-Pilot",
        placeholder=(
            "Example: Identify the highest HSSE risks across the fleet "
            "and recommend priority management actions."
        )
    )

    if st.button("🔎 Analyze HSSE"):

        if question.strip():

            st.subheader("HSSE Intelligence Analysis")

            st.write("**Question / Task:**")
            st.write(question)

            st.write("**Current system facts:**")
            st.write(f"• Fleet monitored: {len(VESSELS)} vessels")
            st.write(f"• Recorded HSSE events: {len(st.session_state.incidents)}")
            st.write(f"• Open action records: {len(st.session_state.actions)}")
            st.write(f"• Risk register entries: {len(st.session_state.risk_register)}")

            st.warning(
                "AI model connection will be activated as the next integration "
                "stage. This module is currently operating from application data."
            )

        else:
            st.warning("Enter a question or HSSE analysis request first.")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
    <b>SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL
    OPERATIONS CONTROL CENTRE</b><br>
    Company • Shore • Fleet • Vessel • Risk • Compliance • Intelligence
    </div>
    """,
    unsafe_allow_html=True
)
