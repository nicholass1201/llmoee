from sqlalchemy import Column, Integer, String, Text, DateTime
# from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# oee_project table 
#  must match Project_schema 
class Project(Base):
    print("===================chatbot_models project class====")
    __tablename__ = "oee_project"
 
    project_id = Column(Integer, primary_key=True)
    company_id = Column(String, nullable=False)
    project_code = Column(String, nullable=False)    
    project_name = Column(String, nullable=True)
    project_detail = Column(Text, nullable=True)
    bot_type_cd   = Column(String, nullable=True)         
    project_type_cd   = Column(String, nullable=True)
    llm_type_cd   = Column(String, nullable=True)
    llm_nm_cd   = Column(String, nullable=True)        
    src_type_cd   = Column(String, nullable=True)
    src_file_path   = Column(String, nullable=True)
    answer_image_path   = Column(String, nullable=True)         
    in_service_yn   = Column(String, nullable=True)             
    service_start_dt   = Column(String, nullable=True)         
    service_expire_dt   = Column(String, nullable=True)             
    order_sn   = Column(Integer, nullable=True)
    order_field_cd_project   = Column(String, nullable=True)
    order_field_cd_project_atch_doc   = Column(String, nullable=True)
    order_field_cd_category   = Column(String, nullable=True)
    order_field_cd_intent   = Column(String, nullable=True)
    del_yn   = Column(String, nullable=True)
    create_id   = Column(String, nullable=False)
    create_dt   = Column(DateTime, nullable=False)
    modify_id   = Column(String, nullable=True)
    modify_dt   = Column(DateTime, nullable=True)
    delete_id   = Column(String, nullable=True)
    delete_dt   = Column(DateTime, nullable=True)

class Project_rag_doc(Base):
    print("==========chatbot_models Proj_atch_doc class===============")
    __tablename__ = "oee_project_rag_doc"
    project_rag_doc_id = Column(Integer, primary_key=True)    
    company_id = Column(String, nullable=False)    
    project_id = Column(Integer, nullable=False)    
    doc_type_cd = Column(String, nullable=False)    
    src_url_addr = Column(String, nullable=True)    
    src_file_name = Column(String, nullable=True)    
    src_real_file_name = Column(String, nullable=True)        
    applying_yn = Column(String, nullable=False)    
    last_applying_dt = Column(DateTime, nullable=True)    
    order_sn = Column(Integer, nullable=False)    
    create_id = Column(String, nullable=False)        
    create_dt = Column(String, nullable=False)    
    modify_id = Column(String, nullable=True)    
    modify_dt = Column(String, nullable=True)    


class Proj_atch_doc_file(Base):
    print("==========chatbot_models Proj_atch_doc_file class===============")
    __tablename__ = "oee_project_atch_doc_file"
    proj_doc_file_id = Column(Integer, primary_key=True)        
    proj_doc_id = Column(Integer, nullable=False)    
    company_id = Column(String, nullable=False)    
    project_id = Column(Integer, nullable=False)    
    original_file_name = Column(String, nullable=False)        
    real_file_name = Column(String, nullable=False)                
    create_id = Column(String, nullable=True)        
    create_dt = Column(String, nullable=True)    
    modify_id = Column(String, nullable=True)    
    modify_dt = Column(String, nullable=True)    

class Category(Base):
    print("chatbot_models oee_category class")
    __tablename__ = "oee_category"     
    
    category_id = Column(Integer, primary_key=True)    
    company_id = Column(String, nullable=False)    
    project_id = Column(Integer, nullable=False)    
    category_name = Column(String, nullable=False)  
    parent_category_id = Column(Integer, nullable=True)          
    #parent_category_name = Column(String, nullable=False)      
    category_level = Column(Integer, nullable=False)          
    leaf_level_yn = Column(String, nullable=False)    
    order_sn = Column(Integer, nullable=True)          
    create_id = Column(String, nullable=False)        
    create_dt = Column(String, nullable=False)    
    modify_id = Column(String, nullable=True)    
    modify_dt = Column(String, nullable=True)   


class Intent(Base):
    print("========== chatbot_models oee_intent class")
    __tablename__ = "oee_intent"     
    
    intent_id = Column(Integer, primary_key=True)  
    company_id = Column(String, nullable=False)          
    project_id = Column(Integer, nullable=False)    
    category1_name = Column(String, nullable=False)          
    category2_name = Column(String, nullable=False)          
    category3_name = Column(String, nullable=False)                  
    intent_name = Column(String, nullable=False)  
    order_sn = Column(Integer, nullable=True)          
    intent_type_cd = Column(String, nullable=False)        
    parent_msg_mgnt_code = Column(String, nullable=True)          
    intent_level = Column(Integer, nullable=False)          
    in_service_yn = Column(String, nullable=False)        
    required_entity_names = Column(String, nullable=False)        
    exclusive_entity_names = Column(String, nullable=False)        
    querys = Column(String, nullable=False)        
    answer_type_cd = Column(String, nullable=False)        
    answer_texts = Column(String, nullable=False)        
    answer_image_file_names = Column(String, nullable=False)        
    msg_mgnt_code = Column(String, nullable=False)        
    following_action_yn = Column(String, nullable=False)        
    re_query_msg_mgnt_code = Column(String, nullable=False)        
    create_id = Column(String, nullable=False)        
    create_dt = Column(String, nullable=False)    
    modify_id = Column(String, nullable=True)    
    modify_dt = Column(String, nullable=True)       