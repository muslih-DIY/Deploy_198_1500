from ReadConfig import config
from dataclasses import dataclass,field

conf = config()

@dataclass
class _oracledb:
    class_type:str
    dbname  :str 
    dbuser  :str 
    host    :str 
    password:str 
    port    :int = 1521
    sid     :str =field(init=False)

    def __post_init__(self):
        self.sid = f"{self.host}:{self.port}/{self.dbname}"

@dataclass
class _postgresdb:
    class_type:str
    dbname  :str 
    dbuser  :str 
    host    :str 
    password:str 
    port    :int = 5432

conf = config()
conf.register([_oracledb,_postgresdb])
conf.load()
print(conf.postgresdb.port)
print(conf.oracledbsdc.__repr__())
print(conf.glob.ip)
