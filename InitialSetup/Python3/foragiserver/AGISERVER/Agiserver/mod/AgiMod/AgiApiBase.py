from abc import ABC
from typing import  List, Protocol
from dataclasses import dataclass,field
from pystrix.agi  import core as agiapp
from pystrix.agi import AGI
import functools
from datetime import datetime

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

class LoggerProtocol(Protocol):
    
    def save(self,data_dict: dict):
        ...

class ApiProtocol(Protocol):
    
    flag_field_key:List
    name:str
    def call_clean_map(self,input_data: dict):
        ...
    def arginput_call_clean_map(self,args:List):
        ...
    def call(self,input_data:dict):
        ...
    def generate_input_dict(self,input_args:List)-> dict:
        ...

@dataclass
class AbstractAgiApiInterface(ABC):
    """
    Override this Agiworks function to do tasks.
       def Agiworks(self, agi:AGI,tid:str,src:str,conid:str,args: List[str]):pass
    """
    Name:str
    Api:ApiProtocol
    logger:LoggerProtocol
    verbose_field:List = field(default_factory=list)
    dialplan_field_map:dict = field(default_factory=dict)
    dialplan_fields:List = field(default_factory=list)
    response_field:List = field(init=False)
   
    debug : bool = False
    
    def __post_init__(self):
        self.dialplan_field_map_key:set = set(self.dialplan_field_map.keys())
        self.dialplan_field:set = set(list(self.dialplan_field_map.values())+ self.dialplan_fields)
        self.time_fun = datetime.now
    def save_log(self,Api: ApiProtocol,tid,src,conid,input_dict,response,service_name):
        "save the log"
        data = self.get_log_data(Api,tid,src,conid,input_dict,response,service_name)
        self.logger.save(data)


    def Apihandler(
        self,
        Api:ApiProtocol,
        tid: str,
        src: str,
        conid: str,
        args: list,
        service_name:str='') -> dict:
        """
        Simply call the API and log rlevent field using save function
        return response dict
        self,tid: str,src: str,conid: str,args: list
        inputs : 
            tid: str    -- transactionid from dialplan
            src: str    -- calling source 
            conid:str   -- container id from dialplan
            args:list   -- input arguments [order is very important]
        response dictionary

         The Apihandler will log the response
        """
        
        input_dict = Api.generate_input_dict(args)

        if self.debug:print('input dict :',input_dict)  

        response:dict = Api.call_clean_map(input_dict)

        if self.debug:
            print('response Data :',response)
        
        self.save_log(Api,tid,src,conid,input_dict,response,service_name)
        
        return response
        
    def dialplan_key_maper(self,response: dict):
        """
        This will replace the key using dialplan_field_map:dict
        """
        new_response = {}
        
        for key,value in response.items():
            if key not in self.dialplan_field_map_key:
                new_response[key]=value
                continue
            new_response[self.dialplan_field_map[key]] = value
        
        return new_response

    def update_to_dialplan(self,agi, response: dict):
        """
        This will use verbose_field:List,
                      dialplan_fields:List,
                      keys in dialplan_field_map:dict
        """
        if not response:
            return

        dialplan_field = self.dialplan_field

        verbouse_field = self.verbose_field

    
        for key,values in response.items():

            if key in dialplan_field:
                agi.execute(agiapp.SetVariable(key,str(values) if values else ''))
            if key in verbouse_field:
                agi.execute(agiapp.Verbose(f'{key}:{values}'))




    def Agihandler(self, agi:AGI, args, kwargs, match, path):
        """This is the Agihandler call the Apihandler and call Agiwrok"""
        agi.execute(agiapp.SetVariable('CDR(agi_other)','1'))
        agienv = agi.get_environment()
        tid=agi.execute(agiapp.GetVariable("tid"))
        if not tid:tid = agienv['agi_uniqueid']
        src=agienv['agi_callerid']
        conid=agi.execute(agiapp.GetVariable("CONTAINERID"))
        Agiresponse = self.Agiworks(agi,tid,src,conid,args)
        self.update_to_dialplan(agi,Agiresponse)
        
        
    def Agiworks(self, agi:AGI,tid:str,src:str,conid:str,args: List[str]):
        """
        Override this function to do tasks after collecting basic data from Asterisk.

        default it will run     1. call Api and get response
                                1. cleaned_response = self.dialplan_key_maper(response)
                                2. update_to_dialplan(agi,cleaned_response) 

        response = self.Apihandler(self.Api,tid,src,conid,args)
        cleaned_response = self.dialplan_key_maper(response)
        self.update_to_dialplan(agi,cleaned_response) 
        
        """
        response = self.Apihandler(self.Api,tid,src,conid,args)
        return self.dialplan_key_maper(response)
              


    def get_log_data(
        self,
        Api: ApiProtocol,
        tid: str,
        src: str,
        conid:str,
        input_dict: dict,
        response_dict: dict,
        service_name:str=''):
        "Basic logging function"
        flag_field = Api.flag_field_key
        
        if not service_name:
            service_name = self.Name

        return {
                'api_date':self.time_fun(),
                'agi_service':service_name[:15],
                'contid':conid,'transid':tid,'src':src,
                'inputs':Api.extract_input_log(input_dict),
                'status_code':response_dict.get('status_code',None),
                'res_flag':response_dict.get(flag_field,None),
                'responses':Api.extract_response_log(response_dict),
                'ivr_flag':response_dict.get('iflag',None)}
