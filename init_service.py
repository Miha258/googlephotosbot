from Google import create_service
from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import Flow
from config import *


API_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = 'client_secret_GoogleAPITutorials_PhotoDesktopApp.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing',
          'https://www.googleapis.com/auth/photoslibrary.appendonly'
        ]

def init_service(code: str = None) -> Resource:
    service: Resource = create_service(CLIENT_SECRET_FILE,API_NAME, API_VERSION,code,SCOPES)  
    return service 

  
def get_auth_url() -> str:
  flow = flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            redirect_uri=f'https://{server_host()}/'
  )
  auth_url, _ = flow.authorization_url(prompt='consent')
  return auth_url

