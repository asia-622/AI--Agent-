import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="AI Agent + Dashboard", layout="wide")

# Sidebar - Toggle between AI & Dashboard
st.sidebar.title("🚀 Control Panel")
page = st.sidebar.selectbox("Choose Mode:", ["🤖 AI Agent", "📊 Dashboard"])

# SAMPLE DATA FOR DASHBOARD
@st.cache_data
def get_dashboard_data():
    dates = pd.date_range('2024-01-01', periods=30)
    return pd.DataFrame({
        'Date': dates,
        'Users': np.random.randint(50, 500, 30).cumsum(),
        'Queries': np.random.randint(10, 100, 30),
        'AI_Responses': np.random.randint(8, 95, 30),
        'Accuracy': np.random.uniform(0.8, 0.98, 30)
    })

df = get_dashboard_data()

# ========================================
# 📊 DASHBOARD SECTION
# ========================================
if page == "📊 Dashboard":
    st.title("📈 AI Agent Analytics Dashboard")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", f"{df['Users'].iloc[-1]:,}")
    col2.metric("Total Queries", f"{df['Queries'].sum():,}")
    col3.metric("AI Responses", f"{df['AI_Responses'].sum():,}")
    col4.metric("Avg Accuracy", f"{df['Accuracy'].mean():.1%}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 User Growth")
        st.line_chart(df[['Users']].tail(14))
    
    with col2:
        st.subheader("💬 Activity")
        st.bar_chart(df[['Queries', 'AI_Responses']].tail(14))
    
    # Accuracy
    st.subheader("🎯 Accuracy Trend")
    st.line_chart(df['Accuracy'].tail(30))

# ========================================
# 🤖 AI AGENT SECTION  
# ========================================
elif page == "🤖 AI Agent":
    st.title("🤖 AI Agent Chat")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI Response (Demo - APNA AI CODE YAHAN)
        with st.chat_message("assistant"):
            response = f"""
            **✅ Your Query:** {prompt}
            
            **AI Response:**
            - Main aapka AI agent hun!
            - Dashboard data: {df['Users'].iloc[-1]:,} users
            - Accuracy: {df['Accuracy'].mean():.1%}
            
            Kya help chahiye? 🤖
            """
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("**AI Agent + Dashboard Ready!** 🎉")
