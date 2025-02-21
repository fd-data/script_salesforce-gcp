import pandas as pd
from google.cloud import bigquery

def generate_bigquery_schema(df):
    schema = []
    for column in df.columns:
        dtype = df[column].dtype

        # Ajustando o tipo de dado conforme a estrutura do BigQuery
        if pd.api.types.is_integer_dtype(dtype):
            schema.append(bigquery.SchemaField(column, 'INT64'))
        elif pd.api.types.is_float_dtype(dtype):
            schema.append(bigquery.SchemaField(column, 'FLOAT64'))
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            schema.append(bigquery.SchemaField(column, 'TIMESTAMP'))
        elif pd.api.types.is_bool_dtype(dtype):
            schema.append(bigquery.SchemaField(column, 'BOOLEAN'))
        else:
            schema.append(bigquery.SchemaField(column, 'STRING'))

    return schema