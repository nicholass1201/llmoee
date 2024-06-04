from fastapi import FastAPI, UploadFile, File, Form, Depends, Request
from pydantic import BaseModel
from oee_db_conn import EngineConn

from sqlalchemy import *
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
import uvicorn

# project managment
import oee_project
from oee_chatbot_models import Project
import oee_project_schema

# project 첨부 문서 관리
import oee_project_rag_docs
from oee_chatbot_models import Project_rag_doc 
import oee_project_rag_docs_schema


# 카테고리 관리
import oee_category_biz
from oee_chatbot_models import Category
import oee_category_schema


# 인텐트 관리
import oee_intent_biz
from oee_chatbot_models import Intent
import oee_intent_schema

from oeeLlmCbMgr101 import oee_llm_cb_submgr101
from oeeLlmCbMgr102 import oee_llm_cb_submgr102
from oeeLlmCbMgr201 import oee_llm_cb_submgr201
from oeeLlmCbMgr202 import oee_llm_cb_submgr202

print("===================mngWc_app FastAPI loading1==========")
app = FastAPI()
engine = EngineConn()


router = APIRouter(
    prefix = "/wc/v1"
)

# from fastapi import UploadFile, File
import sys, os
from datetime import datetime
from typing import List
import secrets
from starlette.responses import FileResponse
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 디렉토리 생성
def makedirs(varRagDir):
    if not os.path.exists(varRagDir):
        os.makedirs(varRagDir)

# 0으로 채우기  
# i: 입력 문자열, width: 전체문자열 길이        
def lpad(i, width, fillchar='0'):
    return str(i).rjust(width, fillchar)        

@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to the Mental Health Chatbot API!"}

@router.post("/projectRagDoc/uploadUrls" )
def projectRagDoc_urlUpload(  params : oee_project_rag_docs_schema.ProjectRagDocUrlParam ):
    print("====================mngWc_app projectRagDoc_urlUpload start ==========")

    for param1 in params.project_rag_doc_list:
        print("====================mngWc_app projectRagDoc_urlUpload param1: " , param1)            
        # print("====================mngWc_app projectRagDoc_urlUpload param1.project_rag_doc_list: " , param1.project_rag_doc_list)                    
        
        oee_project_rag_docs_schema.ProjectRagDoc_schema.company_id=params.company_id
        oee_project_rag_docs_schema.ProjectRagDoc_schema.project_id=params.project_id                
        oee_project_rag_docs_schema.ProjectRagDoc_schema.src_url_addr=param1.src_url_addr                         
        oee_project_rag_docs_schema.ProjectRagDoc_schema.doc_type_cd=param1.doc_type_cd                                 
        oee_project_rag_docs_schema.ProjectRagDoc_schema.applying_yn=param1.applying_yn                                         
        oee_project_rag_docs_schema.ProjectRagDoc_schema.create_id=param1.create_id        
        param2 = oee_project_rag_docs_schema.ProjectRagDoc_schema
        print("====================mngWc_app projectRagDoc_urlUpload param2: " , param2)            
        session  = engine.sessionmaker()     
        stmt1 =  delete(Project_rag_doc).where(Project_rag_doc.project_id==param2.project_id, Project_rag_doc.src_url_addr==param2.src_url_addr) 
        v_result1=session.execute(stmt1)
        session.commit() 

        session  = engine.sessionmaker()     
        stmt2 = insert(Project_rag_doc).values(company_id=param2.company_id, project_id=param2.project_id,
                src_url_addr=param2.src_url_addr,                            
                doc_type_cd=param2.doc_type_cd,                            
                applying_yn=param2.applying_yn,                                            
                create_id=param2.create_id
                )
        v_result2=session.execute(stmt2)
        session.commit() 


    api = "mngChatBot.projectRagDoc.projectRagDoc_urlUpload"
    status="ok"
    error_message="0"
    total_cnt="0"
    print("====================mngWc_app projectRagDoc_urlUpload error_message: " , error_message)    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt
 
    }


