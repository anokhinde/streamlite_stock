'''


'''


import streamlit as st 
import json 
import pandas as pd
import numpy as np
import plotly.express as px 


st.title("Data Developer Salary in 2024 DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")

st.image('/source/image.png')
# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib).")


def load_data(name:str) -> pd.DataFrame:
    '''
    Загрузка датафрейма из директории проекта
    '''
    return pd.read_csv(f'/data/{name}.csv')



def main():
    pass 

