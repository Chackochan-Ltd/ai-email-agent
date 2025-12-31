import streamlit as st
import pandas as pd
import os
import subprocess

st.set_page_config(
    page_title="AI Email Automation Agent",
    layout="wide"
)

st.title("📧 AI Email Automation Agent")
st.caption("Gmail + Gemini | End-to-End Automation Control Panel")

LOG_FILE = "data/logs.csv"

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("⚙️ Controls")

auto_send = st.sidebar.toggle(
    "Enable Auto-Send Replies",
    value=True
)

if auto_send:
    st.sidebar.success("Auto-send is ENABLED")
else:
    st.sidebar.warning("Auto-send is DISABLED (manual run only)")

run_agent = st.sidebar.button("▶️ Run Email Agent")

# ----------------------------
# Run Agent
# ----------------------------
if run_agent:
    st.info("Running email automation agent...")
    subprocess.run(
        ["python", "app/main.py"],
        check=False
    )
    st.success("Agent execution completed.")

# ----------------------------
# Logs Section
# ----------------------------
st.subheader("📊 Workflow Logs")

if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)

    if not df.empty:
        st.dataframe(
            df.sort_values("timestamp", ascending=False),
            use_container_width=True
        )
    else:
        st.warning("Log file is empty.")
else:
    st.warning("No logs found. Run the agent to generate logs.")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption(
    "Built as a production-style AI automation system with Gmail API, Gemini AI, "
    "and human-in-the-loop safety controls."
)
