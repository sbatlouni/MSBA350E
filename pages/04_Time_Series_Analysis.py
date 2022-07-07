from collections import namedtuple
import altair as alt
import math
import pandas as pd
import os
from datetime import date, datetime, timedelta
import streamlit as st
from scipy import stats

st.markdown("# Time Series Analysis")
st.sidebar.markdown("# Time Series Analysis")
st.markdown("## This page provides an overview of the trends in cases, tests, deaths, and vaccines over time")
st.markdown("# ")


# Reading the data
combined_df = pd.read_csv(os.getcwd() + '/data/processed/combined_dataset.csv')
combined_df['Year-Week-dt'] = combined_df['Year-Week'].apply(lambda x: datetime.strptime(x + '-0', "%Y-%W-%w"))
combined_df['Year-Week'] = combined_df['Year-Week'].apply(lambda x: x.split('-')[0] + '-' + '0' if len(x.split('-')[1]) == 1 else '' + x.split('-')[1] )




forcast_value = st.sidebar.slider('Input Forcast Intervals', min_value=0, max_value=10)
date_range = st.sidebar.date_input('Date Analysis Range', (min(combined_df['Year-Week-dt']), max(combined_df['Year-Week-dt'])))

min_date = date_range[0]
max_date = date_range[1]
combined_df = combined_df[combined_df['Year-Week-dt'] >= datetime(min_date.year, min_date.month, min_date.day)]
combined_df = combined_df[combined_df['Year-Week-dt'] <= datetime(max_date.year, max_date.month, max_date.day)]


selected_zips = st.sidebar.multiselect('Zip Code', combined_df['Zip Code'].unique())

if(len(selected_zips) > 0):
    combined_df = combined_df[combined_df['Zip Code'].isin(selected_zips)]

######################## CASES OVER TIME ####################################################
st.markdown('### Cases Over Time')
cases_over_time = combined_df[['Year-Week-dt', 'Cases - Weekly']].groupby('Year-Week-dt').max()
cases_over_time = cases_over_time.reset_index()
cases_over_time['date_ordinal'] = pd.to_datetime(cases_over_time['Year-Week-dt']).apply(lambda x: x.toordinal())

slope, intercept, r, p, std_err = stats.linregress(cases_over_time['date_ordinal'], cases_over_time['Cases - Weekly'])

for i in range(forcast_value):
    new_date = max(cases_over_time['Year-Week-dt']) + timedelta(days=i*7)
    record = {
                  'date_ordinal': new_date.toordinal()
                , 'Year-Week-dt': new_date
            }
    cases_over_time = cases_over_time.append(record, ignore_index=True)

def regression_constructor(x):
  return slope * x + intercept
cases_over_time['line of best fit'] = cases_over_time['date_ordinal'].apply(regression_constructor)

cases_over_time = cases_over_time.set_index('Year-Week-dt')
st.line_chart(cases_over_time[['Cases - Weekly', 'line of best fit']].sort_index())


######################## TESTS OVER TIME ####################################################
st.markdown('### Tests Over Time')
tests_over_time = combined_df[['Year-Week-dt', 'Tests - Weekly']].groupby('Year-Week-dt').max()
tests_over_time = tests_over_time.reset_index()
tests_over_time['date_ordinal'] = pd.to_datetime(tests_over_time['Year-Week-dt']).apply(lambda x: x.toordinal())

slope, intercept, r, p, std_err = stats.linregress(tests_over_time['date_ordinal'], tests_over_time['Tests - Weekly'])

for i in range(forcast_value):
    new_date = max(tests_over_time['Year-Week-dt']) + timedelta(days=i*7)
    record = {
                  'date_ordinal': new_date.toordinal()
                , 'Year-Week-dt': new_date
            }
    tests_over_time = tests_over_time.append(record, ignore_index=True)

def regression_constructor(x):
  return slope * x + intercept
tests_over_time['line of best fit'] = tests_over_time['date_ordinal'].apply(regression_constructor)

tests_over_time = tests_over_time.set_index('Year-Week-dt')
st.line_chart(tests_over_time[['Tests - Weekly', 'line of best fit']].sort_index())


######################## DEATHS OVER TIME ####################################################
st.markdown('### Deaths Over Time')
deaths_over_time = combined_df[['Year-Week-dt', 'Deaths - Weekly']].groupby('Year-Week-dt').max()
deaths_over_time = deaths_over_time.reset_index()
deaths_over_time['date_ordinal'] = pd.to_datetime(deaths_over_time['Year-Week-dt']).apply(lambda x: x.toordinal())

slope, intercept, r, p, std_err = stats.linregress(deaths_over_time['date_ordinal'], deaths_over_time['Deaths - Weekly'])

for i in range(forcast_value):
    new_date = max(deaths_over_time['Year-Week-dt']) + timedelta(days=i*7)
    record = {
                  'date_ordinal': new_date.toordinal()
                , 'Year-Week-dt': new_date
            }
    deaths_over_time = deaths_over_time.append(record, ignore_index=True)

def regression_constructor(x):
  return slope * x + intercept
deaths_over_time['line of best fit'] = deaths_over_time['date_ordinal'].apply(regression_constructor)

deaths_over_time = deaths_over_time.set_index('Year-Week-dt')
st.line_chart(deaths_over_time[['Deaths - Weekly', 'line of best fit']].sort_index())



######################## VACCINES OVER TIME ####################################################
st.markdown('### Vaccines Over Time')
vaccines_over_time = combined_df[['Year-Week-dt', 'Deaths - Weekly']].groupby('Year-Week-dt').max()
vaccines_over_time = vaccines_over_time.reset_index()
vaccines_over_time['date_ordinal'] = pd.to_datetime(vaccines_over_time['Year-Week-dt']).apply(lambda x: x.toordinal())

slope, intercept, r, p, std_err = stats.linregress(vaccines_over_time['date_ordinal'], vaccines_over_time['Deaths - Weekly'])
for i in range(forcast_value):
    new_date = max(vaccines_over_time['Year-Week-dt']) + timedelta(days=i*7)
    record = {
                  'date_ordinal': new_date.toordinal()
                , 'Year-Week-dt': new_date
            }
    vaccines_over_time = vaccines_over_time.append(record, ignore_index=True)
def regression_constructor(x):
  return slope * x + intercept
vaccines_over_time['line of best fit'] = vaccines_over_time['date_ordinal'].apply(regression_constructor)

vaccines_over_time = vaccines_over_time.set_index('Year-Week-dt')
st.line_chart(vaccines_over_time[['Deaths - Weekly', 'line of best fit']].sort_index())





