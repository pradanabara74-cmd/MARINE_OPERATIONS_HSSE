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
# SESSION DATA
# ============================================================

if "incidents" not in st.session_state:
    st.session_state.incidents = []

if "near_miss" not in st.session_state:
    st.session_state.near_miss = []

if "corrective_actions" not in st.session_state:
    st.session_state.corrective_actions = []

if "observations" not in st.session_state:
    st.session_state.observations = []

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚓ SHIPPING COMPANY HSSE")
st.sidebar.caption("Operations Control Centre")

st.sidebar.markdown("### CONTROL CENTRE")

menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Executive Dashboard",
        "🏢 Company & Shore HSSE",
        "🚢 Fleet HSSE",
        "🦺 Safety Management",
        "❤️ Health Management",
        "🔐 Security Management",
        "🌱 Environmental Management",
        "⚠️ Incident & Near Miss",
        "🎯 Risk Management",
        "🚨 Emergency Response",
        "📋 Compliance & Audit",
        "✅ Corrective Actions",
        "📈 HSSE KPI",
        "🤖 AI HSSE Intelligence",
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

selected_vessel = st.sidebar.selectbox(
    "Selected Vessel",
    ["ALL VESSELS"] + VESSELS
)

st.sidebar.caption(
    "Health • Safety • Security • Environment"
)

# ============================================================
# HEADER
# ============================================================

st.title(
    "⚓ SHIPPING COMPANY HEALTH, SAFETY, SECURITY & "
    "ENVIRONMENTAL OPERATIONS CONTROL CENTRE"
)

st.caption(
    "Company • Shore Office • Fleet • Vessel • Personnel • "
    "Contractors • Risk • Compliance • Emergency Response • "
    "HSSE Intelligence"
)

st.divider()

# ============================================================
# 1. EXECUTIVE DASHBOARD
# ============================================================

