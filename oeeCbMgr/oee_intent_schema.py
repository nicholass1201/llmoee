import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class commonSearchParam(BaseModel):
    page_num:str
    count_per_page:str
    order_type:str

class IntentBaseParam(BaseModel) : 
    intent_id:Optional[str ] = None
    company_id:str
    project_id:str
    intent_name:str
    required_entity_names: Optional[str ] = None 
    exclusive_entity_names:Optional[str ] = None         
    category1_name:str
    category2_name:str
    category3_name:str            


class Intent_schema(BaseModel) : 
    intent_id:Optional[int ] = None
    project_id:str
    company_id:str    
    category1_name:Optional[str ] = None
    category2_name:Optional[str ] = None
    category3_name:Optional[str ] = None
    intent_name:Optional[str ] = None  
    order_sn:Optional[int ] = None
    intent_type_cd:Optional[str ] = None  
    parent_msg_mgnt_code:Optional[str ] = None  
    intent_level:Optional[int ] = None
    in_service_yn:Optional[str ] = None  
    required_entity_names:Optional[str ] = None  
    exclusive_entity_names:Optional[str ] = None  
    querys:Optional[str ] = None  
    answer_type_cd:Optional[int ] = None  
    answer_texts:Optional[str ] = None  
    answer_image_file_names:Optional[str ] = None  
    msg_mgnt_code:Optional[str ] = None  
    following_action_yn:Optional[str ] = None  
    re_query_msg_mgnt_code:Optional[str ] = None  
    create_id:Optional[str ] = None    
    modify_id:Optional[str ] = None     

    
class IntentSrchParam(IntentBaseParam):
    page_num:str
    count_per_page:str
    order_type:str    
    #project_name:str

# 프로젝트 문서 리스트
class IntentList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    intent_list: List[Intent_schema] = []

    class Config:
        orm_mode = False