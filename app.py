"""
13th Five-Year Plan · Mid-Term Review
Multi-user management system — Streamlit + Supabase
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
import io
from datetime import datetime
import time

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="13th FYP · MTR",
    page_icon="🇧🇹",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None,
                "About": "13th Five-Year Plan Management System · Royal Government of Bhutan"}
)

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=DM+Sans:wght@300..600&family=JetBrains+Mono:wght@400;500&display=swap');

/* App background */
.stApp { background: #F2EBDE; }
.main .block-container { padding-top: 24px; }

/* All text */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Headings */
h1, h2, h3 { font-family: 'Fraunces', serif !important; font-weight: 400 !important; letter-spacing: -0.01em; }
h1 { font-size: 2rem !important; color: #1B140B !important; }
h2 { font-size: 1.5rem !important; color: #1B140B !important; }
h3 { font-size: 1.1rem !important; color: #1B140B !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #ECE3D2 !important;
    border: 1px solid #C9B991 !important;
    padding: 18px 20px !important;
    border-radius: 0 !important;
}
[data-testid="stMetricLabel"] > div {
    font-size: 10px !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; color: #6B5B45 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif !important;
    font-size: 26px !important; color: #1B140B !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important;
}

/* Sidebar */
[data-testid="stSidebar"] { background: #1B140B !important; border-right: none !important; }
[data-testid="stSidebar"] * { color: #ECE3D2 !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: 'Fraunces', serif !important; color: #F2EBDE !important;
}
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    font-size: 13px !important; color: #C9B991 !important;
    padding: 6px 8px !important; border-radius: 0 !important;
    border-left: 2px solid transparent !important; display: block !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    color: #F2EBDE !important; border-left-color: #C25B12 !important;
    background: rgba(194,91,18,0.12) !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; border: 1px solid rgba(201,185,145,0.4) !important;
    color: #C9B991 !important; font-size: 12px !important;
    border-radius: 0 !important; width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(201,185,145,0.1) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(201,185,145,0.2) !important; }

/* Buttons */
.stButton > button {
    background: #C25B12 !important; color: white !important;
    border: none !important; border-radius: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important; letter-spacing: 0.04em !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #E07120 !important; }
.stButton > button[kind="secondary"] {
    background: #8E2A1F !important;
}
.stButton > button[kind="secondary"]:hover { background: #A63320 !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    border: 1px solid #C9B991 !important; border-radius: 0 !important;
    background: #F2EBDE !important; font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: #C25B12 !important;
    box-shadow: 0 0 0 3px rgba(194,91,18,0.12) !important;
}
.stSelectbox > div > div {
    border: 1px solid #C9B991 !important; border-radius: 0 !important;
    background: #F2EBDE !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #ECE3D2 !important;
    border-bottom: 1px solid #C9B991 !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    color: #6B5B45 !important; padding: 12px 20px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #C25B12 !important; border-bottom-color: #C25B12 !important;
    background: transparent !important;
}

/* Data tables */
[data-testid="stDataFrame"] { border: 1px solid #C9B991; }
.stDataFrame thead th {
    background: #E2D6BE !important; font-size: 10px !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: #3B2F1F !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: 0 !important; }

/* Divider */
hr { border-color: #C9B991 !important; }

/* Caption */
[data-testid="stCaptionContainer"] { color: #6B5B45 !important; font-size: 12px !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }

/* Upload */
[data-testid="stFileUploader"] {
    border: 1px dashed #C9B991 !important;
    background: #ECE3D2 !important; border-radius: 0 !important;
}

/* Radio in main area */
.stRadio > label { font-size: 13px !important; color: #3B2F1F !important; }

/* Form submit button full width */
[data-testid="stForm"] .stButton > button { width: 100% !important; }

/* Success / warning / error */
div[data-testid="stAlert"] div { font-family: 'DM Sans', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
CLUSTERS = ["Economic", "Social", "Governance", "Security"]
ACTIVITY_TYPES = [
    "Original", "New (MTR addition)", "Transfer of activities", "Dropped"
]
FUNDING_STATUSES = [
    "To be proposed", "Committed", "Mobilised",
    "Committed/mobilised", "To be explored",
    "Committed/To be proposed", "Mobilised/To be proposed",
    "On going", "Other"
]
ROLES = ["admin", "editor", "viewer"]

CLUSTER_COLORS = {
    "Economic": "#C25B12", "Social": "#1F5F66",
    "Governance": "#5C2A4B", "Security": "#8E2A1F"
}
PALETTE = ["#C25B12","#1F5F66","#5C2A4B","#8E2A1F","#B58A14","#3A5A40",
           "#E07120","#3B2F1F","#978770","#6B5B45"]

PLOT_LAYOUT = dict(
    paper_bgcolor="#ECE3D2", plot_bgcolor="#ECE3D2",
    font=dict(family="DM Sans", color="#1B140B", size=11),
    margin=dict(l=10, r=10, t=46, b=10),
    legend=dict(font=dict(size=11)),
)

# ─── SUPABASE ─────────────────────────────────────────────────────────────────
@st.cache_resource
def init_supabase():
    url = "https://mferkujrkuhkriwildgk.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mZXJrdWpya3Voa3Jpd2lsZGdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3ODcxNzE3NSwiZXhwIjoyMDk0MjkzMTc1fQ.jBOhSXWlu419Mk0sIjmuPRwygxHE4fIljC-J255CpDU"
    return create_client(url, key)

supabase = init_supabase()

# ─── AUTH ─────────────────────────────────────────────────────────────────────
def do_login(email: str, password: str):
    try:
        resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return resp.user, resp.session, None
    except Exception as e:
        return None, None, str(e)

def do_logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def get_profile(user_id: str) -> dict:
    try:
        resp = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return resp.data or {}
    except Exception:
        return {"role": "viewer", "full_name": "Unknown"}

def check_auth():
    if "user" not in st.session_state:
        return None, None
    return st.session_state["user"], st.session_state.get("profile", {})

def role_rank(role: str) -> int:
    return {"viewer": 0, "editor": 1, "admin": 2}.get(role, 0)

def has_role(profile: dict, min_role: str) -> bool:
    return role_rank(profile.get("role", "viewer")) >= role_rank(min_role)

# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_activities() -> pd.DataFrame:
    try:
        resp = supabase.table("activities").select("*").order("id").execute()
        return pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Could not load activities: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def load_agencies() -> pd.DataFrame:
    try:
        resp = supabase.table("agencies").select("*").order("revised_outlay", desc=True).execute()
        return pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Could not load agencies: {e}")
        return pd.DataFrame()

def clear_cache():
    load_activities.clear()
    load_agencies.clear()

def log_action(user_id, action: str, table: str, record_id, details=None):
    try:
        supabase.table("audit_log").insert({
            "user_id": str(user_id),
            "action": action,
            "table_name": table,
            "record_id": str(record_id),
            "details": details or {},
        }).execute()
    except Exception:
        pass

# ─── LOGIN ────────────────────────────────────────────────────────────────────
def show_login():
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style="text-align:center; padding:48px 0 28px">
            <div style="background:#1B140B;color:#F2EBDE;width:56px;height:56px;
                display:inline-flex;align-items:center;justify-content:center;
                font-family:'Fraunces',serif;font-size:30px;font-style:italic;
                box-shadow:3px 3px 0 #C25B12;margin-bottom:18px">B</div>
            <h1 style="font-family:'Fraunces',serif;font-weight:400;font-size:26px;
                color:#1B140B;margin:0 0 4px">13th Five-Year Plan</h1>
            <p style="color:#6B5B45;font-size:11px;letter-spacing:0.18em;
                text-transform:uppercase;margin:0 0 32px">
                Mid-Term Review · Management System
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login"):
            email = st.text_input("Email address", placeholder="you@gov.bt")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please enter your email and password.")
            else:
                with st.spinner("Signing in…"):
                    user, session, err = do_login(email.strip(), password)
                if err:
                    st.error("Incorrect email or password.")
                else:
                    profile = get_profile(user.id)
                    st.session_state["user"] = user
                    st.session_state["session"] = session
                    st.session_state["profile"] = profile
                    st.rerun()

        st.markdown("""
        <p style="text-align:center;color:#978770;font-size:12px;margin-top:18px">
            Contact your administrator to get an account.
        </p>""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def show_sidebar(profile: dict) -> str:
    with st.sidebar:
        st.markdown("""
        <div style="padding:24px 4px 16px;border-bottom:1px solid rgba(201,185,145,0.25);margin-bottom:12px">
            <div style="font-family:'Fraunces',serif;font-size:20px;color:#F2EBDE;line-height:1.2">
                13th FYP · MTR</div>
            <div style="font-size:10px;letter-spacing:0.16em;text-transform:uppercase;
                color:#C25B12;margin-top:5px">Management System</div>
        </div>
        """, unsafe_allow_html=True)

        role = profile.get("role", "viewer")
        pages = ["📊  Dashboard", "🔍  Activity Explorer", "🏛  Agencies", "🤖  AI Assistant"]
        if role in ("admin", "editor"):
            pages += ["✏️  Manage Activities", "🏢  Manage Agencies"]
        if role == "admin":
            pages += ["📥  Import Data", "👥  User Management"]

        page = st.radio("Navigate", pages, label_visibility="collapsed")

        st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)
        st.markdown("---")
        name = profile.get("full_name") or profile.get("email", "User")
        st.markdown(f"""
        <div style="padding:4px 0 10px">
            <div style="font-size:13px;color:#C9B991">{name}</div>
            <div style="font-size:10px;letter-spacing:0.12em;text-transform:uppercase;
                color:#C25B12;margin-top:3px">{role}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Sign out"):
            do_logout()

    return page

# ─── DASHBOARD ────────────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown("## Dashboard")
    st.caption("Live overview · data refreshes every 30 seconds")

    acts = load_activities()
    ags = load_agencies()

    if acts.empty and ags.empty:
        st.info("No data yet. An **Admin** can upload the Excel file under **Import Data**.")
        return

    # KPIs
    total_init = ags["initial_outlay"].sum() if not ags.empty and "initial_outlay" in ags.columns else 0
    total_rev = ags["revised_outlay"].sum() if not ags.empty and "revised_outlay" in ags.columns else 0
    delta = total_rev - total_init
    new_n = len(acts[acts.get("activity_type","") == "New (MTR addition)"]) if not acts.empty else 0
    drop_n = len(acts[acts.get("activity_type","") == "Dropped"]) if not acts.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Activities", f"{len(acts):,}",
                  f"across {acts['agency'].nunique()} agencies" if "agency" in acts.columns else "")
    with c2:
        st.metric("Initial Outlay", f"Nu. {total_init/1000:,.1f} B", "million Ngultrum")
    with c3:
        st.metric("Revised Outlay", f"Nu. {total_rev/1000:,.1f} B",
                  f"{delta/1000:+.1f} B vs. initial")
    with c4:
        st.metric("MTR Changes", f"{new_n + drop_n}",
                  f"{new_n} new · {drop_n} dropped")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns([2, 1])

    with col1:
        if not ags.empty and "revised_outlay" in ags.columns:
            top = ags.nlargest(15, "revised_outlay").copy()
            short = top["agency_name"].str[:38]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=short, x=top["initial_outlay"],
                name="Initial", orientation="h",
                marker_color="#C9B991", marker_line_width=0,
            ))
            fig.add_trace(go.Bar(
                y=short, x=top["revised_outlay"],
                name="Revised", orientation="h",
                marker_color="#C25B12", marker_line_width=0,
            ))
            fig.update_layout(
                **PLOT_LAYOUT,
                title="Top 15 Agencies — Initial vs Revised Outlay (M Nu.)",
                barmode="group", height=520,
                xaxis=dict(title="M Nu.", gridcolor="rgba(201,185,145,0.35)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if not acts.empty and "cluster" in acts.columns:
            cd = acts.groupby("cluster")["outlay"].sum().reset_index().dropna()
            cd = cd[cd["cluster"].notna() & (cd["cluster"] != "")]
            fig2 = go.Figure(go.Pie(
                labels=cd["cluster"], values=cd["outlay"],
                hole=0.58,
                marker=dict(colors=[CLUSTER_COLORS.get(c, "#999") for c in cd["cluster"]],
                            line=dict(color="#F2EBDE", width=3)),
            ))
            fig2.update_layout(
                **PLOT_LAYOUT,
                title="By Cluster (Original Outlay)", height=290,
            )
            st.plotly_chart(fig2, use_container_width=True)

        if not acts.empty and "activity_type" in acts.columns:
            td = acts["activity_type"].value_counts().reset_index()
            td.columns = ["type", "count"]
            fig3 = px.bar(td, x="count", y="type", orientation="h",
                          color="type",
                          color_discrete_map={
                              "Original": "#3B2F1F",
                              "New (MTR addition)": "#3A5A40",
                              "Dropped": "#8E2A1F",
                              "Transfer of activities": "#B58A14",
                          })
            fig3.update_layout(
                **PLOT_LAYOUT,
                title="Activity Types", height=230,
                showlegend=False,
                yaxis_title=None, xaxis_title="Count",
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig3, use_container_width=True)

    # Net change chart
    if not ags.empty and "initial_outlay" in ags.columns and "revised_outlay" in ags.columns:
        dd = ags.copy()
        dd["diff"] = dd["revised_outlay"] - dd["initial_outlay"]
        dd = dd[dd["diff"].abs() > 0.01].sort_values("diff", ascending=True)
        if not dd.empty:
            fig4 = go.Figure(go.Bar(
                y=dd["agency_name"].str[:45],
                x=dd["diff"],
                orientation="h",
                marker_color=dd["diff"].apply(lambda x: "#3A5A40" if x >= 0 else "#8E2A1F"),
                marker_line_width=0,
            ))
            fig4.update_layout(
                **PLOT_LAYOUT,
                title="Net Outlay Change at Mid-Term Review (M Nu.)",
                height=420,
                xaxis=dict(gridcolor="rgba(201,185,145,0.35)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig4, use_container_width=True)

    # Funding status breakdown
    if not acts.empty and "funding_status" in acts.columns:
        def simplify_status(s):
            if not s: return "Unspecified"
            s = str(s)
            if "To be proposed" in s and "Committed" not in s: return "To be proposed"
            if "Committed" in s and "mobilised" in s.lower(): return "Committed/Mobilised"
            if s.strip().startswith("Committed"): return "Committed"
            if "Mobili" in s: return "Mobilised"
            if "To be explored" in s: return "To be explored"
            if "going" in s.lower(): return "Ongoing"
            return "Other"

        acts2 = acts.copy()
        acts2["status_simple"] = acts2["funding_status"].apply(simplify_status)
        status_cluster = acts2.groupby(["cluster", "status_simple"]).size().reset_index(name="count")
        status_cluster = status_cluster[status_cluster["cluster"].notna() & (status_cluster["cluster"] != "")]

        STATUS_COLORS = {
            "To be proposed": "#C9B991", "Committed": "#3A5A40",
            "Committed/Mobilised": "#1F5F66", "Mobilised": "#5C2A4B",
            "To be explored": "#B58A14", "Ongoing": "#C25B12",
            "Other": "#978770", "Unspecified": "#E2D6BE",
        }
        fig5 = px.bar(status_cluster, x="cluster", y="count", color="status_simple",
                      color_discrete_map=STATUS_COLORS,
                      barmode="stack", labels={"count": "Activities", "status_simple": "Funding Status"})
        fig5.update_layout(
            **PLOT_LAYOUT,
            title="Funding Status by Cluster",
            height=340,
            xaxis_title=None,
            yaxis=dict(gridcolor="rgba(201,185,145,0.35)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig5, use_container_width=True)

# ─── ACTIVITY EXPLORER ────────────────────────────────────────────────────────
def page_explorer():
    st.markdown("## Activity Explorer")
    st.caption("Browse, filter, and search all plan activities. Use the export button to download any filtered view.")

    acts = load_activities()
    if acts.empty:
        st.info("No activities loaded yet.")
        return

    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        search = st.text_input("🔍  Search activities", placeholder="activity name, project, remarks…")
    with c2:
        agency_opts = ["All"] + sorted(acts["agency"].dropna().unique().tolist())
        agency_f = st.selectbox("Agency", agency_opts)
    with c3:
        cluster_f = st.selectbox("Cluster", ["All"] + CLUSTERS)
    with c4:
        type_f = st.selectbox("Type", ["All"] + ACTIVITY_TYPES)

    f = acts.copy()
    if search:
        mask = (
            f.get("activity", pd.Series(dtype=str)).str.contains(search, case=False, na=False) |
            f.get("project", pd.Series(dtype=str)).str.contains(search, case=False, na=False) |
            f.get("remarks", pd.Series(dtype=str)).str.contains(search, case=False, na=False)
        )
        f = f[mask]
    if agency_f != "All":
        f = f[f["agency"] == agency_f]
    if cluster_f != "All":
        f = f[f["cluster"] == cluster_f]
    if type_f != "All":
        f = f[f["activity_type"] == type_f]

    total_outlay = f["outlay"].sum() if "outlay" in f.columns else 0
    st.caption(f"**{len(f):,}** activities · Total outlay: **Nu. {total_outlay:,.1f} M**")

    display_cols = [c for c in
        ["project", "activity", "agency", "cluster", "outlay", "revised_outlay",
         "activity_type", "funding_status", "funding_source", "lead_agency", "remarks"]
        if c in f.columns]

    col_cfg = {
        "project":        st.column_config.TextColumn("Project", width=200),
        "activity":       st.column_config.TextColumn("Activity", width=280),
        "agency":         st.column_config.TextColumn("Agency", width=90),
        "cluster":        st.column_config.TextColumn("Cluster", width=90),
        "outlay":         st.column_config.NumberColumn("Outlay (M Nu.)", format="%.1f", width=120),
        "revised_outlay": st.column_config.NumberColumn("Revised (M Nu.)", format="%.1f", width=120),
        "activity_type":  st.column_config.TextColumn("Type", width=120),
        "funding_status": st.column_config.TextColumn("Funding Status", width=160),
        "funding_source": st.column_config.TextColumn("Funding Source", width=180),
        "lead_agency":    st.column_config.TextColumn("Lead", width=100),
        "remarks":        st.column_config.TextColumn("Remarks", width=300),
    }

    st.dataframe(f[display_cols], column_config=col_cfg,
                 use_container_width=True, height=560)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        f.to_excel(writer, index=False, sheet_name="Filtered Activities")
    buf.seek(0)
    st.download_button(
        "⬇  Export to Excel",
        buf,
        f"activities_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# ─── AGENCIES ─────────────────────────────────────────────────────────────────
def page_agencies():
    st.markdown("## Agencies")
    st.caption("Outlay by implementing agency — initial plan vs. revised mid-term.")

    ags = load_agencies()
    if ags.empty:
        st.info("No agency data loaded yet.")
        return

    c1, c2 = st.columns(2)
    with c1:
        sort_by = st.selectbox("Sort by", ["Revised Outlay", "Initial Outlay", "Net Change", "Agency Name"])
    with c2:
        ascending = st.checkbox("Ascending order", False)

    ags2 = ags.copy()
    ags2["change"] = ags2["revised_outlay"] - ags2["initial_outlay"]
    sort_map = {
        "Revised Outlay": "revised_outlay",
        "Initial Outlay": "initial_outlay",
        "Net Change": "change",
        "Agency Name": "agency_name",
    }
    ags2 = ags2.sort_values(sort_map[sort_by], ascending=ascending)

    # Bar chart
    top = ags2.head(20)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=top["agency_name"].str[:40], x=top["initial_outlay"],
                         name="Initial", orientation="h",
                         marker_color="#C9B991", marker_line_width=0))
    fig.add_trace(go.Bar(y=top["agency_name"].str[:40], x=top["revised_outlay"],
                         name="Revised", orientation="h",
                         marker_color="#C25B12", marker_line_width=0))
    fig.update_layout(
        **PLOT_LAYOUT,
        title="Top 20 Agencies — Outlay Comparison (M Nu.)",
        barmode="group", height=560,
        xaxis=dict(title="M Nu.", gridcolor="rgba(201,185,145,0.35)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        legend=dict(orientation="h", y=1.06, x=1, xanchor="right"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Table
    def fmt_change(row):
        pct = (row["change"] / row["initial_outlay"] * 100) if row["initial_outlay"] else 0
        return f"{row['change']:+,.1f} ({pct:+.1f}%)"

    ags2["Change (M Nu.)"] = ags2.apply(fmt_change, axis=1)
    display_cols = [c for c in ["agency_name","initial_outlay","revised_outlay","Change (M Nu.)","remarks"] if c in ags2.columns]
    col_cfg = {
        "agency_name":    st.column_config.TextColumn("Agency", width=340),
        "initial_outlay": st.column_config.NumberColumn("Initial (M Nu.)", format="%.2f"),
        "revised_outlay": st.column_config.NumberColumn("Revised (M Nu.)", format="%.2f"),
        "Change (M Nu.)": st.column_config.TextColumn("Change"),
        "remarks":        st.column_config.TextColumn("Remarks", width=350),
    }
    st.dataframe(ags2[display_cols], column_config=col_cfg, use_container_width=True, height=400)

# ─── MANAGE ACTIVITIES ────────────────────────────────────────────────────────
def page_manage_activities(profile: dict):
    st.markdown("## Manage Activities")
    role = profile.get("role", "viewer")

    acts = load_activities()

    tab_edit, tab_add, tab_bulk = st.tabs(
        ["✏️  Edit / Delete", "➕  Add New Activity", "📋  Bulk Edit (table)"]
    )

    # ── EDIT / DELETE ──
    with tab_edit:
        if acts.empty:
            st.info("No activities in the database yet.")
        else:
            fc1, fc2, fc3 = st.columns([2, 1, 1])
            with fc1:
                search = st.text_input("Search", placeholder="activity or project name…", key="me_s")
            with fc2:
                ag_opts = ["All"] + sorted(acts["agency"].dropna().unique().tolist())
                ag_f = st.selectbox("Agency", ag_opts, key="me_ag")
            with fc3:
                cl_f = st.selectbox("Cluster", ["All"] + CLUSTERS, key="me_cl")

            f = acts.copy()
            if search:
                f = f[f["activity"].str.contains(search, case=False, na=False) |
                      f["project"].str.contains(search, case=False, na=False)]
            if ag_f != "All": f = f[f["agency"] == ag_f]
            if cl_f != "All": f = f[f["cluster"] == cl_f]

            if f.empty:
                st.info("No activities match these filters.")
            else:
                labels = f.apply(
                    lambda r: f"[{r.get('agency','')}]  {str(r.get('activity',''))[:80]}", axis=1
                ).tolist()
                selected = st.selectbox(f"Select from {len(f)} matching activities", labels)
                idx = labels.index(selected)
                row = f.iloc[idx]

                st.markdown("---")
                with st.form("edit_act"):
                    c1, c2 = st.columns(2)
                    with c1:
                        project       = st.text_input("Project", value=str(row.get("project","") or ""))
                        activity      = st.text_input("Activity *", value=str(row.get("activity","") or ""))
                        agency        = st.text_input("Agency code", value=str(row.get("agency","") or ""))
                        lead_agency   = st.text_input("Lead agency", value=str(row.get("lead_agency","") or ""))
                    with c2:
                        outlay         = st.number_input("Outlay (M Nu.)", value=float(row.get("outlay") or 0), step=0.01)
                        revised_outlay = st.number_input("Revised Outlay (M Nu.)", value=float(row.get("revised_outlay") or 0), step=0.01)
                        cluster = st.selectbox("Cluster", CLUSTERS,
                            index=CLUSTERS.index(row.get("cluster","Economic")) if row.get("cluster") in CLUSTERS else 0)
                        activity_type = st.selectbox("Activity Type", ACTIVITY_TYPES,
                            index=ACTIVITY_TYPES.index(row.get("activity_type","Original")) if row.get("activity_type") in ACTIVITY_TYPES else 0)
                    funding_source = st.text_input("Funding Source", value=str(row.get("funding_source","") or ""))
                    fs_opts = FUNDING_STATUSES
                    fs_val  = row.get("funding_status","To be proposed")
                    fs_idx  = fs_opts.index(fs_val) if fs_val in fs_opts else 0
                    funding_status = st.selectbox("Funding Status", fs_opts, index=fs_idx)
                    remarks = st.text_area("Remarks", value=str(row.get("remarks","") or ""))

                    bc1, bc2, _ = st.columns([1, 1, 3])
                    with bc1:
                        save = st.form_submit_button("💾  Save changes")
                    with bc2:
                        delete = st.form_submit_button("🗑  Delete", type="secondary")

                if save:
                    payload = dict(
                        project=project or None, activity=activity,
                        agency=agency or None, lead_agency=lead_agency or None,
                        outlay=outlay, revised_outlay=revised_outlay,
                        cluster=cluster, activity_type=activity_type,
                        funding_source=funding_source or None,
                        funding_status=funding_status,
                        remarks=remarks or None,
                        updated_at=datetime.utcnow().isoformat(),
                    )
                    try:
                        supabase.table("activities").update(payload).eq("id", int(row["id"])).execute()
                        log_action(st.session_state["user"].id, "UPDATE", "activities", row["id"])
                        clear_cache()
                        st.success("✅  Activity updated!")
                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

                if delete:
                    if not has_role(profile, "admin"):
                        st.error("Only Admins can delete records.")
                    else:
                        try:
                            supabase.table("activities").delete().eq("id", int(row["id"])).execute()
                            log_action(st.session_state["user"].id, "DELETE", "activities", row["id"])
                            clear_cache()
                            st.success("Record deleted.")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    # ── ADD NEW ──
    with tab_add:
        st.markdown("**Add a new activity to the plan database**")
        with st.form("add_act"):
            c1, c2 = st.columns(2)
            with c1:
                project       = st.text_input("Project")
                activity      = st.text_input("Activity *")
                agency        = st.text_input("Agency code")
                lead_agency   = st.text_input("Lead agency")
            with c2:
                outlay         = st.number_input("Outlay (M Nu.)", min_value=0.0, step=0.01)
                revised_outlay = st.number_input("Revised Outlay (M Nu.)", min_value=0.0, step=0.01)
                cluster        = st.selectbox("Cluster", CLUSTERS)
                activity_type  = st.selectbox("Activity Type", ACTIVITY_TYPES)
            funding_source = st.text_input("Funding Source")
            funding_status = st.selectbox("Funding Status", FUNDING_STATUSES)
            remarks        = st.text_area("Remarks")
            submitted = st.form_submit_button("➕  Add Activity", use_container_width=True)

        if submitted:
            if not activity.strip():
                st.error("Activity name is required.")
            else:
                try:
                    res = supabase.table("activities").insert(dict(
                        project=project or None, activity=activity.strip(),
                        agency=agency or None, lead_agency=lead_agency or None,
                        outlay=outlay, revised_outlay=revised_outlay,
                        cluster=cluster, activity_type=activity_type,
                        funding_source=funding_source or None,
                        funding_status=funding_status,
                        remarks=remarks or None,
                        created_by=str(st.session_state["user"].id),
                    )).execute()
                    log_action(st.session_state["user"].id, "INSERT", "activities", res.data[0]["id"])
                    clear_cache()
                    st.success("✅  Activity added!")
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── BULK EDIT ──
    with tab_bulk:
        st.markdown("**Edit multiple rows at once**")
        st.info("Make your changes in the table below, then click **Save all changes**. "
                "Shows up to 200 rows — use filters in Activity Explorer to narrow down first.", icon="ℹ️")

        edit_cols = [c for c in
            ["id","project","activity","agency","cluster","outlay","revised_outlay",
             "funding_status","activity_type","remarks"]
            if c in acts.columns]

        edited_df = st.data_editor(
            acts[edit_cols].head(200),
            column_config={
                "id":             st.column_config.NumberColumn("ID", disabled=True, width=60),
                "project":        st.column_config.TextColumn("Project", width=180),
                "activity":       st.column_config.TextColumn("Activity", width=280),
                "agency":         st.column_config.TextColumn("Agency", width=90),
                "cluster":        st.column_config.SelectboxColumn("Cluster", options=CLUSTERS),
                "outlay":         st.column_config.NumberColumn("Outlay (M)", format="%.2f"),
                "revised_outlay": st.column_config.NumberColumn("Revised (M)", format="%.2f"),
                "funding_status": st.column_config.SelectboxColumn("Funding", options=FUNDING_STATUSES),
                "activity_type":  st.column_config.SelectboxColumn("Type", options=ACTIVITY_TYPES),
                "remarks":        st.column_config.TextColumn("Remarks", width=260),
            },
            use_container_width=True, num_rows="fixed", height=520,
        )

        if st.button("💾  Save all changes", type="primary"):
            errors = []
            with st.spinner("Saving…"):
                for _, row in edited_df.iterrows():
                    try:
                        supabase.table("activities").update({
                            "project":        row.get("project"),
                            "activity":       row.get("activity"),
                            "agency":         row.get("agency"),
                            "cluster":        row.get("cluster"),
                            "outlay":         float(row.get("outlay") or 0),
                            "revised_outlay": float(row.get("revised_outlay") or 0),
                            "funding_status": row.get("funding_status"),
                            "activity_type":  row.get("activity_type"),
                            "remarks":        row.get("remarks"),
                            "updated_at":     datetime.utcnow().isoformat(),
                        }).eq("id", int(row["id"])).execute()
                    except Exception as e:
                        errors.append(str(e))
            if errors:
                st.error(f"{len(errors)} rows failed: {errors[0]}")
            else:
                log_action(st.session_state["user"].id, "BULK_UPDATE", "activities", "multiple")
                clear_cache()
                st.success(f"✅  Saved {len(edited_df)} rows.")

# ─── MANAGE AGENCIES ──────────────────────────────────────────────────────────
def page_manage_agencies(profile: dict):
    st.markdown("## Manage Agencies")

    ags = load_agencies()
    tab_edit, tab_add = st.tabs(["✏️  Edit / Delete", "➕  Add New Agency"])

    with tab_edit:
        if ags.empty:
            st.info("No agencies in the database yet.")
        else:
            names = ags["agency_name"].tolist()
            selected = st.selectbox("Select agency", names)
            row = ags[ags["agency_name"] == selected].iloc[0]

            with st.form("edit_ag"):
                name    = st.text_input("Agency name *", value=str(row.get("agency_name","")))
                c1, c2  = st.columns(2)
                with c1:
                    initial = st.number_input("Initial Outlay (M Nu.)", value=float(row.get("initial_outlay") or 0), step=0.01)
                with c2:
                    revised = st.number_input("Revised Outlay (M Nu.)", value=float(row.get("revised_outlay") or 0), step=0.01)
                remarks = st.text_area("Remarks", value=str(row.get("remarks","") or ""))
                bc1, bc2, _ = st.columns([1, 1, 3])
                with bc1: save   = st.form_submit_button("💾  Save")
                with bc2: delete = st.form_submit_button("🗑  Delete", type="secondary")

            if save:
                try:
                    supabase.table("agencies").update({
                        "agency_name": name, "initial_outlay": initial,
                        "revised_outlay": revised, "remarks": remarks or None,
                    }).eq("id", int(row["id"])).execute()
                    log_action(st.session_state["user"].id, "UPDATE", "agencies", row["id"])
                    clear_cache()
                    st.success("✅  Agency updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

            if delete:
                if not has_role(profile, "admin"):
                    st.error("Only Admins can delete agencies.")
                else:
                    try:
                        supabase.table("agencies").delete().eq("id", int(row["id"])).execute()
                        clear_cache()
                        st.success("Agency deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_add:
        with st.form("add_ag"):
            name    = st.text_input("Agency name *")
            c1, c2  = st.columns(2)
            with c1:
                initial = st.number_input("Initial Outlay (M Nu.)", min_value=0.0, step=0.01)
            with c2:
                revised = st.number_input("Revised Outlay (M Nu.)", min_value=0.0, step=0.01)
            remarks  = st.text_area("Remarks")
            submitted = st.form_submit_button("➕  Add Agency", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Agency name is required.")
            else:
                try:
                    supabase.table("agencies").insert({
                        "agency_name": name.strip(),
                        "initial_outlay": initial,
                        "revised_outlay": revised,
                        "remarks": remarks or None,
                    }).execute()
                    log_action(st.session_state["user"].id, "INSERT", "agencies", name)
                    clear_cache()
                    st.success(f"✅  Agency '{name}' added!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ─── IMPORT DATA ──────────────────────────────────────────────────────────────
def page_import(user):
    st.markdown("## Import Data")
    st.caption("Upload an Excel file to populate or update the database.")

    st.warning(
        "**Heads up:** 'Append' adds records to whatever is already in the database. "
        "'Replace all' wipes existing data first, then imports. When in doubt, use Append.",
        icon="⚠️"
    )

    mode = st.radio("Import mode",
                    ["Append — add to existing data", "Replace all — wipe then import"])

    uploaded = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
    if not uploaded:
        st.info("Drop your .xlsx file above and a preview will appear.")
        return

    try:
        xl = pd.ExcelFile(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return

    st.success(f"**{uploaded.name}** uploaded · Sheets: {', '.join(xl.sheet_names)}")

    # Detect main sheet
    main_sheet = next(
        (s for s in xl.sheet_names if "Plan Database" in s or "13th" in s),
        xl.sheet_names[0]
    )
    has_header_row = "Plan Database" in main_sheet

    try:
        df = pd.read_excel(xl, sheet_name=main_sheet, header=1 if has_header_row else 0)
        df = df.dropna(how="all")
    except Exception as e:
        st.error(f"Error reading sheet '{main_sheet}': {e}")
        return

    st.markdown(f"**Preview** — *{main_sheet}* · {len(df)} rows")
    st.dataframe(df.head(6), use_container_width=True)

    COL_MAP = {
        "Project": "project",
        "Activity": "activity",
        "Outlay (Nu. in Million)": "outlay",
        "Revised Outlay Nu. in million": "revised_outlay",
        "Funding Source": "funding_source",
        "Funding status": "funding_status",
        "Lead Implementing Agency": "lead_agency",
        "Agency": "agency",
        "Cluster": "cluster",
        "Activity Type (MTR Update)": "activity_type",
        "Remarks": "remarks",
        "MTR Remarks": "remarks",
    }
    df = df.rename(columns={k: v for k, v in COL_MAP.items() if k in df.columns})

    if "activity" not in df.columns:
        st.error("Could not find an 'Activity' column. Make sure you're uploading the correct file.")
        return

    # Count valid rows
    valid = df[df["activity"].notna() & (df["activity"].astype(str).str.strip() != "")]
    st.caption(f"{len(valid)} valid activity rows found")

    if st.button("🚀  Start import", type="primary"):
        with st.spinner("Importing…"):
            progress = st.progress(0, text="Preparing…")

            if "Replace" in mode:
                supabase.table("activities").delete().neq("id", 0).execute()
                progress.progress(10, text="Cleared existing activities.")

            records = []
            for _, row in valid.iterrows():
                rec = {}
                for col in ["project","activity","agency","lead_agency",
                            "funding_source","funding_status","cluster","activity_type","remarks"]:
                    v = row.get(col)
                    rec[col] = str(v).strip() if pd.notna(v) and str(v).strip().lower() != "nan" else None
                for col in ["outlay", "revised_outlay"]:
                    try:
                        v = row.get(col)
                        rec[col] = float(v) if pd.notna(v) else None
                    except Exception:
                        rec[col] = None
                if rec.get("activity"):
                    records.append(rec)

            BATCH = 100
            for i in range(0, len(records), BATCH):
                supabase.table("activities").insert(records[i:i+BATCH]).execute()
                pct = min(10 + int(85 * (i + BATCH) / len(records)), 95)
                progress.progress(pct, text=f"Inserted {min(i+BATCH, len(records))} / {len(records)} activities…")

            # Agency sheet
            if "Outlay -Agency wise" in xl.sheet_names:
                try:
                    ag_df = pd.read_excel(xl, sheet_name="Outlay -Agency wise", header=1)
                    ag_df = ag_df.dropna(subset=["Agency"])
                    ag_df = ag_df[ag_df["Agency"].astype(str).str.strip().str.len() > 2]

                    if "Replace" in mode:
                        supabase.table("agencies").delete().neq("id", 0).execute()

                    ag_records = []
                    for _, row in ag_df.iterrows():
                        name = str(row.get("Agency","")).strip()
                        if not name or name.lower() in ("total","grand total","nan"):
                            continue
                        try:
                            v = row.get("Final Initial Outlay \n(Nu. in million)", 0)
                            init_v = 0.0 if (v is None or str(v).strip() in ('', 'nan', 'NaN')) else float(v)
                        except Exception:
                            init_v = 0.0
                        try:
                            v = row.get("Revised MTR Outlay (Nu. in million)", 0)
                            rev_v = 0.0 if (v is None or str(v).strip() in ('', 'nan', 'NaN')) else float(v)
                        except Exception:
                            rev_v = 0.0
                        rmk = row.get("Remarks","")
                        rmk = str(rmk).strip() if pd.notna(rmk) and str(rmk).lower() != "nan" else None
                        if init_v == 0 and rev_v == 0:
                            continue
                        ag_records.append({
                            "agency_name": name,
                            "initial_outlay": init_v,
                            "revised_outlay": rev_v,
                            "remarks": rmk,
                        })

                    for i in range(0, len(ag_records), BATCH):
                        supabase.table("agencies").insert(ag_records[i:i+BATCH]).execute()

                    progress.progress(98, text=f"Imported {len(ag_records)} agency records.")
                except Exception as e:
                    st.warning(f"Activities imported OK, but agency sheet failed: {e}")

            log_action(user.id, "IMPORT", "activities", "bulk",
                       {"count": len(records), "mode": mode})
            clear_cache()
            progress.progress(100, text="Done!")

        st.success(f"✅  Imported **{len(records)}** activities successfully!")
        st.balloons()

# ─── USER MANAGEMENT ──────────────────────────────────────────────────────────
def page_users(user):
    st.markdown("## User Management")
    st.caption("Manage who can access the system and at what permission level.")

    tab_all, tab_invite, tab_log = st.tabs(["👥  All Users", "📨  Invite User", "📋  Audit Log"])

    # ── ALL USERS ──
    with tab_all:
        try:
            resp = supabase.table("profiles").select("*").order("created_at", desc=True).execute()
            users_df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
        except Exception as e:
            st.error(f"Could not load users: {e}")
            users_df = pd.DataFrame()

        if users_df.empty:
            st.info("No users found. Use the Invite tab to add the first user.")
        else:
            disp_cols = [c for c in ["full_name","email","role","created_at"] if c in users_df.columns]
            st.dataframe(users_df[disp_cols], use_container_width=True,
                         column_config={
                             "full_name": st.column_config.TextColumn("Name", width=200),
                             "email":     st.column_config.TextColumn("Email", width=250),
                             "role":      st.column_config.TextColumn("Role", width=100),
                             "created_at":st.column_config.DatetimeColumn("Created", width=160),
                         })

            st.markdown("---")
            st.markdown("**Update a user's role**")
            if "email" in users_df.columns:
                sel_email = st.selectbox("Select user", users_df["email"].tolist())
                sel_row   = users_df[users_df["email"] == sel_email].iloc[0]
                cur_role  = sel_row.get("role","viewer")
                new_role  = st.selectbox("New role", ROLES,
                    index=ROLES.index(cur_role) if cur_role in ROLES else 0,
                    help="admin: full access · editor: add/edit, no delete · viewer: read-only")
                col1, _ = st.columns([1, 4])
                with col1:
                    if st.button("Update role"):
                        try:
                            supabase.table("profiles").update({"role": new_role}).eq("id", sel_row["id"]).execute()
                            log_action(user.id, "UPDATE_ROLE", "profiles", sel_row["id"],
                                       {"email": sel_email, "role": new_role})
                            st.success(f"Updated {sel_email} → **{new_role}**")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    # ── INVITE ──
    with tab_invite:
        st.markdown("**Invite a new team member**")
        st.info(
            "Supabase will send an email with a link so the person can set their own password. "
            "If you don't receive the email, check your Supabase project's **Auth → Email Templates** settings.",
            icon="📧"
        )
        with st.form("invite_form"):
            inv_email = st.text_input("Email address *")
            inv_name  = st.text_input("Full name")
            inv_role  = st.selectbox("Role", ROLES,
                help="admin: full access · editor: add/edit/bulk, no delete · viewer: read-only")
            inv_sub   = st.form_submit_button("📨  Send invitation", use_container_width=True)

        if inv_sub:
            if not inv_email.strip():
                st.error("Email is required.")
            else:
                try:
                    resp = supabase.auth.admin.invite_user_by_email(inv_email.strip())
                    uid  = resp.user.id
                    supabase.table("profiles").upsert({
                        "id":        str(uid),
                        "email":     inv_email.strip(),
                        "full_name": inv_name.strip() or None,
                        "role":      inv_role,
                    }).execute()
                    log_action(user.id, "INVITE", "profiles", uid,
                               {"email": inv_email, "role": inv_role})
                    st.success(f"✅  Invitation sent to **{inv_email}** as **{inv_role}**.")
                except Exception as e:
                    st.error(f"Error inviting user: {e}")

    # ── AUDIT LOG ──
    with tab_log:
        try:
            resp = supabase.table("audit_log").select("*").order("created_at", desc=True).limit(200).execute()
            log_df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
        except Exception as e:
            st.error(f"Could not load audit log: {e}")
            log_df = pd.DataFrame()

        if log_df.empty:
            st.info("No audit log entries yet.")
        else:
            disp = [c for c in ["created_at","action","table_name","record_id","user_id"] if c in log_df.columns]
            st.dataframe(log_df[disp], use_container_width=True, height=500,
                         column_config={
                             "created_at": st.column_config.DatetimeColumn("Timestamp", width=160),
                             "action":     st.column_config.TextColumn("Action", width=120),
                             "table_name": st.column_config.TextColumn("Table", width=100),
                             "record_id":  st.column_config.TextColumn("Record", width=100),
                             "user_id":    st.column_config.TextColumn("User ID", width=280),
                         })

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    user, profile = check_auth()

    if user is None:
        show_login()
        return

    page = show_sidebar(profile)
    role = profile.get("role", "viewer")

    route_map = {
        "📊  Dashboard":          page_dashboard,
        "🔍  Activity Explorer":  page_explorer,
        "🏛  Agencies":           page_agencies,
        "🤖  AI Assistant":       page_ai_assistant,
    }
    if has_role(profile, "editor"):
        route_map["✏️  Manage Activities"] = lambda: page_manage_activities(profile)
        route_map["🏢  Manage Agencies"]   = lambda: page_manage_agencies(profile)
    if has_role(profile, "admin"):
        route_map["📥  Import Data"]       = lambda: page_import(user)
        route_map["👥  User Management"]   = lambda: page_users(user)

    fn = route_map.get(page)
    if fn:
        fn()
    else:
        st.error("You don't have permission to view this page.")


if __name__ == "__main__":
    main()
# ─── AI ASSISTANT ─────────────────────────────────────────────────────────────
def page_ai_assistant():
    st.markdown("## AI Assistant")
    st.caption("Ask anything about the 13th Five-Year Plan data. Powered by Claude AI.")

    # Init chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_context_loaded" not in st.session_state:
        st.session_state.chat_context_loaded = False

    # Load data for context
    acts = load_activities()
    ags  = load_agencies()

    # Build a compact data summary for Claude's context
    def build_context():
        lines = []
        lines.append("=== 13th Five-Year Plan Mid-Term Review Database ===")
        lines.append(f"Total activities: {len(acts)}")

        if not acts.empty:
            total_outlay = acts['outlay'].sum()
            lines.append(f"Total original outlay: Nu. {total_outlay:,.1f} million")

            # Cluster summary
            if 'cluster' in acts.columns:
                lines.append("\n--- Outlay by Cluster ---")
                cluster_grp = acts.groupby('cluster')['outlay'].agg(['sum','count'])
                for cl, row in cluster_grp.iterrows():
                    lines.append(f"  {cl}: Nu. {row['sum']:,.1f}M ({int(row['count'])} activities)")

            # Activity type summary
            if 'activity_type' in acts.columns:
                lines.append("\n--- Activity Types ---")
                type_grp = acts['activity_type'].value_counts()
                for t, c in type_grp.items():
                    lines.append(f"  {t}: {c}")

            # Funding status summary
            if 'funding_status' in acts.columns:
                lines.append("\n--- Funding Status Summary ---")
                fund_grp = acts['funding_status'].value_counts().head(8)
                for f, c in fund_grp.items():
                    lines.append(f"  {f}: {c} activities")

            # Top agencies by outlay
            if 'agency' in acts.columns:
                lines.append("\n--- Top 10 Agencies by Original Outlay ---")
                ag_grp = acts.groupby('agency')['outlay'].sum().nlargest(10)
                for ag, v in ag_grp.items():
                    lines.append(f"  {ag}: Nu. {v:,.1f}M")

        # Agency-wise initial vs revised
        if not ags.empty:
            lines.append("\n--- Agency Outlay: Initial vs Revised (MTR) ---")
            total_init = ags['initial_outlay'].sum()
            total_rev  = ags['revised_outlay'].sum()
            lines.append(f"Total initial: Nu. {total_init:,.1f}M")
            lines.append(f"Total revised: Nu. {total_rev:,.1f}M")
            lines.append(f"Net change: Nu. {total_rev - total_init:+,.1f}M ({(total_rev-total_init)/total_init*100:+.1f}%)")

            lines.append("\nAgency changes (sorted by increase):")
            ags2 = ags.copy()
            ags2['diff'] = ags2['revised_outlay'] - ags2['initial_outlay']
            for _, r in ags2.sort_values('diff', ascending=False).head(15).iterrows():
                lines.append(f"  {r['agency_name']}: {r['diff']:+,.1f}M (initial {r['initial_outlay']:,.1f} → revised {r['revised_outlay']:,.1f})")

        # Sample of individual activities (first 200 for context)
        if not acts.empty:
            lines.append("\n--- Activity Records (sample) ---")
            sample_cols = [c for c in ['project','activity','agency','cluster','outlay','activity_type','funding_status','remarks'] if c in acts.columns]
            for _, row in acts[sample_cols].head(200).iterrows():
                parts = []
                for col in sample_cols:
                    v = row.get(col)
                    if v and str(v).strip() and str(v).lower() != 'nan':
                        parts.append(f"{col}: {str(v)[:80]}")
                lines.append("  | " + " | ".join(parts))

        return "\n".join(lines)

    # Suggestion chips
    suggestions = [
        "Which cluster has the highest outlay?",
        "Which agencies had the biggest increase at MTR?",
        "How many activities were dropped?",
        "What is the total outlay for the Economic cluster?",
        "Show me activities with no funding committed",
        "Which agencies had their outlay reduced?",
        "What are the new activities added at MTR?",
        "Summarise the overall plan performance",
    ]

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🇧🇹"):
                st.markdown(msg["content"])

    # Suggestion chips — only show if no conversation yet
    if not st.session_state.chat_history:
        st.markdown("**Try asking:**")
        cols = st.columns(2)
        for i, sug in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state._ai_prompt = sug
                    st.rerun()

    # Handle suggestion button clicks
    pre_prompt = st.session_state.pop("_ai_prompt", None)

    # Chat input
    user_input = st.chat_input("Ask about the plan data…")
    if pre_prompt:
        user_input = pre_prompt

    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call Claude
        with st.chat_message("assistant", avatar="🇧🇹"):
            with st.spinner("Analysing plan data…"):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

                    # Build context once per session
                    if not st.session_state.chat_context_loaded:
                        st.session_state.plan_context = build_context()
                        st.session_state.chat_context_loaded = True

                    system_prompt = f"""You are an expert analyst for the Royal Government of Bhutan's 13th Five-Year Plan Mid-Term Review. You have deep knowledge of the plan database and help officials understand the data.

Here is the complete plan database summary:

{st.session_state.plan_context}

Guidelines:
- Answer questions directly and precisely using the data above
- Use Nu. (Ngultrum) and millions when discussing outlays
- Be concise but thorough — officials need clear, actionable insights
- When listing items, use bullet points or tables for clarity
- If asked to compare, show both figures and the difference
- If data is not available for a question, say so clearly
- Format numbers with commas for readability (e.g. 12,345.6)
- You represent the Government of Bhutan — be professional and precise"""

                    # Build messages for API
                    messages = []
                    for h in st.session_state.chat_history[:-1]:  # exclude current
                        messages.append({"role": h["role"], "content": h["content"]})
                    messages.append({"role": "user", "content": user_input})

                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1500,
                        system=system_prompt,
                        messages=messages,
                    )
                    reply = response.content[0].text

                except ImportError:
                    reply = "⚠️ The `anthropic` package is not installed. Please add `anthropic>=0.25.0` to requirements.txt on GitHub and redeploy."
                except KeyError:
                    reply = "⚠️ No Anthropic API key found. Please add `ANTHROPIC_API_KEY = \"sk-ant-...\"` to your Streamlit secrets."
                except Exception as e:
                    reply = f"⚠️ Error calling AI: {str(e)}"

            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("---")
        col1, _ = st.columns([1, 5])
        with col1:
            if st.button("🗑 Clear chat"):
                st.session_state.chat_history = []
                st.session_state.chat_context_loaded = False
                st.rerun()
