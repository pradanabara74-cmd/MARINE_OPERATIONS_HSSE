import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime, date

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None

st.set_page_config(page_title='SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE', page_icon='■', layout='wide', initial_sidebar_state='expanded')

VESSELS = ['ASL MANTRUS','ASL MULIA','ASL SENTOSA','ASL VICTORY','ASL INTAN','ASL GEMINI','ASL BEAVER','ASL CRESST','ASL CALYPSO','ASL PHOENIX','ASL MARINE 8','AST LEGEND','TERAS HYDRA','AST MAJU','KARYA ABADI 8','NUSANTARA ABADI 1','CAPITOL T2002','CAPITOL T2001','TB1000-06','TB1000-07','WHALE 3']
STORE_KEYS = ['company_records','fleet_reviews','observations','health_records','security_records','environment_records','incidents','near_miss','risk_records','emergency_records','audit_findings','corrective_actions']
for key in STORE_KEYS:
    if key not in st.session_state:
        st.session_state[key] = []
# ===== PERMANENT HSSE DATA STORAGE =====
DATA_FILE = "hsse_data.json"

def save_hsse_data():
    data = {}
    for key in STORE_KEYS:
        data[key] = st.session_state.get(key, [])
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        st.error(f"Failed to save HSSE data: {e}")

def load_hsse_data():
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in STORE_KEYS:
            if key in data:
                st.session_state[key] = data[key]
    except Exception as e:
        st.warning(f"Failed to load HSSE data: {e}")

if "hsse_data_loaded" not in st.session_state:
    load_hsse_data()
    st.session_state.hsse_data_loaded = True


def now(): return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def vessel_count(rows, vessel): return sum(1 for r in rows if r.get('Vessel') == vessel)
def open_actions(vessel=None):
    rows = st.session_state.corrective_actions
    if vessel: rows = [r for r in rows if r.get('Vessel') == vessel]
    return [r for r in rows if str(r.get('Status','OPEN')).upper() not in ('CLOSED','COMPLETED')]
def risk_band(score):
    if score >= 15: return 'CRITICAL/HIGH'
    if score >= 8: return 'MEDIUM'
    return 'LOW'
def hsse_score(vessel):
    penalty = 0
    penalty += vessel_count(st.session_state.incidents, vessel) * 12
    penalty += vessel_count(st.session_state.near_miss, vessel) * 4
    penalty += len([r for r in st.session_state.risk_records if r.get('Vessel') == vessel and int(r.get('Risk Score',0)) >= 15]) * 10
    penalty += len([r for r in st.session_state.audit_findings if r.get('Vessel') == vessel and r.get('Classification') in ('Major','Non-Conformity')]) * 8
    penalty += len(open_actions(vessel)) * 3
    return max(0, 100-penalty)
def status_from_score(score):
    if score >= 90: return 'GOOD'
    if score >= 75: return 'MONITORING'
    if score >= 60: return 'ATTENTION'
    return 'CRITICAL'
def show_table(title, rows):
    if rows:
        st.subheader(title); st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

def get_gemini_client():
    if genai is None: return None
    try: api_key = str(st.secrets.get('GEMINI_API_KEY','')).strip()
    except Exception: api_key = ''
    return genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
) if api_key else None

