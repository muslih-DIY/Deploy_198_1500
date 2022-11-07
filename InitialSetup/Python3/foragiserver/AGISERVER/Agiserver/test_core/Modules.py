from typing import Dict, List
from Agiserver.mod.ObserverLogger.Logger import ObserverLogger,FileHandler
from Agiserver.test_core.Settings import LOG_DIR,API_LOG_TABLE,CONFIG_DIR
from Agiserver.mod.dbwrapers.pg_wraper import pg2_wrap
from Agiserver.mod.ConfigMod.ReadConfig import config
from dataclasses import dataclass,asdict
import csv


@dataclass
class _postgresdb:
    class_type:str
    database  :str 
    user  :str 
    host    :str 
    password:str 
    port    :int = 5432

    def to_dict(self):
        return asdict(self)

conf = config(CONFIG_DIR)
conf.register([_postgresdb])
conf.load()

print('conf ready')



fileLogger = FileHandler(f'{LOG_DIR}/mylogger.log','TESTER:')

class PgHandler(pg2_wrap):

    table:str = API_LOG_TABLE
    Log_Dir:str = LOG_DIR

    def log(self,data:List[Dict]):
        for row in data:
            if not self.dict_insert(values=row,table=self.table):
                print(self.error)
                with open(f'{self.Log_Dir}/{self.table}.csv', 'w') as fp:
                    write = csv.writer(fp)
                    write.writerow(row.values())
        return 1


DbHandler = PgHandler(conf.postgresdb.to_dict())

print('dbHandler ready')


LogQ = ObserverLogger(DbHandler,f'{LOG_DIR}/Qloggerlog.log','LogQ',batch_size=5)


