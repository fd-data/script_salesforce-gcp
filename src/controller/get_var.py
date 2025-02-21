import pandas as pd
import json

def get_data_handle(nome_base: str, var: str, cast_df: bool):
    """
    Retorna o valor da variável referente à base inserida no "handle-config.json", podendo ser:

    "nome": Nome da base a qual o processo será executado
    "project_id": Id do projeto no GCP
    "dataset_id": Id do dataset no GCP
    "table_id": Id da tabela a ser alimentada no GCP
    "column_mapping": Mapeamento de campos para conversão do DataFrame
    "query_file_path": Query a ser executada na Salesforce para a coleta de dados
    """
    with open('./config/handle-config.json', 'r') as file:
        config = json.load(file)

    # Filtra a base pelo nome
    base = next((item for item in config if item.get("nome") == nome_base), None)

    if not base:
        raise ValueError(f"Base '{nome_base}' não encontrada no arquivo de configuração.")

    # Obtém o valor da variável solicitada
    column_catch = base.get(var, {})

    # Se `cast_df` for True e `column_catch` for convertível, retorna um DataFrame
    if cast_df:
        if isinstance(column_catch, (list, dict)):  
            return pd.DataFrame(column_catch)
        else:
            raise TypeError(f"Não é possível converter '{var}' para DataFrame.")

    return column_catch