@router.post('/projectRagDoc/uploadFiles')
async def projectRagDocUploadFiles(param1: oee_project_rag_docs_schema.ProjectRagDoc_form = Depends(oee_project_rag_docs_schema.ProjectRagDoc_form.as_form) , in_files: List[UploadFile] = File(...)):
    file_urls=[]
    for file in in_files:

        print("============== company_id: " , param1.company_id)        
        print("============== project_id: " , param1.project_id)                
        print("============== doc_type_cd: " , param1.doc_type_cd)                                
        print("============== applying_yn: " , param1.applying_yn)                                        
        print("============== BASE_DIR: " , BASE_DIR)                
        print("============== file.filename: " , file.filename)        


        varBaseDir= BASE_DIR
        varProjectCode = lpad(param1.project_id, 6, '0')        

        #varRagDir = varBaseDir + "/item38/000039"
        varRagDirRag = varBaseDir + "/ragSrcFiles/" + param1.company_id + "/" + varProjectCode 
        varRagDirDownload = varBaseDir + "/ragSrcFiles/" + param1.company_id + "/" + varProjectCode + "/download"         

       # 디렉토리 없으면 생성 
        # makedirs(varRagDirRag)
        makedirs(varRagDirDownload)        

        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        ymdSsAndHex16 = ''.join([currentTime,secrets.token_hex(16)])
        saved_file_name=ymdSsAndHex16 + "_"+ file.filename

        file_location_Rag = os.path.join(varRagDirRag,file.filename)
        with open(file_location_Rag, "wb+") as file_object_rag:
            file_object_rag.write(file.file.read())

        print("============== ymdSsAndHex16: " , ymdSsAndHex16)        
        print("============== saved_file_name: " , saved_file_name)        

        file_location_download = os.path.join(varRagDirDownload,saved_file_name)
        shutil.copyfile(file_location_Rag, file_location_download)
        #file_location_download = os.path.join(varRagDirDownload,saved_file_name)
        #with open(file_location_download, "wb+") as file_object_download:
        #    file_object_download.write(file.file.read())

        oee_project_rag_docs_schema.ProjectRagDoc_schema.company_id=param1.company_id
        oee_project_rag_docs_schema.ProjectRagDoc_schema.project_id=param1.project_id                
        oee_project_rag_docs_schema.ProjectRagDoc_schema.src_file_name=file.filename                
        oee_project_rag_docs_schema.ProjectRagDoc_schema.src_real_file_name=saved_file_name                         
        oee_project_rag_docs_schema.ProjectRagDoc_schema.doc_type_cd=param1.doc_type_cd                                 
        oee_project_rag_docs_schema.ProjectRagDoc_schema.applying_yn=param1.applying_yn                                         
        oee_project_rag_docs_schema.ProjectRagDoc_schema.create_id=param1.create_id        
        param2 = oee_project_rag_docs_schema.ProjectRagDoc_schema
        print("============== param2: " , param2)        

        session  = engine.sessionmaker()     
        stmt1 =  delete(Project_rag_doc).where(Project_rag_doc.project_id==param2.project_id, Project_rag_doc.src_file_name==param2.src_file_name) 
        v_result1=session.execute(stmt1)
        session.commit() 

        session  = engine.sessionmaker()     
        stmt2 = insert(Project_rag_doc).values(company_id=param2.company_id, project_id=param2.project_id,
                src_file_name=param2.src_file_name,                            
                src_real_file_name=param2.src_real_file_name,            
                doc_type_cd=param2.doc_type_cd,                            
                applying_yn=param2.applying_yn,                                            
                create_id=param2.create_id
                )
        v_result2=session.execute(stmt2)
        session.commit() 
        
        print("===========벡터db 폴더 생성=========== v_result2:", v_result2)       
        
 
        api = "mngChatBot.projectRagDoc.uploadFiles"
        status="ok"
        error_message="0"
        total_cnt=1


    session.close()

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

 
 

