from dataclasses import dataclass,field
from typing import  List
from Agiserver.mod.AgiMod.AgiApiBase import (AbstractAgiApiInterface,
                                            ApiProtocol,LoggerProtocol)
from Agiserver.core import ApiModels
from Agiserver.core.Logger import LogQ
from Agiserver.core.Settings import debug 

@dataclass
class AppealDocketAgi(AbstractAgiApiInterface):
    """ This will collect the Docket details to raise Appeal against It """
    
    Name:str = 'AppealDocket'
    Api:ApiProtocol = ApiModels.Get_Appeal_docket(debug=debug)
    logger:LoggerProtocol = LogQ

    verbose_field:List = field(default_factory=lambda:['GV_Message','imsg'])
    dialplan_field_map:dict = field(default_factory=lambda:{'iflag':'IFLAG'})
    dialplan_fields:List = field(default_factory=lambda:[
                                                    'S_OBJECT_CODE0','creationDate0','resolvedDate0',
                                                    'S_OBJECT_CODE1','creationDate1','resolvedDate1',
                                                    'S_OBJECT_CODE2','creationDate2','resolvedDate2',])
    verbose_field:List = field(default_factory=lambda:['GV_Message','imsg']+[
                                                    'S_OBJECT_CODE0','creationDate0','resolvedDate0',
                                                    'S_OBJECT_CODE1','creationDate1','resolvedDate1',
                                                    'S_OBJECT_CODE2','creationDate2','resolvedDate2',])
    response_field:List = field(init=False)
    debug: bool=debug


@dataclass
class AppealAgi(AbstractAgiApiInterface):
    """ take "IV_PHONENUMBER","S_OBJECT_CODE","CLI" as input and book appeal on the docket(S_OBJECT_CODE)"""
    
    Name:str = 'Appeal'
    Api:ApiProtocol = ApiModels.BookAppeal(debug=debug) 
    logger:LoggerProtocol = LogQ

    verbose_field:List = field(default_factory=lambda:['GV_Message','imsg'])
    dialplan_field_map:dict = field(default_factory=lambda:{
                                        'A_OBJECT_CODE':'APPNO','iflag':'IFLAG'})
    response_field:List = field(init=False)
    debug: bool=debug
