from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from decouple import config

import sys, os
print("=================__file__: ", __file__)
print("=================os.path.dirname(os.path.abspath(os.path.dirname(__file__))): ", os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
BASE_DIR = config( 'BASE_DIR' )
sys.path.append( BASE_DIR + "/oeeCbMgr")
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import oee_project_rag_docs_schema
import oee_project_rag_docs

from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION'))

# documents = loader.load()
 
from langchain.text_splitter import CharacterTextSplitter

#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#docs = text_splitter.split_documents(documents)
#embeddings_model = OpenAIEmbeddings(temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION'))
# load it into Chroma

# db = Chroma.from_documents(docs, embeddings_model)

template = """ 
학습된 문서내에서 존대말로 답변해 주세요 학습된 문서내의 질문이 아니면 '관련없음'으로 대답해 주세요
{context}
Question: {question}
Answer:"""

prompt = PromptTemplate.from_template(template)

# question="클라우드고객센터 Lite pro 서비스 요금 알려줘"
# question="엘지유플러스의 정도경영 추진조직은 어떻게 되나요?"
# 질문하신 내용은 업무와 관련이 없습니다. 
#question="삼성전자 소개해 줘"


def biz_rag_predict( company_id:str, project_id:int, query:str, before_intent_id:int ):
    # project_id query befoer_intent_id
    print("============ oee_chat_sub_llm_predict_101 biz_predict q: " , query)    
    print("============ oee_chat_sub_llm_predict_101 biz_predict project_id: " , project_id)        
    # oee_project_rag_docs_schema.ProjDocSrchParam.proj_doc_id="7"
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.company_id=company_id   
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.project_id=project_id  
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.project_rag_doc_id=""      
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.src_file_name = ""
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.src_file_name = ""
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.src_url_addr  = ""
    #oee_project_rag_docs_schema.ProjDocSrchParam.atch_type_cd="02"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.page_num="1"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.count_per_page="10"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.order_type="asc"                        
    param=oee_project_rag_docs_schema.ProjectRagDocSrchParam
    
    total_cnt, _projDoc_list = oee_project_rag_docs.get_projectRagDoc_list( param )   
    print("========oee_chat_sub_llm_predict_101 total_cnt: ", total_cnt)             
    print("========oee_chat_sub_llm_predict_101 _projDoc_list: ", _projDoc_list)                 
    for row in _projDoc_list:
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.project_code: ", row.project_code)                
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.project_id: ", row.project_id)        
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.project_rag_doc_id: ", row.project_rag_doc_id)                
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.company_id: ", row.company_id)
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.doc_type_cd: ", row.doc_type_cd)        
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.src_url_addr: ", row.src_url_addr)
        print("========oee_chat_sub_llm_predict_101 projDoc_biz.src_file_name: ", row.src_file_name)        

        print("===========load to vector db 1===========") 
        #varRagDir = "/home/sdiaadmin/llm/llmoee/data/item/000001"  # main문으로 하면 상대경로 인식하는데, import로 호출해서 실행할때 상대경로 인식 못함 /home/sdiaadmin/llm/llmoee/data/db8
        varRagDir = BASE_DIR  + "/ragDBData/" + row.company_id + "/" + row.project_code

        print("========oee_chat_sub_llm_predict_101 varRagDir: ", varRagDir)                
        vectorstore = Chroma(persist_directory = varRagDir  , 
                embedding_function = 
                #OpenAIEmbeddings(temperature=0 )
                OpenAIEmbeddings()
                )
        print("===========load to vector db 2===========")
        print("===========load to vector db 2=========== vectorstore:", vectorstore)
        varDocTypeCd = row.doc_type_cd
        if varDocTypeCd=="01" :  # 첨부구분코드: 01: FILE, 02: WEB, 03: KMS텍스트 05: KMS연계(FILE), 06: KMS연계(WEB)
            varSource= row.src_file_name
        elif varDocTypeCd=="02" : 
            varSource= row.src_url_addr

        print("===========load to vector db 2=========== varDocTypeCd:", varDocTypeCd)
        print("===========load to vector db 2=========== varSource:", varSource)        
        result1 = vectorstore.get(where={"source": varSource})  # AI바우쳐 관련 내용
        print("===========load to vector db 2=========== vectorstore 컬럼수 : " , len(result1))
        print("===========load to vector db 2=========== vectorstore result1 : " , result1)        
        print("===========load to vector db 2=========== vectorstore 리스트 건수: ", len(result1['ids']) )        

        retriever = vectorstore.as_retriever()        

        qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | llm 
        )

        result = qa_chain.invoke(query).content        
        print("====================== 101 biz result:", result)
        #print(result)
        return result
    print("====================== 101 biz end=========")

 

if __name__ == '__main__':
    query="스마트컨택 프리미엄 소개해줘"
    result = biz_rag_predict(company_id="item3", project_id="3", query=query, before_intent_id=0,  )

    #query="LG 유플러스가 매년 정보서비스를 대상으로 어떤 인증을 받았나요?"
    #result = biz_rag_predict(company_id="item", project_id="2", query=query, before_intent_id=0,  )

    print("chatMain_biz __main__ result: " , result)      