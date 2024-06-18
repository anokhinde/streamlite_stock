'''

'''

import streamlit as st 
import json 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 

def load_data() -> pd.DataFrame:
    '''
    Загрузка датафрейма из директории проекта
    '''
    return pd.read_csv('data\\Dataset salary 2024.csv', sep=',')


@st.cache_data
def data_cooking(year:int):
    '''
    Функция для предобработки данных
    '''
    df = load_data()
    df = df.query('work_year == @year')[['experience_level', 'job_title', 'salary_in_usd', 'company_location', 'company_size']]
    experience = df.experience_level.unique()
    job = df.job_title.unique()

    return df, experience, job

def create_widgets(by:str, df:pd.DataFrame):
    '''
    Функция для построения метрик
    '''
    
    name = f'salary_by_{by}'
    col1, col2, col3 = st.columns(3)

    with col1:
        df_max = (df[[by, 'salary_in_usd']]
            .groupby(by, as_index=False).agg({'salary_in_usd':'max'})
            .rename(columns={'salary_in_usd':name}))
        label = f'Max salary'        
        value = df_max[name].max()
        st.metric(label=label, value=value)
        pass

    with col2:
        df_mean = (df[[by, 'salary_in_usd']]
            .groupby(by, as_index=False).agg({'salary_in_usd':'mean'})
            .rename(columns={'salary_in_usd':name}))
        label = 'Mean salary'
        value = round(df_mean[name].mean(), 2)
        st.metric(label=label, value=value)
        pass

    with col3:
        df_min = (df[[by, 'salary_in_usd']]
            .groupby(by, as_index=False).agg({'salary_in_usd':'min'})
            .rename(columns={'salary_in_usd':name}))
        label = f'Min salary '
        value = round(df_min[name].min(),2)
        st.metric(label=label, value=value)
        pass

def plot_avg_salary(by:str, df:pd.DataFrame):
    '''
    Функция для построения графика среднего заработка по категориям (страна, размер компании, грейд)
    '''
    name = f'avg_salary_by_{by}'
    avg_salary_by_country = (df[[by, 'salary_in_usd']]
            .groupby(by, as_index=False).agg({'salary_in_usd':'mean'})
            .rename(columns={'salary_in_usd':name}))

    fig = px.histogram(avg_salary_by_country, x=by, y=name,
            barmode='group',
            height=500)
    st.plotly_chart(fig)

df, experience, job = data_cooking(year=2024)

st.title("Зарплаты специалистов по данным в 2024 году")
st.write(""" """)

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard about Data Developer Salary in 2024.
    """
)
st.sidebar.info('')



#====================================
#              Side bar
#==================================== 

job_option = st.sidebar.selectbox(
    'Set job title',
    job
)

experience_option = st.sidebar.selectbox(
    'Set experience',
    experience
)

df_job_experience = df.query('job_title == @job_option and experience_level == @experience_option')

tab1, tab2, tab3 = st.tabs(["Средий доход по грейду", "Средний доход по странам", "Средний доход по размеру компании"])

with tab1:
    plot_avg_salary(by='experience_level', df=df.query('job_title == @job_option'))
    create_widgets(by='experience_level', df=df_job_experience)
with tab2:    
    plot_avg_salary(by='company_location', df=df_job_experience)
    create_widgets(by='company_location', df=df_job_experience)
with tab3:
    plot_avg_salary(by='company_size', df=df_job_experience)
    create_widgets(by='company_size', df=df_job_experience)

            

min_salary = int(df_job_experience.salary_in_usd.min())
max_salary = int(df_job_experience.salary_in_usd.max())

#добавление шкалы зарплаты в табличку 
st.data_editor(
    df_job_experience.sort_values('salary_in_usd', ascending=False),
    column_config={
        "salary_in_usd": st.column_config.ProgressColumn(
            "USD salary volume",
            help="The salary volume in USD",
            format="$%f",
            min_value=min_salary,
            max_value=max_salary,
        ),
    },
    hide_index=True,
)
