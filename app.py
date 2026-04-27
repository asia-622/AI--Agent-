
import streamlit as st
import pandas as pd
import plotly.express as px
from file_handler import FileHandler
from data_preprocessing import DataProcessor
from dashboard import Dashboard
from chatbot import UniversityAIAgent
from utils import setup_page_config, get_download_link
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="🎓 University AI Analytics Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

setup_page_config()

class UniversityAnalyticsApp:
    def __init__(self):
        self.file_handler = FileHandler()
        self.data_processor = None
        self.dashboard = None
        self.agent = None
        self.df = None
        self.processed_data = None
        
    def sidebar(self):
        with st.sidebar:
            st.title("🎓 University AI Agent")
            st.markdown("---")
            
            # File Upload
            uploaded_file = st.file_uploader(
                "📁 Upload Dataset (CSV/Excel/JSON)",
                type=['csv', 'xlsx', 'xls', 'json'],
                help="Upload university dataset (up to 200MB)"
            )
            
            if uploaded_file:
                self.file_handler.load_file(uploaded_file)
                st.success(f"✅ Loaded: {self.file_handler.filename}")
                st.info(f"📊 Shape: {self.file_handler.df.shape}")
                
                if st.button("🔄 Process Data", type="primary"):
                    with st.spinner("Processing dataset..."):
                        self.data_processor = DataProcessor(self.file_handler.df)
                        self.processed_data = self.data_processor.process()
                        self.df = self.processed_data['df']
                        self.dashboard = Dashboard(self.df, self.processed_data)
                        self.agent = UniversityAIAgent(self.df, self.processed_data)
                        st.session_state['data_ready'] = True
                        st.rerun()
            
            # API Key
            st.markdown("---")
            api_key = st.text_input("🔑 OpenAI API Key", type="password", 
                                  help="Required for AI Agent")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                st.success("✅ API Key set!")
            
            st.markdown("---")
            st.markdown("[⭐ Star on GitHub](https://github.com/)")

    def main_page(self):
        if 'data_ready' not in st.session_state:
            st.session_state['data_ready'] = False
        
        if not st.session_state.get('data_ready', False):
            st.info("👆 Please upload a dataset and process it first!")
            self.sidebar()
            return

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard", "🎯 AI Agent", "🔍 Student Search", 
            "📈 Subject Analysis", "⚖️ Comparison", "📥 Download"
        ])
        
        with tab1:
            self.dashboard.display_overview()
        
        with tab2:
            if self.agent:
                self.agent.chat_interface()
        
        with tab3:
            self.student_search()
        
        with tab4:
            self.subject_analysis()
        
        with tab5:
            self.student_comparison()
        
        with tab6:
            self.download_section()
    
    def student_search(self):
        st.subheader("🔍 Student Search")
        name = st.text_input("Enter student name:")
        if name and self.df is not None:
            student_data = self.data_processor.search_student(name)
            if student_data:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Marks", f"{student_data['total_marks']:.1f}")
                    st.metric("Average", f"{student_data['average']:.1f}")
                    st.metric("Attendance %", f"{student_data['attendance']:.1f}%")
                with col2:
                    self.dashboard.plot_student_performance(student_data)
    
    def subject_analysis(self):
        st.subheader("📈 Subject Analysis")
        self.dashboard.subject_analysis()
    
    def student_comparison(self):
        st.subheader("⚖️ Student Comparison")
        names = st.text_input("Enter student names (comma separated):")
        if names:
            name_list = [n.strip() for n in names.split(",")]
            self.dashboard.compare_students(name_list[:5])
    
    def download_section(self):
        st.subheader("📥 Download Results")
        if self.df is not None:
            csv = self.df.to_csv(index=False)
            st.download_button(
                "📄 Download Cleaned Data (CSV)",
                csv,
                f"{self.file_handler.filename}_cleaned.csv",
                "text/csv"
            )

def main():
    st.title("🎓 University AI Analytics Agent")
    st.markdown("### Production-ready AI Agent with RAG + Tools + Memory")
    
    app = UniversityAnalyticsApp()
    app.sidebar()
    app.main_page()

if __name__ == "__main__":
    main()
