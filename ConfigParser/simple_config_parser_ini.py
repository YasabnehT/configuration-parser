import configparser
config = configparser.ConfigParser()
config["DEFAULT"] = {
    'ServerAliveInterval':'45',
    'Compression':'yes',
    'CompressionLevel':'9'}
config['forge.example'] = {}
config['forge.example']['User'] = 'hg'
config['topsecret.server.example'] = {}
topsecret = config['topsecret.server.example']
topsecret['Port'] = '50022'
topsecret['ForwardX11'] = 'no'
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini','w') as configfile:
    config.write(configfile)


config.sections()