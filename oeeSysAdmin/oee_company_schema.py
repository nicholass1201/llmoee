# project 관리
import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class CompanyMainBaseParam(BaseModel) : 
    company_id:Optional[str ] = None
    company_name:Optional[str ] = None   


class CompanyMain_schema(BaseModel) : 
    company_id:str    
    response_texts:str

class answer_schema(BaseModel) : 
    pass


class CompanySrchParam(CompanyMainBaseParam):  # pass 참조: https://velog.io/@kjh03160/Request-Body-POST-PUT
    page_num:str
    count_per_page:str
    order_type:str        

class Company_schema(BaseModel) : 
    company_id:str
    company_name:Optional[str ] = None    
    summary_svc_yn:Optional[str ] = None        
    ac_svc_yn:Optional[str ] = None        
    callbot_svc_yn:Optional[str ] = None            
    summary_llm_type_cd:Optional[str ] = None        
    ac_llm_type_cd:Optional[str ] = None                    
    callbot_llm_type_cd:Optional[str ] = None                        
    summary_llm_nm_cd:Optional[str ] = None                    
    ac_llm_nm_cd:Optional[str ] = None                    
    callbot_llm_nm_cd:Optional[str ] = None                        
    rag_db_type_cd:Optional[str ] = None                                
    default_dir_path:Optional[str ] = None                
    seat_cnt:Optional[int ] = None

    create_id:Optional[str ] = None
    create_ip:Optional[str ] = None
    modify_id:Optional[str ] = None
    modify_ip:Optional[str ] = None


class CompanyList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    company_list: List[Company_schema] = []


    class Config:
        orm_mode = False