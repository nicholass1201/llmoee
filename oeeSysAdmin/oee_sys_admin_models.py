from sqlalchemy import Column, Integer, String, Text, DateTime
# from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# ac_project 테이블 
#  Project_schema와 일치해야 함. 
class Company(Base):
    print("===================chatbot_models project class====")
    __tablename__ = "oee_company"
 
    company_id = Column(String, primary_key=True)
    company_name = Column(String, nullable=False)
    summary_svc_yn   = Column(String, nullable=True)
    ac_svc_yn   = Column(String, nullable=True)
    callbot_svc_yn   = Column(String, nullable=True)    
    summary_llm_type_cd   = Column(String, nullable=True)
    ac_llm_type_cd   = Column(String, nullable=True)
    callbot_llm_type_cd   = Column(String, nullable=True)    
    summary_llm_nm_cd   = Column(String, nullable=True)
    ac_llm_nm_cd   = Column(String, nullable=True)
    callbot_llm_nm_cd   = Column(String, nullable=True)    
    rag_db_type_cd   = Column(String, nullable=True)
    default_dir_path   = Column(String, nullable=True)        
    seat_cnt = Column(Integer, nullable=True)

    create_id   = Column(String, nullable=True)
    create_ip   = Column(String, nullable=True)    
    create_dt   = Column(DateTime, nullable=True)
    modify_id   = Column(String, nullable=True)
    modify_ip   = Column(String, nullable=True)    
    modify_dt   = Column(DateTime, nullable=True)
 