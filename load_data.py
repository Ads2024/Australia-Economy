import pandas as pd
import os
import requests as re 
import yaml
from requests.exceptions import JSONDecodeError
import geopy
from datetime import datetime,timedelta

STATE_BALANCE_PAYMENTS='balance_of_payments_states'
GENERAL_BALANCE_PAYMENTS='general_balance_of_payments'
TRADE='export_imports'
IMPORT='merchandise_imports'
EXPORT='merchandise_exports'
NEXT_EXECUTION_FILE='next_execution.txt'
queries=[STATE_BALANCE_PAYMENTS,GENERAL_BALANCE_PAYMENTS,TRADE,IMPORT,EXPORT]


def filepath(directory=None, filename=None):
    if directory is None and filename is not None:
        return os.path.join(os.getcwd(),filename)
    if filename is None:
        return os.path.join(os.getcwd(), directory)
    return os.path.join(os.getcwd(), directory, filename)

def load_config(file_name,query):
    with open(filepath(filename=file_name),'r',encoding='utf-8') as file:
        config=yaml.safe_load(file)
    return config[query]


def get_abs_data(url):
    headers={'Accept':'application/json'}
    print(f'Requsting data from {url}')
    print(f'Headers: {headers}')
    try:
        response =re.get(url,headers=headers)
        response.raise_for_status()  
        try:
            data = response.json()
        
        except ValueError: 
            print(f'Response content is not JSON: {response.text}')  
    except re.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    return data
    
def structure_content(content):
    if 'dataSets' not in content.keys():
        print('No data in content')
    try:
        observations=content['dataSets'][0]['observations']
        dimensions=content['structure']['dimensions']['observation']
        dimension_names={}
        for dim in dimensions:
            dimension_names[dim['id']]=[value['name']for value in dim['values']]
        records=[]
        for key,value in observations.items():
            indices =key.split(':')
            record={i:dimension_names[i][int(index)] for i,index in zip(dimension_names.keys(),indices)}
            record['value']=value[0]
            records.append(record)
        return pd.DataFrame(records)
    except KeyError as e:
        print(f'Key not found: {e}')
        return pd.DataFrame()

def add_state_geo_codes(dataframe,column_name):
    try:
        geolocator=geopy.Nominatim(user_agent='open_data_app')
        dataframe['latitude']=None
        dataframe['longitude']=None
        for i in range(len(dataframe)):
            location=geolocator.geocode(dataframe[column_name][i])
            if location is not None:
                dataframe.loc[i,'latitude']=location.latitude
                dataframe.loc[i,'longitude']=location.longitude
    except Exception as e:
        print(e)
        static_code={
            'New South Wales': '-33.8688,151.2093',
            'Victoria': '-37.8136,144.9631',
            'Queensland': '-27.4698,153.0251',
            'South Australia': '-34.9285,138.6007',
            'Western Australia': '-31.9505,115.8605',
            'Tasmania': '-42.8821,147.3272',
            'Northern Territory': '-12.4634,130.8456',
            'Australian Capital Territory': '-35.2809,149.1300',
            'Australia': '-25.2744,133.7751'
        }
        for i in range(len(dataframe)):
            state_name=dataframe[column_name].iloc[i]
            if state_name in static_code.keys():
                dataframe.loc[i,'latitude']=static_code[state_name].split(',')[0]
                dataframe.loc[i,'longitude']=static_code[state_name].split(',')[1]
            else:
                print(f'No coordinates found for {state_name}')
  

        return dataframe

     


def save_data(data,directory=None,filename=None):
    if data is None or data.empty:
        print(f'No data to save for {filename}')
        return None
    path=filepath(directory,filename)
    try:
        data.to_csv(path,index=False)
    except Exception as e:
        print(e)
        return None
    return print(f"Data saved at {path}")

def should_run_data_load():
    if not os.path.exists(NEXT_EXECUTION_FILE):
        return True
    with open(NEXT_EXECUTION_FILE,'r') as file:
        next_execution_str=file.read().strip()
        next_execution=datetime.strptime(next_execution_str,'%Y-%m-%d')
        return datetime.now()>=next_execution
    
def updated_next_period():
    next_execution=datetime.today()+timedelta(days=365)
    with open(NEXT_EXECUTION_FILE,'w') as file:
        file.write(next_execution.strftime('%Y-%m-%d'))
    return next_execution

def data_load():
    if should_run_data_load():   
        for query in queries:  
            config=load_config('links.yaml',query)
            data=get_abs_data(config)
            data=structure_content(data)
            if query==STATE_BALANCE_PAYMENTS:
                data=add_state_geo_codes(data,'REGION')
            save_data(data,'data',f'{query}.csv')
        updated_next_period() 





    