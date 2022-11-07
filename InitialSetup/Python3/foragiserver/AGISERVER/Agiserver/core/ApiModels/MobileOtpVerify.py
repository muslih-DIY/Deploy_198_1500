from dataclasses import dataclass,field
from typing import List
from Agiserver.mod import ApiBase
from Agiserver.core.ConfigModels import (urls,IVRS_FLAG)


@dataclass
class OtpSendApi(ApiBase.ApiConfigBase):
    """
    Input:
        MSISDN 
        ValiditySpan default 4 minutes
    Response:
        OtpId : 504247
        OTP_Flag: Y/N
        GV_MESSAGE: <message>
        ResultCode: 0000
    """
    name: str ='SendOtp'
    url: str  =   urls.SendOtp
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["MSISDN"])
    default_input: dict = field(default_factory=lambda:{"ValiditySpan" : "4"})
    flag_field_key: str =  'OTP_Flag'

    log_inputs_keys:List = field(default_factory=lambda:["MSISDN"])
    log_response_keys:List = field(default_factory=lambda:["OtpId"])

    flag_map_dict: dict = field(default_factory=lambda:{
        'Y':IVRS_FLAG.SUCCESS,
        'N':IVRS_FLAG.FAILURE})    

@dataclass
class ValidateOtp(ApiBase.ApiConfigBase):
    """
    Input:
        OTPId : 504247  (from otpsend api)
        OTPCode :288789 (from mobile)
    Response:
        V_Flag: Y/N
        GV_MESSAGE:<msg>
        ResultCode: 0000
    """
    name: str ='ValidateOtp'
    url: str  =   urls.ValidateOtp
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["OTPId","OTPCode"])
    default_input: dict = field(default_factory=lambda:{})
    flag_field_key: str =  'V_Flag'
    log_inputs_keys:List = field(default_factory=lambda:["OTPId"])    
    flag_map_dict: dict = field(default_factory=lambda:{
        'Y':IVRS_FLAG.SUCCESS,
        'N':IVRS_FLAG.FAILURE})