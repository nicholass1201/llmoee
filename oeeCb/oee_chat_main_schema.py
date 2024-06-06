# project 관리
import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class commonSearchParam(BaseModel):
    page_num:str
    count_per_page:str
    order_type:str    

class ChatMainBaseParam(BaseModel) : 
    company_id:str
    project_id:int
    query:str
    before_intent_id:int

class ChatMain_schema(BaseModel) : 
    company_id:str    
    project_id:int
    response_type:str
    response_texts:str
    image_file_names:str
    indent_id:str
    before_intent_id:str
    answer_mgnt_code:str    
    response_src_cd:str    # 답변 출처 코드 : 01: llm 02:. intent (히스토리 내역도 결국 히스토리에서 선택하여 인텐트 저장)                 

class answer_schema(BaseModel) : 
    answer_type:int
    answer_texts:str
    image_file_names:str
    value:str


class ChatMainSrchParam(ChatMainBaseParam):  # pass 참조: https://velog.io/@kjh03160/Request-Body-POST-PUT
    pass
    #page_num:str
    #count_per_page:str
    #order_type:str        

# 프로젝트 문서 리스트
class AnswerList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    response: ChatMain_schema
    answerList: List[answer_schema] = []

    class Config:
        orm_mode = False