@router.post('/projectRagDoc/downloadFiles')
async def projectRagDocDownloadFiles(param1 : oee_project_rag_docs_schema.ProjectRagDocSrchParam):


    print("============== BASE_DIR: " , BASE_DIR)    

  
    param1.page_num = "1" ;         
    param1.count_per_page = "10" ;                     
    param1.order_type = "asc" ;      
    print("mngWc_app projectRagDocDownloadFiles param1: " , param1)    

    total_cnt, _projectRagDoc_list = projectRagDoc_biz.get_projectRagDoc_list(param1)    
    print("mngWc_app projectRagDocDownloadFiles total_cnt: " , total_cnt)    
    print("mngWc_app projectRagDocDownloadFiles _projectRagDoc_list: " , _projectRagDoc_list)        

    varBaseDir= BASE_DIR    
    varProjectCode = lpad(param1.project_id, 6, '0')            
    varRagDir = varBaseDir + "/ragSrcFiles/" + param1.company_id + "/" + varProjectCode + "/download/" 
        # varRagDirDownload = varBaseDir + "/ragSrcFiles/" + param1.company_id + "/" + varProjectCode + "/download"         
    print("mngWc_app projectRagDocDownloadFiles varRagDir: " , varRagDir)        
    
    targetFile=""
    filename=""    

    for row in _projectRagDoc_list:
        filename = row.src_real_file_name

        targetFile = varRagDir + filename
        print("===================== biz filename: ", filename)   
        print("===================== biz targetFile: ", targetFile)           
 
    

    return FileResponse(targetFile, media_type='application/octet-stream',filename=filename)


 

@router.post("/project/list" , response_model=oee_project_schema.ProjectList)
def project_list(param : oee_project_schema.ProjectSearchParam):
    print("===================mngWc_app project_list start==========")
    total_cnt, _project_list = project_biz.get_project_list(param)    
    print("mngWc_app project_list total_cnt: " , total_cnt)    
    print("mngWc_app project_list _project_list: " , _project_list)        

    for row in _project_list:
        print("========_project_list.project_id: ", row.project_id)        
        print("========_project_list.company_id: ", row.company_id)
        print("========_project_list.project_name: ", row.project_name)
        print("========_project_list.llm_type_cd: ", row.llm_type_cd)        
        print("========_project_list.llm_nm_cd: ", row.llm_nm_cd)        
        print("========_project_list.delete_dt: ", row.delete_dt)                


    api = "mngChatBot.project.project_list"
    status="ok"
    error_message="0"
    print("===================mngWc_app project_list error_message: " , error_message)    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt ,
        'project_list': _project_list
    }
        
@router.post("/project/insert")
async def project_insert(param : oee_project_schema.Project_schema):
    print("app_sqlalchemy_query_project project_insert start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    oee_project_schema.ProjectSearchParam.project_name=param.project_name
    oee_project_schema.ProjectSearchParam.project_id=""
    oee_project_schema.ProjectSearchParam.in_service_yn=""
    oee_project_schema.ProjectSearchParam.company_id=param.company_id    
    oee_project_schema.ProjectSearchParam.page_num = "1" ;         
    oee_project_schema.ProjectSearchParam.count_per_page = "10" ;                     
    oee_project_schema.ProjectSearchParam.order_type = "asc" ;      

    projectSearch= oee_project_schema.ProjectSearchParam

    total_cnt, _project_list = project_biz.get_project_list(projectSearch)    
    print("_company_list len: " , len(_project_list))

    if (len(_project_list)>0 ) : 
        print("_project_list len>0: " , len(_project_list))     
        api = "mngChatBot.project.insert"
        status="error"
        error_message="동일한 project_nm이 이미 등록되어 있습니다."
        total_cnt=0

    else:
        session  = engine.sessionmaker()    
        sProject_code="000000"
        stmt = insert(Project).values(company_id=param.company_id,
                project_code=sProject_code,
                project_name=param.project_name, project_detail=param.project_detail,    
                bot_type_cd=param.bot_type_cd, 
                project_type_cd=param.project_type_cd,
                llm_type_cd=param.llm_type_cd,
                llm_nm_cd=param.llm_nm_cd,                        
                src_type_cd=param.src_type_cd,
                src_file_path=param.src_file_path,
                in_service_yn=param.in_service_yn,            
                service_start_dt=param.service_start_dt,
                service_expire_dt=param.service_expire_dt,                        
                del_yn= 'N',
                create_id=param.create_id,            
                )
        v_result=session.execute(stmt)
        print("/project/insert: " , v_result)    
        print("/project/insert.lastrowid: " , v_result.lastrowid)
        session.commit()
        session.close()
        
        api = "mngChatBot.project.insert"
        status="ok"
        error_message="0"
        total_cnt=1

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }


