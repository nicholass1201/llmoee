from decouple import config
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.chat_models import ChatOpenAI
import sys, os
import oee_project_rag_docs_schema
import oee_project_rag_docs

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = config('BASE_DIR')
# Create folder
def makedirs(varRagDir):
    if not os.path.exists(varRagDir):
        os.makedirs(varRagDir)

# pad with 0  
# i: input sentence, width: 전체문자열 길이        
def lpad(i, width, fillchar='0'):
    return str(i).rjust(width, fillchar) 


def storingRagDocUrl(params : oee_project_rag_docs_schema.ProjectRagDocUrlParam):
    print("===========biz_rag_save=========== params:", params)
    #param.page_num="1"            
    #param.count_per_page="10"            
    #param.order_type="asc"                        

    print("======== oee_project_rag_docs. params.project_id: ", params.project_id)        
    print("======== oee_project_rag_docs. params.company_id: ", params.company_id)

    varBaseDir = BASE_DIR
    varProjectCode = lpad(params.project_id, 6, '0')        

    varRagDBDir = varBaseDir + "/ragDBData/" + params.company_id + "/" + varProjectCode 
    print("============= varRagDBDir:", varRagDBDir)    

    vectorstore = Chroma(
        persist_directory = varRagDBDir,        
        embedding_function = OpenAIEmbeddings() # OpenAIEmbeddings(temperature=0)
    )
    print("======== oee_project_rag_docs. vectorstore._collection.count 1: ",vectorstore._collection.count())

    arrAtch=[]  
    for row in params.project_rag_doc_list:
        print("======== oee_project_rag_docs. row.project_rag_doc_id: ", row.project_rag_doc_id)                        
        print("======== oee_project_rag_docs. row.applying_yn: ", row.applying_yn)
        print("======== oee_project_rag_docs. row.src_url_addr: ", row.src_url_addr)

        if row.applying_yn == "Y" :
            arrAtch.append(row.src_url_addr)

        # 적용여부와 관계없이 무조건 삭제 , Y이면 추가, N이면 삭제 후 추가 안함. 
        result1 = vectorstore.get(where={"source": row.src_url_addr})  # AI바우쳐 관련 내용
        print("삭제전 컬럼수 : " , len(result1))
        print("삭제전 리스트 건수: ", len(result1['ids']) )

        print("데이터 삭제 시작!!!!")
        for i in range(0, len(result1['ids']) ):
            # print(i)
            iNum = result1['ids'][i]
            vectorstore._collection.delete(ids=iNum)

        result2 = vectorstore.get(where={"source": row.src_url_addr})  # AI바우쳐 관련 내용
        print("삭제후 컬럼수 : " , len(result2))
        print("삭제후 리스트 건수: ", len(result2['ids']) )


    print("======== oee_project_rag_docs. vectorstore._collection.count 2: ",vectorstore._collection.count())
    print("======== oee_project_rag_docs biz_rag_save arrAtch: ", arrAtch)                
    print("======== oee_project_rag_docs biz_rag_save len(arrAtch) : ", len(arrAtch) )                    

    # 적용여부 건수가 1이상이면 저장
    if len(arrAtch) > 0 :
        print("============= RAG storing 시작 BASE_DIR:", BASE_DIR)            
        loader = WebBaseLoader(arrAtch)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
        all_splits = text_splitter.split_documents(data)

        # 디렉토리 없으면 생성 
        makedirs(varRagDBDir)   
        #embeddings = OpenAIEmbeddings()
        #embeddings1 = OpenAIEmbeddings(temperature=0)
        embeddings1 = OpenAIEmbeddings()
        # vectorstore = Chroma.from_documents \
        #     (documents=all_splits, 
        #         embedding = 
        #          OpenAIEmbeddings(temperature=0 ),                 
        #         persist_directory=varRagDBDir
        #     )

        vectorstore = Chroma.from_documents (
                documents=all_splits, embedding = embeddings1, persist_directory=varRagDBDir
            )


        print("===========벡터db에 load2=========== vectorstore:", vectorstore)
        print("===========벡터db에 load2=========== vectorstore._collection.count() 3:", vectorstore._collection.count())    
        vectorstore.persist() ;     
        print("===========벡터db에 저장1===========")



    #  저장된 문서가 있는지 검색
    for row in params.project_rag_doc_list:
        print("======== oee_project_rag_docs. row.project_rag_doc_id 3: ", row.project_rag_doc_id)                        
        print("======== oee_project_rag_docs. row.applying_yn 3: ", row.applying_yn)
        print("======== oee_project_rag_docs. row.src_url_addr 3: ", row.src_url_addr)
        result3 = vectorstore.get(where={"source": row.src_url_addr})  # AI바우쳐 관련 내용
        print("저장후 컬럼수 1: " , len(result3))
        print("저장후 리스트 건수: ", len(result3['ids']) )


    retriever = vectorstore.as_retriever()
    from langchain.prompts import PromptTemplate
    from langchain.schema.runnable import RunnablePassthrough

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    print("===========벡터db에 저장2===========")
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

    question="AI바우처 공급기업이 뭐예요?"
    #question="LG 유플러스 소개해줘?"
    # 질문하신 내용은 업무와 관련이 없습니다. 
    # question="삼성전자 소개해 줘"
    print("q: " , question)
    result = qa_chain.invoke(question).content        
    print("결과: ", result)


