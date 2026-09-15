import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# # SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL OPERATIONS CONTROL CENTRE
# Health • Safety • Security • Environment
# ============================================================

st.set_page_config(
    page_title="SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FLEET
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
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .sub-title {
        font-size: 18px;
        color: #666666;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .status-good {
        padding: 14px;
        border-radius: 8px;
        background-color: rgba(0, 170, 80, 0.10);
        border-left: 5px solid #00a650;
        font-weight: 600;
    }

    .status-warning {
        padding: 14px;
        border-radius: 8px;
        background-color: rgba(255, 170, 0, 0.12);
        border-left: 5px solid #ffaa00;
        font-weight: 600;
    }

    .status-critical {
        padding: 14px;
        border-radius: 8px;
        background-color: rgba(220, 0, 0, 0.10);
        border-left: 5px solid #dc0000;
        font-weight: 600;
    }

    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #dddddd;
        color: #777777;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚓ SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE")

st.sidebar.caption(
    "Health • Safety • Security • Environment"
)

menu = st.sidebar.radio(
    "HSSE CONTROL CENTRE",
    [
        "🏠 HSSE Dashboard",
        "🚨 Incident & Accident",
        "⚠️ Near Miss",
        "👷 Unsafe Act / Condition",
        "👁️ Safety Observation",
        "📋 Permit to Work",
        "🛡️ Risk Assessment / JSA",
        "🗣️ Toolbox Meeting",
        "🔍 HSSE Inspection",
        "📑 Audit & Findings",
        "✅ Corrective Actions",
        "🚒 Emergency Response",
        "🌱 Environmental",
        "🎓 Training & Competency",
        "📊 HSSE KPI",
        "🚢 Fleet HSSE Monitoring",
        "🧠 HSSE Intelligence",
    ]
)

st.sidebar.divider()

selected_vessel = st.sidebar.selectbox(
    "Selected Vessel",
    ["ALL VESSELS"] + VESSELS
)

st.sidebar.metric("Fleet", len(VESSELS))

st.sidebar.caption(
    f"System time: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">⚓ SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL OPERATIONS CONTROL CENTRE</div>',

st.markdown(
    '<div class="sub-title">Shipping Company • Shore Management • Fleet Operations • Health • Safety • Security • Environment</div>',
    unsafe_allow_html=True
)

# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 HSSE Dashboard":

    st.header("📊 HSSE Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Fleet", "21")
    col2.metric("Active Vessels", "21")
    col3.metric("Open HSSE Actions", "0")
    col4.metric("Critical Events", "0")

    st.divider()

    st.subheader("🧠 Operational HSSE Intelligence")

    st.markdown(
        """
        <div class="status-good">
        HSSE STATUS: SYSTEM READY
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write(
        "SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE siap menerima dan "
"menganalisis data HSSE perusahaan, shore management, fleet, dan seluruh armada."

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
# INCIDENT
# ============================================================

elif menu == "🚨 Incident & Accident":

    st.header("🚨 Incident & Accident Management")

    st.write(
        "Register, monitor and investigate marine HSSE incidents "
        "and accidents."
    )

    uploaded = st.file_uploader(
        "Upload Incident / Accident Data (CSV)",
        type=["csv"],
        key="incident"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)

            st.success(
                f"{len(df)} incident/accident records loaded."
            )

            st.subheader("Incident Records")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# NEAR MISS
# ============================================================

elif menu == "⚠️ Near Miss":

    st.header("⚠️ Near Miss Intelligence")

    uploaded = st.file_uploader(
        "Upload Near Miss Data (CSV)",
        type=["csv"],
        key="near_miss"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)

            st.metric("Near Miss Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# UNSAFE ACT / CONDITION
# ============================================================

elif menu == "👷 Unsafe Act / Condition":

    st.header("👷 Unsafe Act / Unsafe Condition")

    uploaded = st.file_uploader(
        "Upload Unsafe Act / Condition Data (CSV)",
        type=["csv"],
        key="unsafe"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# SAFETY OBSERVATION
# ============================================================

elif menu == "👁️ Safety Observation":

    st.header("👁️ Safety Observation")

    uploaded = st.file_uploader(
        "Upload Safety Observation Data (CSV)",
        type=["csv"],
        key="observation"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Safety Observations", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# PERMIT TO WORK
# ============================================================

elif menu == "📋 Permit to Work":

    st.header("📋 Permit to Work Control")

    st.info(
        "Monitor Hot Work, Enclosed Space Entry, "
        "Working Aloft, Electrical Work and other permits."
    )

    uploaded = st.file_uploader(
        "Upload Permit to Work Data (CSV)",
        type=["csv"],
        key="ptw"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Permit Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# RISK ASSESSMENT
# ============================================================

elif menu == "🛡️ Risk Assessment / JSA":

    st.header("🛡️ Risk Assessment / JSA")

    uploaded = st.file_uploader(
        "Upload Risk Assessment / JSA Data (CSV)",
        type=["csv"],
        key="risk"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Risk Assessments", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# TOOLBOX
# ============================================================

elif menu == "🗣️ Toolbox Meeting":

    st.header("🗣️ Toolbox Meeting")

    uploaded = st.file_uploader(
        "Upload Toolbox Meeting Records (CSV)",
        type=["csv"],
        key="toolbox"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Toolbox Meetings", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# INSPECTION
# ============================================================

elif menu == "🔍 HSSE Inspection":

    st.header("🔍 HSSE Inspection")

    uploaded = st.file_uploader(
        "Upload HSSE Inspection Data (CSV)",
        type=["csv"],
        key="inspection"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Inspection Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# AUDIT
# ============================================================

elif menu == "📑 Audit & Findings":

    st.header("📑 HSSE Audit & Findings")

    uploaded = st.file_uploader(
        "Upload Audit & Findings Data (CSV)",
        type=["csv"],
        key="audit"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Audit / Finding Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# CORRECTIVE ACTIONS
# ============================================================

elif menu == "✅ Corrective Actions":

    st.header("✅ Corrective Action Tracker")

    uploaded = st.file_uploader(
        "Upload Corrective Action Data (CSV)",
        type=["csv"],
        key="corrective"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Corrective Actions", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# EMERGENCY RESPONSE
# ============================================================

elif menu == "🚒 Emergency Response":

    st.header("🚒 Emergency Response")

    st.warning(
        "Emergency preparedness and response monitoring."
    )

    emergency_types = [
        "Fire",
        "Collision",
        "Grounding",
        "Oil Spill",
        "Man Overboard",
        "Flooding",
        "Loss of Propulsion",
        "Loss of Steering",
        "Medical Emergency",
        "Security Incident",
        "Abandon Ship",
    ]

    emergency_df = pd.DataFrame(
        {
            "Emergency Scenario": emergency_types,
            "Readiness": ["MONITOR"] * len(emergency_types),
        }
    )

    st.dataframe(
        emergency_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# ENVIRONMENT
# ============================================================

elif menu == "🌱 Environmental":

    st.header("🌱 Environmental Intelligence")

    uploaded = st.file_uploader(
        "Upload Environmental Data (CSV)",
        type=["csv"],
        key="environment"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Environmental Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# TRAINING
# ============================================================

elif menu == "🎓 Training & Competency":

    st.header("🎓 HSSE Training & Competency")

    uploaded = st.file_uploader(
        "Upload Training / Competency Data (CSV)",
        type=["csv"],
        key="training"
    )

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.metric("Training Records", len(df))
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Unable to read CSV: {e}")

# ============================================================
# KPI
# ============================================================

elif menu == "📊 HSSE KPI":

    st.header("📊 HSSE Performance Indicators")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("LTI", "0")
    c2.metric("TRC", "0")
    c3.metric("Near Miss", "0")
    c4.metric("Environmental Spill", "0")

    st.caption(
        "KPI values will be calculated from verified operational data."
    )

# ============================================================
# FLEET MONITORING
# ============================================================

elif menu == "🚢 Fleet HSSE Monitoring":

    st.header("🚢 Fleet HSSE Monitoring")

    fleet_df = pd.DataFrame(
        {
            "Vessel": VESSELS,
            "Status": ["ACTIVE"] * 21,
            "HSSE Monitoring": ["READY"] * 21,
        }
    )

    st.dataframe(
        fleet_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# HSSE INTELLIGENCE
# ============================================================

elif menu == "🧠 HSSE Intelligence":

    st.header("🧠 HSSE Intelligence Centre")

    st.write(
        "HSSE Intelligence akan menggabungkan incident, near miss, "
        "unsafe conditions, inspections, audits, corrective actions, "
        "environmental data dan fleet monitoring."
    )

    st.subheader("FACTS")

    st.info(
        "Belum ada dataset HSSE gabungan yang dianalisis."
    )

    st.subheader("RISK")

    st.warning(
        "Risk assessment hanya akan dibuat berdasarkan data "
        "operasional yang tersedia."
    )

    st.subheader("DATA GAPS")

    st.write(
        "Data yang belum tersedia akan ditandai sebagai "
        "DATA BELUM TERSEDIA dan tidak diasumsikan oleh sistem."
    )

    st.subheader("PRIORITY ACTIONS")

    st.write(
        "Priority Actions akan ditentukan berdasarkan "
        "severity, status, due date dan verified HSSE data."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL OPERATIONS CONTROL CENTRE •
    Health • Safety • Security • Environment •
    Fleet Monitoring • Risk • Intelligence
    </div>
    """,
    unsafe_allow_html=True
)
