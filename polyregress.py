import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout='wide')
st.markdown(
    f"""
    <h1 style='text-align: center;'>JP Morgan Cash Flow Data Polynomial Analysis</h1>
    """,
    unsafe_allow_html=True
)

JPmorgan_Cashflow_data = pd.read_csv(r"/Users/risaiah/Desktop/GitHub Repositories/Data-Science-Econometrics-Personal/Polynomial/JPcashflow.csv")
JPmorgan_Cashflow_data = JPmorgan_Cashflow_data.drop(1)

with st.expander('Preview Data'):
    st.dataframe(JPmorgan_Cashflow_data)
    st.caption('Values of \'-\' are replaced with 0 for simplicity.')

col1, colraw, col2, col3  =  st.columns([5,1,9,9])
selecteddate=col1.selectbox('Variable Name',JPmorgan_Cashflow_data['Column1'][1:])

x_int = list(JPmorgan_Cashflow_data['Column1']).index(selecteddate)
JPtimedata = pd.to_datetime(JPmorgan_Cashflow_data.iloc[0][3:])
JProwdata = JPmorgan_Cashflow_data.iloc[x_int][3:]
JProwdata = JProwdata.apply(lambda x: x.replace("$","").replace(",","").replace('-','0'))
JProwdata = pd.to_numeric(JProwdata)
length_ofdata = np.arange(len(JProwdata))
data_variable_name = JPmorgan_Cashflow_data.iloc[x_int][0]

JPtimedata_reference = mdates.date2num(JPtimedata)

def polyfitplot(polyfiti, titl=True):
    P = np.polyfit(JPtimedata_reference, JProwdata, polyfiti)
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
    
    if titl == False:
        fig.update_layout(
            title=f"Fitted at Polynomial = {polyfiti}",
            title_x=0.3,
            title_y=0.95
        )
        
    else:
        fig.update_layout(
            title=f"{selecteddate} Fitted at Polynomial = {polyfiti}",
            title_x=0.3,
            title_y=0.95
        ) 

    fig.update_xaxes(title_text = "Dates")
    fig.update_yaxes(title_text = "Dollars (Trillions)")

    fig.add_trace(actual_data)
    fig.add_trace(polyfit_data)
    
    fig.update_layout(width=450, height=250)

    return fig

a=col1.number_input('Graph 1 Polynomial', step=1, min_value=0)
b=col1.number_input('Graph 2 Polynomial', step=1, min_value=0)
c=col1.number_input('Graph 3 Polynomial', step=1, min_value=0)
d=col1.number_input('Graph 4 Polynomial', step=1, min_value=0)
yep = col1.checkbox('Title Display?')

col2.plotly_chart(polyfitplot(a, titl=yep))
col3.plotly_chart(polyfitplot(b, titl=yep))
col2.plotly_chart(polyfitplot(c, titl=yep))
col3.plotly_chart(polyfitplot(d, titl=yep))


st.caption('Thank you for viewing. Please contact db2019@hawaii.edu if you have any questions. Copyrights reserved.')