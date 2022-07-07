from collections import namedtuple
import altair as alt
import math
import pandas as pd
import os
from datetime import date, datetime
import streamlit as st

st.markdown("# Zip Code Analysis")
st.sidebar.markdown("# Zip Code Analysis")
st.markdown("## This page provides a summary of the cases, deaths, and vaccines per zip code")
st.markdown("# ")

# Reading the data
combined_df = pd.read_csv(os.getcwd() + '/data/processed/combined_dataset.csv')

selected_zips = st.sidebar.multiselect('Zip Code', combined_df['Zip Code'].unique())

if(len(selected_zips) > 0):
    combined_df = combined_df[combined_df['Zip Code'].isin(selected_zips)]

st.markdown('### Total Cases by Zip Code')
st.bar_chart(combined_df[['Zip Code', 'Cases - Cumulative']].groupby('Zip Code').max())

st.markdown('### Total Deaths by Zip Code')
st.bar_chart(combined_df[['Zip Code', 'Deaths - Cumulative']].groupby('Zip Code').max())

st.markdown('### Total Vaccines by Zip Code')
st.bar_chart(combined_df[['Zip Code', 'Total Doses - Cumulative']].groupby('Zip Code').max())

st.markdown('### Deaths to Cases by Zip Code')
death_ratio_by_zip_df = combined_df[['Zip Code', 'Cases - Cumulative', 'Deaths - Cumulative']].groupby('Zip Code').max()
death_ratio_by_zip_df['Death Ratio'] = death_ratio_by_zip_df['Deaths - Cumulative'] / death_ratio_by_zip_df['Cases - Cumulative']
death_ratio_by_zip_df = death_ratio_by_zip_df[['Death Ratio']]
st.bar_chart(death_ratio_by_zip_df)

st.markdown('### Vaccines to Cases by Zip Code')
vax_ratio_by_zip_df = combined_df[['Zip Code', 'Cases - Cumulative', 'Total Doses - Cumulative']].groupby('Zip Code').max()
vax_ratio_by_zip_df['Vax Ratio'] = vax_ratio_by_zip_df['Total Doses - Cumulative'] / vax_ratio_by_zip_df['Cases - Cumulative']
vax_ratio_by_zip_df = vax_ratio_by_zip_df[['Vax Ratio']]
st.bar_chart(vax_ratio_by_zip_df)