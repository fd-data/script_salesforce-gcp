import os
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce

def authenticate_salesforce():

    load_dotenv()
    client_id = os.getenv("SF_CLIENT_ID")
    client_secret = os.getenv("SF_CLIENT_SECRET")
    username = os.getenv("SF_USERNAME")
    password = os.getenv("SF_PASSWORD")
    security_token = os.getenv("SF_SECURITY_TOKEN")
    auth_url = os.getenv("SF_AUTH_URL")

    if not all([client_id, client_secret, username, password, security_token, auth_url]):
        raise EnvironmentError("As variáveis de ambiente para autenticação do Salesforce via Connected App não foram definidas corretamente.")

    # Fazendo a requisição para obter o access token via OAuth 2.0
    response = requests.post(
        auth_url,
        data={
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': f"{password}{security_token}"
        }
    )

    if response.status_code != 200:
        raise Exception(f"Falha na autenticação: {response.json()}")

    auth_response = response.json()
    access_token = auth_response['access_token']
    instance_url = auth_response['instance_url']

    # Conectando ao Salesforce usando o access token obtido
    sf = Salesforce(instance_url=instance_url, session_id=access_token)
    
    return sf
