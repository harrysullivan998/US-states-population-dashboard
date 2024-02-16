import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

from helper import read_data, change_population_map


if "selected_state" not in st.session_state:
    st.session_state["selected_state"] = 1
if "year_range" not in st.session_state:
    st.session_state["year_range"] = [2010, 2023]

st.set_page_config(

    layout="wide",
)

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)



df, df_change = read_data('usa-data.csv')



st.title('Population change of states in the USA')


map_column, space_column, slider_column = st.columns([3, 1, 2])

with map_column:


    fig = change_population_map(df=df_change)

    selected_points = plotly_events(fig, 
                                click_event=True, 
                                hover_event=False,
                                override_height=300)

    if selected_points:
        st.session_state["selected_state"] = selected_points[0]['pointNumber']

with space_column:
    pass

with slider_column:


    st.markdown("""
                
    #
    The slider can be used to change the year range for both the map and the state-specific metrics below. 
                
    Clicking on a state will change the focus of the graph and metrics!
""")

    with st.form(key='slider form'):

        
        st.session_state['year_range'] = st.select_slider(label='Select year range',
                            options=[num for num in range(2010, 2024)],
                            value=[2010, 2023],
                            )
        st.form_submit_button(label='Update map and metrics')

        

selected_state_df = df[df.index == st.session_state['selected_state']]
selected_state_df = (selected_state_df.set_index(["State Code", "State"])
        .stack()
        .reset_index()
        .rename(columns={'level_2':'Year',
                        0: 'Population'}
        )
                )


graph_column, space_column2, metric_column = st.columns([3,1,2])

with graph_column:

    selected_state_line = px.line(selected_state_df, 
                                x="Year", 
                                y="Population", 
                                title=f'Population of {selected_state_df.State.max()} over time',
    ).update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10, pad=0),
        )
    st.plotly_chart(selected_state_line,
                    border = True)
    
with space_column2:
    pass

with metric_column:

    st.markdown("###")

    population_selected_state_year_range_end = selected_state_df[selected_state_df['Year'] == str(st.session_state['year_range'][1])]['Population'].max()
    population_selected_state_year_range_beginning = selected_state_df[selected_state_df['Year'] == str(st.session_state['year_range'][0])]['Population'].max()

    st.metric(label=f"Population of {selected_state_df['State'].max()} in {st.session_state['year_range'][1]} and change from {st.session_state['year_range'][0]}",
              value = f"{population_selected_state_year_range_end:,}",
              delta = f"{int(population_selected_state_year_range_end - population_selected_state_year_range_beginning):,}",
            )

    end_year_ranked = df[str(st.session_state['year_range'][1])].rank(ascending=False)
    start_year_ranked = df[str(st.session_state['year_range'][0])].rank(ascending=False)

    end_rank_selected_state = end_year_ranked[end_year_ranked.index == st.session_state['selected_state']].max()
    start_rank_selected_state = start_year_ranked[start_year_ranked.index == st.session_state['selected_state']].max()


    st.metric(
        label=f"Population rank across states in {str(st.session_state['year_range'][1])} and change from {str(st.session_state['year_range'][0])}",
        value=int(end_rank_selected_state),
        delta=int(end_rank_selected_state - start_rank_selected_state))


