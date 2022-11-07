from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (AbstractAgiApiInterface,
                                            ApiProtocol,LoggerProtocol)
from Agiserver.core import ApiModels
from Agiserver.core.Logger import LogQ
from Agiserver.core.Settings import debug 


@dataclass
class VipCheckingAgi(AbstractAgiApiInterface):
    """ This will collect the landline number """
    
    Name:str = 'VipCheckingAgi'
    Api:ApiProtocol = ApiModels.CheckVip(debug=debug)
    logger:LoggerProtocol = LogQ
    
    # log_response_keys:List = field(default_factory=lambda:['AcctNbr'])
    
    dialplan_field_map:dict = field(default_factory=lambda:{'iflag':'IFLAG','VIP_FLAG':'vipf'})
    # response_field:List = field(init=False)
    
    verbose_field:List = field(default_factory=lambda:['GV_MESSAGE','imsg'])
    debug: bool=debug
