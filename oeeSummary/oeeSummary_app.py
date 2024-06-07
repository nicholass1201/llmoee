from datetime import datetime
from fastapi import APIRouter
from fastapi import FastAPI, Depends, Path, HTTPException
from fastapi.encoders import jsonable_encoder
import uvicorn
import json # 참고: https://blog.naver.com/sp_sosa/222841775690
import sys, os
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from decouple import config

# import chatSubRag_biz
import  oee_summary_schema
# import summaryMain_biz
import  oee_summary_biz

app = FastAPI()
#engine = engineconn()
#session  = engine.sessionmaker()
 
router = APIRouter(
    prefix = "/oee/v1"
)

original_text="NewJeans뉴진스왼쪽부터 하니, 다니엘, 민지, 혜인, 해린기본 정보결성 지역대한민국 서울특별시장르K-pop댄스 팝활동 시기2022년 7월 22일 ~레이블하이브소속사어도어웹사이트newjeans.kr 구성원민지하니다니엘해린혜인 NewJeans(뉴진스)는 2022년 7월 22일에 데뷔한 대한민국의 5인조 걸 그룹으로, 소속사는 하이브 산하의 레이블인 어도어이다. SM 엔터테인먼트 비주얼 디렉터 출신으로 하이브에 영입된 민희진이 프로듀서로 나서서 발굴한 걸 그룹이다. 2022년 8월 18일에 《엠카운트다운》에서 데뷔 3주만에 첫 1위에 올랐다. 2023년 8월에 잼버리 폐회식 K-POP 공연에 출연했다."
chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION') )

messages = [
    SystemMessage(
        content="3줄로 요약해서 한국어로 답변해 주세요."
    ),
    HumanMessage(
        content=original_text        
    ),
]

response_langchain = chatgpt(messages)
print(response_langchain)

@router.post("/summary/predict" )
def summary_predict(param :  oee_summary_schema.SummaryMainSrchParam):
    print("===================ChatMain_app chat_predict start==========")
    data = {}    
    # query = "엘지유플러스의 인사제도에 대해 소개해주세요"    
    original_text = param.original_text
    company_id = param.company_id
    print("chatMain_app chat_predict original_text: " , original_text)        
    print("chatMain_app chat_predict company_id: " , company_id)        

    # company_id= 1    
     
    messages = [
        SystemMessage(
            content="3줄로 요약해서 한국어 존대말로 답변해 주세요."
        ),
        HumanMessage(
            content=original_text
        ),
    ]
    response_text = chatgpt(messages)    
    currentTime = datetime.now().strftime( "%Y%m%d%H%M%S" )

    api = "oeeSummary.summary_predict"
    status="ok"
    error_message="0"
    total_cnt=1

    data['api'] = api
    data['status'] = status
    data['error_message'] = error_message
    data['total_cnt'] = total_cnt    

    response_sub = {}
    response_sub['company_id'] = company_id    
    response_sub['response_text'] = response_text.content                   
    response_sub['current_time'] = currentTime        

    data['response'] =  response_sub   

    json_string = jsonable_encoder(data)    
    print("===================ChatMain_app project_list chat_jsonTest2: " , json_string)    

    return json_string
 
 
if __name__ == '__main__':
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=8002) 