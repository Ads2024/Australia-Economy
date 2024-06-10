import pandas as pd
import os
import requests as re 
import yaml
from requests.exceptions import JSONDecodeError

STATE_BALANCE_PAYMENTS='balance_of_payments_states'
GENERAL_BALANCE_PAYMENTS='general_balance_of_payments'
TRADE='export_imports'
IMPORT='merchandise_imports'
EXPORT='merchandise_exports'

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

def save_data(data,directory=None,filename=None):
    path=filepath(directory,filename)
    try:
        if data is not None:
            data.to_csv(path,index=False)
    except Exception as e:
        print(e)
        return None
    return print(f"Data saved at {path}")


def main():
    for query in queries:
        config=load_config('links.yaml',query)
        data=get_abs_data(config)
        data=structure_content(data)
        save_data(data,'data',f'{query}.csv')    

if __name__=='__main__':
    main()




    