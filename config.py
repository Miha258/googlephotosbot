from configparser import RawConfigParser
import os

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'server.config')
config = RawConfigParser()
res = config.read(initfile)

def server_port():
    return config.get('SERVER','PORT')

def server_host():
    return config.get('SERVER','HOST')




