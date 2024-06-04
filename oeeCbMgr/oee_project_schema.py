import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class commonSearchParam(BaseModel):
    page_num:str
    count_per_page:str
    order_type:str    

class ProjectBaseParam(BaseModel) : 
    company_id:str
    project_id:Optional[str ] = None
    project_name:Optional[str ] = None 
    bot_type_cd:Optional[str ] = None 
    project_type_cd:Optional[str ] = None 
    src_type_cd:Optional[str ] = None 
    in_service_yn:Optional[str ] = None 

class Project_schema(BaseModel) : 
    company_id:str
    project_id: Optional[int ] = None
    project_code:Optional[str ] = None
    project_name:Optional[str ] = None
    bot_type_cd:Optional[str ] = None
    project_type_cd:Optional[str ] = None
    llm_type_cd:Optional[str ] = None
    llm_nm_cd:Optional[str ] = None           
    src_type_cd:Optional[str ] = None
    in_service_yn: Optional[str ] = None
    project_detail:Optional[str ] = None
    src_file_path: Optional[str ] = None
    # src_file_path: str   # 필수아닌데 Optional로 설정 않하면 에러발생 
        # astapi.exceptions.ResponseValidationError: 1 validation errors:
          #  {'type': 'string_type', 'loc': ('response', 'project_list', 0, 'src_file_path'), 'msg': 'Input should be a valid string', 'input': None, 'url': 'https://errors.pydantic.dev/2.4/v/string_type'}

    service_start_dt:  Optional[datetime.datetime ] = None
    service_expire_dt: Optional[datetime.datetime ] = None 
    del_yn: Optional[str ] = None
    create_id:Optional[str ] = None
    modify_id:Optional[str ] = None        

class ProjectSearchParam(ProjectBaseParam):
    page_num:str
    count_per_page:str
    order_type:str    
    #project_name:str

# 프로젝트 리스트
# 참조 : https://github.com/pahkey/fastapi-book/blob/master/domain/question/question_schema.py
class ProjectList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    project_list: List[Project_schema] = []

    class Config:
        orm_mode = True

