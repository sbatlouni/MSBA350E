from collections import namedtuple
import altair as alt
import math
import pandas as pd
import os
from datetime import date, datetime
import streamlit as st

st.markdown("# Data Profiling")
st.sidebar.markdown("# Data Profiling")
st.markdown("## This page is to allow data analysts to explore the underlying raw data")
st.markdown("# ")

# Reading the data
tests_and_deaths_raw = pd.read_csv(os.getcwd() + r'\data\raw\COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv')
vaccinations_raw = pd.read_csv(os.getcwd() + r'\data\raw\COVID-19_Vaccinations_by_ZIP_Code.csv')

# Conforming tests_and_deaths
tests_and_deaths_conformed = tests_and_deaths_raw.copy()
tests_and_deaths_conformed['Year-Week'] = pd.to_datetime(tests_and_deaths_conformed['Week Start'], format='%m/%d/%Y').dt.year.astype("string") +'-'+ tests_and_deaths_conformed['Week Number'].astype("string") 
tests_and_deaths_conformed = tests_and_deaths_conformed.rename(columns={'ZIP Code': 'Zip Code'}).set_index(['Zip Code', 'Year-Week'])

# Conforming vaccinations_raw
vaccinations_raw_conformed = vaccinations_raw.copy()
vaccinations_raw_conformed['Week Number'] = pd.to_datetime(vaccinations_raw_conformed['Date'], format='%m/%d/%Y').dt.isocalendar().week
vaccinations_raw_conformed['Year'] = pd.to_datetime(vaccinations_raw_conformed['Date'], format='%m/%d/%Y').dt.year
vaccinations_raw_conformed['Year-Week'] = vaccinations_raw_conformed['Year'].astype("string") +'-'+ vaccinations_raw_conformed['Week Number'].astype("string")

# Changing the granularity of the data so the two match
# These are aggregated by sum
vaccination_weekly_df = (vaccinations_raw_conformed[['Zip Code', 'Year-Week', 'Total Doses - Daily', '1st Dose - Daily', 
                                           'Vaccine Series Completed - Daily', 'Total Doses - Daily - Age 5+', 
                                           'Total Doses - Daily - Age 12+', 'Total Doses - Daily - Age 18+', 
                                           'Total Doses - Daily - Age 65+', '1st Dose - Daily - Age 5+', '1st Dose - Daily - Age 12+', 
                                           '1st Dose - Daily - Age 18+', '1st Dose - Daily - Age 65+', 
                                           'Vaccine Series Completed - Daily - Age 5+', 'Vaccine Series Completed - Daily - Age 12+', 
                                           'Vaccine Series Completed - Daily - Age 18+', 'Vaccine Series Completed - Daily - Age 65+']]
                        .groupby(['Zip Code', 'Year-Week']).sum())

# These are aggregated by max because they are cumilative
vaccination_weekly_cumilative_df = (vaccinations_raw_conformed[['Zip Code', 'Year-Week', 'Total Doses - Cumulative', '1st Dose - Cumulative',
                                                      '1st Dose - Percent Population', 'Vaccine Series Completed - Cumulative', 
                                                      'Vaccine Series Completed  - Percent Population']]
                                    .groupby(['Zip Code', 'Year-Week']).max())
vaccination_weekly_merged_df = vaccination_weekly_df.join(vaccination_weekly_cumilative_df, how='inner')

combined_dataset = pd.read_csv(os.getcwd() + r'\data\processed\combined_dataset.csv')

st.markdown("## Dataset 1:")
st.markdown("## COVID-19 Cases, Tests, and Deaths by ZIP Code")
st.markdown("### Previewing the Data")
st.dataframe(tests_and_deaths_raw)

st.markdown("## Dataset 2:")
st.markdown("## COVID-19 Vaccinations by ZIP Code")
st.markdown("### Previewing the Data")
st.dataframe(vaccinations_raw)

st.markdown("## Dataset 3:")
st.markdown("## Combined Dataset")
st.markdown("### Previewing the Data")
st.dataframe(combined_dataset)


