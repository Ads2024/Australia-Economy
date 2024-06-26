"""
Created on Sun June 09 2024
@Author: Adam M.
"""

import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
from mitosheet.streamlit.v1 import spreadsheet
import plotly.figure_factory as ff
import base64
from load_data import filepath,data_load
 
############################################
# Functions to load data and plot charts
############################################

def split_date(df,column):
    df['Year']=df[column].str.split('-').str[0]
    if df[column].str.split('-').str[1].str.isnumeric().all():
        df['Month']=df[column].str.split('-').str[1]
    else:
        df['Quarter']=df[column].str.split('-').str[1]
    return df
# --------------------------------------------
# Load markdown file
# --------------------------------------------
def markdown_readme(file_name):
    with open(os.path.join(os.getcwd(),file_name)) as f:
        st.markdown(f.read())
# --------------------------------------------
# Read GIF file
# --------------------------------------------

def read_gif(file_name):
    with open(os.path.join(os.getcwd(),file_name),'rb') as f:
        contents=f.read()
        data_url=base64.b64encode(contents).decode('utf-8')
    return data_url
# --------------------------------------------
# Load data from data directory
# --------------------------------------------
def load_data(data_file):
    data_files={
        'Balance of Payments by State':'balance_of_payments_states.csv',
        'General Balance of Payments':'general_balance_of_payments.csv',
        'Export and Imports':'export_imports.csv',
        'Merchandise Imports':'merchandise_imports.csv',
        'Merchandise Exports':'merchandise_exports.csv'
    }
    data= pd.read_csv(filepath('data',data_files[data_file]))
    data=split_date(data,'TIME_PERIOD')
    return data
# --------------------------------------------
# Plot different types of charts
# --------------------------------------------
def plot_charts(data,file_type,filter_column=None,filter_value='All',slice=False,slice_value=0):
    p1,p2,p3=st.columns(3)

    if filter_value=='All'and slice==False:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        pie=grouped[grouped['value']>0]
        fig_bar=px.bar(grouped,x='Year',y='value',color=file_type,title=f'{data_file} Bar - Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color=file_type,markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names=file_type,title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)
    elif filter_value!='All' and slice==False:
        filtered_data=data[data[filter_column]==filter_value]
        pie=filtered_data[filtered_data['value']>0]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        fig_bar=px.bar(grouped,x='Year',y='value',color=file_type,title=f'{data_file} Bar Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color=file_type,markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names=file_type,title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)
    elif filter_value=='All' and slice==True and slice_value==0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[slice_value]
        pie=grouped[grouped['value']>0]
        fig_bar=px.bar(grouped,x='Year',y='value',color='Reference',title=f'{data_file} Bar - Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color='Reference',markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names='Reference',title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)
    elif filter_value!='All' and slice==True and slice_value==0:
        filtered_data=data[data[filter_column]==filter_value]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[slice_value]
        pie=filtered_data[filtered_data['value']>0]
        fig_bar=px.bar(grouped,x='Year',y='value',color='Reference',title=f'{data_file} Bar Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color='Reference',markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names='Reference',title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)
    elif filter_value=='All' and slice==True and slice_value>0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        pie=grouped[grouped['value']>0]
        fig_bar=px.bar(grouped,x='Year',y='value',color='Reference',title=f'{data_file} Bar - Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color='Reference',markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names='Reference',title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)
    elif filter_value!='All' and slice==True and slice_value>0:
        filtered_data=data[data[filter_column]==filter_value]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        pie=grouped[grouped['value']>0]
        fig_bar=px.bar(grouped,x='Year',y='value',color='Reference',title=f'{data_file} Bar Chart')
        p1.plotly_chart(fig_bar)
        fig_line=px.line(grouped,x='Year',y='value',color='Reference',markers=True,title=f'{data_file} Line - Chart')
        p2.plotly_chart(fig_line)
        fig_pie=px.pie(pie,values='value',names='Reference',title=f'{data_file} Pie - Chart')
        p3.plotly_chart(fig_pie)

    return p1,p2,p3


def plot_proportion(data,file_type,filter_column=None,filter_value='All',slice=False,slice_value=0):
    p4,p5,p6=st.columns(3)

    if filter_value=='All'and slice==False:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Sunburst)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Funnel)')
        p6.plotly_chart(fig_funnel)
    elif filter_value!='All' and slice==False:
        filtered_data=data[data[filter_column]==filter_value]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Sunburst)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Funnel)')
        p6.plotly_chart(fig_funnel)
    elif filter_value=='All' and slice==True and slice_value==0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[slice_value]
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=['Reference','Year'],values='value',title=f'{data_file} (Sunburst)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Funnel)')
        p6.plotly_chart(fig_funnel)
    elif filter_value!='All' and slice==True and slice_value==0:
        filtered_data=data[data[filter_column]==filter_value]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[slice_value]
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=['Reference','Year'],values='value',title=f'{data_file} (Treemap)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Treemap)')
        p6.plotly_chart(fig_funnel)
    elif filter_value=='All' and slice==True and slice_value>0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=['Reference','Year'],values='value',title=f'{data_file} (Sunburst)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Funnel)')
        p6.plotly_chart(fig_funnel)
    elif filter_value!='All' and slice==True and slice_value>0:
        filtered_data=data[data[filter_column]==filter_value]
        grouped=filtered_data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        fig_treemap=px.treemap(grouped,path=[file_type,'Year'],values='value',title=f'{data_file} (Treemap)')
        p4.plotly_chart(fig_treemap)
        fig_sunburst=px.sunburst(grouped,path=['Reference','Year'],values='value',title=f'{data_file} (Sunburst)')
        p5.plotly_chart(fig_sunburst)
        fig_funnel=px.funnel(grouped,x='value',y=file_type,color='Year',title=f'{data_file} (Funnel)')
        p6.plotly_chart(fig_funnel)
    
    return p4,p5,p6