@router.post("/project/modify")
async def project_modify(param : oee_project_schema.Project_schema):
    print("app_sqlalchemy_query_project project_modify start==========")
    print("===================mngWc_app project_list start==========")
    #total_cnt, _project_list = project_biz.get_project_list(param)    

    #for row in _project_list :
    #    print ( row.project_id, row.company_id, row.project_name)

    print("===================mngWc_app param.project_id: " , param.project_id)    
    print("===================mngWc_app param.project_name: " , param.project_name)    
    print("===================mngWc_app param.project_detail: " , param.project_detail)            
    session  = engine.sessionmaker()    
    stmt = update(Project).where(Project.project_id==param.project_id).values(project_name=param.project_name, project_detail=param.project_detail,
            bot_type_cd=param.bot_type_cd, 
            project_type_cd=param.project_type_cd,
            src_type_cd=param.src_type_cd,
            src_file_path=param.src_file_path,
            service_start_dt=param.service_start_dt,
            service_expire_dt=param.service_expire_dt,                        
            )
    # stmt = update(Project).where(Project.project_id==1).values(project_name="project1 - updated2", project_detail="detail 2222")
    v_result=session.execute(stmt)
    print("/project/modify: " , v_result)
    session.commit()
    session.close()

    api = "mngChatBot.project.modify"
    status="ok"
    error_message="0"
    total_cnt=1
    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/project/delete")
async def project_delete(param : oee_project_schema.Project_schema):
    print("app_sqlalchemy_query_company project delete start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    session  = engine.sessionmaker()    
    stmt =  delete(Project).where(Project.project_id==param.project_id) 
    v_result=session.execute(stmt)
    print("/project/delete: " , v_result)
    api = "mngChatBot.project.delete"
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

 

@router.post("/project/applyingInServiceYn")
async def project_applyingInServiceYn(param : oee_project_schema.Project_schema):
    print("app_sqlalchemy_query_project project_applyingInServiceYn start==========")
    print("===================mngWc_app project_applyingInServiceYn start==========")
    #total_cnt, _project_list = project_biz.get_project_list(param)    

    #for row in _project_list :
    #    print ( row.project_id, row.company_id, row.project_name)

    print("===================mngWc_app param.project_id: " , param.project_id)    
    print("===================mngWc_app param.in_service_yn: " , param.in_service_yn)    

    session  = engine.sessionmaker()    
    stmt = update(Project).where(Project.project_id==param.project_id).values(
            in_service_yn=param.in_service_yn,
            modify_id=param.modify_id            

            )
    # stmt = update(Project).where(Project.project_id==1).values(project_name="project1 - updated2", project_detail="detail 2222")
    v_result=session.execute(stmt)
    print("/project/applyingInServiceYn: " , v_result)
    session.commit()
    session.close()

    api = "mngChatBot.project.applyingInServiceYn"
    status="ok"
    error_message="0"
    total_cnt=1
    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }


@router.post("/projectRagDoc/list" , response_model=oee_project_rag_docs_schema.ProjectRagDocList)
def projectRagDoc_list(param : oee_project_rag_docs_schema.ProjectRagDocSrchParam):
    print("====================mngWc_app projectRagDoc_list start ==========")
    total_cnt, _projectRagDoc_list = projectRagDoc_biz.get_projectRagDoc_list(param)    
    print("mngWc_app projectRagDoc_list total_cnt: " , total_cnt)    
    print("mngWc_app projectRagDoc_list _projectRagDoc_list: " , _projectRagDoc_list)        
    api = "mngChatBot.projectRagDoc.projectRagDoc_list"
    status="ok"
    error_message="0"
    print("====================mngWc_app projectRagDoc_list error_message: " , error_message)    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt,
        'proj_doc_list': _projectRagDoc_list
    }

 