def hsse_fallback_analysis():
    incidents = st.session_state.get("incidents", [])
    near_miss = st.session_state.get("near_miss", [])
    risk_records = st.session_state.get("risk_records", [])
    corrective_actions = st.session_state.get("corrective_actions", [])

    vessel = selected_vessel if "selected_vessel" in globals() else "ALL VESSELS"

    def relevant(rows):
        if vessel == "ALL VESSELS":
            return rows
        return [
            r for r in rows
            if str(r.get("Vessel", "")).upper() == str(vessel).upper()
        ]

    inc = relevant(incidents)
    nm = relevant(near_miss)
    risks = relevant(risk_records)
    actions = relevant(corrective_actions)

    open_actions = [
        r for r in actions
        if str(r.get("Status", "OPEN")).upper()
        not in ("CLOSED", "COMPLETED")
    ]

    high_risks = [
        r for r in risks
        if int(r.get("Risk Score", 0) or 0) >= 15
    ]

    scope = vessel

    return f"""
### HSSE Executive Analysis — {scope}

**Operational Facts**
- Recorded incidents: **{len(inc)}**
- Recorded near misses: **{len(nm)}**
- High-risk records: **{len(high_risks)}**
- Open corrective actions: **{len(open_actions)}**

### Risk Assessment
{"🔴 High-risk records require immediate management attention." if high_risks else "🟢 No high-risk record is currently identified from the supplied data."}

### Near Miss Review
{"🟠 Near-miss records are present and should be reviewed for recurring causes." if nm else "🟢 No near-miss record is currently recorded for this scope."}

### Corrective Actions
{"🟠 Open corrective actions require follow-up and verification of closure." if open_actions else "🟢 No open corrective action is currently recorded for this scope."}

### Priority Actions
1. Verify that all HSSE records for **{scope}** are current and complete.
2. Review high-risk items and implement controls before further exposure.
3. Investigate near misses and record root causes and preventive measures.
4. Follow up outstanding corrective actions until verified closed.
5. Escalate significant HSSE risks to the Marine Superintendent and DPA.

### Intelligence Status
**Local HSSE Intelligence fallback active.**
Analysis is based only on records currently stored in this application.
"""


def ask_gemini(prompt):
    client = get_gemini_client()

    if client is None:
        return hsse_fallback_analysis()

    instruction = """
You are an HSSE Intelligence Copilot for a marine shipping company.
Use ONLY supplied data.
Never invent operational facts.
"""

    try:
        res = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=instruction
            ),
        )
        return res.text

    except Exception:
        return hsse_fallback_analysis()

st.sidebar.title('■ SHIPPING COMPANY HSSE'); st.sidebar.caption('Operations Control Centre'); st.sidebar.markdown('### CONTROL CENTRE')
menus=['■ Executive Dashboard','■ Company & Shore HSSE','■ Fleet HSSE','■ Safety Management','❤■ Health Management','■ Security Management','■ Environmental Management','■■ Incident & Near Miss','■ Risk Management','■ Emergency Response','■ Compliance & Audit','■ Corrective Actions','■ HSSE KPI','■ AI HSSE Intelligence']
menu=st.sidebar.radio('Navigation',menus,label_visibility='collapsed')
st.sidebar.divider(); selected_vessel=st.sidebar.selectbox('Selected Vessel',['ALL VESSELS']+VESSELS); st.sidebar.caption('Health • Safety • Security • Environment')

st.title('■ SHIPPING COMPANY HEALTH, SAFETY, SECURITY & ENVIRONMENTAL OPERATIONS CONTROL CENTRE')
st.caption('Company • Shore Office • Fleet • Vessel • Personnel • Contractors • Risk • Compliance • Emergency Response • HSSE Intelligence')
st.divider()

if menu=='■ Executive Dashboard':
    st.header('■ HSSE Executive Dashboard')
    events=len(st.session_state.incidents)+len(st.session_state.near_miss)
    c1,c2,c3,c4=st.columns(4); c1.metric('Fleet',len(VESSELS)); c2.metric('Active Vessels',len(VESSELS)); c3.metric('Open HSSE Actions',len(open_actions())); c4.metric('Reported Events',events)
    critical_risks=sum(1 for r in st.session_state.risk_records if int(r.get('Risk Score',0))>=15)
    overdue=sum(1 for r in open_actions() if r.get('Due Date','9999-12-31') < str(date.today()))
    a,b,c=st.columns(3); a.metric('Critical / High Risks',critical_risks); b.metric('Audit Findings',len(st.session_state.audit_findings)); c.metric('Overdue Actions',overdue)
    st.subheader('■ Fleet HSSE Overview')
    fleet=[]
    for v in VESSELS:
        score=hsse_score(v); fleet.append({'Vessel':v,'HSSE Score':score,'HSSE Status':status_from_score(score),'Incidents':vessel_count(st.session_state.incidents,v),'Near Miss':vessel_count(st.session_state.near_miss,v),'Open Actions':len(open_actions(v))})
    st.dataframe(pd.DataFrame(fleet),use_container_width=True,hide_index=True)

