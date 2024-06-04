from oee_db_conn import EngineConn
from oee_chatbot_models import Project_rag_doc, Project
from oee_project_rag_docs_schema import ProjectRagDocSrchParam

engine = EngineConn()

def get_projectRagDoc_list(param : ProjectRagDocSrchParam):
    print("====================oee_project_rag_docs get_projectRagDoc_list start========param", param)    
    print("====================oee_project_rag_docs get_projectRagDoc_list start param.project_id:", param.project_id)    

    int_page_num = int(param.page_num) 
    int_page_num=int_page_num-1
    int_page_size = int(param.count_per_page)
    skip = int_page_num * int_page_size

    session  = engine.sessionmaker()
    total_cnt = session.query(Project_rag_doc).count()
    print("oee_project_rag_docs get_projectRagDoc_list project_cnt: " , total_cnt)    
    print("oee_project_rag_docs get_projectRagDoc_list int_page_size: " , int_page_size)    
    print("oee_project_rag_docs get_projectRagDoc_list skip: " , skip)            

    sSrcFileName = param.src_file_name
    sProjectRagDocId = param.project_rag_doc_id    

    result_list = session.query(Project_rag_doc)
    if ((str(sProjectRagDocId).strip() )==""):
        if ((str(sSrcFileName).strip() )==""):
                result_list = result_list \
                        .filter(
                                Project_rag_doc.company_id == param.company_id ,
                                Project_rag_doc.project_id == int(param.project_id),
                                )
        else:
                result_list = result_list \
                        .filter(
                                Project_rag_doc.company_id == param.company_id ,
                                Project_rag_doc.project_id == int(param.project_id),
                                Project_rag_doc.src_file_name.ilike('%' + param.src_file_name + '%')
                                )
    else:
        result_list = result_list \
                .filter(
                        Project_rag_doc.company_id == param.company_id ,
                        Project_rag_doc.project_id == int(param.project_id),
                        Project_rag_doc.project_rag_doc_id == int(param.project_rag_doc_id),                        
                        )
    

        #.join(project, Project_rag_doc.project_id == project.project_id, isouter=True)
        #.add_columns(project.project_code)        
    result_list = result_list.join(Project, Project_rag_doc.project_id == Project.project_id, isouter=True)
    result_list = result_list.add_columns(Project_rag_doc.project_rag_doc_id, Project_rag_doc.company_id, Project.project_code, Project_rag_doc.project_id,  Project_rag_doc.doc_type_cd,  Project_rag_doc.src_url_addr, Project_rag_doc.src_file_name, Project_rag_doc.src_real_file_name, Project_rag_doc.applying_yn, Project_rag_doc.last_applying_dt) 
    result_list = result_list.order_by(Project_rag_doc.order_sn.desc()) \
            .offset(skip).limit(int_page_size).all()    
    print("oee_project_rag_docs get_projectRagDoc_list result_list: " , result_list)            
    print("====================oee_project_rag_docs get_projectRagDoc_list end==========")
    return total_cnt, result_list