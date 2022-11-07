from Agiserver.mod.ApiMod.ApiBase import ApiConfigBase
from dataclasses import dataclass,field
from Agiserver.core.ConfigModels import (urls,IVRS_FLAG)
from typing import List



@dataclass
class ChdNoApi(ApiConfigBase):
    """
    args order ['OLD_NO']
    
    """
    url :str = urls.changed
    input_keys:List=field(default_factory=lambda:['OLD_NO'])
    flag_field_key: str = 'NEW_NO'
    log_inputs_keys:List = field(default_factory=lambda:["OLD_NO"])

    def clean_response(self, response: dict) -> dict:
        if response.get('NEW_NO','NA')=='NA':response['NEW_NO']=''
        return response
        

@dataclass
class CheckVip(ApiConfigBase):
    """
    args order ['LV_PHONE_NO']
    """
    url :str = urls.vip
    input_keys:List=field(default_factory=lambda:['LV_PHONE_NO'])
    flag_field_key: str = 'VIP_FLAG'
    log_inputs_keys:List = field(default_factory=lambda:["LV_PHONE_NO"])  
    def clean_response(self, response: dict) -> dict:
        response['VIP_FLAG'] = 'VIP' if response.get('VIP_FLAG','N')=='Y' else 'NVP'
        return response

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
    log_inputs_keys:List = field(default_factory=lambda:[
                                'IV_PHONENUMBER',
                                'IV_ServiceCode',
                                'IV_ComplaintCode'
                                ])
    log_response_keys:List = field(default_factory=lambda:['S_OBJECT_ID'])
    flag_map_dict: dict = field(default_factory=lambda:{
        '0':IVRS_FLAG.NEW_TICKET_CREATED,
        '1':IVRS_FLAG.TICKET_ALREADY_EXIST,
        '6':IVRS_FLAG.SUSPENDED_NUMBER,
        '7':IVRS_FLAG.INVALID_NUMBER,
        '8':IVRS_FLAG.INVALID_NUMBER,
        '3':IVRS_FLAG.INVALID_NUMBER,
        '2':IVRS_FLAG.INVALID_NUMBER,
        '9':IVRS_FLAG.INVALID_NUMBER,
        '4':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '5':IVRS_FLAG.OTHER_TECHNICAL_ISSUE
        })

@dataclass
class Get_Appeal_docket(ApiConfigBase):
    """
    input order "IV_PHONENUMBER","ORDERSTATE"
    """
    name: str ='get_app_dock'
    url: str  =   urls.appeal
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["IV_PHONENUMBER","ORDERSTATE"])
    flag_field_key: str = 'A_FLAG'
    log_inputs_keys:List = field(default_factory=lambda:[
                                "IV_PHONENUMBER",
                                "ORDERSTATE"
                                ])
    log_response_keys:List = field(default_factory=lambda:[
                                                            'S_OBJECT_CODE0',
                                                            'S_OBJECT_CODE1',
                                                            'S_OBJECT_CODE2'
                                                            ])    
    flag_map_dict: dict = field(default_factory=lambda:{
        '9':IVRS_FLAG.SUCCESS,
        '6':IVRS_FLAG.API_INPUT_ERROR,
        '4':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '5':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '10':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '7':IVRS_FLAG.TARGET_NOT_FOUND
        })

    def clean_response(self, response: dict) -> dict:

        S_OBJECT_CODE = response.pop('S_OBJECT_CODE',{})

        if S_OBJECT_CODE is None or S_OBJECT_CODE==[None]:return response

        for i in range(len(S_OBJECT_CODE)):
            response.update({
                f"S_OBJECT_CODE{i}":S_OBJECT_CODE[i]['S_OBJECT_CODE'],
                f"creationDate{i}":S_OBJECT_CODE[i]['creationDate'],
                f"resolvedDate{i}":S_OBJECT_CODE[i]['resolvedDate'],
            })
        return response

@dataclass
class BookAppeal(ApiConfigBase):
    """
    input order "IV_PHONENUMBER","S_OBJECT_CODE","CLI"
    Response : 
    """
    name: str ='book_appeal'
    url: str  =   urls.appeal
    method: str ='post'
    input_keys: List = field(default_factory=lambda:["IV_PHONENUMBER","S_OBJECT_CODE","CLI"])
    default_input: dict = field(default_factory=lambda:{"ORDERSTATE" : ""})
    flag_field_key: str =  'A_FLAG'
    log_inputs_keys:List = field(default_factory=lambda:[
                                "IV_PHONENUMBER",
                                "S_OBJECT_CODE",
                                "CLI"
                                ])
        
    log_response_keys:List = field(default_factory=lambda:['A_OBJECT_CODE'])
    flag_map_dict: dict = field(default_factory=lambda:{
        '0':IVRS_FLAG.NEW_TICKET_CREATED,
        '2':IVRS_FLAG.TICKET_ALREADY_EXIST,
        '4':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '1':IVRS_FLAG.TARGET_NOT_FOUND,
        '8':IVRS_FLAG.TARGET_NOT_FOUND,
        '3':IVRS_FLAG.SHORT_DURATION_LIMITS,
        '7':IVRS_FLAG.LONG_DURATION_LIMITS,
        '5':IVRS_FLAG.UNKNOWN_CUSTOMER,
        '10':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '6':IVRS_FLAG.OTHER_TECHNICAL_ISSUE,
        '11':IVRS_FLAG.SUSPENDED_NUMBER
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
    log_inputs_keys:List = field(default_factory=lambda:["ServiceNumber"])
    log_response_keys:List = field(default_factory=lambda:['AcctNbr'])    
    flag_map_dict: dict = field(default_factory=lambda:{
        '200':IVRS_FLAG.SUCCESS,
        '400':IVRS_FLAG.INVALID_NUMBER,
        'default':IVRS_FLAG.FAILURE
        })

    def clean_response(self, response: dict) -> dict:
        """clean amount :-> remove every ',' in ther amount"""
        ## clean amount :-> remove every ',' in ther amount
        Alter_fields = ["Amount1","Amount2","Amount3","UnbilledAmount","BilledAmount"]

        for k in Alter_fields:
            amt = response.pop(k,'0')
            response[k] = amt.replace(',','') if not amt is None else None

        return response

