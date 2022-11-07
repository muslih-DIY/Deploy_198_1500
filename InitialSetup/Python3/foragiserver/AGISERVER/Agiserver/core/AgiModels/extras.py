import re
from typing import  List,Dict,Any
from pystrix.agi.agi import AGI
from pystrix.agi.core import (
    GetOption,
    GetData,
    SayDigits,
    StreamFile,
    WaitForDigit,
    GetVariable,
    Hangup)

def PlayFromDict(agi: AGI,play_dict: Dict[Any,List[str]],key):
    "Play the prompts in the list of key"
    prompts = play_dict.get(key,play_dict.get('default',''))
    [agi.execute(StreamFile(p)) for p in prompts]
    return

def ThankHangup(agi:AGI):
    "play thank you for using bsnl service and hangup"
    agi.execute(StreamFile('thankyou'))
    agi.execute(Hangup())

def RetryLimit(agi: AGI):
    "announce retrylimit exceded and thank you finally hangup"
    agi.execute(StreamFile('retrylimit'))
    agi.execute(StreamFile('thankyou'))
    agi.execute(Hangup())
    return
def TecErrorHangup(agi: AGI):
    "announce technical error and thank you finally hangup"
    agi.execute(StreamFile('sorry-tech-issue-try-later'))
    agi.execute(StreamFile('thankyou'))
    agi.execute(Hangup())
    return
def dtmf_capture(agi:AGI,prompts:List[str],dtmf_keys: List[str],attempt:int,timeout:int)-> str:
    "timeout in seconds"
    while attempt>0:
        for s in prompts:
            option = agi.execute(GetOption(s,dtmf_keys,10))
            if option:
                return option[0]

        option = agi.execute(WaitForDigit(timeout*1000))
        if option:
            return option[0]
        attempt-=1
        if attempt>0:
            agi.execute(StreamFile('entersel'))

    return ''




def GetConform(agi:AGI,attempt:int=3,interval:int=4):
    "Return the 1 or 2 otherwise return None"
    return dtmf_capture(agi,['confrm','reenter'],('1','2'),attempt,interval)



def GetOTP(agi:AGI,attempt:int=3,otplength:int=6,intervel_ms:int=7000) -> str:
    " Get OTP from Asterisk Dialplan "
    while attempt>0:
        OTP,timeout = agi.execute(GetData('rmn-enter-otp',intervel_ms,otplength))
        if len(OTP or '')==otplength:return OTP
        attempt = attempt-1
    return ''

def GetMobile(agi: AGI,prompts:str,attempt:int=3,intervel_ms:int=7000):
    'rmncap_entermob'
    
    while attempt>=0:
        attempt-=1
        mobile,timeout = agi.execute(GetData(prompts,intervel_ms,max_digits=10))
        ## not a valid mobile number
        if not (
            mobile and 
            re.search(r'^[6-9]\d{9}$',mobile) and 
            not re.search(r'^9{10}$|^8{10}$|^7{10}$|^6{10}$',mobile)):
            agi.execute(StreamFile('invalid-number'))
            continue
        agi.execute(StreamFile('noent'))
        agi.execute(SayDigits(mobile))
        ## get confirmation
        if not GetConform(agi)=='1':
            continue
        return '0'+mobile
    return ''
            


