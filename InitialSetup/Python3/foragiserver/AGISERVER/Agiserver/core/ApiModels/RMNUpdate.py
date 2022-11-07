from dataclasses import dataclass,field
from typing import List
from Agiserver.mod import ApiBase
from Agiserver.core.ConfigModels import (urls,IVRS_FLAG)

@dataclass
class GetRmn(ApiBase.ApiConfigBase):
    """
    args order ["IV_EXTID"]
    number like 02169-298491
    response:
        'RMN': '<mobile/null>', 'FLAG': '<Y/N>', 'GV_MESSAGE': 'message'
    """    
    url :str = urls.getrmn
    name: str ='GetRmn'
    input_keys:List=field(default_factory=lambda:['IV_EXTID'])
    flag_field_key: str = 'FLAG' 
    log_response_keys:List = field(default_factory=lambda:['RMN'])


@dataclass
class UpdateRmn(ApiBase.ApiConfigBase):
    """
    Input:
        order "PHONE_NO","OTPId","OTPCode","NewMN"
        PHONE_NO : <landline/Service-number>

        UpdateMode[default] :
            0   : rmn
            1   : email
        OTPId : <otpid>
        OTPCode : <otp>
        NewMN : <new rmn>
        NewEmail : <new email>
    Response:
        URMN_Flag:
            901     : rmnupdated succesfully
            903     : Existing RMN is same as that of new given
            902     : error asper the message

        GV_MESSAGE  : <message>
        ResultCode  :
        CUST_ORDER_NBR :
    """
    name: str ='UpdateRmn'
    url: str  =   urls.UpdateRmn
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["PHONE_NO","OTPId","OTPCode","NewMN"])
    default_input: dict = field(default_factory=lambda:{"UpdateMode" : "0","NewEmail" : ""})
    flag_field_key: str =  'URMN_Flag'

    log_inputs_keys:List = field(default_factory=lambda:["PHONE_NO","NewMN"])

    flag_map_dict: dict = field(default_factory=lambda:{
        '901':IVRS_FLAG.SUCCESS,
        '903':IVRS_FLAG.NOCHANGE,
        '902':IVRS_FLAG.FAILURE})