elif menu=='■ Company & Shore HSSE':
    st.header('■ Company & Shore Office HSSE'); st.info('Monitoring HSSE performance for company management and shore-based operations.')
    with st.form('company_form'):
        c1,c2=st.columns(2)
        with c1: review=st.text_area('Management HSSE Review / Notes',height=180)
        with c2: inspection=st.selectbox('Inspection Status',['Not Started','In Progress','Completed']); inspection_date=st.date_input('Inspection Date')
        submitted=st.form_submit_button('Save Company HSSE Record')
    if submitted:
        st.session_state.company_records.append({'Date':now(),'Review':review,'Inspection Status':inspection,'Inspection Date':str(inspection_date)}); st.success('Company HSSE record saved.')
    show_table('Company HSSE Records',st.session_state.company_records)

elif menu=='■ Fleet HSSE':
    st.header('■ Fleet HSSE'); vessel=st.selectbox('Vessel',VESSELS)
    score=hsse_score(vessel); c1,c2,c3,c4=st.columns(4); c1.metric('HSSE Status',status_from_score(score)); c2.metric('Incidents',vessel_count(st.session_state.incidents,vessel)); c3.metric('Near Miss',vessel_count(st.session_state.near_miss,vessel)); c4.metric('Open Actions',len(open_actions(vessel)))
    remarks=st.text_area(f'HSSE Review — {vessel}',height=180)
    if st.button('Save Fleet HSSE Review'):
        st.session_state.fleet_reviews.append({'Date':now(),'Vessel':vessel,'HSSE Score':score,'Status':status_from_score(score),'Remarks':remarks}); st.success('Fleet HSSE review saved.')
    show_table('Fleet HSSE Review History',[r for r in st.session_state.fleet_reviews if r.get('Vessel')==vessel])

elif menu=='■ Safety Management':
    st.header('■ Safety Management'); vessel=st.selectbox('Vessel',VESSELS); activity=st.selectbox('Safety Activity',['Safety Observation','Unsafe Act','Unsafe Condition','Toolbox Meeting','Permit to Work','JSA / Risk Assessment','Safety Inspection']); description=st.text_area('Description'); severity=st.selectbox('Risk Level',['Low','Medium','High','Critical'])
    if st.button('Save Safety Record'):
        st.session_state.observations.append({'Date':now(),'Vessel':vessel,'Activity':activity,'Description':description,'Risk':severity}); st.success('Safety record saved.')
    show_table('Safety Records',st.session_state.observations)

elif menu=='❤■ Health Management':
    st.header('❤■ Health Management'); vessel=st.selectbox('Vessel',VESSELS); category=st.selectbox('Health Category',['Medical Case','First Aid','Fitness for Duty','Fatigue','Occupational Health','Hygiene','Heat Stress','Other']); report=st.text_area('Health Report / Observation'); status=st.selectbox('Status',['Monitoring','Follow Up','Closed'])
    if st.button('Save Health Record'):
        st.session_state.health_records.append({'Date':now(),'Vessel':vessel,'Category':category,'Report':report,'Status':status}); st.success('Health record saved.')
    show_table('Health Records',st.session_state.health_records)

elif menu=='■ Security Management':
    st.header('■ Security Management'); vessel=st.selectbox('Vessel',VESSELS); level=st.selectbox('Security Level',['Level 1','Level 2','Level 3']); event=st.selectbox('Security Event',['Routine Monitoring','Access Control','Security Breach','Suspicious Activity','Piracy / Armed Robbery','Cyber Security','Other']); report=st.text_area('Security Report')
    if st.button('Save Security Record'):
        st.session_state.security_records.append({'Date':now(),'Vessel':vessel,'Security Level':level,'Event':event,'Report':report}); st.success('Security record saved.'); save_hsse_data()
    show_table('Security Records',st.session_state.security_records)

