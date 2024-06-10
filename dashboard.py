import pandas as pd
import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go

def data_path(directory=None, filename=None):
    if directory is None and filename is not None:
        return os.path.join(os.getcwd(),filename)
    if filename is None:
        return os.path.join(os.getcwd(), directory)
    return os.path.join(os.getcwd(), directory, filename)


def split_date(df,column):
    df['Year']=df[column].str.split('-').str[0]
    if df[column].str.split('-').str[1].str.isnumeric().all():
        df['Month']=df[column].str.split('-').str[1].astype(int)
    else:
        df['Quarter']=df[column].str.split('-').str[1]
    return df

st.set_page_config(page_title='Australian Trade Dashboard',page_icon='📈',layout='wide')
c1,c2=st.columns([0.07,1])
c1.image('assets/australia.png',width=100)
c2.title('Australian Trade Data')
c2.markdown('Desc: This dashboard shows the trade data of Australia | socials: [LinkedIn](https://www.linkedin.com/in/adam-m-62a5b4168/)')


with st.spinner('Loading data...'):
    data_files=[]
    for file in os.listdir(data_path('data')):
        data_files.append(file)
    data_files.sort()

    data_file=st.selectbox('Select data file',data_files,help='Select one data file you want to load')
    data= pd.read_csv(data_path('data',data_file))
    data=split_date(data,'TIME_PERIOD')

    m1,m2,m3,m4=st.columns(4)
    
    m1.write('')
    m2.metric('Performance to pevious year',f"{data['value'].pct_change().iloc[-1]:.2%}")
    m3.metric('Total value',f"${data['value'].sum():,.0f}")
    m4.metric('Average value',f"${data['value'].mean():,.0f}")
    m1.write('')
    
    # load three plots based dataframe context
    p1,p2,p3=st.columns(3)

    if data_file=='balance_of_payments_states.csv':
        fig=px.bar(data,x='Year',y='value',color='REGION',title='Balance of Payments by State')
        p1.plotly_chart(fig)
        fig=px.line(data,x='Year',y='value',color='REGION',title='Balance of Payments by State')
        p2.plotly_chart(fig)
        fig=px.pie(data,values='value',names='REGION',title='Balance of Payments by State')
        p3.plotly_chart(fig)
    elif data_file=='general_balance_of_payments.csv':
        fig=px.bar(data,x='Year',y='value',title='General Balance of Payments')
        p1.plotly_chart(fig)
        fig=px.line(data,x='Year',y='value',title='General Balance of Payments')
        p2.plotly_chart(fig)
        fig=px.pie(data,values='value',names='Year',title='General Balance of Payments')
        p3.plotly_chart(fig)
    elif data_file=='export_imports.csv':
        fig=px.bar(data,x='Year',y='value',color='EXP_IMP',title='Export and Imports')
        p1.plotly_chart(fig)
        fig=px.line(data,x='Year',y='value',color='EXP_IMP',title='Export and Imports')
        p2.plotly_chart(fig)
        fig=px.pie(data,values='value',names='EXP_IMP',title='Export and Imports')
        p3.plotly_chart(fig)
    elif data_file=='merchandise_imports.csv':
        fig=px.bar(data,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Imports')
        p1.plotly_chart(fig)
        fig=px.line(data,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Imports')
        p2.plotly_chart(fig)
        fig=px.pie(data,values='value',names='Year',title='Merchandise Imports')
        p3.plotly_chart(fig)
    elif data_file=='merchandise_exports.csv':
        fig=px.bar(data,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Exports')
        p1.plotly_chart(fig)
        fig=px.line(data,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Exports')
        p2.plotly_chart(fig)
        fig=px.pie(data,values='value',names='Year',title='Merchandise Exports')
        p3.plotly_chart(fig)


    







    



