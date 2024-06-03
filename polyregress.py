import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import plotly.graph_objects as go
import streamlit as st

JPmorgan_Cashflow_data = pd.read_csv(r"/Users/risaiah/Desktop/GitHub Repositories/Data-Science-Econometrics-Personal/Polynomial/JPcashflow.csv")
JPmorgan_Cashflow_data = JPmorgan_Cashflow_data.drop(1)

JPtimedata = pd.to_datetime(JPmorgan_Cashflow_data.iloc[0][3:])
JProwdata = JPmorgan_Cashflow_data.iloc[7][3:]
JProwdata = JProwdata.apply(lambda x: x.replace("$","").replace(",",""))
JProwdata = pd.to_numeric(JProwdata)
length_ofdata = np.arange(len(JProwdata))
data_variable_name = JPmorgan_Cashflow_data.iloc[7][0]

JPtimedata_reference = mdates.date2num(JPtimedata)
P = np.polyfit(JPtimedata_reference, JProwdata, 9)
polyfit_values = np.polyval(P, JPtimedata_reference)


fig = go.Figure()

actual_data = go.Scatter(
    x=JPtimedata,
    y=JProwdata,
    mode='lines',
    name='Actual Data'
)

polyfit_data = go.Scatter(
    x=JPtimedata,
    y=polyfit_values,
    mode='lines',
    name='Polynomial Fit'
)

fig.update_layout(
    title=f"{data_variable_name} Time Series Data",
    title_x=0.3,
    title_y=0.95
)

fig.update_xaxes(title_text = "Dates")
fig.update_yaxes(title_text = "Dollars (Trillions)")

fig.add_trace(actual_data)
fig.add_trace(polyfit_data)

fig.show()
