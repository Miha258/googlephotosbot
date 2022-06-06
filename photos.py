from json_manager import get_from_json
from init_service import init_service
import pickle
import aiohttp



SERVICE = None

def create_album(album_name: str) -> str:
    global SERVICE
    SERVICE = init_service()
    request_body = {
        'album': {'title': album_name}
    }
    album = SERVICE.albums().create(body=request_body).execute()
    return album.get('id')


async def create_mediafile(url: str,message_id: str) -> bytes:
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }
    headers['X-Goog-Upload-File-Name'] = message_id
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response: 
            img = await response.read()

        async with session.post(upload_url,data=img) as response:
            return await response.read()


async def insert_mediafile_in_album(album_name: str,url: str,message_id: str) -> None:
    global SERVICE

    album_id = get_from_json(album_name)['album_id']
    SERVICE = init_service()
    uploadToken = await create_mediafile(url,message_id)
    uploadToken = uploadToken.decode('utf-8')
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
    else:
        print('Помилка ініціалізації сервісу Google')




