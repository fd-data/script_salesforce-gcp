import pandas as pd
from datetime import datetime, timedelta
from src.controller.get_var import get_data_handle

def execute_query_salesforce(nome_base: str, sf):
    """
    Executa uma query no Salesforce a partir de um arquivo SQL e retorna os resultados em um DataFrame.

    Parâmetros:
    - query_file_path: Caminho para o arquivo .sql contendo a query.
    - sf: Instância autenticada do Salesforce.

    Retorna:
    - DataFrame com os resultados da query.
    """
    # Captura o nome do arquivo sql a ser extraído
    query_file_path = get_data_handle(nome_base, var='query_file_path', cast_df=False)
    query_file_path = f'src/view/{query_file_path}'

    # Lê o conteúdo do arquivo SQL
    with open(query_file_path, 'r') as file:
        query = file.read()

    # Define a data em que a query será executada
    time_delta = 1 # Quantidade de dias que a data de hoje será subtraída (D-1, D-2, etc..)
    data_filtro = (datetime.now() - timedelta(days=time_delta)).strftime('%Y-%m-%d') # Define a data atual para o filtro

    # Formata a data atual no padrão Salesforce
    query = query.format(data_filtro=data_filtro)

    # Executa a query e transforma os resultados em um DataFrame
    result = sf.query_all(query)
    df = pd.DataFrame(result.get('records', []))
    df['data_ingestao'] = datetime.now().strftime('%Y-%m-%d')

    if 'attributes' in df.columns:
        df.drop(columns='attributes', inplace=True)

    return df