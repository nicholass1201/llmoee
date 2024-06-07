# project 관리
import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class SummaryMainBaseParam(BaseModel) : 
    company_id:str
    original_text:str

class SummaryMain_schema(BaseModel) : 
    company_id:str    
    response_texts:str

class answer_schema(BaseModel) : 
    pass


class SummaryMainSrchParam(SummaryMainBaseParam):  # pass 참조: https://velog.io/@kjh03160/Request-Body-POST-PUT
    pass
    #page_num:str
    #count_per_page:str
    #order_type:str        

 

    class Config:
        orm_mode = False