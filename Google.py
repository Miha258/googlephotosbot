import pickle
import os
from config import *

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.discovery import Resource
from google.oauth2.credentials import Credentials

class InvalidCode(Exception): pass

def create_service(client_secret_file, api_name, api_version,code=None, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred: Credentials = pickle.load(token)
    
    if cred and not cred.valid:
        cred.refresh(Request())
    
    if code:
        try:
            flow: Flow = Flow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                scopes=SCOPES,
                redirect_uri=f'http://{server_host()}:{server_port()}'
            )
            flow.fetch_token(code=code)
            cred = flow.credentials
            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
        except Exception:
            raise InvalidCode('Неправельний код авторизації')
    try:
        service: Resource = build(API_SERVICE_NAME, API_VERSION, credentials=cred,static_discovery=False)
        return service
    except Exception as e:
        print(e)
    return None

        