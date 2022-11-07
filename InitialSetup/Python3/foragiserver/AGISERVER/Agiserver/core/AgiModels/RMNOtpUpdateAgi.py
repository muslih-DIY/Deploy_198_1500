from dataclasses import dataclass,field
from pystrix.agi.agi import AGI
import time
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (
    AbstractAgiApiInterface as AgiApiInterface,
    ApiProtocol,AGI,LoggerProtocol)
from Agiserver.core import ApiModels,Logger,Settings
from Agiserver.core.ConfigModels import IVRS_FLAG
from .extras import *
from .MobOtpVerify import OtpVerification




@dataclass
class RMNCaptureMenu(AgiApiInterface):
    """
    RMN CAPTURING MANUE in AGISERVER
    Take landline number as input
    src number 
    src_ll = agi.execute(GetVariable("BSNL-LL")) in the landline format if it is a bsnl landline
    ["PHONE_NO"]
    """
    Name:str = 'RmnCapture'
    Api: ApiProtocol = ApiModels.GetRmn()
    logger:LoggerProtocol = Logger.LogQ
    verbose_field:List = field(default_factory=lambda:['GV_MESSAGE','imsg'])
    dialplan_fields:List = field(default_factory=lambda:["iflag"])
    debug: bool=Settings.debug


    @staticmethod
    def WouldYouLiketoChangeRMN(agi:AGI,rmn:str):
        """
        \n #### Confirmation for changing the existing RMN
            \n ##### Your registered mobile number is ending with number
            \n ##### Would yo like to change your rmn if yes press 1 no press 2
            
        \n ##### if no response recieved it will be hangup with retry limit exceeded announcement.

        """
        agi.execute(StreamFile('rmncap_lastrmndig'))
        agi.execute(SayDigits(rmn[-4:]))
        reply = dtmf_capture(
            agi=agi,
            prompts=['rmncap_wouldchange','rmncap_pr1yes','rmncap_pr2no'],
            dtmf_keys=(1,2),
            attempt=4,
            timeout=5)
        
        if not reply:
            return RetryLimit(agi)
        return reply
        

    def Agiworks(self, agi: AGI, tid: str, src: str, conid: str, args: List[str]):
        src_ll:str = agi.execute(GetVariable("BSNL-LL")) 
        landline:str = args[0]
        rmn_details = self.Apihandler(self.Api,tid,src,conid,[landline],'GetRmn')
        rmn = rmn_details.get('RMN','')
        is_valid_rmn = (rmn and re.search(r'^[6-9]\d{9}$',rmn[-10:]) and not re.search(r'^9{10}$|^8{10}$|^7{10}$|^6{10}$',rmn[-10:]))

        ## if no rmn and calling from other than landline
        if  not (is_valid_rmn or (src_ll and src_ll==landline)):
            ## announce : please call from landline number or visit nearby exchange
            agi.execute(StreamFile('please_call_from_landline'))
            return  agi.execute(Hangup())

        ## if already having valid rmn ask for confirmation for change
        if is_valid_rmn:
            reply = self.WouldYouLiketoChangeRMN(agi,rmn)
            if reply !='1':
                return ThankHangup(agi)
        

        ## if source number is other than landline or rmn
        if  not (src_ll and src_ll==landline or src[-10:]==rmn[-10:]):
            """
            if calling from number other than landline number or rmn
            we will verify rmn number by sending otp
            """
            verifyotp = OtpVerification()
            response  = verifyotp.Agiworks(agi,tid,src,conid,[rmn])
            if not response.get('iflag')==IVRS_FLAG.SUCCESS:
                return ThankHangup(agi)

        # if customer calling from landline number or other number(having valid rmn)

        updatermn = GetNumberUpdateRMN()
        ## collect new number and send for update rmn
        return updatermn.Agiworks(agi,tid,src,conid,[landline,rmn])


