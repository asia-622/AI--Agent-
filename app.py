import streamlit as st

# Safe imports
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except:
    PLOTLY_AVAILABLE = False
    st.warning("📊 Charts disabled (Plotly not available)")

import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("🤖 AI Agent Dashboard")

# Data
data = {
    'Date': pd.date_range('2024-01-01', periods=7),
    'Users': [100, 150, 200, 250, 300, 350, 400],
    'Queries': [50, 75, 100, 125, 150, 175, 200]
}
df = pd.DataFrame(data)

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", "400")
col2.metric("Total Queries", "875")
col3.metric("Growth", "+25%")

# Charts (Safe)
if PLOTLY_AVAILABLE:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df, x='Date', y='Users', title="Users")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='Date', y='Queries', title="Queries")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("🔄 Install plotly for charts")

# AI Section
st.header("🤖 AI Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

st.success("✅ DASHBOARD WORKING!")
