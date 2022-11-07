
from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import AbstractAgiApiInterface,ApiProtocol,LoggerProtocol
from Agiserver.test_core import ApiModels
from Agiserver.test_core.Modules import LogQ
from Agiserver.test_core.Settings import debug 

@dataclass
class ComplaintAgi(AbstractAgiApiInterface):
    Name:str = 'complaint'
    Api:ApiProtocol = ApiModels.ComplaintBook(debug=debug)
    logger:LoggerProtocol = LogQ
    log_inputs_keys:List = field(default_factory=lambda:[
                                'IV_PHONENUMBER',
                                'IV_ServiceCode',
                                'IV_ComplaintCode'
                                ])
    log_response_keys:List = field(default_factory=lambda:['S_OBJECT_ID'])
    verbose_field:List = field(default_factory=lambda:['GV_Message','imsg'])
    dialplan_field_map:dict = field(default_factory=lambda:{
                                'S_OBJECT_ID':'DOCKETID',
                                'iflag':'CFLAG'
                                })
    response_field:List = field(init=False)
    debug: bool=debug

