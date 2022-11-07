import pytest
from dataclasses import dataclass,field
from IvrsSystem.AGI.Agiserver.mod.ApiMod.test_APIs import ComplaintBook
from Agiserver.mod.AgiMod.AgiApiBase import AbstractAgiApiInterface,ApiProtocol,LoggerProtocol
from typing import  List

from Agiserver.test_core.Modules import LogQ

debugmod = True
@dataclass
class ComplaintAgi(AbstractAgiApiInterface):
    Name:str = 'complaint'
    Api:ApiProtocol = ComplaintBook(debug=debugmod)
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
    debug: bool=debugmod



def test_complaint_agi():
    LogQ.start()
    agi = ComplaintAgi()
    response = agi.Apihandler('test','test123','TEST',['020-42352079','Z2','91883347066'])
    cleaned_response = agi.dialplan_key_maper(response)
    print(cleaned_response)
    LogQ.stop_gracefully()