elif menu=='■ Environmental Management':
    st.header('■ Environmental Management'); vessel=st.selectbox('Vessel',VESSELS); category=st.selectbox('Environmental Category',['Oil Spill','Garbage','Sewage','Air Emission','Ballast Water','Hazardous Material','Environmental Observation','Other']); report=st.text_area('Environmental Report'); status=st.selectbox('Status',['Normal','Monitoring','Action Required','Critical'])
    if st.button('Save Environmental Record'):
        st.session_state.environment_records.append({'Date':now(),'Vessel':vessel,'Category':category,'Report':report,'Status':status}); st.success('Environmental record saved.'); save_hsse_data()
    show_table('Environmental Records',st.session_state.environment_records)

elif menu=='■■ Incident & Near Miss':
    st.header('■■ Incident & Near Miss Management'); report_type=st.radio('Report Type',['Incident / Accident','Near Miss']); vessel=st.selectbox('Vessel',VESSELS); event_date=st.date_input('Event Date'); description=st.text_area('Event Description'); severity=st.selectbox('Severity',['Low','Medium','High','Critical']); immediate=st.text_area('Immediate Action')
    if st.button('Submit Event Report'):
        record={'Date':str(event_date),'Vessel':vessel,'Description':description,'Severity':severity,'Immediate Action':immediate,'Recorded':now()}; st.session_state.incidents.append(record) if report_type=='Incident / Accident' else st.session_state.near_miss.append(record); st.success('HSSE event recorded successfully.'); save_hsse_data()
    show_table('Incident Records',st.session_state.incidents); show_table('Near Miss Records',st.session_state.near_miss)

elif menu=='■ Risk Management':
    st.header('■ HSSE Risk Management'); vessel=st.selectbox('Vessel',VESSELS); hazard=st.text_input('Hazard'); likelihood=st.slider('Likelihood',1,5,1); consequence=st.slider('Consequence',1,5,1); score=likelihood*consequence; st.metric('Risk Score',score); band=risk_band(score)
    if score>=15: st.error('HIGH / CRITICAL RISK')
    elif score>=8: st.warning('MEDIUM RISK')
    else: st.success('LOW RISK')
    control=st.text_area('Risk Control / Mitigation')
    if st.button('Save Risk Assessment'):
        st.session_state.risk_records.append({'Date':now(),'Vessel':vessel,'Hazard':hazard,'Likelihood':likelihood,'Consequence':consequence,'Risk Score':score,'Risk Level':band,'Control / Mitigation':control}); st.success('Risk assessment saved.'); save_hsse_data()
    show_table('Risk Register',st.session_state.risk_records)

elif menu=='■ Emergency Response':
    st.header('■ Emergency Response'); vessel=st.selectbox('Vessel',VESSELS); emergency=st.selectbox('Emergency Type',['Fire','Collision','Grounding','Flooding','Oil Spill','Man Overboard','Medical Emergency','Security Threat','Abandon Ship','Other']); status=st.selectbox('Emergency Status',['Standby','Activated','Under Control','Closed']); actions=st.text_area('Emergency Situation / Actions')
    if st.button('Save Emergency Record'):
        st.session_state.emergency_records.append({'Date':now(),'Vessel':vessel,'Emergency Type':emergency,'Status':status,'Situation / Actions':actions}); st.success('Emergency record saved.'); save_hsse_data()
    show_table('Emergency Records',st.session_state.emergency_records)