@router.post("/projectRagDoc/delete")
async def projectRagDoc_delete(param : oee_project_rag_docs_schema.ProjectRagDoc_schema):
    print("app_sqlalchemy_query_project projectRagDoc_delete delete start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)   
    session  = engine.sessionmaker()     
    stmt =  delete(Project_rag_doc).where(Project_rag_doc.project_rag_doc_id==param.project_rag_doc_id) 
    v_result=session.execute(stmt)
    print("/projectRagDoc/delete: " , v_result)
    api = "mngChatBot.projectRagDoc.delete"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/projectRagDoc/storingRagDoc")
async def storingRagDoc(params : oee_project_rag_docs_schema.ProjectRagDocUrlParam ):
    print("app projectRagDoc applyingProjectRagDoc start==========")
    api = "mngChatBot.projectRagDoc.applyingProjectRagDoc"
    
    oee_project_schema.ProjectSearchParam.company_id = params.company_id    
    oee_project_schema.ProjectSearchParam.project_id = params.project_id
    oee_project_schema.ProjectSearchParam.project_name = ""    
    oee_project_schema.ProjectSearchParam.page_num = "1" ;         
    oee_project_schema.ProjectSearchParam.count_per_page = "10" ;                     
    oee_project_schema.ProjectSearchParam.order_type = "asc" ;      

    
    p_total_cnt, _project_list = project_biz.get_project_list(oee_project_schema.ProjectSearchParam)    
    print("================ applyingprojectRagDoc p_total_cnt: ", p_total_cnt)     
    print("================ applyingprojectRagDoc len : _project_list: ", len(_project_list ) )        


    for row in _project_list:
        print("========applyingprojectRagDoc _project_list.project_id: ", row.project_id)        
        print("========applyingprojectRagDoc _project_list.company_id: ", row.company_id)
        print("========applyingprojectRagDoc _project_list.llm_nm_cd: ", row.llm_nm_cd)        
        sllm_nm_cd = row.llm_nm_cd


    for paramRagDoc in params.project_rag_doc_list:
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.company_id = params.company_id 
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.project_id = params.project_id         
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.project_rag_doc_id = paramRagDoc.project_rag_doc_id                 
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.src_file_name= ""
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.page_num = "1" ;         
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.count_per_page = "10" ;                     
        oee_project_rag_docs_schema.ProjectRagDocSrchParam.order_type = "asc" ;              
        param2 = oee_project_rag_docs_schema.ProjectRagDocSrchParam
        total_cnt, _projectRagDoc_list = projectRagDoc_biz.get_projectRagDoc_list(param2)    
        print("========applyingprojectRagDoc total_cnt : ", total_cnt)                                    
        print("========applyingprojectRagDoc _projectRagDoc_list : ", _projectRagDoc_list)                            


        for resultRagDoc in _projectRagDoc_list:
            print("========resultRagDoc : ", resultRagDoc)                            
            # paramRagDoc.src_file_name = resultRagDoc
            if params.doc_type_cd!=resultRagDoc.doc_type_cd:             
                status="error"
                error_message="문서타입코드(doc_type_cd) 불일치"
                return {       
                    'api': api,        
                    'status': status,        
                    'error_message': error_message,        
                    'total_cnt': total_cnt

                }                

            paramRagDoc.src_url_addr = resultRagDoc.src_url_addr
            paramRagDoc.src_file_name = resultRagDoc.src_file_name        
            # params.project_rag_doc_list[0].src_url_addr=resultRagDoc.src_url_addr
            print("========paramRagDoc : ", paramRagDoc)                                            

        print("========applyingprojectRagDoc 수정후 params.project_rag_doc_list: ", params.project_rag_doc_list)        



    if sllm_nm_cd=="101" : 
        print("========applyingprojectRagDoc sllm_nm_cd 101 : ", sllm_nm_cd)                    
        if params.doc_type_cd=="01":     #  01: FILE, 02: WEB, 03: KMS텍스트 05: KMS연계(FILE), 06: KMS연계(WEB)
            chatSubLlmMng101_biz.storingRagDocFile(params)
        elif params.doc_type_cd=="02":    
            chatSubLlmMng101_biz.storingRagDocUrl(params)            
    elif sllm_nm_cd=="102" : 
        print("========applyingprojectRagDoc sllm_nm_cd 102 : ", sllm_nm_cd)                    
        chatSubLlmMng102_biz.storingRagDoc(params)
    elif sllm_nm_cd=="201" : 
        print("========applyingprojectRagDoc sllm_nm_cd 201 : ", sllm_nm_cd)                    
        chatSubLlmMng201_biz.biz_rag_save(params)
    elif sllm_nm_cd=="202" : 
        print("========applyingprojectRagDoc sllm_nm_cd 202 : ", sllm_nm_cd)                    
        chatSubLlmMng202_biz.biz_rag_save(params)


    session  = engine.sessionmaker()
    for param1 in params.project_rag_doc_list:
        stmt =  update(Project_rag_doc).where(Project_rag_doc.project_rag_doc_id==param1.project_rag_doc_id).values(
                applying_yn=param1.applying_yn,            
                last_applying_dt=param1.last_applying_dt
                )
        v_result=session.execute(stmt)
        print("/projectRagDoc/applyingProjectRagDoc: " , v_result)

        status="ok"
        error_message="0"
        total_cnt=1

        session.commit() 
    session.close()

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/category/list" , response_model=oee_category_schema.CategoryList)
def category_list(param : oee_category_schema.CategorySrchParam):
    print("====================mngWc_app category_list start==========")
    total_cnt, _category_list = category_biz.get_category_list(param)    
    print("mngWc_app category_list total_cnt: " , total_cnt)    
    api = "mngChatBot.mngWc.category_list"
    status="ok"
    error_message="0"
    print("====================mngWc_app category_list error_message: " , error_message)    
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt,
        'category_list': _category_list
    }
    