if menu == "📊 Executive Dashboard":

    st.header("📊 HSSE Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Fleet", len(VESSELS))
    c2.metric("Active Vessels", len(VESSELS))
    c3.metric(
        "Open HSSE Actions",
        len(st.session_state.corrective_actions)
    )
    c4.metric(
        "Reported Events",
        len(st.session_state.incidents) +
        len(st.session_state.near_miss)
    )

    st.subheader("🏢 Company HSSE Status")

    company_status = pd.DataFrame({
        "Area": [
            "Health",
            "Safety",
            "Security",
            "Environment",
            "Emergency Preparedness",
            "Compliance"
        ],
        "Status": [
            "MONITORING",
            "MONITORING",
            "MONITORING",
            "MONITORING",
            "READY",
            "MONITORING"
        ]
    })

    st.dataframe(
        company_status,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🚢 Fleet HSSE Overview")

    fleet = pd.DataFrame({
        "Vessel": VESSELS,
        "HSSE Status": ["MONITORING"] * len(VESSELS),
        "Open Incident": [0] * len(VESSELS),
        "Near Miss": [0] * len(VESSELS),
        "Open Actions": [0] * len(VESSELS)
    })

    st.dataframe(
        fleet,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# 2. COMPANY & SHORE HSSE
# ============================================================

elif menu == "🏢 Company & Shore HSSE":

    st.header("🏢 Company & Shore Office HSSE")

    st.info(
        "Monitoring HSSE performance for company management "
        "and shore-based operations."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Management Review")
        st.text_area(
            "Management HSSE Review / Notes",
            height=180
        )

    with col2:
        st.subheader("Shore Office Inspection")
        st.selectbox(
            "Inspection Status",
            ["Not Started", "In Progress", "Completed"]
        )
        st.date_input("Inspection Date")

    st.button("Save Company HSSE Record")

# ============================================================
# 3. FLEET HSSE
# ============================================================

elif menu == "🚢 Fleet HSSE":

    st.header("🚢 Fleet HSSE")

    vessel = st.selectbox(
        "Vessel",
        VESSELS,
        index=0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("HSSE Status", "MONITORING")
    c2.metric("Incidents", "0")
    c3.metric("Near Miss", "0")
    c4.metric("Open Actions", "0")

    st.subheader(f"HSSE Review — {vessel}")

    st.text_area(
        "Fleet / Vessel HSSE Remarks",
        height=180
    )

    st.button("Save Fleet HSSE Review")

# ============================================================
# 4. SAFETY MANAGEMENT
# ============================================================

elif menu == "🦺 Safety Management":

    st.header("🦺 Safety Management")

    vessel = st.selectbox("Vessel", VESSELS)

    activity = st.selectbox(
        "Safety Activity",
        [
            "Safety Observation",
            "Unsafe Act",
            "Unsafe Condition",
            "Toolbox Meeting",
            "Permit to Work",
            "JSA / Risk Assessment",
            "Safety Inspection"
        ]
    )

    description = st.text_area("Description")

    severity = st.selectbox(
        "Risk Level",
        ["Low", "Medium", "High", "Critical"]
    )

    if st.button("Save Safety Record"):
        st.session_state.observations.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Vessel": vessel,
            "Activity": activity,
            "Description": description,
            "Risk": severity
        })

        st.success("Safety record saved.")

    if st.session_state.observations:
        st.dataframe(
            pd.DataFrame(st.session_state.observations),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# 5. HEALTH MANAGEMENT
# ============================================================

elif menu == "❤️ Health Management":

    st.header("❤️ Health Management")

    vessel = st.selectbox("Vessel", VESSELS)

    st.selectbox(
        "Health Category",
        [
            "Medical Case",
            "First Aid",
            "Fitness for Duty",
            "Fatigue",
            "Occupational Health",
            "Hygiene",
            "Heat Stress",
            "Other"
        ]
    )

    st.text_area("Health Report / Observation")

    st.selectbox(
        "Status",
        ["Monitoring", "Follow Up", "Closed"]
    )

    st.button("Save Health Record")

# ============================================================
# 6. SECURITY MANAGEMENT
# ============================================================

elif menu == "🔐 Security Management":

    st.header("🔐 Security Management")

    vessel = st.selectbox("Vessel", VESSELS)

    st.selectbox(
        "Security Level",
        ["Level 1", "Level 2", "Level 3"]
    )

    st.selectbox(
        "Security Event",
        [
            "Routine Monitoring",
            "Access Control",
            "Security Breach",
            "Suspicious Activity",
            "Piracy / Armed Robbery",
            "Cyber Security",
            "Other"
        ]
    )

    st.text_area("Security Report")

    st.button("Save Security Record")

# ============================================================
# 7. ENVIRONMENTAL MANAGEMENT
# ============================================================

elif menu == "🌱 Environmental Management":

    st.header("🌱 Environmental Management")

    vessel = st.selectbox("Vessel", VESSELS)

    st.selectbox(
        "Environmental Category",
        [
            "Oil Spill",
            "Garbage",
            "Sewage",
            "Air Emission",
            "Ballast Water",
            "Hazardous Material",
            "Environmental Observation",
            "Other"
        ]
    )

    st.text_area("Environmental Report")

    st.selectbox(
        "Status",
        ["Normal", "Monitoring", "Action Required", "Critical"]
    )

    st.button("Save Environmental Record")

# ============================================================
# 8. INCIDENT & NEAR MISS
# ============================================================

elif menu == "⚠️ Incident & Near Miss":

    st.header("⚠️ Incident & Near Miss Management")

    report_type = st.radio(
        "Report Type",
        ["Incident / Accident", "Near Miss"]
    )

    vessel = st.selectbox("Vessel", VESSELS)

    event_date = st.date_input("Event Date")

    description = st.text_area("Event Description")

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )

    immediate_action = st.text_area("Immediate Action")

    if st.button("Submit Event Report"):

        record = {
            "Date": str(event_date),
            "Vessel": vessel,
            "Description": description,
            "Severity": severity,
            "Immediate Action": immediate_action
        }

        if report_type == "Incident / Accident":
            st.session_state.incidents.append(record)
        else:
            st.session_state.near_miss.append(record)

        st.success("HSSE event recorded successfully.")

    if st.session_state.incidents:
        st.subheader("Incident Records")
        st.dataframe(
            pd.DataFrame(st.session_state.incidents),
            use_container_width=True,
            hide_index=True
        )

    if st.session_state.near_miss:
        st.subheader("Near Miss Records")
        st.dataframe(
            pd.DataFrame(st.session_state.near_miss),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# 9. RISK MANAGEMENT
# ============================================================

elif menu == "🎯 Risk Management":

    st.header("🎯 HSSE Risk Management")

    vessel = st.selectbox("Vessel", VESSELS)

    hazard = st.text_input("Hazard")

    likelihood = st.slider(
        "Likelihood",
        1,
        5,
        1
    )

    consequence = st.slider(
        "Consequence",
        1,
        5,
        1
    )

    risk_score = likelihood * consequence

    st.metric("Risk Score", risk_score)

    if risk_score >= 15:
        st.error("HIGH / CRITICAL RISK")
    elif risk_score >= 8:
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")

    st.text_area("Risk Control / Mitigation")

    st.button("Save Risk Assessment")

# ============================================================
# 10. EMERGENCY RESPONSE
# ============================================================

elif menu == "🚨 Emergency Response":

    st.header("🚨 Emergency Response")

    vessel = st.selectbox("Vessel", VESSELS)

    emergency = st.selectbox(
        "Emergency Type",
        [
            "Fire",
            "Collision",
            "Grounding",
            "Flooding",
            "Oil Spill",
            "Man Overboard",
            "Medical Emergency",
            "Security Threat",
            "Abandon Ship",
            "Other"
        ]
    )

    st.selectbox(
        "Emergency Status",
        [
            "Standby",
            "Activated",
            "Under Control",
            "Closed"
        ]
    )

    st.text_area("Emergency Situation / Actions")

    st.button("Save Emergency Record")

# ============================================================
# 11. COMPLIANCE & AUDIT
# ============================================================

elif menu == "📋 Compliance & Audit":

    st.header("📋 Compliance & Audit")

    vessel = st.selectbox("Vessel", VESSELS)

    audit_type = st.selectbox(
        "Audit / Inspection",
        [
            "ISM Internal Audit",
            "ISPS Audit",
            "MLC Inspection",
            "HSSE Inspection",
            "Flag State",
            "Port State Control",
            "Client Audit",
            "Management Inspection",
            "Other"
        ]
    )

    finding = st.text_area("Finding / Observation")

    classification = st.selectbox(
        "Classification",
        [
            "Observation",
            "Minor",
            "Major",
            "Non-Conformity"
        ]
    )

    due_date = st.date_input("Target Close Date")

    st.button("Save Audit Finding")

# ============================================================
# 12. CORRECTIVE ACTIONS
# ============================================================

elif menu == "✅ Corrective Actions":

    st.header("✅ Corrective Action Tracker")

    vessel = st.selectbox("Vessel", VESSELS)

    action = st.text_area("Corrective Action")

    responsible = st.text_input(
        "Responsible Person / Department"
    )

    due_date = st.date_input("Due Date")

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Critical"]
    )

    if st.button("Add Corrective Action"):

        st.session_state.corrective_actions.append({
            "Vessel": vessel,
            "Action": action,
            "Responsible": responsible,
            "Due Date": str(due_date),
            "Priority": priority,
            "Status": "OPEN"
        })

        st.success("Corrective action added.")

    if st.session_state.corrective_actions:

        st.dataframe(
            pd.DataFrame(
                st.session_state.corrective_actions
            ),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# 13. HSSE KPI
# ============================================================

elif menu == "📈 HSSE KPI":

    st.header("📈 HSSE KPI & Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Incidents",
        len(st.session_state.incidents)
    )

    c2.metric(
        "Near Miss",
        len(st.session_state.near_miss)
    )

    c3.metric(
        "Safety Records",
        len(st.session_state.observations)
    )

    c4.metric(
        "Corrective Actions",
        len(st.session_state.corrective_actions)
    )

    st.subheader("Fleet KPI")

    kpi_data = pd.DataFrame({
        "Vessel": VESSELS,
        "HSSE Score": [100] * len(VESSELS),
        "Status": ["GOOD"] * len(VESSELS)
    })

    st.dataframe(
        kpi_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# 14. AI HSSE INTELLIGENCE
# ============================================================

elif menu == "🤖 AI HSSE Intelligence":

    st.header("🤖 AI HSSE Intelligence")

    st.info(
        "HSSE Intelligence Centre for Marine Superintendent, "
        "DPA and Marine Operations Management."
    )

    question = st.text_area(
        "Ask HSSE Intelligence",
        placeholder=(
            "Example: Identify the highest HSSE risks "
            "across the fleet."
        )
    )

    if st.button("Analyze HSSE"):

        if not question.strip():

            st.warning(
                "Enter a question or HSSE instruction first."
            )

        else:

            st.subheader("🔎 HSSE Intelligence Analysis")

            st.write(
                "Current fleet under monitoring:",
                len(VESSELS),
                "vessels."
            )

            st.write(
                "Recorded incidents:",
                len(st.session_state.incidents)
            )

            st.write(
                "Recorded near misses:",
                len(st.session_state.near_miss)
            )

            st.write(
                "Open corrective actions:",
                len(st.session_state.corrective_actions)
            )

            st.success(
                "HSSE monitoring analysis completed."
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚓ SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE • "
    "Health • Safety • Security • Environment • "
    "Fleet Monitoring • Risk • Compliance • Intelligence"
)
