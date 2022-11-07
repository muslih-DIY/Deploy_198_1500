import configparser
from pathlib import Path
import os


class config:

    _config_class = {}
        # '_oracledb':_oracledb,
        # '_postgresdb':_postgresdb
        # }
    PATH = os.path.join(Path(__file__).resolve().parent, 'config.ini')
    def __init__(self,path: str=None) -> None:
        
        if path:
            self.PATH = path
        
    class DictClass(object):
        def __init__(self, **kwargs):
            self._kwargs = kwargs
            for key in kwargs:
                setattr(self, key, kwargs[key])  
                      
        def __repr__(self) -> str:
            kstr = ', '.join([f"{k}={i}" for  k,i in self._kwargs.items()])
            return f'DictClass({kstr})'

    def load(self):
        configfile = self.readConfigDict()
        for conf_name,conf in configfile.items():
            class_type = conf.get('class_type',None)
            if class_type is None:
                setattr(self,conf_name,self.DictClass(**conf))
                continue
            setattr(self,conf_name,self._config_class[class_type](**conf))

    
    def register(self,confclasses:list):
        for confclass in confclasses:
            self._config_class.update({confclass.__name__:confclass})


    def readConfig(self,filename=None):
        if filename is None:filename=self.PATH
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def readConfigDict(self,filename=None):
        if filename is None:filename=self.PATH
        config:configparser.ConfigParser = configparser.ConfigParser()
        config.read(filename)
        return config._sections       