@router.post("/category/insert")
async def category_insert(param : oee_category_schema.Category_schema):
    print("============ mngWc_app category insert start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    session  = engine.sessionmaker()
    stmt = insert(Category).values(company_id=param.company_id, project_id=param.project_id,
            category_name=param.category_name,
            parent_category_id=int(param.parent_category_id),            
            category_level=param.category_level,            
            leaf_level_yn=param.leaf_level_yn,            
            order_sn=param.order_sn,                        
            create_id=param.create_id            
            )
    v_result=session.execute(stmt)
    print("============ mngWc_app /category/insert: " , v_result)
    api = "mngChatBot.category.insert"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/category/update")
async def category_update(param : oee_category_schema.Category_schema):
    print("============ mngWc_app category insert update==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)    
    session  = engine.sessionmaker()    
    stmt =  update(Category).where(Category.category_id==param.category_id).values(
            category_name=param.category_name,
            parent_category_id=param.parent_category_id ,           
            category_level=param.category_level ,                       
            order_sn=param.order_sn                        
            )
    v_result=session.execute(stmt)
    print("/category/update: " , v_result)
    api = "mngChatBot.category.update"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt
    }

@router.post("/category/delete")
async def category_delete(param : oee_category_schema.Category_schema):
    print("============ mngWc_app category delete==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)    
    session  = engine.sessionmaker()    

    sCategory_id = param.category_id    
    sParent_category_id = param.parent_category_id    

    if ((str(sCategory_id).strip() )!=""):    
        stmt =  delete(Category).where(Category.category_id==param.category_id) 
    elif ((str(sParent_category_id).strip() )!=""):    
        stmt =  delete(Category).where(Category.parent_category_id==param.parent_category_id)    

    v_result=session.execute(stmt)
    print("/category/delete: " , v_result)
    api = "mngChatBot.category.delete"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }


@router.post("/intent/list" , response_model=oee_intent_schema.IntentList)
def intent_list(param : oee_intent_schema.IntentSrchParam):
    print("====================mngWc_app intent_list start==========")
    session  = engine.sessionmaker()
    total_cnt, _intent_list = intent_biz.get_intent_list(param)    
    print("mngWc_app intent_list total_cnt: " , total_cnt)    
    api = "mngChatBot.mngWc.intent_list"
    status="ok"
    error_message="0"
    print("====================mngWc_app intent_list _intent_list: " , _intent_list)    

    for row in _intent_list:
        print("========_intent_list.project_id: ", row.project_id)        
        print("========_intent_list.company_id: ", row.company_id)
        print("========_intent_list.intent_id: ", row.intent_id)        

    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_count': total_cnt,
        'intent_list': _intent_list
    }


