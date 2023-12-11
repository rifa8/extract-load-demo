from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
import json
import os

# extract from GCloud Storage
def read_from_gcs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_text()

bucket_name = os.getenv('BUCKET_NAME')
blob_name = 'rifa-task-1.json'
data = json.loads(read_from_gcs(bucket_name, blob_name))
df = pd.DataFrame(data)


# convert data type and column name
def cleaning(df):
    df.dropna(inplace=True)

    df['dateOfBirth'] = pd.to_datetime(df['dateOfBirth'], dayfirst=True)
    df['dateOfBirth'] = df['dateOfBirth'].dt.strftime('%d-%m-%Y')
    df['yearOfBirth'] = pd.to_numeric(df['yearOfBirth'])
    df['wand'] = df['wand'].apply(lambda x: str(x))

    df = df.rename(columns={
        'dateOfBirth': 'date_of_birth',
        'yearOfBirth': 'year_of_birth',
        'eyeColour': 'eye_colour',
        'hairColour': 'hair_colour',
        'hogwartsStudent': 'hogwarts_student',
        'hogwartsStaff': 'hogwarts_staff'
        }
    )
    
    return df

data_to_load = cleaning(df)


# create dataset in BigQuery
def create_dataset_bq(client, dataset):
    dataset_ref = client.dataset(dataset)

    try:
        dataset = client.get_dataset(dataset_ref)
        print('Dataset {} already exists.'.format(dataset))
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'asia-southeast1'
        dataset = client.create_dataset(dataset)
        print('Dataset {} created.'.format(dataset.dataset_id))
    return dataset

bigquery_client = bigquery.Client()
dataset = 'rifa_task1'
create_dataset_bq(bigquery_client, dataset)


# load to BigQuery
def load_to_bq(df, dataset):
    #define new table name that will be created based on the Pandas DataFrame
    table_id = 'task1_table'

    df.to_gbq(destination_table=f'{dataset}.{table_id}', if_exists='replace')

load_to_bq(data_to_load, dataset)
