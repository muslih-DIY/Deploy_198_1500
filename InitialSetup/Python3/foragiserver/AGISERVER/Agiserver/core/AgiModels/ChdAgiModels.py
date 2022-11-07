from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (AbstractAgiApiInterface,
                                            ApiProtocol,LoggerProtocol)
from Agiserver.core import ApiModels
from Agiserver.core.Logger import LogQ
from Agiserver.core.Settings import debug 


@dataclass
class ChdNoAgi(AbstractAgiApiInterface):
    """ This will collect the landline number for API to find number changed"""
    
    Name:str = 'ChdNoAgi'
    Api:ApiProtocol = ApiModels.ChdNoApi(debug=debug)
    logger:LoggerProtocol = LogQ
    dialplan_field_map:dict = field(default_factory=lambda:{'iflag':'IFLAG'})
    debug: bool=debug
    verbose_field:List = field(default_factory=lambda:['GV_MESSAGE','imsg'])
    dialplan_fields:List = field(default_factory=lambda:["NEW_NO"])