@router.post("/intent/insert")
async def intent_insert(param : oee_intent_schema.Intent_schema):
    print("============ mngWc_app intent insert start==========")
    print("============ mngWc_app intent insert param.create_id: ", param.create_id)    
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)    
    session  = engine.sessionmaker()    
    stmt = insert(Intent).values(
            company_id=param.company_id, project_id=param.project_id,
            category1_name=param.category1_name,
            category2_name=param.category2_name,
            category3_name=param.category3_name,                        
            intent_name=param.intent_name,                        
            order_sn=param.order_sn,                        
            intent_type_cd=param.intent_type_cd,                        
            parent_msg_mgnt_code=param.parent_msg_mgnt_code,                        
            intent_level=param.intent_level,                        
            in_service_yn=param.in_service_yn,                        
            required_entity_names=param.required_entity_names,                                                                                                
            exclusive_entity_names=param.exclusive_entity_names,                        
            querys=param.querys,                        
            answer_type_cd=param.answer_type_cd,   
            answer_texts=param.answer_texts,                        
            answer_image_file_names=param.answer_image_file_names,                        
            msg_mgnt_code=param.msg_mgnt_code,               
            following_action_yn=param.following_action_yn,   
            re_query_msg_mgnt_code=param.re_query_msg_mgnt_code,                        
            create_id=param.create_id                          
            )
    v_result=session.execute(stmt)
    print("============ mngWc_app /category/insert: " , v_result)
    api = "mngChatBot.category.insert"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }


@router.post("/intent/update")
async def projectRagDoc_update(param : oee_intent_schema.Intent_schema):
    print("============ mngWc_app intent insert update==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name) 
    session  = engine.sessionmaker()       
    stmt =  update(Intent).where(Intent.intent_id==param.intent_id).values(
            company_id=param.company_id, project_id=param.project_id,
            category1_name=param.category1_name,
            category2_name=param.category2_name,
            category3_name=param.category3_name,                        
            intent_name=param.intent_name,                        
            order_sn=param.order_sn,                        
            intent_type_cd=param.intent_type_cd,                        
            parent_msg_mgnt_code=param.parent_msg_mgnt_code,                        
            intent_level=param.intent_level,                        
            in_service_yn=param.in_service_yn,                        
            required_entity_names=param.required_entity_names,                                                                                                
            exclusive_entity_names=param.exclusive_entity_names,                        
            querys=param.querys,                        
            answer_type_cd=param.answer_type_cd,   
            answer_texts=param.answer_texts,                        
            answer_image_file_names=param.answer_image_file_names,                        
            msg_mgnt_code=param.msg_mgnt_code,               
            following_action_yn=param.following_action_yn,   
            re_query_msg_mgnt_code=param.re_query_msg_mgnt_code,                        
            create_id=param.create_id        
            )
    v_result=session.execute(stmt)
    print("/intent/update: " , v_result)
    api = "mngChatBot.intent.update"
    status="ok"
    error_message="0"
    total_cnt=1

    session.commit() 
    session.close()
    return {       
        'api': api,        
        'status': status,        
        'error_message': error_message,        
        'total_cnt': total_cnt

    }

@router.post("/intent/delete")
async def intent_delete(param : oee_intent_schema.Intent_schema):
    print("============ mngWc_app intent delete start==========")
    #print("project_id: " , project_id)    
    #print("project_name: " , project_name)        
    session  = engine.sessionmaker()    
    stmt =  delete(Intent).where(Intent.intent_id==param.intent_id) 
    v_result=session.execute(stmt)
    print("/intent/delete: " , v_result)
    api = "mngChatBot.intent.delete"
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
    uvicorn.run(app, host="0.0.0.0", port=8000)        