@dataclass
class UpdateRMNOtp(AgiApiInterface):
    """ 
     This will collect mobile number,landline number as input
     send otp to mobile (WCT API) ,
     collect the otp
     verify the otp against otpid and update the RMN of landline number (WCT API) 

     args :  ["PHONE_NO","NewMN"]

     set dialplan variable Status as SUCEES/FAILURE
    """
    
    Name:str = 'UpdateRMN'
    Api: ApiProtocol = None
    otpsendapi:ApiProtocol = ApiModels.OtpSendApi(debug=Settings.debug)
    updatermn_otp:ApiProtocol = ApiModels.UpdateRmn(debug=Settings.debug)
    logger:LoggerProtocol = Logger.LogQ
    verbose_field:List = field(default_factory=lambda:['GV_MESSAGE','imsg'])
    dialplan_fields:List = field(default_factory=lambda:["iflag"])
    debug: bool=Settings.debug
    
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

    def Agiworks(self, agi: AGI, tid: str, src: str, conid: str, args: List[str]):
    
 
        def ValidatOTP_RMNupdate(Landline:str,OtpId:str,OTP:str,NewRMN: str)-> dict:
            " Validate otp with the otpid and update rmnreturn response from api"
            otp_validation_response = self.Apihandler(self.updatermn_otp,tid,src,conid,[Landline,OtpId,OTP,NewRMN],'RMNupdateOTP')
            return otp_validation_response

        landline,newrmn = args

        ## sending otp
        OTPid = self.SendOtp(agi,tid ,src ,conid, [newrmn]) 
      
        OTPDURATION:int = 4*60 #  4 sec
        response:dict = {}
        now = time.time()
        OTP=option=''


        # Validating the OTP within OTPDURATION
        while 1:
            Duration = OTPDURATION - int(time.time()-now)
            print(Duration)
            if Duration<=0:
                response['iflag']=IVRS_FLAG.OTP_TIMEOUT
                break
            if not OTP:
                OTP = GetOTP(agi,min((Duration-10)/7,3))
                continue
            if not option:
                attempt = min((Duration-5)/4,3)
                if attempt<1:
                    response['iflag']=IVRS_FLAG.OTP_TIMEOUT
                    break
                agi.execute(StreamFile('rmn-you-entered'))
                agi.execute(SayDigits(OTP))
                option = GetConform(agi,attempt)
                if option=='2':
                    OTP=option=''
                continue

            ## finishing point of RMN update     
            response = ValidatOTP_RMNupdate(landline,OTPid,OTP,newrmn)
            flag = response.get('iflag',IVRS_FLAG.OTHER_TECHNICAL_ISSUE)
            play_dict = {
                IVRS_FLAG.SUCCESS:['rmn-successful-register'],
                IVRS_FLAG.NOCHANGE:['invalid-number'],
                IVRS_FLAG.FAILURE:['rmn-invalid-otp'],
                'default':['sorry-tech-issue-try-later']
                }
            PlayFromDict(agi,play_dict,flag)    
            ThankHangup(agi)
            return response


        return response
    
        
@dataclass
class GetNumberUpdateRMN(UpdateRMNOtp):
     """
     = > This will collect landline number from asterisk
     = > collect new mobile number from AGI script   
     = > send otp to mobile (WCT API) ,
     = > collect the otp
     = > verify the otp against otpid and update the RMN of landline number (WCT API) 

     args :  ["PHONE_NO"]
     """
     def Agiworks(self, agi: AGI, tid: str, src: str, conid: str, args: List[str]):
         landline = args[0]
         rmn = args[1]
         mobilenumber = GetMobile(agi,'rmncap_entermob',5,12000)
         if not mobilenumber:
            return RetryLimit(agi)
         if rmn == mobilenumber:
            # This mobile is already same as that of your rmn 
            agi.execute(StreamFile('invalid-number'))
            return ThankHangup(agi) 
              
         return super().Agiworks(agi, tid, src, conid,[landline,mobilenumber])