elif menu=='■ Compliance & Audit':
    st.header('■ Compliance & Audit'); vessel=st.selectbox('Vessel',VESSELS); audit=st.selectbox('Audit / Inspection',['ISM Internal Audit','ISPS Audit','MLC Inspection','HSSE Inspection','Flag State','Port State Control','Client Audit','Management Inspection','Other']); finding=st.text_area('Finding / Observation'); classification=st.selectbox('Classification',['Observation','Minor','Major','Non-Conformity']); due=st.date_input('Target Close Date')
    if st.button('Save Audit Finding'):
        st.session_state.audit_findings.append({'Date':now(),'Vessel':vessel,'Audit / Inspection':audit,'Finding':finding,'Classification':classification,'Target Close Date':str(due),'Status':'OPEN'}); st.success('Audit finding saved.'); save_hsse_data()
    show_table('Audit Findings',st.session_state.audit_findings)

elif menu=='■ Corrective Actions':
    st.header('■ Corrective Action Tracker'); vessel=st.selectbox('Vessel',VESSELS); action=st.text_area('Corrective Action'); responsible=st.text_input('Responsible Person / Department'); due=st.date_input('Due Date'); priority=st.selectbox('Priority',['Low','Medium','High','Critical']); status=st.selectbox('Status',['OPEN','IN PROGRESS','COMPLETED','CLOSED'])
    if st.button('Add Corrective Action'):
        st.session_state.corrective_actions.append({'Created':now(),'Vessel':vessel,'Action':action,'Responsible':responsible,'Due Date':str(due),'Priority':priority,'Status':status}); st.success('Corrective action added.'); save_hsse_data()
    show_table('Corrective Action Register',st.session_state.corrective_actions)

elif menu=='■ HSSE KPI':
    st.header('■ HSSE KPI & Performance'); c1,c2,c3,c4=st.columns(4); c1.metric('Incidents',len(st.session_state.incidents)); c2.metric('Near Miss',len(st.session_state.near_miss)); c3.metric('Safety Records',len(st.session_state.observations)); c4.metric('Open Corrective Actions',len(open_actions()))
    rows=[]
    for v in VESSELS:
        score=hsse_score(v); rows.append({'Vessel':v,'HSSE Score':score,'Status':status_from_score(score),'Incidents':vessel_count(st.session_state.incidents,v),'Near Miss':vessel_count(st.session_state.near_miss,v),'Open Actions':len(open_actions(v))})
    st.subheader('Fleet KPI'); st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

elif menu=='■ AI HSSE Intelligence':
    st.header('■ AI HSSE Intelligence'); st.info('HSSE Intelligence Centre for Marine Superintendent, DPA and Marine Operations Management.')
    question=st.text_area('Ask HSSE Intelligence',placeholder='Example: Identify the highest HSSE risks across the fleet.')
    if st.button('Analyze HSSE',type='primary'):
        if not question.strip(): st.warning('Enter a question or HSSE instruction first.')
        else:
            data={'fleet_size':len(VESSELS),'incidents':st.session_state.incidents,'near_miss':st.session_state.near_miss,'safety_records':st.session_state.observations,'health_records':st.session_state.health_records,'security_records':st.session_state.security_records,'environment_records':st.session_state.environment_records,'risk_register':st.session_state.risk_records,'emergency_records':st.session_state.emergency_records,'audit_findings':st.session_state.audit_findings,'corrective_actions':st.session_state.corrective_actions,'fleet_scores':{v:hsse_score(v) for v in VESSELS}}
            st.subheader('■ HSSE Intelligence Analysis')
            prompt=f'''USER QUESTION: {question}\n\nCURRENT HSSE DATA:\n{json.dumps(data,default=str,ensure_ascii=False)}\n\nReturn sections: EXECUTIVE SUMMARY, CRITICAL/HIGH RISKS, INCIDENT & NEAR MISS, COMPLIANCE/AUDIT, CORRECTIVE ACTION PRIORITIES, DATA GAPS, RECOMMENDED ACTIONS. Do not invent missing facts.'''
            with st.spinner('Analyzing current HSSE records...'): answer=ask_gemini(prompt)
            st.markdown(answer)

st.divider(); st.caption('■ SHIPPING COMPANY HSSE OPERATIONS CONTROL CENTRE • Health • Safety • Security • Environment • Fleet Monitoring • Risk • Compliance • Intelligence')