def plot_distribution(data,file_type,filter_column=None,filter_value='All',slice=False,slice_value=0):
    p7,p8=st.columns(2)
    if filter_value=='All'and slice==False:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        fig_box=px.box(grouped,x=file_type,y='value',title=f'{data_file} (Box - Chart)')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(grouped,x='value',title=f'{data_file} (Histogram)')
        p8.plotly_chart(fig_hist)
    elif filter_value!='All' and slice==False:
        filtered_data=data[data[filter_column]==filter_value]
        filtered_data['value']=np.abs(filtered_data['value'])
        fig_box=px.box(filtered_data,x=file_type,y='value',title=f'Box - Chart for {filter_value}')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(filtered_data,x='value',title=f'Histogram for {filter_value}')
        p8.plotly_chart(fig_hist)
    elif filter_value=='All' and slice==True and slice_value==0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[slice_value]
        fig_box=px.box(grouped,x='Reference',y='value',title=f'{data_file} (Box - Chart)')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(grouped,x='value',title=f'{data_file} (Histogram)')
        p8.plotly_chart(fig_hist)
    elif filter_value!='All' and slice==True and slice_value==0:
        filtered_data=data[data[filter_column]==filter_value]
        filtered_data['value']=np.abs(filtered_data['value'])
        filtered_data['Reference']=filtered_data[f'{filter_column}'].str.split(' ').str[slice_value]
        fig_box=px.box(filtered_data,x='Reference',y='value',title=f'Box - Chart for {filter_value}')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(filtered_data,x='value',title=f'Histogram for {filter_value}')
        p8.plotly_chart(fig_hist)
    elif filter_value=='All' and slice==True and slice_value>0:
        grouped=data.groupby(['Year',file_type]).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        grouped['Reference']=grouped[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        fig_box=px.box(grouped,x='Reference',y='value',title=f'{data_file} (Box - Chart)')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(grouped,x='value',title=f'{data_file} (Histogram)')
        p8.plotly_chart(fig_hist)
    elif filter_value!='All' and slice==True and slice_value>0:
        filtered_data=data[data[filter_column]==filter_value]
        filtered_data['value']=np.abs(filtered_data['value'])
        filtered_data['Reference']=filtered_data[f'{filter_column}'].str.split(' ').str[:slice_value].apply(lambda x: ' '.join(x))
        fig_box=px.box(filtered_data,x='Reference',y='value',title=f'Box - Chart for {filter_value}')
        p7.plotly_chart(fig_box)
        fig_hist=px.histogram(filtered_data,x='value',title=f'Histogram for {filter_value}')
        p8.plotly_chart(fig_hist)

    return p7,p8

def titles(absolute_section=False,distribution_Section=False):
    if absolute_section:
        ab=st.columns(1)[0]
        ab.markdown('### Absolute Payment Proportions')
        st.markdown('- This section shows the proportion of payments in the dataset, including treemap, sunburst, and funnel charts. The treemap chart shows the proportion of payments by region, data item, export/import, or commodity. The sunburst chart shows the proportion of payments by region and year. The funnel chart shows the proportion of payments by region, data item, export/import, or commodity.')
        return ab 
    if distribution_Section:
        dist=st.columns(1)[0]
        dist.markdown('### Distribution of Payments')
        st.markdown('- This section shows the distribution of payments in the dataset, including box and histogram charts. The box chart shows the distribution of payments by region, data item, export/import, or commodity. The histogram chart shows the frequency of payments in the dataset.')
        return dist
    else:
        return None
    
############################################
# Streamlit Global Configuration
############################################

st.set_page_config(page_title='Australian Trade Dashboard',page_icon='📈',layout='wide')
gif=read_gif('assets/Aus_gif.webp')
st.markdown(f'''
    <div style="display: flex; justify-content: center;">
        <img src="data:image/gif;base64,{gif}" style="width:10%;height:10%;object-fit:contain;">
    </div>
    ''',unsafe_allow_html=True)
c1,c2=st.columns([0.10,1])
c1.image('assets/australia.png',width=100)
c2.title('Australian Trade Data')
c2.markdown(' **Desc:** This dashboard shows the trade data of Australia | **socials:** [LinkedIn](https://www.linkedin.com/in/adam-m-62a5b4168/)')

    
decription_mode=st.toggle('Show Description',value=False)
if decription_mode:
    with st.expander('Description'):
        markdown_readme('README.md')


with st.spinner('Loading data...'):
    data_files={
        'Balance of Payments by State':'balance_of_payments_states.csv',
        'General Balance of Payments':'general_balance_of_payments.csv',
        'Export and Imports':'export_imports.csv',
        'Merchandise Imports':'merchandise_imports.csv',
        'Merchandise Exports':'merchandise_exports.csv'
    }

    data_file=st.selectbox('Select Data',data_files.keys(),help='Select one data file you want to load')
    data= pd.read_csv(filepath('data',data_files[data_file]))
    data=split_date(data,'TIME_PERIOD')

############################################
# Streamlit App
############################################

    def app():
        data_load()
        if data_file=='Balance of Payments by State':
            unique_regions=data['REGION'].unique()
            choices=np.insert(unique_regions,0,'All')
            region=st.selectbox('Select Region',choices)
            m2,m3,m4=st.columns(3)
            m2.metric('Performance to pevious year',f"{data['value'].pct_change().iloc[-1]:.2%}",delta=f"{data['value'].pct_change().iloc[-1]:.3%}",delta_color='normal')
            m3.metric('Total value',f"${data['value'].sum():,.0f}")
            m4.metric('Average value',f"${data['value'].mean():,.0f}")
            plot_charts(data,file_type='REGION',filter_column='REGION',filter_value=region)
            absolute_headings=titles(absolute_section=True)
            plot_proportion(data,file_type='REGION',filter_column='REGION',filter_value=region)
            distribution_headings=titles(distribution_Section=True)
            plot_distribution(data,file_type='REGION',filter_column='REGION',filter_value=region)
        elif data_file=='General Balance of Payments':
            metrics_value=data[~data['DATA_ITEM'].str.contains('Total',case=False)]
            unique_data_items=data['DATA_ITEM'].unique()
            choices=np.insert(unique_data_items,0,'All')
            data_item=st.selectbox('Select Data Item',choices)
            m2,m3,m4=st.columns(3)
            m2.metric('Performance to pevious year',f"{metrics_value['value'].pct_change().iloc[-1]:.2%}",delta=f"{metrics_value['value'].pct_change().iloc[-1]:.3%}",delta_color='normal')
            m3.metric('Total value',f"${metrics_value['value'].sum():,.0f}")
            m4.metric('Average value',f"${metrics_value['value'].mean():,.0f}")
            plot_charts(data,file_type='DATA_ITEM',filter_column='DATA_ITEM',filter_value=data_item,slice=True,slice_value=3)
            absolute_headings=titles(absolute_section=True)
            plot_proportion(data,file_type='DATA_ITEM',filter_column='DATA_ITEM',filter_value=data_item,slice=True,slice_value=0)
            distribution_headings=titles(distribution_Section=True)
            plot_distribution(data,file_type='DATA_ITEM',filter_column='DATA_ITEM',filter_value=data_item,slice=True,slice_value=0)
        elif data_file=='Export and Imports':
            metrics_value=data[~data['DATA_ITEM'].str.contains('Total',case=False)]
            unique_data_items=data['DATA_ITEM'].unique()
            choices=np.insert(unique_data_items,0,'All')
            data_item=st.selectbox('Select Data Item',choices)
            m2,m3,m4=st.columns(3)
            m2.metric('Performance to pevious year',f"{metrics_value['value'].pct_change().iloc[-1]:.2%}",delta=f"{metrics_value['value'].pct_change().iloc[-1]:.3%}",delta_color='normal')
            m3.metric('Total value',f"${metrics_value['value'].sum():,.0f}")
            m4.metric('Average value',f"${metrics_value['value'].mean():,.0f}")
            plot_charts(data,file_type='EXP_IMP',filter_column='DATA_ITEM',filter_value=data_item)
            absolute_headings=titles(absolute_section=True)
            plot_proportion(data,file_type='EXP_IMP',filter_column='DATA_ITEM',filter_value=data_item)
            distribution_headings=titles(distribution_Section=True)
            plot_distribution(data,file_type='EXP_IMP',filter_column='DATA_ITEM',filter_value=data_item)           
        elif data_file=='Merchandise Imports':
            metrics_value=data[~data['COMMODITY_SITC'].str.contains('Total',case=False)]
            unique_commodities=data['COMMODITY_SITC'].unique()
            choices=np.insert(unique_commodities,0,'All')
            commodity=st.selectbox('Select Commodity',choices)
            m2,m3,m4=st.columns(3)
            m2.metric('Performance to pevious year',f"{metrics_value['value'].pct_change().iloc[-1]:.2%}",delta=f"{metrics_value['value'].pct_change().iloc[-1]:.3%}",delta_color='normal')
            m3.metric('Total value',f"${metrics_value['value'].sum():,.0f}")
            m4.metric('Average value',f"${metrics_value['value'].mean():,.0f}")
            plot_charts(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)
            absolute_headings=titles(absolute_section=True)
            plot_proportion(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)
            distribution_headings=titles(distribution_Section=True)
            plot_distribution(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)
        elif data_file=='Merchandise Exports':
            metrics_value=data[~data['COMMODITY_SITC'].str.contains('Total',case=False)]
            unique_commodities=data['COMMODITY_SITC'].unique()
            choices=np.insert(unique_commodities,0,'All')
            commodity=st.selectbox('Select Commodity',choices)
            m2,m3,m4=st.columns(3)
            m2.metric('Performance to pevious year',f"{metrics_value['value'].pct_change().iloc[-1]:.2%}",delta=f"{metrics_value['value'].pct_change().iloc[-1]:.3%}",delta_color='normal')
            m3.metric('Total value',f"${metrics_value['value'].sum():,.0f}")
            m4.metric('Average value',f"${metrics_value['value'].mean():,.0f}")
            plot_charts(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)
            absolute_headings=titles(absolute_section=True)
            plot_proportion(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)
            distribution_headings=titles(distribution_Section=True)
            plot_distribution(data,file_type='COMMODITY_SITC',filter_column='COMMODITY_SITC',filter_value=commodity,slice=True,slice_value=3)

        

        if data_file=='Balance of Payments by State':
            c5=st.columns(1)[0]
            c5.markdown('### Geographic') 
            p9,p10=st.columns(2)
            grouped=data.groupby(['Year','REGION','latitude','longitude']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            st.map(grouped,size='value',latitude='latitude',longitude='longitude')

        else:
            c5=st.columns(1)[0]
            c5.markdown('')

        st.markdown('### Data Table')
        spreadsheet(data)

        with st.expander('Data Description'):
            st.write(data.describe())

        st.markdown('### Data Source')
        st.markdown('Australian Bureau of Statistics (ABS)')


if __name__=='__main__':
    app()


    
    



    







    



