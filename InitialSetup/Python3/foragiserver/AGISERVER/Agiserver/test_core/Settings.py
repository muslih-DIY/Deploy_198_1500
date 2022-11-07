import os
from pathlib import Path
from enum import IntEnum

debug = False

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')
CONFIG_DIR = os.path.join(BASE_DIR, 'test_core/config/config.ini')
BASE_LOG_FILE = 'ivrs_basic_log.log'
API_LOG_TABLE = 'ivrs_basic_log'
LOCATION = '1500'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# loggf = update_wrapper(partial(filelog,filename=os.path.join(LOG_DIR,BASE_LOG_FILE)), filelog)

# loggq = logging_queue(
#     query=f"insert into ivrs_basic_log values({','.join(['%s']*9)})",
#     database='postgres',
#     fileloger=loggf,
#     updation_time=4,
#     daemon=True)
# loggq.start()

class hosts:
    osbcdr = 'https://osb.cdr.bsnl.co.in'  
    #osbcdr = 'https://10.195.215.51'
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
    SendOTP     =   hosts.osbcdr+'/osb/IVRSSendOTPRequests/OTPSendRest'
    rmn_upd     =   'https://portal2.bsnl.in/myportal/rmnrequest'
    
# class IVRS_FLAG:
#     SUCCESS = 1
#     FAILURE  = 0
#     TICKET_ALREADY_EXIST = 2
#     NEW_TICKET_CREATED = 3
#     SUSPENDED_NUMBER = 4
#     INVALID_NUMBER = 5
#     UNKNOWN_CUSTOMER = 5 
#     INVALID_SERVICE = 6  
#     API_INPUT_ERROR = 7
#     TARGET_NOT_FOUND = 8
#     DURATION_LIMITS = 9

#     TIMEOUT = -1
#     READ_TIMEOUT = -2
#     CONNECT_TIMEOUT = -3    
#     OTHER_TECHNICAL_ISSUE = -4
#     ERROR_AGI_INTERFACE_INPUT = -5
#     RESPONSE_FLAG_MISSING = -6
    

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

