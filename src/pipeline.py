import pandas as pd
import sqlite3
from google.cloud import bigquery


def load_data_to_bigquery(project_id, dataset_id, table_id, dataframe):
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )
    job = client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
    job.result()
    print(f"BigQuery: Loaded {len(dataframe)} rows into {table_id} table.")

def load_data_to_sqlite(database_path, table_name, dataframe):
    conn = sqlite3.connect(database_path)
    dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"SQLite: Loaded {len(dataframe)} rows into {table_name} table.")

def extract_data(file_path):
    xls = pd.ExcelFile(file_path)
    dataframes = {sheet.lower(): pd.read_excel(xls, sheet) for sheet in xls.sheet_names}
    return dataframes

def transform_data(dataframes):
    cases = dataframes["cases"]
    # Cálculo de KPIs
    kpis = {
        "total_cases": cases["id_case"].nunique(),
        "total_recovered": cases[cases["id_status"] == 1].shape[0],  # Assuming status id 1 is recovered
        "total_deaths": cases[cases["id_status"] == 2].shape[0],  # Assuming status id 2 is death
        "avg_recovery_time": (pd.to_datetime(cases["date_recovery"]) - pd.to_datetime(cases["date_symptom"])).mean().days
    }
    cases['age_group'] = (cases['age'] // 10) * 10
    death_percentage_by_age_group = cases[cases['id_status'] == 2].groupby('age_group').size() / cases.groupby('age_group').size() * 100
    death_percentage_by_age_group = death_percentage_by_age_group.fillna(0).reset_index(name='death_percentage')
    return kpis, death_percentage_by_age_group

# Crear dataset en BigQuery y ejecutar el esquema
def create_bigquery_dataset_and_tables(project_id, dataset_id, schema_path):
    client = bigquery.Client(project=project_id)
    dataset_ref = bigquery.Dataset(f'{project_id}.{dataset_id}')
    client.create_dataset(dataset_ref, exists_ok=True, timeout=30)
    print(f"BigQuery: Dataset {dataset_id} created or already exists.")
    with open(schema_path, 'r') as schema_file:
        schema = schema_file.read()
        queries = schema.split(';')
        for query in queries:
            if query.strip():
                client.query(query).result()

# Crear la base de datos en sqlite y ejecutar el esquema
def create_sqlite_db_and_tables(database_path, schema_path):
    conn = sqlite3.connect(database_path)
    with open(schema_path, 'r') as schema_file:
        conn.executescript(schema_file.read())
    conn.close()
    print(f"SQLite: Dataset {database_path} created or already exists.")