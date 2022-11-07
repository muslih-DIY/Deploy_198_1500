from Agiserver.mod.ApiMod.ApiBase import ApiConfigBase
from dataclasses import dataclass,field
from typing import List
from enum import IntEnum

debug:bool = True

class IVRS_FLAG(IntEnum):
    SUCCESS = 1
    FAILURE  = 0
    TICKET_ALREADY_EXIST = 2
    NEW_TICKET_CREATED = 3
    SUSPENDED_NUMBER = 4
    INVALID_NUMBER = 5
    UNKNOWN_CUSTOMER = 5 
    INVALID_SERVICE = 6  
    API_INPUT_ERROR = 7
    TARGET_NOT_FOUND = 8
    DURATION_LIMITS = 9
    NOCHANGE    =   2

    TIMEOUT = -1
    READ_TIMEOUT = -2
    CONNECT_TIMEOUT = -3    
    OTHER_TECHNICAL_ISSUE = -4
    ERROR_AGI_INTERFACE_INPUT = -5
    UNKNOWN_FLAG = -6    

    def __str__(self) -> str:
        return str(self.value)

    def str(self):
        return self.__str__()

class hosts:
    osbcdr = 'https://osb.cdr.bsnl.co.in'  
    # osbcdr = 'https://10.198.215.51'
class urls:
    bill        =   hosts.osbcdr+'/osb/IVRStoBillingStatusRequestService/IVRStoBillingStatusServiceRest'
    complaint   =   hosts.osbcdr+'/osb/IVRSComplaintBookingService/ComplaintBookingRest'
    sendapp     =   hosts.osbcdr+'/osb/IVRSDownloadBSNLAppService/DownloadBSNLRest'
    lead        =   hosts.osbcdr+'/osb/IVRSNewConnectionService/NewConnectionRest'
    changed     =   hosts.osbcdr+'/osb/IVRSChangeNumberService/GetChangeNumber'
    getrmn      =   hosts.osbcdr+'/osb/IVRSGetRMNService/GetRMNRest/'
    vip         =   hosts.osbcdr+'/osb/IVRSGetVIPFlagService/GetVIPRest'
    appeal      =   hosts.osbcdr+'/osb/IVRSAppealBookingService/IVRSAppealRest'
    complaint_status = hosts.osbcdr+'/osb/IVRSTTService/IVRSTTRest'
    ttstatus    =   hosts.osbcdr+'/osb/IVRSTTService/IVRSTTRest'
    SendOtp     =   hosts.osbcdr+'/osb/IVRSSendOTPRequests/OTPSendRest'
    ValidateOtp =   hosts.osbcdr+'/osb/IVRSOTPValidateService/OTPValidationRest'
    UpdateRmn   =   hosts.osbcdr+'/osb/IVRSUpdateNbrEmailService/UpdateNbrEmail'

    
@dataclass
class GetRmn(ApiConfigBase):
    """
    args order ["IV_EXTID"]
    """    
    url :str = urls.getrmn
    input_keys:List=field(default_factory=lambda:['IV_EXTID'])
    flag_field_key: str = 'RMN' 


@dataclass
class ChdNoApi(ApiConfigBase):
    """
    args order ['OLD_NO']
    
    """
    url :str = urls.changed
    input_keys:List=field(default_factory=lambda:['OLD_NO'])
    flag_field_key: str = 'NEW_NO' 

    def clean_response(self, response: dict) -> dict:
        if response.get('NEW_NO','NA')=='NA':response['NEW_NO']=''
        return response

@dataclass
class CheckVip(ApiConfigBase):
    """
    args order ['LV_PHONE_NO']
    
    """
    url :str = urls.vip
    input_keys:List=field(default_factory=lambda :['LV_PHONE_NO'])
    flag_field_key: str = 'VIP_FLAG'    


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




@dataclass
class BillApi(ApiConfigBase):
    """
    input is: -> [number]
    """
    name: str='Bill'
    url :str = urls.bill
    method: str = 'get'
    input_keys:List=field(default_factory=lambda:['ServiceNumber'])
    flag_field_key: str = 'ResultCode'

@dataclass
class Get_Appeal_docket(ApiConfigBase):
    name: str ='get_app_dock'
    url: str  =   urls.appeal
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["IV_PHONENUMBER","ORDERSTATE"])
    flag_field_key: str = 'A_FLAG'
    flag_map_dict: dict = field(default_factory=lambda:{
        '11':IVRS_FLAG.SUSPENDED_NUMBER,
        '9':IVRS_FLAG.SUCCESS,
        '6':IVRS_FLAG.API_INPUT_ERROR,
        '4':IVRS_FLAG.API_INPUT_ERROR,
        '5':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '10':IVRS_FLAG.SUCCESS
        })

 
    def clean_response(self, response: dict) -> dict:

        S_OBJECT_CODE = response.pop('S_OBJECT_CODE',{})

        if S_OBJECT_CODE is None or S_OBJECT_CODE==[None]:return response

        for i in range(len(S_OBJECT_CODE)):
            response.update({
                f"S_OBJECT_CODE{i}":S_OBJECT_CODE[i]['S_OBJECT_CODE'],
                f"creationDate{i}":S_OBJECT_CODE[i]['creationDate'],
                f"closeDate{i}":S_OBJECT_CODE[i]['closeDate'],
            })
        return response

@dataclass
class BookAppeal(ApiConfigBase):
    name: str ='book_appeal'
    url: str  =   urls.appeal
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["IV_PHONENUMBER","S_OBJECT_CODE","CLI"])
    default_input: dict = field(default_factory=lambda:{"ORDERSTATE" : ""})
    flag_field_key: str =  'A_FLAG'
    flag_map_dict: dict = field(default_factory=lambda:{
        '0':IVRS_FLAG.NEW_TICKET_CREATED,
        '2':IVRS_FLAG.TICKET_ALREADY_EXIST,
        '4':IVRS_FLAG.API_INPUT_ERROR,
        '1':IVRS_FLAG.TARGET_NOT_FOUND,
        '8':IVRS_FLAG.TARGET_NOT_FOUND,
        '3':IVRS_FLAG.DURATION_LIMITS,
        '7':IVRS_FLAG.DURATION_LIMITS,
        '5':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '10':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '11':IVRS_FLAG.SUSPENDED_NUMBER
        })


@dataclass
class SendOtp(ApiConfigBase):
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
    flag_map_dict: dict = field(default_factory=lambda:{
        'Y':IVRS_FLAG.SUCCESS,
        'N':IVRS_FLAG.FAILURE})

@dataclass
class ValidateOtp(ApiConfigBase):
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
    flag_map_dict: dict = field(default_factory=lambda:{
        'Y':IVRS_FLAG.SUCCESS,
        'N':IVRS_FLAG.FAILURE})

@dataclass
class UpdateRmn(ApiConfigBase):
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
    flag_map_dict: dict = field(default_factory=lambda:{
        '901':IVRS_FLAG.SUCCESS,
        '903':IVRS_FLAG.NOCHANGE,
        '902':IVRS_FLAG.FAILURE})




@dataclass
class TTstatus(ApiConfigBase):
    name: str='TTstatus'
    url :str = urls.ttstatus
    method: str = 'post'
    input_keys:List=field(default_factory=lambda:['IV_PHONENUMBER','S_OBJECT_Code'])
    flag_field_key: str = 'T_FLAG'
