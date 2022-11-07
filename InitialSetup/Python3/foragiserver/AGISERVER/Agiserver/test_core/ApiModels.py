import pytest
from Agiserver.mod.ApiMod.ApiBase import ApiConfigBase
from dataclasses import dataclass,field
from typing import List
from Agiserver.test_core.Settings import (urls,IVRS_FLAG)

@dataclass
class ComplaintBook(ApiConfigBase):
    """
    args order ["IV_PHONENUMBER","IV_ServiceCode","CLI"]
    
    """
    name: str='Complaint'
    url :str = urls.complaint
    method: str = 'post'
    input_keys:List=field(default_factory=lambda:["IV_PHONENUMBER","IV_ServiceCode","CLI"])
    default_input:dict =field(default_factory=lambda:{"IV_ComplaintCode" : "01"})
    flag_field_key: str = 'S_FLAG'    

    flag_map_dict: dict = field(default_factory=lambda:{
        '0':IVRS_FLAG.NEW_TICKET_CREATED,
        '1':IVRS_FLAG.TICKET_ALREADY_EXIST,
        '6':IVRS_FLAG.SUSPENDED_NUMBER,
        '3':IVRS_FLAG.INVALID_NUMBER,
        '2':IVRS_FLAG.INVALID_NUMBER,
        '4':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '5':IVRS_FLAG.OTHER_TECHNICAL_ISSUE
        })

