import datetime

from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class commonSearchParam(BaseModel):
    page_num:str
    count_per_page:str
    order_type:str    

class CategoryBaseParam(BaseModel) : 
    category_id:Optional[str ] = None
    company_id:str
    project_id:str
    category_name:str
    parent_category_id: Optional[str ] = None    
    # parent_category_name: Optional[str ] = None        


class Category_schema(BaseModel) : 
    category_id: Optional[int ] = None    
    company_id:Optional[str ] = None  
    project_id:Optional[int ] = None  
    category_name:Optional[str ] = None  
    parent_category_id: Optional[int ] = None
    before_category_name: Optional[str ] = None        
    category_level:Optional[int ] = None      
    leaf_level_yn:Optional[str ] = None  
    order_sn: Optional[int ] = None
    create_id:Optional[str ] = None    
    modify_id:Optional[str ] = None    


class CategorySrchParam(CategoryBaseParam):
    page_num:str
    count_per_page:str
    order_type:str    
    #project_name:str

# 프로젝트 문서 리스트
class CategoryList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    category_list: List[Category_schema] = []

    class Config:
        orm_mode = True