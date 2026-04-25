import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 AI Dashboard")

# Simple Data
data = {
    'Metric': ['Users', 'Queries', 'Accuracy', 'Response Rate'],
    'Value': [1250, 3400, 92.5, 95.2]
}
df = pd.DataFrame(data)

# Simple Charts
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df, x='Metric', y='Value', 
                title="AI Agent Stats")
    st.plotly_chart(fig)

with col2:
    fig2 = px.pie(df, names='Metric', values='Value')
    st.plotly_chart(fig2)

st.success("✅ Dashboard Working!")
