from dotenv import load_dotenv
from decouple import config
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import oee_project_rag_docs_schema
import oee_project_rag_docs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = config('BASE_DIR')
# 디렉토리 생성
def makedirs(varRagDir):
    if not os.path.exists(varRagDir):
        os.makedirs(varRagDir)

# 0으로 채우기  
# i: 입력 문자열, width: 전체문자열 길이        
def lpad(i, width, fillchar='0'):
    return str(i).rjust(width, fillchar) 

def storingRagDoc(params : oee_project_rag_docs_schema.ProjectRagDocUrlParam):
    print("===========biz_rag_save=========== params:", params)
    #param.page_num="1"            
    #param.count_per_page="10"            
    #param.order_type="asc"                        

    print("========oee_project_rag_docs. params.project_id: ", params.project_id)        
    print("========oee_project_rag_docs. params.company_id: ", params.company_id)

    varProjectCode = lpad(params.project_id, 6, '0')
    varAtchDir = BASE_DIR +  "/ragSrcFiles/" + params.company_id + "/" + varProjectCode + "/"
    print("========oee_project_rag_docs. varAtchDir: ", varAtchDir)                        
    arrAtch=[]  

    for row in params.project_rag_doc_list:
        print("========oee_project_rag_docs. row.project_rag_doc_id: ", row.project_rag_doc_id)                        
        print("========oee_project_rag_docs. row.applying_yn: ", row.applying_yn)
        print("========oee_project_rag_docs. row.src_url_addr: ", row.src_url_addr)
        print("========oee_project_rag_docs. row.src_file_name: ", row.src_file_name)        

        varFullDocName= varAtchDir+ row.src_file_name
        arrAtch.append(varFullDocName)

    print("========oee_project_rag_docs biz_rag_save varFullDocName: ", varFullDocName)                
    print("========oee_project_rag_docs biz_rag_save arrAtch: ", arrAtch)                    
    #loader = WebBaseLoader([strAtch_url_addr])
    #loader = PyPDFLoader(arrAtch)
    loader = PyPDFLoader(varFullDocName)
    data = loader.load()
    #print("============= data:", data)


    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
    all_splits = text_splitter.split_documents(data)
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma


    varBaseDir= BASE_DIR
    varProjectCode = lpad(params.project_id, 6, '0')        

    #varRagDir = varBaseDir + "/item38/000039"
    varRagDBDir = varBaseDir + "/ragDBData/" + params.company_id + "/" + varProjectCode 
    print("============= varRagDBDir:", varRagDBDir)    
       # 디렉토리 없으면 생성 
    # makedirs(varRagDirRag)
    makedirs(varRagDBDir)   


    # persist_directory = './db9'
    vectorstore = Chroma.from_documents \
        (documents=all_splits, 
            embedding = 
            OpenAIEmbeddings(temperature=0, openai_api_key=config('OPENAI_API_KEY')), 
            openai_organization=config('OPENAI_APOPENAI_ORGANIZATION'),
            persist_directory=varRagDBDir
        )
    print("===========벡터db에 load2=========== vectorstore:", vectorstore)
    vectorstore.persist() ; 
    print("===========벡터db에 저장1===========")
    retriever = vectorstore.as_retriever()
    from langchain.prompts import PromptTemplate
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI( model_name="gpt-3.5-turbo", temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION'))
    
    print("===========벡터db에 저장2==========")
    # db = Chroma.from_documents(docs, embeddings_model)

    template = """ 
    학습된 문서내에서 존대말로 답변해 주세요 학습된 문서내의 질문이 아니면 '관련없음'으로 대답해 주세요
    {context}
    Question: {question}
    Answer:"""

    prompt = PromptTemplate.from_template(template)

    qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt 
        | llm 
    )

    # question="스마트컨택 프리미엄이 뭐에요?"
    question="AI바우처란"
    #question="LG 유플러스 소개해줘?"
    # 질문하신 내용은 업무와 관련이 없습니다. 
    # question="삼성전자 소개해 줘"
    print("q: " , question)
    result = qa_chain.invoke(question).content        
    print("결과: ", result)


if __name__ == '__main__': 
 
    print("==================== chatSubLlmMng101_biz start ==========")

    oee_project_rag_docs_schema.ProjectRagDocUrlParam.company_id="item3"    
    oee_project_rag_docs_schema.ProjectRagDocUrlParam.project_id="3"    
    oee_project_rag_docs_schema.ProjectRagDocUrlParam.project_rag_doc_list=[]

    oee_project_rag_docs_schema.ProjectRagDoc_schema.project_rag_doc_id="51"
    oee_project_rag_docs_schema.ProjectRagDoc_schema.applying_yn="Y"
    oee_project_rag_docs_schema.ProjectRagDoc_schema.src_url_addr=""
    oee_project_rag_docs_schema.ProjectRagDoc_schema.src_file_name="2024년 AI바우처 지원사업 설명회 자료집.pdf"        
    oee_project_rag_docs_schema.ProjectRagDoc_schema.create_id="admin"        
      

    oee_project_rag_docs_schema.ProjectRagDocUrlParam.project_rag_doc_list.append(oee_project_rag_docs_schema.ProjectRagDoc_schema)

    param=oee_project_rag_docs_schema.ProjectRagDocUrlParam
    
    print("==================== param:", param)    
    print("==================== param.proj_doc_id:", param.company_id)        
    storingRagDoc(param)    
    # print("==================== total_cnt:", total_cnt)    


 