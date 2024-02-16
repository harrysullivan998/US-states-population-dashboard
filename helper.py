import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def read_data(filename:str) -> pd.DataFrame:
    """Reads in csv file, performs data manipulations and returns dfs"""

    df = pd.read_csv(filename)

    for column in range(2010, 2024):
        df[str(column)] = df[str(column)].str.replace(',','').astype(float).astype(int)

    df_change = df.copy()
    df_change['Population Change'] = df_change[str(st.session_state['year_range'][1])] - df_change[str(st.session_state['year_range'][0])]

    return df, df_change


def absolute_population_map(df:pd.DataFrame) -> px.choropleth:

    map_plot = px.choropleth(df, 
                        locations='State Code', 
                        color='2014', 
                        locationmode="USA-states",
                        scope="usa",
                        hover_name='State',
                        hover_data='2014',
                        range_color=[0, df['2014'].max()],
                        color_continuous_scale="Viridis",
    ).update_layout(
        width=800,
        margin=dict(l=0, r=10, t=30, b=20, pad=0),
    )
    return map_plot



def change_population_map(df:pd.DataFrame) -> px.choropleth:

    map_plot = px.choropleth(df, 
                        locations='State Code', 
                        color='Population Change', 
                        locationmode="USA-states",
                        scope="usa",
                        hover_name='State',
                        hover_data='Population Change',
                        range_color=[df['Population Change'].min(), df['Population Change'].max()],
                        color_continuous_scale="Viridis",
    ).update_layout(
        width=650,
        margin=dict(l=0, r=10, t=30, b=20, pad=0),
    )
    return map_plot