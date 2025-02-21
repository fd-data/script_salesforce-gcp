import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from src.controller.get_var import get_data_handle

def import_to_bq(df: pd.DataFrame, schema, nome_base: str):
    """
    Importa um DataFrame para o BigQuery.

    Parâmetros:
    - df: DataFrame do pandas a ser carregado.
    - path_key: Caminho para o arquivo de credenciais do serviço.
    - project_id: ID do projeto no BigQuery.
    - dataset_id: ID do dataset no BigQuery.
    - table_id: Nome da tabela no BigQuery.
    - schema: Esquema da tabela no BigQuery.
    """
    # Coleta as credenciais para o acesso ao GCP
    path_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    project_id = get_data_handle(nome_base, var='project_id', cast_df=False)
    dataset_id = get_data_handle(nome_base, var='dataset_id', cast_df=False)
    table_id = get_data_handle(nome_base, var='table_id', cast_df=False)

    credentials = service_account.Credentials.from_service_account_file(path_key)
    client = bigquery.Client(project=project_id, credentials=credentials)

    table_ref = f'{project_id}.{dataset_id}.{table_id}'

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Aguarda a conclusão do job

        print(f"Dados enviados com sucesso para {table_ref}: {df.shape[0]} registros.")
    except Exception as e:
        print(f"Erro ao enviar os dados para o BigQuery: {e}")
