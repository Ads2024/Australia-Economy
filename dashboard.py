import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
from mitosheet.streamlit.v1 import spreadsheet
import plotly.figure_factory as ff
import geopy

def data_path(directory=None, filename=None):
    if directory is None and filename is not None:
        return os.path.join(os.getcwd(),filename)
    if filename is None:
        return os.path.join(os.getcwd(), directory)
    return os.path.join(os.getcwd(), directory, filename)


def split_date(df,column):
    df['Year']=df[column].str.split('-').str[0]
    if df[column].str.split('-').str[1].str.isnumeric().all():
        df['Month']=df[column].str.split('-').str[1]
    else:
        df['Quarter']=df[column].str.split('-').str[1]
    return df

st.set_page_config(page_title='Australian Trade Dashboard',page_icon='📈',layout='wide')
c1,c2=st.columns([0.07,1])
c1.image('assets/australia.png',width=100)
c2.title('Australian Trade Data')
c2.markdown('Desc: This dashboard shows the trade data of Australia | socials: [LinkedIn](https://www.linkedin.com/in/adam-m-62a5b4168/)')


with st.spinner('Loading data...'):
    data_files={
        'Balance of Payments by State':'balance_of_payments_states.csv',
        'General Balance of Payments':'general_balance_of_payments.csv',
        'Export and Imports':'export_imports.csv',
        'Merchandise Imports':'merchandise_imports.csv',
        'Merchandise Exports':'merchandise_exports.csv'
    }


    data_file=st.selectbox('Select Data',data_files.keys(),help='Select one data file you want to load')
    data= pd.read_csv(data_path('data',data_files[data_file]))
    data=split_date(data,'TIME_PERIOD')

    if data_file=='Balance of Payments by State':
        unique_regions=data['REGION'].unique()
        choices=np.insert(unique_regions,0,'All')
        region=st.selectbox('Select Region',choices)
    elif data_file=='General Balance of Payments':
        unique_data_items=data['DATA_ITEM'].unique()
        choices=np.insert(unique_data_items,0,'All')
        data_item=st.selectbox('Select Data Item',choices)
    elif data_file=='Export and Imports':
         unique_data_items=data['DATA_ITEM'].unique()
         choices=np.insert(unique_data_items,0,'All')
         data_item=st.selectbox('Select Data Item',choices)
    elif data_file=='Merchandise Imports':
         unique_commodities=data['COMMODITY_SITC'].unique()
         choices=np.insert(unique_commodities,0,'All')
         commodity=st.selectbox('Select Commodity',choices)
    elif data_file=='Merchandise Exports':
         unique_commodities=data['COMMODITY_SITC'].unique()
         choices=np.insert(unique_commodities,0,'All')
         commodity=st.selectbox('Select Commodity',choices)


    m1,m2,m3,m4=st.columns(4)
    
    m1.write('')
    m2.metric('Performance to pevious year',f"{data['value'].pct_change().iloc[-1]:.2%}")
    m3.metric('Total value',f"${data['value'].sum():,.0f}")
    m4.metric('Average value',f"${data['value'].mean():,.0f}")
    m1.write('')
    
    # load three plots based dataframe context
    p1,p2,p3=st.columns(3)

    if data_file=='Balance of Payments by State':
        if region=='All':
            grouped=data.groupby(['Year','REGION']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',color='REGION',title='Balance of Payments by State (Bar - Chart)')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',color='REGION',title='Balance of Payments by State (Line - Chart)')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='REGION',title='Balance of Payments by State (Pie - Chart)')
            p3.plotly_chart(fig_pie)
        else:
            filtered_data=data[data['REGION']==region]
            state_grouped=filtered_data.groupby(['Year','REGION']).sum().reset_index()
            fig_bar=px.bar(state_grouped,x='Year',y='value',color='REGION',title=f'Balance of Payments by State (Bar - Chart) for {region}')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(state_grouped,x='Year',y='value',color='REGION',title=f'Balance of Payments by State (Line - Chart) for {region}')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='REGION',title=f'Balance of Payments by State (Pie - Chart)')
            p3.plotly_chart(fig_pie)  
    
    elif data_file=='General Balance of Payments':
        if data_item=='All':
            grouped=data.groupby(['Year','DATA_ITEM']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',title='General Balance of Payments (Bar - Chart)')
            p1.plotly_chart(fig_bar)
            fig_stack=px.bar(grouped,x='Year',y='value',color='DATA_ITEM',title='General Balance of Payments (Stacked - Chart)')
            p2.plotly_chart(fig_stack)
            fig_pie=px.pie(data,values='value',names='Year',title='General Balance of Payments (Pie - Chart)')
            p3.plotly_chart(fig_pie)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            grouped=filtered_data.groupby(['Year','DATA_ITEM']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',title=f'General Balance of Payments (Bar - Chart) for {data_item}')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',title=f'General Balance of Payments (Line - Chart) for {data_item}')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='General Balance of Payments (Pie - Chart)')
            p3.plotly_chart(fig_pie)

    elif data_file=='Export and Imports':
        if data_item=='All':
            grouped=data.groupby(['Year','EXP_IMP']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',color='EXP_IMP',title='Export and Imports (Bar - Chart)')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',color='EXP_IMP',title='Export and Imports (Line - Chart)')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='EXP_IMP',title='Export and Imports (Pie - Chart)')
            p3.plotly_chart(fig_pie)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            grouped=filtered_data.groupby(['Year','EXP_IMP']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',title=f'Export and Imports (Bar - Chart) for {data_item}')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',title=f'Export and Imports (Line - Chart) for {data_item}')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='Export and Imports (Pie - Chart)')
            p3.plotly_chart(fig_pie)

    elif data_file=='Merchandise Imports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Imports (Bar - Chart)')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Imports (Line - Chart)')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='Merchandise Imports (Pie - Chart)')
            p3.plotly_chart(fig_pie)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            grouped=filtered_data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',title=f'Merchandise Imports (Bar - Chart) for {commodity}')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',title=f'Merchandise Imports (Line - Chart) for {commodity}')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='Merchandise Imports (Pie - Chart)')
            p3.plotly_chart(fig_pie)

    elif data_file=='Merchandise Exports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Exports (Bar - Chart)')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',color='COMMODITY_SITC',title='Merchandise Exports (Line - Chart)')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='Merchandise Exports (Pie - Chart)')
            p3.plotly_chart(fig_pie)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            grouped=filtered_data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_bar=px.bar(grouped,x='Year',y='value',title=f'Merchandise Exports (Bar - Chart) for {commodity}')
            p1.plotly_chart(fig_bar)
            fig_line=px.line(grouped,x='Year',y='value',title=f'Merchandise Exports (Line - Chart) for {commodity}')
            p2.plotly_chart(fig_line)
            fig_pie=px.pie(data,values='value',names='Year',title='Merchandise Exports (Pie - Chart)')
            p3.plotly_chart(fig_pie)

    # proportion vizuals treemap and sunburst

    c3=st.columns(1)[0]
    c3.markdown('### Absolute Payment Proportions')

    p4,p5,p6=st.columns(3)

    if data_file=='Balance of Payments by State':
        if region=='All':
            grouped=data.groupby(['Year','REGION']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','REGION']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['REGION','Year'],values='value',title='Balance of Payments by State (Treemap)')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['REGION','Year'],values='value',title='Balance of Payments by State (Sunburst)')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='REGION',color='Year',title='Balance of Payments by State (Funnel)')
            p6.plotly_chart(fig_funnel)
        else:
            filtered_data=data[data['REGION']==region]
            filtered_data['value']=np.abs(filtered_data['value'])
            funnel=filtered_data.groupby(['Year','REGION']).sum().reset_index()
            state_grouped=filtered_data.groupby(['Year','REGION']).sum().reset_index()
            fig_treemap=px.treemap(state_grouped,path=['REGION','Year'],values='value',title=f'Balance of Payments by State (Treemap) for {region}')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(state_grouped,path=['REGION','Year'],values='value',title=f'Balance of Payments by State (Sunburst) for {region}')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='REGION',color='Year',title=f'Balance of Payments by State (Funnel) for {region}')
            p6.plotly_chart(fig_funnel)
    
    elif data_file=='General Balance of Payments':
        if data_item=='All':
            grouped=data.groupby(['Year','DATA_ITEM']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','DATA_ITEM']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['DATA_ITEM','Year'],values='value',title='General Balance of Payments (Treemap)')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['DATA_ITEM','Year'],values='value',title='General Balance of Payments (Sunburst)')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='DATA_ITEM',color='Year',title='General Balance of Payments (Funnel)')
            p6.plotly_chart(fig_funnel)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            filtered_data['value']=np.abs(filtered_data['value'])
            grouped=filtered_data.groupby(['Year','DATA_ITEM']).sum().reset_index()
            funnel=grouped.groupby(['Year','DATA_ITEM']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['DATA_ITEM','Year'],values='value',title=f'General Balance of Payments (Treemap) for {data_item}')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['DATA_ITEM','Year'],values='value',title=f'General Balance of Payments (Sunburst) for {data_item}')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='DATA_ITEM',color='Year',title=f'General Balance of Payments (Funnel) for {data_item}')
            p6.plotly_chart(fig_funnel)
    elif data_file=='Export and Imports':
        if data_item=='All':
            grouped=data.groupby(['Year','EXP_IMP']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','EXP_IMP']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['EXP_IMP','Year'],values='value',title='Export and Imports (Treemap)')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['EXP_IMP','Year'],values='value',title='Export and Imports (Sunburst)')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='EXP_IMP',color='Year',title='Export and Imports (Funnel)')
            p6.plotly_chart(fig_funnel)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            grouped=filtered_data.groupby(['Year','EXP_IMP']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','EXP_IMP']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['EXP_IMP','Year'],values='value',title=f'Export and Imports (Treemap) for {data_item}')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['EXP_IMP','Year'],values='value',title=f'Export and Imports (Sunburst) for {data_item}')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='EXP_IMP',color='Year',title=f'Export and Imports (Funnel) for {data_item}')
            p6.plotly_chart(fig_funnel)
    elif data_file=='Merchandise Imports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['COMMODITY_SITC','Year'],values='value',title='Merchandise Imports (Treemap)')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['COMMODITY_SITC','Year'],values='value',title='Merchandise Imports (Sunburst)')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='COMMODITY_SITC',color='Year',title='Merchandise Imports (Funnel)')
            p6.plotly_chart(fig_funnel)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            grouped=filtered_data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['COMMODITY_SITC','Year'],values='value',title=f'Merchandise Imports (Treemap) for {commodity}')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['COMMODITY_SITC','Year'],values='value',title=f'Merchandise Imports (Sunburst) for {commodity}')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='COMMODITY_SITC',color='Year',title=f'Merchandise Imports (Funnel) for {commodity}')
            p6.plotly_chart(fig_funnel)
    elif data_file=='Merchandise Exports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['COMMODITY_SITC','Year'],values='value',title='Merchandise Exports (Treemap)')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['COMMODITY_SITC','Year'],values='value',title='Merchandise Exports (Sunburst)')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='COMMODITY_SITC',color='Year',title='Merchandise Exports (Funnel)')
            p6.plotly_chart(fig_funnel)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            grouped=filtered_data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            funnel=grouped.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            fig_treemap=px.treemap(grouped,path=['COMMODITY_SITC','Year'],values='value',title=f'Merchandise Exports (Treemap) for {commodity}')
            p4.plotly_chart(fig_treemap)
            fig_sunburst=px.sunburst(grouped,path=['COMMODITY_SITC','Year'],values='value',title=f'Merchandise Exports (Sunburst) for {commodity}')
            p5.plotly_chart(fig_sunburst)
            fig_funnel=px.funnel(funnel,x='value',y='COMMODITY_SITC',color='Year',title=f'Merchandise Exports (Funnel) for {commodity}')
            p6.plotly_chart(fig_funnel)

    c4=st.columns(1)[0]
    c4.markdown('### Distribution of Payments')
    p7,p8=st.columns(2)

    if data_file=='Balance of Payments by State':
        if region=='All':
            grouped=data.groupby(['Year','REGION']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            fig_box=px.box(grouped,x='REGION',y='value',title='Balance of Payments by State (Box - Chart)')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(grouped,x='value',title='Balance of Payments by State (Histogram)')
            p8.plotly_chart(fig_hist)
        else:
            filtered_data=data[data['REGION']==region]
            filtered_data['value']=np.abs(filtered_data['value'])
            fig_box=px.box(filtered_data,x='REGION',y='value',title=f'Balance of Payments by State (Box - Chart) for {region}')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(filtered_data,x='value',title=f'Balance of Payments by State (Histogram) for {region}')
            p8.plotly_chart(fig_hist)

    elif data_file=='General Balance of Payments':
        if data_item=='All':
            grouped=data.groupby(['Year','DATA_ITEM']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            fig_box=px.box(grouped,x='DATA_ITEM',y='value',title='General Balance of Payments (Box - Chart)')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(grouped,x='value',title='General Balance of Payments (Histogram)')
            p8.plotly_chart(fig_hist)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            filtered_data['value']=np.abs(filtered_data['value'])
            fig_box=px.box(filtered_data,x='DATA_ITEM',y='value',title=f'General Balance of Payments (Box - Chart) for {data_item}')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(filtered_data,x='value',title=f'General Balance of Payments (Histogram) for {data_item}')
            p8.plotly_chart(fig_hist)
    elif data_file=='Export and Imports':
        if data_item=='All':
            grouped=data.groupby(['Year','EXP_IMP']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            fig_box=px.box(grouped,x='EXP_IMP',y='value',title='Export and Imports (Box - Chart)')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(grouped,x='value',title='Export and Imports (Histogram)')
            p8.plotly_chart(fig_hist)
        else:
            filtered_data=data[data['DATA_ITEM']==data_item]
            filtered_data['value']=np.abs(filtered_data['value'])
            fig_box=px.box(filtered_data,x='EXP_IMP',y='value',title=f'Export and Imports (Box - Chart) for {data_item}')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(filtered_data,x='value',title=f'Export and Imports (Histogram) for {data_item}')
            p8.plotly_chart(fig_hist)
    elif data_file=='Merchandise Imports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            fig_box=px.box(grouped,x='COMMODITY_SITC',y='value',title='Merchandise Imports (Box - Chart)')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(grouped,x='value',title='Merchandise Imports (Histogram)')
            p8.plotly_chart(fig_hist)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            filtered_data['value']=np.abs(filtered_data['value'])
            fig_box=px.box(filtered_data,x='COMMODITY_SITC',y='value',title=f'Merchandise Imports (Box - Chart) for {commodity}')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(filtered_data,x='value',title=f'Merchandise Imports (Histogram) for {commodity}')
            p8.plotly_chart(fig_hist)
    elif data_file=='Merchandise Exports':
        if commodity=='All':
            grouped=data.groupby(['Year','COMMODITY_SITC']).sum().reset_index()
            grouped['value']=np.abs(grouped['value'])
            fig_box=px.box(grouped,x='COMMODITY_SITC',y='value',title='Merchandise Exports (Box - Chart)')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(grouped,x='value',title='Merchandise Exports (Histogram)')
            p8.plotly_chart(fig_hist)
        else:
            filtered_data=data[data['COMMODITY_SITC']==commodity]
            filtered_data['value']=np.abs(filtered_data['value'])
            fig_box=px.box(filtered_data,x='COMMODITY_SITC',y='value',title=f'Merchandise Exports (Box - Chart) for {commodity}')
            p7.plotly_chart(fig_box)
            fig_hist=px.histogram(filtered_data,x='value',title=f'Merchandise Exports (Histogram) for {commodity}')
            p8.plotly_chart(fig_hist)

    c5=st.columns(1)[0]
    c5.markdown('### Geographic') # Only for Balance of Payments by State
    p9,p10=st.columns(2)
    if data_file=='Balance of Payments by State':
        # get the latitude and longitude of each state using geopy
        geolocator=geopy.Nominatim(user_agent='OpenStreetMap')
        lat_lon=[]
        for state in data['REGION'].unique():
            location=geolocator.geocode(state)
            if location is not None:
                lat_lon.append([state,location.latitude,location.longitude])
        lat_lon=pd.DataFrame(lat_lon,columns=['REGION','LAT','LON'])
        data=pd.merge(data,lat_lon,on='REGION')

        grouped=data.groupby(['Year','REGION','LAT','LON']).sum().reset_index()
        grouped['value']=np.abs(grouped['value'])
        st.map(grouped,size='value',latitude='LAT',longitude='LON')

    
    else:
        p9.write('')
        p10.write('')


with st.expander('View Full Raw Table Data'):
    spreadsheet(data)


    
    



    







    



