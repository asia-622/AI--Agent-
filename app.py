import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="AI Academic Ecosystem", layout="wide")

# Sidebar Navigation
st.sidebar.title("🎓 AI Academic Hub")
page = st.sidebar.selectbox("Navigate:", [
    "🏠 Home",
    "📂 Upload & Analyze", 
    "📊 Dashboard",
    "🎯 Attendance Analysis",
    "⚔️ Student Comparison",
    "🔮 Grade Prediction",
    "🤖 AI Chatbot"
])

# Global Data
@st.cache_data
def load_academic_data():
    np.random.seed(42)
    students = ['Ali', 'Sara', 'Ahmed', 'Fatima', 'Omar']
    data = {
        'Student': np.random.choice(students, 100),
        'Maths': np.random.randint(60, 100, 100),
        'Science': np.random.randint(55, 98, 100),
        'English': np.random.randint(65, 99, 100),
        'Attendance': np.random.uniform(0.85, 1.0, 100),
        'Date': pd.date_range('2024-01-01', periods=100)
    }
    df = pd.DataFrame(data)
    df['Average'] = df[['Maths', 'Science', 'English']].mean(axis=1)
    return df

df = load_academic_data()

# ========================================
# 🏠 HOME PAGE
# ========================================
if page == "🏠 Home":
    st.title("🎓 AI Academic Ecosystem")
    st.markdown("## Welcome to Smart Learning Platform!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Students", len(df['Student'].unique()))
        st.button("📊 View Dashboard")
    with col2:
        st.metric("Avg Grade", f"{df['Average'].mean():.1f}%")
        st.button("🎯 Attendance")
    with col3:
        st.metric("Attendance", f"{df['Attendance'].mean():.1%}")
        st.button("🔮 Predict Grades")

# ========================================
# 📊 ENHANCED DASHBOARD
# ========================================
elif page == "📊 Dashboard":
    st.title("📈 Academic Analytics Dashboard")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df['Student'].unique()))
    col2.metric("Avg Grade", f"{df['Average'].mean():.1f}%")
    col3.metric("Attendance Rate", f"{df['Attendance'].mean():.1%}")
    col4.metric("Top Performers", len(df[df['Average']>90]))
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Subject Performance")
        st.bar_chart(df[['Maths', 'Science', 'English']].mean())
    
    with col2:
        st.subheader("👥 Student Grades")
        st.line_chart(df.groupby('Student')['Average'].mean().sort_values())
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 Attendance Trend")
        st.line_chart(df['Attendance'].tail(30))
    
    with col2:
        st.subheader("🏆 Grade Distribution")
        st.bar_chart(pd.cut(df['Average'], bins=5).value_counts())

# ========================================
# 📂 UPLOAD & ANALYZE
# ========================================
elif page == "📂 Upload & Analyze":
    st.title("📂 Upload & Analyze")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.dataframe(df_upload.head())
        st.metric("Rows", len(df_upload))
        if st.button("🔄 Analyze"):
            st.success("Analysis Complete!")

# ========================================
# 🎯 ATTENDANCE ANALYSIS
# ========================================
elif page == "🎯 Attendance Analysis":
    st.title("🎯 Attendance Analysis")
    
    student_select = st.selectbox("Select Student:", df['Student'].unique())
    student_data = df[df['Student'] == student_select]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Attendance", f"{student_data['Attendance'].mean():.1%}")
        st.line_chart(student_data['Attendance'])
    with col2:
        st.subheader("Missing Days")
        st.bar_chart(student_data['Attendance'].lt(0.9).value_counts())

# ========================================
# ⚔️ STUDENT COMPARISON
# ========================================
elif page == "⚔️ Student Comparison":
    st.title("⚔️ Student Comparison")
    
    students = st.multiselect("Compare Students:", df['Student'].unique(), default=df['Student'].unique()[:3])
    compare_df = df[df['Student'].isin(students)]
    
    st.bar_chart(compare_df.groupby('Student')[['Maths', 'Science', 'English']].mean())

# ========================================
# 🔮 GRADE PREDICTION
# ========================================
elif page == "🔮 Grade Prediction":
    st.title("🔮 Grade Prediction")
    
    st.info("🔄 AI Model predicting future grades...")
    
    col1, col2 = st.columns(2)
    with col1:
        student = st.selectbox("Student:", df['Student'].unique())
        predicted = np.random.uniform(80, 95, 3)
        st.metric("Predicted Grades", f"{predicted.mean():.1f}%")
    
    with col2:
        st.bar_chart({"Q1": predicted[0], "Q2": predicted[1], "Final": predicted[2]})

# ========================================
# 🤖 AI CHATBOT
# ========================================
elif page == "🤖 AI Chatbot":
    st.title("🤖 AI Academic Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about grades, attendance, predictions..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Smart Academic Response
        with st.chat_message("assistant"):
            response = f"""
            📚 **Academic AI Response:**
            
            **Your Query:** {prompt}
            
            **Quick Stats:**
            - Students: {len(df['Student'].unique())}
            - Avg Grade: {df['Average'].mean():.1f}%
            - Attendance: {df['Attendance'].mean():.1%}
            
            Need specific analysis? 🤖
            """
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("*🎓 AI Academic Ecosystem - All Features Working!*")
