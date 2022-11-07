from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (AbstractAgiApiInterface,
                                            ApiProtocol,LoggerProtocol)
from Agiserver.core import ApiModels
from Agiserver.core.Logger import LogQ
from Agiserver.core.Settings import debug 


@dataclass
class BillStatusAgi(AbstractAgiApiInterface):
    """ This will collect the landline number for API"""
    
    Name:str = 'BillStatus'
    Api:ApiProtocol = ApiModels.BillApi(debug=debug)
    logger:LoggerProtocol = LogQ

    dialplan_field_map:dict = field(default_factory=lambda:{'iflag':'IFLAG'})
    response_field:List = field(init=False)
    debug: bool=debug
    dialplan_fields:List = field(
        default_factory=lambda:["AcctNbr","LastPaymentDate1","Amount1","LastPaymentDate2",
                                "Amount2","BillGenerationDate","LastPaymentDate3","Amount3",
                                "UnbilledAmount","Unbilleddate","BilledAmount","DueDate"])
    verbose_field:List = field(default_factory=lambda:['ResultMsg','imsg'])
