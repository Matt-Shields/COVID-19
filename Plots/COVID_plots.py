"""
Plotting routines for daily updates of COVID 19 data
"""

import pandas as pd
import os.path
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def print_data():
    cd = read_data()
    print(cd)

def read_data():
    my_path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(my_path, "../csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
    covid_data = pd.read_csv(filepath,parse_dates=True)
    return covid_data

def transform_data(countries):
    raw_data = read_data()
    _tmp_df = pd.DataFrame(dtype=float)

    for k,v in countries.items():
        if 'all' in v and len(v)==1:
            """ Entire country only"""
            _tmp = raw_data.groupby('Country/Region').sum().loc[k][2:]
            _tmp_df[k] = pd.to_numeric(_tmp)
        else:
            """Specific or multiple region in country"""
            for vi in v:
                if vi is 'all':
                    """ Include entire country"""
                    _tmp = raw_data.groupby('Country/Region').sum().loc[k][2:]
                    _tmp_df[k] = pd.to_numeric(_tmp)
                else:
                    "Individual regions"
                    _tmp = raw_data.loc[(raw_data['Province/State'] == vi) &
                                        (raw_data['Country/Region'] == k)].reset_index().loc[0][5:]
                    _col = vi + ', ' + k
                    _tmp_df[_col] = pd.to_numeric(_tmp)

    plot_df = _tmp_df.rename_axis('Date').reset_index()
    # Percent diff
    _tmp_diff = plot_df.iloc[:,1:]
    plot_df_perc_diff = _tmp_diff.pct_change() * 100
    plot_df_perc_diff['Date'] = plot_df.loc[1:]['Date']
    return plot_df, plot_df_perc_diff


def plot_data(countries):
    """Plot routines"""
    # Absolute number of confirmed cases
    plot_df, perc_diff = transform_data(countries)
    fig0, ax0 = plt.subplots()
    plot_df.plot.line(x='Date',ax=ax0)
    ax0.set_ylabel('Total number of confirmed cases')
    # Percent change in absolute cases
    fig1, ax1 = plt.subplots()
    perc_diff.plot.line(x='Date',ax=ax1)
    ax1.set_ylabel('Percent change in number of confirmed cases from previous day')



