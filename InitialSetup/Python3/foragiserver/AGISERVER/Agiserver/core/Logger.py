from typing import Dict, List
from Agiserver.mod.dbwrapers.pg_wraper import pg2_wrap
from Agiserver.mod.ObserverLogger.Logger import ObserverLogger,FileHandler
from Agiserver.core.Settings import LOG_DIR,API_LOG_TABLE,CONFIG_DIR
from Agiserver.core.ConfigModels import postgresdb,env_postgresdb_conf_mapper
from Agiserver.mod.ConfigMod.ReadConfig import config
import csv
import os

conf = config(CONFIG_DIR)
conf.register([postgresdb])

conf.load()

pgconf_env :dict = {}
for key,var in env_postgresdb_conf_mapper.items():
    if os.environ.get(var,None):pgconf_env[key]=os.environ.get(var,None)


pgconf = postgresdb(**pgconf_env).to_dict() if pgconf_env else conf.postgresdb.to_dict()

print('Configuration Loaded..')

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

#print('ini:',conf.postgresdb.to_dict())
#print(pgconf)

DbHandler = PgHandler(pgconf)




LogQ = ObserverLogger(DbHandler,f'{LOG_DIR}/Qloggerlog.log','LogQ',batch_size=5)

print('LogQ is  Ready to run ..')