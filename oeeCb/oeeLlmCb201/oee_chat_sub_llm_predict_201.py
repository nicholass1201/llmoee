
def biz_rag_predict(project_id:int, query:str, before_intent_id:int):
    # project_id query before_intent_id
    print("============ 201 chatMain_biz biz_predict project_id: " , project_id)    
    print("============ 201 chatMain_biz biz_predict query: " , query)    
    print("============ 201 chatMain_biz biz_predict before_intent_id: " , before_intent_id)            
    result = "sllm201 결과입니다."  
    #print(result)
    return result

 

if __name__ == '__main__':
    # query = "엘지유플러스의 인사제도에 대해 소개해주세요"
    # query = "엘지유플러스에 대해 소개해주세요"
    query="스마트컨택 프리미엄이 뭐에요?"
    result = biz_rag_predict(project_id=1, query=query, before_intent_id=0)
    print("chatMain_biz __main__ query: " , query)          
    print("chatMain_biz __main__ result: " , result)      
