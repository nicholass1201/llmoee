from fastapi import APIRouter
import uvicorn
from fastapi import FastAPI, Depends, Path, HTTPException
import json # 참고: https://blog.naver.com/sp_sosa/222841775690
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sqlalchemy import *   # insert, update, delete statements
from oeeCbMgr.oee_db_conn import EngineConn
from fastapi.encoders import jsonable_encoder

from oee_sys_admin_models import Company
import oee_company_schema
import oee_company_biz

app = FastAPI()
engine = EngineConn()
#session  = engine.sessionmaker()

router = APIRouter(
    prefix = "/oee/v1"
)

@router.post("/company/list" , response_model=oee_company_schema.CompanyList)
def company_list(param : oee_company_schema.CompanySrchParam):
    print("====================sysAcAdmin company_list start==========")
    total_cnt=0
    
    total_cnt, _company_list = oee_company_biz.get_company_list(param)    

    print("company company_list total_cnt: " , total_cnt)    
    api = "sysAcAdmin.company.company_list"
    status="ok"
    error_message="0"
    # print("====================mngAc_app intent_list _intent_list: " , _intent_list)    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt,
        'company_list': _company_list        
    }

@router.post("/company/insert")
async def company_insert(param : oee_company_schema.Company_schema):
    print("app_sqlalchemy_query_company company_insert start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    oee_company_schema.CompanySrchParam.company_id=param.company_id
    oee_company_schema.CompanySrchParam.company_name=""    
    oee_company_schema.CompanySrchParam.page_num = "1" ;         
    oee_company_schema.CompanySrchParam.count_per_page = "10" ;                     
    oee_company_schema.CompanySrchParam.order_type = "asc" ;      
 
    companySearch= oee_company_schema.CompanySrchParam
    total_cnt=0
    total_cnt, _company_list = oee_company_biz.get_company_list(companySearch)    
    print("_company_list len: " , len(_company_list))

    if (len(_company_list)>0 ) : 
        print("_company_list len>0: " , len(_company_list))     
        api = "sysAcAdmin.company.insert"
        status="error"
        error_message="동일한 company_id가 이미 등록되어 있습니다."
        total_cnt=0

    else:
        session  = engine.sessionmaker()    
        stmt = insert(Company).values(company_id=param.company_id,
                company_name=param.company_name, 
                summary_svc_yn=param.summary_svc_yn,
                ac_svc_yn=param.ac_svc_yn,
                callbot_svc_yn=param.ac_svc_yn,
                summary_llm_type_cd=param.summary_llm_type_cd,                                     
                ac_llm_type_cd=param.ac_llm_type_cd,
                callbot_llm_type_cd=param.callbot_llm_type_cd,                
                summary_llm_nm_cd=param.summary_llm_nm_cd,
                ac_llm_nm_cd=param.ac_llm_nm_cd,
                callbot_llm_nm_cd=param.callbot_llm_nm_cd,                
                rag_db_type_cd=param.rag_db_type_cd,
                default_dir_path=param.default_dir_path,                        
                seat_cnt=param.seat_cnt,             
                create_id=param.create_id,            
                )
        v_result=session.execute(stmt)
        print("/company/insert: " , v_result)

        session.commit()
        session.flush()    
        session.close()

        api = "sysAcAdmin.company.insert"
        status="ok"
        error_message="0"
        total_cnt=1


    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/company/delete")
async def company_delete(param : oee_company_schema.Company_schema):
    print("app_sqlalchemy_query_company company delete start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    session  = engine.sessionmaker()    
    stmt =  delete(Company).where(Company.company_id==param.company_id) 
    v_result=session.execute(stmt)
    print("/company/delete: " , v_result)
    api = "sysAcAdmin.company.delete"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.flush()        
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }


@router.post("/company/update")
async def company_delete(param : oee_company_schema.Company_schema):
    print("app_sqlalchemy_query_company company update start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    session  = engine.sessionmaker()    
    stmt =  update(Company).where(Company.company_id==param.company_id).values(company_name=param.company_name, 
                  summary_svc_yn=param.summary_sc_yn,
                  ac_svc_yn=param.ac_svc_yn,
                  callbot_svc_yn=param.ac_svc_yn,                  
                  summary_llm_type_cd=param.summary_llm_type_cd,                                     
                  ac_llm_type_cd=param.ac_llm_type_cd,
                  callbot_llm_type_cd=param.callbot_llm_type_cd,                  
                  summary_llm_nm_cd=param.summary_llm_nm_cd,
                  ac_llm_nm_cd=param.ac_llm_nm_cd,
                  callbot_llm_nm_cd=param.callbot_llm_nm_cd,                  
                  rag_db_type_cd=param.rag_db_type_cd,
                  default_dir_path=param.default_dir_path,                        
                  seat_cnt=param.seat_cnt            
            ) 
    v_result=session.execute(stmt)
    print("/company/update: " , v_result)
    api = "sysAcAdmin.company.update"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.flush()        
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

if __name__ == '__main__':
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=8003) 