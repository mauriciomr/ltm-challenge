import json
from google.cloud import bigquery
from datetime import datetime
from typing import List, Tuple

def q1_memory(local_file_path: str) -> List[Tuple[datetime.date, str]]:
    # Bigquery client
    bigquery_client = bigquery.Client()
    
    # prepare  file to BigQuery
    rows_to_insert = []
    with open(local_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            tweet = json.loads(line)
            date = datetime.strptime(tweet['date'], '%Y-%m-%dT%H:%M:%S%z').date()
            username = tweet['user']['username']
            rows_to_insert.append({'date': date, 'username': username})
    
    # dataset and table in bigquery
    dataset_id = 'ltm-challenge'
    table_id = 'q2'
    
    # check dataset
    dataset_ref = bigquery_client.dataset(dataset_id)
    try:
        bigquery_client.get_dataset(dataset_ref)
    except:
        bigquery_client.create_dataset(dataset_ref)
    
    # bigquery schema
    schema = [
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('username', 'STRING'),
    ]
    
    # check table
    table_ref = dataset_ref.table(table_id)
    try:
        table = bigquery_client.get_table(table_ref)
    except:
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
    
    # insert data
    errors = bigquery_client.insert_rows_json(table, rows_to_insert)
    if errors:
        print(f"Errors inserting rows: {errors}")
        return []
    
    # query to get the top users
    query = f"""
        WITH RankedTweets AS (
            SELECT 
                date, 
                username, 
                COUNT(*) AS tweet_count,
                ROW_NUMBER() OVER (PARTITION BY date ORDER BY COUNT(*) DESC) AS rank
            FROM `{bigquery_client.project}.{dataset_id}.{table_id}`
            GROUP BY date, username
        )
        SELECT date, username
        FROM RankedTweets
        WHERE rank = 1
        ORDER BY date DESC
        LIMIT 10
    """
    
    query_job = bigquery_client.query(query)
    results = query_job.result()
    
    # make the output in tuples
    top_ten_dates_user = [(row.date, row.username) for row in results]
    
    return top_ten_dates_user