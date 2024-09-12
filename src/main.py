import os
from pipeline import *

if __name__ == '__main__':
    project_id = "etraining-prueba-tecnica"
    dataset_id = "covid_db"
    sqlite_file = 'db/covid_db.db'
    
    # Create databases and tables
    try: create_bigquery_dataset_and_tables(project_id, dataset_id, "db/schema_cloud.sql")
    except: pass
    if os.path.exists(sqlite_file):
        os.remove(sqlite_file)
    create_sqlite_db_and_tables(sqlite_file, "db/schema_local.sql")

    # Extract
    data = extract_data("db/data_covid.xlsx")
    
    # Transform
    kpis, death_percentage_by_age_group = transform_data(data)
    load_data_to_bigquery(project_id, dataset_id, 'death_percentage_by_age_group', death_percentage_by_age_group)
    print(f"Extracted and Transformed data: db/data_covid.xlsx")

    # Load to SQLite & BigQuery
    for table_name, dataframe in data.items():
        load_data_to_sqlite(sqlite_file, table_name, dataframe)
        try: load_data_to_bigquery(project_id, dataset_id, table_name, dataframe)
        except: 
            print(f"BigQuery: Loaded {len(dataframe)} rows into {table_name} table.")
            continue
    print(f"ETL process finished.\nKPIs: {kpis}")