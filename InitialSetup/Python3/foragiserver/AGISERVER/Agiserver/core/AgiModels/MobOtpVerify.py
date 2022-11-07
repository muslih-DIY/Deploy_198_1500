from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (
    AbstractAgiApiInterface as AgiApiInterface,
    ApiProtocol,AGI,LoggerProtocol
)
from Agiserver.core import ApiModels,Logger,Settings
from Agiserver.core.ConfigModels import IVRS_FLAG
from pystrix.agi.core import GetOption,GetData,SayDigits,StreamFile
import time
from .extras import *



def GetConform(agi,OTP: str,attempt:int=3,interval:int=4000):
    
    if attempt<1:return ''

    agi.execute(StreamFile('rmn-you-entered'))
    agi.execute(SayDigits(OTP))
    while attempt>0:
        option = agi.execute(GetOption('rmn-press1-confirm',('1','2'),100))
        if not option:
            option = agi.execute(GetOption('rmn-press2-reenter',('1','2'),interval))
        if not option:
            attempt-=1
            continue
        return option[0]
        
    return ''


def GetOTP(agi,attempt:int=3,otplength:int=6,intervel_ms:int=7000) -> str:
    " Get OTP from Asterisk Dialplan "
    while attempt>0:
        OTP,timeout = agi.execute(GetData('rmn-enter-otp',intervel_ms,otplength))
        print(OTP)
        if len(OTP or '')==otplength:return OTP
        attempt = attempt-1
    return ''


@dataclass
class OtpVerification(AgiApiInterface):
    """ 
     This will collect mobile number as input(WCT API)
     send otp to mobile ,
     collect the otp
     verify the otp against otpid (WCT API)

     args :  ["MSISDN"]

     success response:
        V_Flag: Y/N
        GV_MESSAGE:<msg>
        ResultCode: 0000
        iflag:FAILURE/SUCCESS
     
    """
    
    Name:str = 'OtpVerify'
    Api: ApiProtocol =None
    otpsendapi:ApiProtocol = ApiModels.OtpSendApi(debug=Settings.debug)
    otpverify:ApiProtocol = ApiModels.ValidateOtp(debug=Settings.debug)
    logger:LoggerProtocol = Logger.LogQ
    verbose_field:List = field(default_factory=lambda:['GV_MESSAGE','imsg'])
    dialplan_fields:List = field(default_factory=lambda:["NEW_NO","iflag"])
    debug: bool=Settings.debug

    def Agiworks(self, agi: AGI, tid: str, src: str, conid: str, args: List[str]):
        
        def SendOtp(self,agi:AGI,tid,src,conid,number: List):
            # sending otp to the mobile number in the args
            otp_send_response = self.Apihandler(self.otpsendapi,tid,src,conid,number,service_name='MobSendOTP')
            flag = otp_send_response.get('iflag','')
            if flag==IVRS_FLAG.SUCCESS:
                return otp_send_response.get('OtpId')
            ## if Failed play unable to send otp to your mobile number
            ##else we have technical issue please try again later
            if flag==IVRS_FLAG.FAILURE:
                #agi.execute(StreamFile(''))
                agi.execute(Hangup())
            TecErrorHangup(agi)
 
        def ValidatOTP(OtpId:str,OTP:str)-> dict:
            " Validate otp with the otpid return response from api"
            otp_validation_response = self.Apihandler(self.otpverify,tid,src,conid,[OtpId,OTP],'MobValidateOTP')
            return otp_validation_response


        ## sending otp
        OTPid = SendOtp(self,agi,tid ,src ,conid, args)
   


        OTPDURATION:int = 4*60 #  4 sec
        response:dict = {}
        now = time.time()
        OTP=option=''

        # Validating the OTP within OTPDURATION
        while 1:
            Duration = OTPDURATION - int(time.time()-now)
            print(Duration)
            if Duration<0:
                response['iflag']=IVRS_FLAG.OTP_TIMEOUT
                break
            if not OTP:
                OTP = GetOTP(agi,min((Duration-10)/7,3))
                continue
            if not option:
                option = GetConform(agi,OTP,min((Duration-5)/4,3))
                print(option)
                if option=='2':
                    OTP=option=''
                continue
            print(option)

            response = ValidatOTP(OTPid,OTP)
            flag = response.get('iflag',IVRS_FLAG.OTHER_TECHNICAL_ISSUE)
            play_dict = {
                IVRS_FLAG.SUCCESS:[],
                IVRS_FLAG.FAILURE:['rmn-invalid-otp'],
                'default':['rmn-invalid-otp']
                }
            PlayFromDict(agi,play_dict,flag)    
            return response
        return response
    
        



