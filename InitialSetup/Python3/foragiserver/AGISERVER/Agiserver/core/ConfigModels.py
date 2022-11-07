
from dataclasses import dataclass,asdict
from enum import IntEnum
from os import environ



@dataclass
class postgresdb:
    database  :str 
    user  :str 
    host    :str 
    password:str 
    port    :int = 5432
    class_type:str = None

    def to_dict(self):
        return asdict(self)

env_postgresdb_conf_mapper:dict = {
                        'database':'database' ,
                        'user':'dbuser',
                        'host':'dbhost',
                        'password':'dbpassword',
                        'port':'dbport' }

class hosts:
    osbcdr = environ.get('OSBCDR_HOST','https://osb.cdr.bsnl.co.in') 

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
    rmn_upd     =   'https://portal2.bsnl.in/myportal/rmnrequest'

    

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
    SHORT_DURATION_LIMITS = 9
    LONG_DURATION_LIMITS = 10
    OTP_TIMEOUT = 11
    NOCHANGE = 12

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