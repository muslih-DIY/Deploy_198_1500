
from abc import ABC
from datetime import date
from typing import Dict, List, Tuple
from dataclasses import dataclass,field
from requests.exceptions import Timeout,ReadTimeout,ConnectTimeout
from requests import Session
from enum import IntEnum
import functools

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


class IVRS_FLAG(IntEnum):
    SUCCESS = 1
    FAILURE  = 0
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


@dataclass
class ApiConfigBase(ABC):
    """
    name will have default name of the class
    url : url of api
    name: Name of the api
    method: get/post
    header:any header in the dictionary form
    trust_env: trust_env of requests.session
    input_keys: list of the input keys ,later for json/dict from this key ,if argument passed is list
    default_input: Any input which is default can be added here as key:value pair in dict,It can also ovveride in the input_keys
    flag_field_key:Any flag key in the API
    flag_map_dict: It is dictionary which map the 'flag_field_key' value to iflag based on the key[content in flag_field]:value[corresponding falg in iflag]

    log_inputs_keys:List = field(default_factory=list)
    log_response_keys:List = field(default_factory=list)
    
    """
    url:str
    name:str='ApiConfigBase'
    method:str='get'
    time_out:Tuple=(6.05,18)
    header:Dict=field(default_factory=dict)
    trust_env:bool=False
    input_keys:List=field(default_factory=list)
    default_input:Dict=field(default_factory=dict)
    flag_field_key: str = None
    flag_map_dict: dict=field(default_factory=dict)
    
    log_inputs_keys:List = field(default_factory=list)
    log_response_keys:List = field(default_factory=list)

    debug: bool = False
    
    def __post_init__(self):
        self.name = self.__class__.__name__
        self.session = Session()
        self.session.trust_env=self.trust_env
        self.api_method = self.session.post if self.method=='post' else self.session.get
        self.input_load = 'json' if self.method=='post' else 'params'        
        if not (isinstance(self.time_out,tuple) or isinstance(self.time_out,int)):
            self.time_out=(6.05,18)
        
        self.call_clean_map = compose(self.map_ivrs_flag,self.clean_response,self.call)
        self.arginput_call_clean_map = compose(self.call_clean_map,self.generate_input_dict)
    
    def call(self,input_data:dict):
        try:
            re=self.api_method(self.url,**{self.input_load:input_data},headers=self.header, timeout=self.time_out)
        except ConnectTimeout:
            if self.debug == True:raise
            return {'status_code':504, 'imsg': IVRS_FLAG.CONNECT_TIMEOUT.name,'iflag':IVRS_FLAG.CONNECT_TIMEOUT}
        except  ReadTimeout:
            if self.debug == True:raise
            return {'status_code':408,'imsg': IVRS_FLAG.READ_TIMEOUT.name,'iflag':IVRS_FLAG.READ_TIMEOUT}
        except Timeout:
            return {'status_code':111, 'imsg': IVRS_FLAG.TIMEOUT.name,'iflag':IVRS_FLAG.TIMEOUT}
        except Exception as e:
            if self.debug == True:raise
            return {'status_code':000,'imsg':'i-Exception:'+str(e)[:60].replace("'",'|'),'iflag':IVRS_FLAG.OTHER_TECHNICAL_ISSUE}
        try :
            data=re.json()
        except :
            if self.debug == True:raise
            return {'status_code':re.status_code, 'imsg': re.reason+' @json_decode','iflag':IVRS_FLAG.OTHER_TECHNICAL_ISSUE}
        res={'status_code':re.status_code,'imsg':IVRS_FLAG.SUCCESS.name,'iflag':IVRS_FLAG.SUCCESS}    
        
        res.update(data)
        if self.debug:print('API_RESPONS:',res)
        return res
    

    def generate_input_dict(self,input_args:List)-> dict:
        """pass the args in the same order specified in the input_keys"""

        keys = self.input_keys
        default = self.default_input

        if not keys :
            raise ValueError('input keys are not specified')
        if len(keys) !=len(input_args):
            raise ValueError('input and argument length are not matching')
        input = dict(zip(keys,input_args))
        input.update(default)

        return input
    
    def clean_response(self,response:dict)-> dict:
        return response

    def map_ivrs_flag(self,response:dict)-> dict:
        if not response:
            raise ValueError("no response parameter passed")
        iflag = response.get('iflag',None)

        if iflag==IVRS_FLAG.SUCCESS:
            flag_dict = self.flag_map_dict
            flag_field = self.flag_field_key

            if flag_dict and flag_field:
                flag = response.get(flag_field,None)
                default = flag_dict.get('default',IVRS_FLAG.UNKNOWN_FLAG)
                response['iflag'] = flag_dict.get(flag,default)                
            return response
        response.update({'fimsg':response.get('imsg','')[:60]}) 
        return response  
    
    def extract_response_log(self,response):
        log_response = self.log_response_keys
        return '&'.join([f"{val}" if val else '' for key,val in response.items() if key in log_response])[:80] if log_response else None

 
    def extract_input_log(self,input_dict:dict):
        log_input = self.log_inputs_keys

        return '&'.join([f"{val}" for key,val in input_dict.items() if key in log_input])[:80] if log_input else None
                
