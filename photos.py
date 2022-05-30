from json_manager import get_from_json
from init_service import init_service
import os
import pickle
import requests


SERVICE = None

def create_album(album_name: str) -> str:
    global SERVICE
    SERVICE = init_service()
    request_body = {
        'album': {'title': album_name}
    }
    album = SERVICE.albums().create(body=request_body).execute()
    return album.get('id')


def create_mediafile(file_name: str) -> requests.Response:
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }

    image_file = os.path.join(os.getcwd(), file_name)
    headers['X-Goog-Upload-File-Name'] = file_name
    img = open(image_file, 'rb').read() 
    response = requests.post(upload_url, data=img, headers=headers)
    return response


def insert_mediafile_in_album(album_name: str,file_name: str) -> None:
    global SERVICE

    album_id = get_from_json(album_name)['album_id']
    SERVICE = init_service()
    uploadToken = create_mediafile(file_name).content.decode('utf-8')
    request_body = {
        "albumId": album_id,
        'newMediaItems': [
            {
                'description': 'Kuma the corgi',
                'simpleMediaItem': {
                    'uploadToken': uploadToken
                }
            }
        ]
    }
    if SERVICE:
        SERVICE.mediaItems().batchCreate(body=request_body).execute()
        os.remove(file_name)
    else:
        print('Помилка ініціалізації сервісу Google')

