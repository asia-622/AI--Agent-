import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="AI Agent Dashboard", layout="wide")

# Title
st.title("🤖 AI Agent Analytics Dashboard")
st.markdown("---")

# Sample Data (APNA DATA YAHAN DALO)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=30)
    data = {
        'Date': dates,
        'Users': np.random.randint(50, 500, 30).cumsum(),
        'Queries': np.random.randint(10, 100, 30),
        'Responses': np.random.randint(8, 95, 30),
        'Accuracy': np.random.uniform(0.75, 0.98, 30),
        'Category': np.random.choice(['Chat', 'Analysis', 'Code', 'Search'], 30)
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar
st.sidebar.title("⚙️ Controls")
show_ai = st.sidebar.checkbox("🤖 AI Agent")
refresh = st.sidebar.button("🔄 Refresh Data")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{df['Users'].iloc[-1]:,}", f"+{df['Users'].iloc[-1]-df['Users'].iloc[-2]}")
col2.metric("Total Queries", f"{df['Queries'].sum():,}")
col3.metric("Avg Accuracy", f"{df['Accuracy'].mean():.1%}")
col4.metric("Response Rate", f"{(df['Responses'].sum()/df['Queries'].sum()):.1%}")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Users Growth")
    fig1 = px.line(df, x='Date', y='Users', 
                   title="Daily Active Users",
                   markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 Query Categories")
    fig2 = px.pie(df, names='Category', 
                  values='Queries',
                  title="Query Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)
with col1:
    st.subheader("⚡ Performance")
    fig3 = px.bar(df.tail(7), x='Date', y=['Queries', 'Responses'],
                  title="Last 7 Days Activity")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📊 Accuracy Trend")
    fig4 = px.line(df, x='Date', y='Accuracy',
                   title="Model Accuracy",
                   markers=True)
    st.plotly_chart(fig4, use_container_width=True)

# AI Agent Section
if show_ai:
    st.markdown("---")
    st.header("🤖 AI Agent Chat")
    
    # Chat Input
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask AI Agent..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI Response (Demo)
        with st.chat_message("assistant"):
            response = f"✅ Thanks for asking: '{prompt[:20]}...' \n\nDemo response generated!"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("*Dashboard by Blackbox AI*")
