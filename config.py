from configparser import RawConfigParser
import os

thisfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'server')
initfile = os.path.join(thisfolder, 'server.config')
config = RawConfigParser()
res = config.read(initfile)

def server_port():
    return config.get('serverconfig','PORT')

def server_host():
    return config.get('serverconfig','HOST')
