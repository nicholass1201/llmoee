import datetime
from fastapi import FastAPI, Form
from pydantic import BaseModel, validator
from typing import Optional
from typing import List

class commonSearchParam(BaseModel):
    page_num:Optional[str ] = None
    count_per_page:Optional[str ] = None
    order_type:Optional[str ] = None    

class ProjectRagDocBaseParam(BaseModel) : 
    project_rag_doc_id:Optional[str ] = None
    company_id:str
    project_id:int
    doc_type_cd:Optional[str ] = None
    src_file_name:Optional[str ] = None    

class ProjectRagDoc_schema(BaseModel) : 
    project_rag_doc_id: Optional[int ] = None   
    company_id:Optional[str ] = None
    project_id:Optional[int ] = None
    doc_type_cd:Optional[str ] = None
    src_url_addr: Optional[str ] = None
    src_file_name: Optional[str ] = None    
    src_real_file_name: Optional[str ] = None        
    applying_yn:Optional[str ] = None     
    last_applying_dt: Optional[datetime.datetime ] = None
    order_sn:Optional[int ] = None
    create_id:Optional[str ] = None 
    modify_id:Optional[str ] = None    

class ProjectRagDoc_form(BaseModel) : 
    company_id:str
    project_id:int
    doc_type_cd:str    
    applying_yn:str        
    create_id:str    
    
    @classmethod    
    def as_form(
        cls,
        company_id:str = Form(...),
        project_id:str = Form(...),
        doc_type_cd:str = Form(...),        
        applying_yn:str = Form(...),                
        create_id:str = Form(...),        
    ): 
        return cls(  company_id=company_id, project_id=project_id, doc_type_cd=doc_type_cd, applying_yn=applying_yn,create_id=create_id)

class ProjectRagDocSrchParam(ProjectRagDocBaseParam):
    page_num:Optional[str ] = None
    count_per_page:Optional[str ] = None
    order_type:Optional[str ] = None    


class ProjectRagDocUrlParam(BaseModel) : 
    company_id:Optional[str ] = None
    project_id:Optional[int ] = None
    doc_type_cd:Optional[str ] = None    #  01: FILE, 02: WEB, 03: KMS텍스트 05: KMS연계(FILE), 06: KMS연계(WEB)
    project_rag_doc_list: List[ProjectRagDoc_schema] = []

# Project Document List
class ProjectRagDocList(BaseModel) : 
    api  : str = ""
    status : str = ""
    error_code : str = ""
    error_message : str = ""
    total_count : int = 0 
    proj_doc_list: List[ProjectRagDoc_schema] = []

    class Config:
        orm_mode = True
   
