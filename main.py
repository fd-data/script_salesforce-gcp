import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from src.controller.gen_schema_bq import generate_bigquery_schema
from src.controller.query_salesforce import execute_query_salesforce
from src.controller.convert_data import convert_data
from src.controller.import_to_bq import import_to_bq
from config.credentials import authenticate_salesforce

# Criar diretório logs caso não exista
os.makedirs("logs", exist_ok=True)

# Formatar data e hora para nome do arquivo
data_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"logs/execution_{data_log}.log"),  # Salva logs em arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)

def load_config(file_path: str):
    """Carrega e valida o arquivo handle-config.json"""
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        if not isinstance(config, list):
            raise ValueError("Formato inválido no handle-config.json. Esperado uma lista de dicionários.")
        return config
    except Exception as e:
        logging.error(f"Erro ao carregar config: {e}")
        exit(1)  # Para a execução em caso de erro crítico

def process_base(nome_base, sf):
    """Processa uma base do handle-config.json"""
    try:
        logging.info(f"::: Iniciando processo para: {nome_base} :::")

        # Executa a query na Salesforce
        logging.info(f"Executando query para {nome_base} na Salesforce...")
        df = execute_query_salesforce(nome_base, sf)

        # Converte os dados conforme mapeamento
        logging.info("Convertendo os dados necessários...")
        df = convert_data(df, nome_base)

        # Gera o schema para o BigQuery
        logging.info("Ajustando o schema para o banco de dados no GCP...")
        schema = generate_bigquery_schema(df)

        # Importa os dados para o BigQuery
        logging.info("Carregando os dados para o banco de dados no GCP...")
        import_to_bq(df, schema, nome_base)

        return "Sucesso"

    except Exception as e:
        logging.error(f"Erro no processamento de {nome_base}: {e}")
        return f"Erro: {str(e)}"

def main():
    """Função principal que coordena a execução do script"""
    # Carregar variáveis de ambiente
    dotenv_path = os.path.join("config", ".env")
    load_dotenv(dotenv_path)

    # Autenticação na Salesforce
    logging.info("Autenticando na Salesforce...")
    sf = authenticate_salesforce()

    # Carregar configuração
    config_path = os.path.join("config", "handle-config.json")
    config = load_config(config_path)

    # Processar todas as bases
    resultados = {item["nome"]: process_base(item["nome"], sf) for item in config if "nome" in item}

    # Exibir resumo final
    logging.info("::: Processamento finalizado :::")
    for base, status in resultados.items():
        logging.info(f"{base}: {status}")

if __name__ == "__main__":
    main()
