vecChatPredict=[]

import sys, os
import oee_similarity
import oee_chat_main_schema

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print("==========sys.path.append: " , os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from mngChatBot.db_proc_ac import engineconn, text

from oeeCbMgr import oee_project
from oeeCbMgr.oee_chatbot_models import Project
from oeeCbMgr import oee_project_schema

from oeeCbMgr import oee_intent_biz
from oeeCbMgr.oee_chatbot_models import Intent
from oeeCbMgr import oee_intent_schema
 
from oeeLlmCb101 import oee_chat_sub_llm_predict_101
#from oeeLlmCb102 import oee_chat_sub_llm_predict_102
#from oeeLlmCb201 import oee_chat_sub_llm_predict_201
#from oeeLlmCb202 import oee_chat_sub_llm_predict_202

def chatMain_predict(company_id:str,project_id:int, query:str, before_intent_id:int):
    print("===================== biz chatMain_predict start ")        
    print("===================== biz chatMain_predict company_id:", company_id)         
    print("===================== biz chatMain_predict project_id:", project_id)            
    print("===================== biz chatMain_predict query:", query)            
    print("===================== biz chatMain_predict before_intent_id:", before_intent_id)                    
    response_result=""
    arrChatQuery=[] 

    oee_intent_schema.IntentSrchParam.company_id = company_id ; 
    oee_intent_schema.IntentSrchParam.project_id = project_id ; 
    oee_intent_schema.IntentSrchParam.intent_id = "" ;                 
    oee_intent_schema.IntentSrchParam.intent_name = "" ;             

    #oee_intent_schema.IntentSrchParam.required_entity_names = "휴식시간" ;                 
    oee_intent_schema.IntentSrchParam.required_entity_names = "" ;                 
    oee_intent_schema.IntentSrchParam.exclusive_entity_names = ""
    oee_intent_schema.IntentSrchParam.page_num = "1" ;         
    oee_intent_schema.IntentSrchParam.count_per_page = "10" ;                     
    oee_intent_schema.IntentSrchParam.order_type = "asc" ;      

    total_cnt, _intent_list = oee_intent_biz.get_intent_list( intent_schema.IntentSrchParam )        
    print("===================== biz total_cnt: ", total_cnt)
    print("===================== biz len _intent_list: ", len(_intent_list))    

    strStopKeyword="" ; 
    strSourceCd = "" ; 

    for row in _intent_list:
        print("    ")                
        print("===================== biz _intent_row.project_id: ", row.project_id)        
        print("===================== biz _intent_row.company_id: ", row.company_id)
        print("===================== biz _intent_row.intent_id: ", row.intent_id)
        print("===================== _intent_row.intent_name: ", row.intent_name)                
        print("===================== _intent_row.required_entity_names: ", row.required_entity_names)                
        print("===================== _intent_row.exclusive_entity_names: ", row.exclusive_entity_names)                                
        print("===================== _intent_row.querys: ", row.querys)                        
        strQuery = row.querys
        ArrQuery = strQuery.split(';')
        
        for j in range(0, len(ArrQuery)):
            print("========ArrQuery j: ", j)                                
            varChatQuery=[]            
            varChatQuery.append(row.intent_id)
            varChatQuery.append(j)                                
            varChatQuery.append(ArrQuery[j])
            varChatQuery.append(row.required_entity_names)            
            varChatQuery.append(row.exclusive_entity_names)            

            arrChatQuery.append(varChatQuery)            

        print("========ArrQuery: ", ArrQuery[0])   
    containNounYn= "N" ; #  args['nounMatchingYn']
    # strFindKeyword="휴식시간"
    strFindKeyword="" ; 
    #strFindKeyword="교체"
    strStopKeyword=""
    print("=======================================make_chat_main strFindKeyword: ", strFindKeyword)    

    # makeCosSimilarArr(chatbot_data2, sentence1, strFindKeyword , strStopKeyword, containNounYn):
    oee_similarity.arrCosSimilar=[]
    oee_similarity.makeCosSimilarArr(arrChatQuery, query,  containNounYn)   # oee_similarity.


    print("oee_similarity.arrCosSimilar len: ", len(oee_similarity.arrCosSimilar))     
    if (len(oee_similarity.arrCosSimilar) > 0):
        result_data={} ; result_data['query'] = [] ; result_data['result'] = [] ; 
        oee_similarity.arrCosSimilar.sort(key = lambda x:x[3] , reverse=True)          # # oee_similarity.

        smlr_rlt_seq = 0
        for intent_id, question_seq, strA1, strA2, strA3 in oee_similarity.arrCosSimilar :       # # oee_similarity.
            print("oee_similarity.arrCosSimilar smlr_rlt_seq: " , smlr_rlt_seq)    
            print("intent_id, question_seq, strA1, strA2, strA3: " , intent_id, question_seq, strA1, strA2, strA3)
            strA2Rounded=round(strA2[0][0]*100, 2)
            result_data['result'].append({
                'intent_id' : intent_id,
                'question_seq' : question_seq,        
                '내용' : strA1, 
                '형태소분석' : strA3,         
                '유사도' : strA2Rounded     
                })        

            if (smlr_rlt_seq==0):
                print("=========답변================ ")  
                for row2 in _intent_list:
                    if (row2.intent_id==intent_id):                    
                        print("========답변 _intent_row.project_id: ", row2.project_id)        
                        print("========답변 _intent_row.company_id: ", row2.company_id)
                        print("========답변 _intent_row.intent_id: ", row2.intent_id)
                        print("========답변 _intent_row.intent_name: ", row2.intent_name)                
                        print("========답변 _intent_row.required_entity_names: ", row2.required_entity_names)                        
                        print("========답변 _intent_row.exclusive_entity_names: ", row2.exclusive_entity_names)                                
                        print("========답변 _intent_row.querys: ", row2.querys)                        
                        print("========답변 _intent_row.answer_texts: ", row2.answer_texts)                                                
                        strSourceCd = "intent"
                        oee_chat_main_schema.ChatMain_schema.company_id = company_id                                                
                        oee_chat_main_schema.ChatMain_schema.project_id = row2.project_id                        
                        oee_chat_main_schema.ChatMain_schema.intent_id = row2.intent_id                                                                        
                        oee_chat_main_schema.ChatMain_schema.response_texts = row2.answer_texts
                        oee_chat_main_schema.ChatMain_schema.response_src_cd = strSourceCd                        

            smlr_rlt_seq=smlr_rlt_seq+1

    # smlr_rlt_seq = 0
    oee_project_schema.ProjectSearchParam.company_id = company_id    
    oee_project_schema.ProjectSearchParam.project_id = project_id
    oee_project_schema.ProjectSearchParam.project_name = ""    
    oee_project_schema.ProjectSearchParam.page_num = "1" ;         
    oee_project_schema.ProjectSearchParam.count_per_page = "10" ;                     
    oee_project_schema.ProjectSearchParam.order_type = "asc" ;      

    p_total_cnt, _project_list = oee_project.get_project_list(oee_project_schema.ProjectSearchParam)    
    print("================make_chat_main p_total_cnt: ", p_total_cnt)     

    for row in _project_list:
        print("========_project_list.project_id: ", row.project_id)        
        print("========_project_list.company_id: ", row.company_id)
        print("========_project_list.llm_nm_cd: ", row.llm_nm_cd)                
        sllm_nm_cd = row.llm_nm_cd


    print("================make_chat_main strSourceCd: ", strSourceCd)     
    if (strSourceCd==""):   # 답변 출처 코드 : 01: llm 02:. intent (히스토리 내역도 결국 히스토리에서 선택하여 인텐트 저장) 
        print("================  gpt 호출 ================ ")             
        strSourceCd="LLM" 
        # query = sentence1
        print("================make_chat_main biz_rag_predict query: " , query)        
        #response_result = "하드코response_result딩 답변입니다."
        if sllm_nm_cd=="101" :    
            response_result = oee_chat_sub_llm_predict_101.biz_rag_predict(company_id, project_id, query=query, before_intent_id=0)                
        elif sllm_nm_cd=="102" :    
            print("============llm102 project_id 36일때: ", project_id)
            # response_result = oee_chat_sub_llm_predict_102.biz_rag_predict(project_id, query=query, before_intent_id=0)                
        elif sllm_nm_cd=="201" :              
            print("============llm201 project_id 37일때: ", project_id)
            # response_result = oee_chat_sub_llm_predict_201.biz_rag_predict(project_id, query=query, before_intent_id=0)                
        elif sllm_nm_cd=="202" :              
            print("============llm202 project_id 38일때: ", project_id)
            # response_result = oee_chat_sub_llm_predict_202.biz_rag_predict(company_id, project_id, query=query, before_intent_id=0)                
        print("chatMain_app chat_rag_predict response_result: " , response_result)      
        oee_chat_main_schema.ChatMain_schema.company_id = company_id                                                        
        oee_chat_main_schema.ChatMain_schema.project_id = project_id                        
        oee_chat_main_schema.ChatMain_schema.intent_id = ""
        oee_chat_main_schema.ChatMain_schema.response_src_cd = strSourceCd
        # response_src_cd
        oee_chat_main_schema.ChatMain_schema.response_texts = response_result


    return oee_chat_main_schema

if __name__ == '__main__':    
    company_id="item"
    # query = "엘지유플러스의 인사제도에 대해 소개해주세요"        
    query = "엘지유플러스에 대해 소개해주세요"    
    #query = "내 휴식시간 알려줘"        
    project_id=1
    before_intent_id=""

    response_result = chatMain_predict(company_id=company_id, project_id=project_id,  query=query, before_intent_id=before_intent_id)        

    print("=================== __main__ company_id: " , response_result.ChatMain_schema.company_id)      
    print("=================== __main__ project_id: " , response_result.ChatMain_schema.project_id)      
    print("=================== __main__ intent_id: " , response_result.ChatMain_schema.intent_id)              
    print("=================== __main__ response_texts: " , response_result.ChatMain_schema.response_texts)                  
