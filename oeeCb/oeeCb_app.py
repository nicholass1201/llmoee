
from fastapi import APIRouter
import uvicorn
from fastapi import FastAPI, Depends, Path, HTTPException
import json # ref: https://blog.naver.com/sp_sosa/222841775690
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from oeeCbMgr.oee_db_conn import EngineConn
from oeeCbMgr import oee_project
from oeeCbMgr.oee_chatbot_models import Project
from oeeCbMgr import oee_project_schema
from fastapi.encoders import jsonable_encoder

# import chatSubRag_biz
import oee_chat_main_schema
import oee_chat_main_biz

app = FastAPI()
#engine = EngineConn()
#session  = engine.sessionmaker()

router = APIRouter(
    prefix = "/oee/v1"
)

import sys, os
from fastapi import UploadFile, File
from ast import List
import datetime

@router.post("/chat/predict" )
def chat_predict(param : oee_chat_main_schema.ChatMainSrchParam):
    print("===================oeeCb_app chat_predict start==========")
    data = {}    
    # query = "엘지유플러스의 인사제도에 대해 소개해주세요"    
    query = param.query
    company_id = param.company_id
    project_id = param.project_id    
    before_intent_id = param.before_intent_id        
    print("oeeCb_app chat_predict query: " , query)        
    print("oeeCb_app chat_predict company_id: " , company_id)        
    print("oeeCb_app chat_predict project_id: " , project_id)                
    print("oeeCb_app chat_predict before_intent_id: " , before_intent_id)                    

    response_result = oee_chat_main_biz.chatMain_predict(company_id, project_id, query=query, before_intent_id=0)    
    print("chatMain_app chat_predict response_result: " , response_result)                    
    # 하드코딩 부분 시작 ======================
    before_intent_id= 1
    answer_mgnt_code= 1
    response_type_cd    = "01"   # 응답타입: 01: 텍스트, 02: 이미지, 03: 이미지+텍스트, 04: 텍스트+이미지, 05:복합리스트, 06:사용자정의 (복합리스트의 경우 별도 테이블에 추가 정보 등록, 사용자 정의인 경우 답변관리번호로 관리 )


    company_id = response_result.ChatMain_schema.company_id
    project_id = response_result.ChatMain_schema.project_id
    intent_id = response_result.ChatMain_schema.intent_id
    response_texts = response_result.ChatMain_schema.response_texts
    response_src_cd = response_result.ChatMain_schema.response_src_cd    
    print("chatMain_app chat_predict intent_id: " , intent_id)                    

    api = "chat.chat_predict"
    status="ok"
    error_message="0"
    total_cnt=1

    data['api'] = api
    data['status'] = status
    data['error_message'] = error_message
    data['total_cnt'] = total_cnt    
    #data['response'] = []

    response_sub = {}
    response_sub['company_id'] = company_id    
    response_sub['project_id'] = project_id
    response_sub['response_type_cd'] = response_type_cd       
    response_sub['before_intent_id'] = before_intent_id   
    response_sub['response_type_cd'] = response_type_cd   
    response_sub['response_texts'] = response_texts                   
    response_sub['response_src_cd'] = response_src_cd          # 답변 출처 코드 : 01: llm 02:. intent (히스토리 내역도 결국 히스토리에서 선택하여 인텐트 저장)              
    response_sub['indent_id'] = intent_id   

    response_sub['answerList'] = []
    if (response_type_cd=="03") : 
        answer_type="01"
        answer_texts="복합답변입니다."        

        response_sub['answerList'].append (
                {
                    "answer_type" : answer_type,
                    "answer_texts" : answer_texts
                }
            )     
        response_sub['answerList'].append (
        {
            "answer_type" : answer_type,
            "answer_texts" : answer_texts
        } 
        )

    data['response'] =  response_sub   


    #json_string = json.dumps(data)
    json_string = jsonable_encoder(data)    
    print("===================ChatMain_app project_list chat_jsonTest2: " , json_string)    

    return json_string

if __name__ == '__main__':
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=8001) 