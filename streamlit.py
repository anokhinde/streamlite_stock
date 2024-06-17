'''


'''


import streamlit as st 
import json 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 

URL_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Social_Network_Analysis_Visualization.png/1280px-Social_Network_Analysis_Visualization.png'


st.title("Data Developer Salary in 2024 DASHBOARD")
st.write(""" """)

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info('')


def load_data() -> pd.DataFrame:
    '''
    Загрузка датафрейма из директории проекта
    '''
    return pd.read_csv('data\\Dataset salary 2024.csv', sep=',')


@st.cache_data
def data_cooking():
    df = load_data()
    experience = df.experience_level.unique()
    job = df.job_title.unique()
    return df, experience, job

col1, col2 = st.columns([1, 4]) 

df, experience, job = data_cooking()

job_option = st.sidebar.selectbox(
    'Set job title',
    job
)

experience_option = st.sidebar.selectbox(
    'Set experience',
    experience
)

#st.image(URL_IMAGE)
#data = st.dataframe(df.query('job_title == @job_option'))

with col1:
    st.header("col1")
    st.dataframe(df.query('job_title == @job_option and experience_level == @experience_option'))

with col2:
    st.header("col2")
    data = df.query('job_title == @job_option')[['experience_level', 'salary_in_usd']]
    fig, ax = plt.subplots()
    ax.hist(data)
    st.pyplot(fig)
    #st.bar_chart(data, x='experience_level', y='salary_in_usd')
