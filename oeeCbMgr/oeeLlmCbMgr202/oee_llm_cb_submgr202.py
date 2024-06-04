# from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from decouple import config

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import oee_project_rag_docs_schema
import oee_project_rag_docs

def biz_rag_save(param : oee_project_rag_docs_schema.ProjectRagDocSrchParam):
    print("===========biz_rag_save=========== param:", param)
    param.page_num="1"            
    param.count_per_page="10"            
    param.order_type="asc"                        

    total_cnt, _projectRagDoc_list = oee_project_rag_docs.get_projectRagDoc_list(param)        
    arrAtch=[]                
    for row in _projectRagDoc_list:
        print("========oee_project_rag_docs.project_id: ", row.project_id)        
        print("========oee_project_rag_docs.proj_doc_id: ", row.proj_doc_id)                
        print("========oee_project_rag_docs.company_id: ", row.company_id)
        print("========oee_project_rag_docs.atch_url_addr: ", row.atch_url_addr)

        strSrc_url_addr=row.src_url_addr
        arrAtch.append(strSrc_url_addr) 
        #arrAtch.append("https://www.lguplus.com/about/ko/sustainability/practice/information-protection")         
    
    # arrAtch=strAtch_url_addr.split(',')

    #loader = WebBaseLoader([strAtch_url_addr])
    loader = WebBaseLoader(arrAtch)

    data = loader.load()
    # print("============= data:", data)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
    all_splits = text_splitter.split_documents(data)
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma

    varProjectCode = lpad(row.project_id, 6, '0')

    varBaseDir = config('CHROMA_BASE_DIR')
    varRagDir = varBaseDir + "/" + row.company_id + "/" + varProjectCode 
    print("===========create vector db folder=========== varRagDir:", "/home/sdiaadmin/llm/ac/data/item38/000039")
    print("===========create vector db folder=========== varRagDir:", varRagDir)        

    # 디렉토리 없으면 생성 
    makedirs(varRagDir)

    # persist_directory = './db9'
    vectorstore = Chroma.from_documents \
        (documents=all_splits, 
            embedding = 
            OpenAIEmbeddings(temperature=0, openai_api_key=config('OPENAI_API_KEY'), 
            openai_organization=config('OPENAI_ORGANIZATION')), 
            persist_directory=varRagDir
        )
    print("===========벡터db에 load2=========== vectorstore:", vectorstore)

    # vectorstore.add_texts(all_splits)


    retriever = vectorstore.as_retriever()
    from langchain.prompts import PromptTemplate
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION'))

    documents = loader.load()
    
    from langchain.text_splitter import CharacterTextSplitter

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings_model = OpenAIEmbeddings(temperature=0, openai_api_key=config('OPENAI_API_KEY'), openai_organization=config('OPENAI_ORGANIZATION'))
    # load it into Chroma

    
    print("===========벡터db에 저장===========")
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

    question="LG 유플러스가 매년 정보서비스를 대상으로 어떤 인증을 받았나요?"
    #question="LG 유플러스 소개해줘?"
    # 질문하신 내용은 업무와 관련이 없습니다. 
    # question="삼성전자 소개해 줘"
    print("q: " , question)
    result = qa_chain.invoke(question).content        
    print("결과: ", result)




# 0으로 채우기  
# i: 입력 문자열, width: 전체문자열 길이        
def lpad(i, width, fillchar='0'):
    return str(i).rjust(width, fillchar)

# 디렉토리 생성
def makedirs(varRagDir):
    if not os.path.exists(varRagDir):
        os.makedirs(varRagDir)




if __name__ == '__main__': 
 
    print("==================== chatSubLlmMng101_biz start ==========")
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.proj_doc_id="7"
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.company_id="item38"    
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.project_id="39"    
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.atch_type_cd="02"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.page_num="1"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.count_per_page="10"            
    oee_project_rag_docs_schema.ProjectRagDocSrchParam.order_type="asc"                        
    param=oee_project_rag_docs_schema.ProjectRagDocSrchParam
    print("==================== param:", param)    
    print("==================== param.proj_doc_id:", param.proj_doc_id)        
    biz_rag_save(param)    
    print("====================__main__ end" )    


 

