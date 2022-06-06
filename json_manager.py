import json
from typing import Union


def get_from_json(group_name: str) -> Union[None,dict]:
    with open('albums.json','r',encoding="utf-8") as f:
        albums = json.load(f)
    
    if group_name in albums:
        return albums[group_name]
    return None



def add_to_json(group_name: str,album_name: str,album_id: str) -> None: 
    with open('albums.json','r',encoding="utf-8") as f:
        albums = json.load(f)
  
    if not group_name in albums:
        albums[group_name] = {
            'album_name': album_name,
            'album_id': album_id
        }
        with open('albums.json','w',encoding="utf-8") as f:
            albums = json.dump(albums,f,indent = 4)


def remove_from_json(group_name: str) -> None:
    with open('albums.json','r',encoding="utf-8") as f:
        albums = json.load(f)
     
    if group_name in albums:
        del albums[group_name]
    
    with open('albums.json','w',encoding="utf-8") as f:
        json.dump(albums,f,indent = 4)


def remove_all_albums_id() -> None:
    with open('albums.json','r',encoding="utf-8") as f:
        albums = json.load(f)
    
    for album in albums:
        albums[album]["album_id"] = ""
    
    with open('albums.json','w',encoding="utf-8") as f:
        json.dump(albums,f,indent = 4)


def change_album_id(group_name: str,new_id: str) -> None:
    with open('albums.json','r',encoding="utf-8") as f:
        albums = json.load(f)
    
    if group_name in albums:
        albums[group_name]["album_id"] = new_id
    
    with open('albums.json','w',encoding="utf-8") as f:
        json.dump(albums,f,indent = 4)

remove_all_albums_id()