import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("reports.csv")

st.set_page_config(page_title="AquaRoute | Flood-aware mobility", page_icon="🌧️", layout="wide")

DEMO_REPORTS = [
    {"location":"T. Nagar (demo)", "latitude":13.0418, "longitude":80.2337, "severity":"High", "water_depth_cm":25, "notes":"Illustrative demo report", "source":"Sample data", "reported_at":"Demo"},
    {"location":"Velachery (demo)", "latitude":12.9750, "longitude":80.2210, "severity":"Medium", "water_depth_cm":12, "notes":"Illustrative demo report", "source":"Sample data", "reported_at":"Demo"},
    {"location":"Anna Nagar (demo)", "latitude":13.0850, "longitude":80.2101, "severity":"Low", "water_depth_cm":4, "notes":"Illustrative demo report", "source":"Sample data", "reported_at":"Demo"},
]

def load_reports():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            if not df.empty:
                return df
        except Exception:
            pass
    return pd.DataFrame(DEMO_REPORTS)

def save_report(report):
    df = pd.DataFrame([report])
    if DATA_FILE.exists():
        df.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(DATA_FILE, index=False)

st.title("🌧️ AquaRoute")
st.subheader("Hyperlocal flood-aware mobility and road-condition reporting")
st.info("Prototype notice: Map markers labelled “Sample data” are illustrative only. They are not live observations, official warnings, or verified road conditions.")

reports = load_reports()

with st.sidebar:
    st.header("About this prototype")
    st.write("AquaRoute explores how community reports and optional sensor observations could help commuters understand local waterlogging.")
    st.caption("Current stage: student demonstration prototype")
    st.divider()
    st.header("Submit a road report")
    with st.form("report_form", clear_on_submit=True):
        location = st.text_input("Location / road name", placeholder="e.g. Near a named junction")
        col1, col2 = st.columns(2)
        lat = col1.number_input("Latitude", value=13.0827, format="%.6f")
        lon = col2.number_input("Longitude", value=80.2707, format="%.6f")
        severity = st.selectbox("Observed waterlogging", ["Low", "Medium", "High"])
        depth = st.number_input("Estimated water depth (cm)", min_value=0, max_value=200, value=0)
        notes = st.text_area("Additional notes (optional)")
        submitted = st.form_submit_button("Submit report")
        if submitted:
            if not location.strip():
                st.error("Please enter a location or road name.")
            elif not (-90 <= lat <= 90 and -180 <= lon <= 180):
                st.error("Please enter valid coordinates.")
            else:
                report = {
                    "location": location.strip(),
                    "latitude": lat,
                    "longitude": lon,
                    "severity": severity,
                    "water_depth_cm": depth,
                    "notes": notes.strip(),
                    "source": "Community-submitted (unverified)",
                    "reported_at": datetime.now(timezone.utc).isoformat(timespec="minutes")
                }
                save_report(report)
                st.success("Report saved locally. It is unverified and should be checked before being relied upon.")
                st.rerun()

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Reports shown", len(reports))
c2.metric("High-severity reports", int((reports["severity"] == "High").sum()) if "severity" in reports else 0)
c3.metric("Data type", "Demo + local entries")

st.markdown("### Chennai waterlogging overview")
center = [13.0827, 80.2707]
m = folium.Map(location=center, zoom_start=11, control_scale=True)
colors = {"Low":"green", "Medium":"orange", "High":"red"}
for _, r in reports.iterrows():
    try:
        sev = str(r.get("severity", "Unknown"))
        popup = (
            f"<b>{r.get('location','Unknown')}</b><br>"
            f"Severity: {sev}<br>"
            f"Estimated depth: {r.get('water_depth_cm','N/A')} cm<br>"
            f"Source: {r.get('source','Unknown')}<br>"
            f"Reported: {r.get('reported_at','Unknown')}<br>"
            f"Note: {r.get('notes','')}"
        )
        folium.CircleMarker(
            location=[float(r["latitude"]), float(r["longitude"])],
            radius=9, color=colors.get(sev, "blue"), fill=True,
            fill_opacity=0.75, popup=folium.Popup(popup, max_width=300),
            tooltip=f"{r.get('location','Location')} — {sev}"
        ).add_to(m)
    except Exception:
        continue

st_folium(m, use_container_width=True, height=480, returned_objects=[])

st.markdown("### Report register")
display_cols = [c for c in ["location", "severity", "water_depth_cm", "source", "reported_at", "notes"] if c in reports.columns]
st.dataframe(reports[display_cols], use_container_width=True, hide_index=True)

st.markdown("### Route guidance (prototype limitation)")
st.write("This version does not calculate verified safe routes. It can show reported hazard locations, but road closures, passability, traffic and current water depth are not independently verified.")
st.caption("Never use this prototype for emergency decisions. Follow official instructions and local authorities.")