def storingRagDocFile(params : oee_project_rag_docs_schema.ProjectRagDocUrlParam):
    print("===========biz_rag_save=========== params:", params)
    print("======== oee_project_rag_docs. params.project_id: ", params.project_id)        
    print("======== oee_project_rag_docs. params.company_id: ", params.company_id)

    varBaseDir= BASE_DIR
    varProjectCode = lpad(params.project_id, 6, '0')            
    varRagDBDir = varBaseDir + "/ragDBData/" + params.company_id + "/" + varProjectCode     
    vectorstore = Chroma(persist_directory = varRagDBDir  , 
            embedding_function = 
            # OpenAIEmbeddings(temperature=0)
                OpenAIEmbeddings()
            )
    print("======== oee_project_rag_docs. vectorstore._collection.count 1: ",vectorstore._collection.count())
 
    varAtchDir = BASE_DIR +  "ragSrcFiles/" + params.company_id + "/" + varProjectCode + "/"
    print("======== oee_project_rag_docs. varAtchDir: ", varAtchDir)                        
    arrAtch=[]  
    for row in params.project_rag_doc_list:
        print("======== oee_project_rag_docs. row.project_rag_doc_id: ", row.project_rag_doc_id)                        
        print("======== oee_project_rag_docs. row.applying_yn: ", row.applying_yn)
        print("======== oee_project_rag_docs. row.src_url_addr: ", row.src_url_addr)
        print("======== oee_project_rag_docs. row.src_file_name: ", row.src_file_name)        

        varFullDocName= varAtchDir+ row.src_file_name
        arrAtch.append(varFullDocName)

        result1 = vectorstore.get(where={"source": varFullDocName})  # AI바우쳐 관련 내용
        print("삭제전 result1 : " , result1)                
        print("삭제전 컬럼수 : " , len(result1))
        print("삭제전 리스트 건수: ", len(result1['ids']) )

        print("데이터 삭제 시작!!!!")
        for i in range(0, len(result1['ids']) ):
            # print(i)
            iNum = result1['ids'][i]
            vectorstore._collection.delete(ids=iNum)

        result2 = vectorstore.get(where={"source": varFullDocName})  # AI바우쳐 관련 내용
        print("삭제후 result2 : " , result2)
        print("삭제후 컬럼수 : " , len(result2))        
        print("삭제후 리스트 건수: ", len(result2['ids']) )

        print("======== oee_project_rag_docs. vectorstore._collection.count 2: ",vectorstore._collection.count())
        print("======== oee_project_rag_docs biz_rag_save varFullDocName: ", varFullDocName)                
        print("======== oee_project_rag_docs biz_rag_save arrAtch: ", arrAtch)                    
        #loader = WebBaseLoader([strAtch_url_addr])
        #loader = PyPDFLoader(arrAtch)
        # 적용여부 건수가 1이상이면 저장        
        if row.applying_yn == "Y" :
            print("======== oee_project_rag_docs biz_rag_save 저장시작")
            loader = PyPDFLoader(varFullDocName)
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
            all_splits = text_splitter.split_documents(data)
            varProjectCode = lpad(params.project_id, 6, '0')        
            # 디렉토리 없으면 생성 
            makedirs(varRagDBDir)   

            vectorstore = Chroma.from_documents \
                (documents=all_splits, 
                    embedding = 
                    # OpenAIEmbeddings(temperature=0), 
                    OpenAIEmbeddings(), 
                    persist_directory=varRagDBDir
                )

            print("===========벡터db에 저장===========")
            vectorstore.persist() ; 
            print("===========벡터db에 저장=========== vectorstore._collection.count() 개별 저장후 2-1:", vectorstore._collection.count())        


        #  저장된 문서가 있는지 검색
        result3 = vectorstore.get(where={"source": varFullDocName})  # AI바우쳐 관련 내용
        print("저장후 result3 : " , result3)
        print("저장후 컬럼수 : " , len(result3))
        print("저장후 리스트 건수: ", len(result3['ids']) )

    print("===========벡터db에 load2=========== vectorstore 3:", vectorstore)
    print("===========벡터db에 load2=========== vectorstore._collection.count() 3:", vectorstore._collection.count())        

 
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0 )
    
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
 
    print("==================== oee_llm_cb_submgr101 start ==========")
    oee_project_rag_docs_schema.ProjDocSrchParam.proj_doc_id="7"
    oee_project_rag_docs_schema.ProjDocSrchParam.company_id="item"    
    oee_project_rag_docs_schema.ProjDocSrchParam.project_id="38"    
    oee_project_rag_docs_schema.ProjDocSrchParam.atch_type_cd="02"            
    oee_project_rag_docs_schema.ProjDocSrchParam.page_num="1"            
    oee_project_rag_docs_schema.ProjDocSrchParam.count_per_page="10"            
    oee_project_rag_docs_schema.ProjDocSrchParam.order_type="asc"                        
    param=oee_project_rag_docs_schema.ProjDocSrchParam
    print("==================== param:", param)    
    print("==================== param.proj_doc_id:", param.proj_doc_id)        
    storingRagDocUrl(param)    
    # print("==================== total_cnt:", total_cnt)    