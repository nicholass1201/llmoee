import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print("======oee_proj path: ", os.path.dirname(__file__) )
print("======oee_proj path: ", os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from oeeCbMgr.oee_db_conn import EngineConn
from oeeCbMgr.oee_chatbot_models import Project
from oeeCbMgr.oee_project_schema import *

engine = EngineConn()
total_cnt = 0    

def get_project_list(param : ProjectSearchParam):
    print("oee_proj start==========")
    print("oee_proj start==========param: ", param)    

    int_page_num = int(param.page_num) 
    int_page_num = int_page_num - 1
    int_page_size = int(param.count_per_page)
    skip = int_page_num * int_page_size 

    session  = engine.sessionmaker()
    total_cnt = session.query(Project).count()
    print("oee_proj get_project_list project_cnt:" , total_cnt)    
    print("oee_proj param.project_id:" , param.project_id)        

    project_list = session.query(Project)
    project_list_for_totalCnt = session.query(Project) \
        .filter(
                Project.company_id == param.company_id
                ).all()  
    print("oee_proj get_project_list ========================" )        
    total_cnt = len(project_list_for_totalCnt) 
    print("oee_proj get_project_list len(project_list) total_cnt :" , total_cnt)    
    print("oee_proj get_project_list len(project_list) param.project_id :" , param.project_id)        
    sProject_id = param.project_id
    if ((str(sProject_id).strip() )==""):
        print("oee_proj if param.project_id is null")      
        project_list = project_list \
            .filter(Project.project_name.ilike('%' + param.project_name + '%') ,
                    Project.company_id == param.company_id ,
                )                  
        sServiceYn = param.in_service_yn
        # if ((param.in_service_yn.strip() )!=""):    
        if ((str(sServiceYn).strip() )!=""):    
            project_list = project_list \
                .filter(
                        Project.in_service_yn == param.in_service_yn 
                    )                  
        
    else:
        print("oee_proj if sProject_id:", sProject_id)                        
        project_list = project_list \
            .filter(
                Project.company_id == param.company_id ,
                Project.project_id == int(param.project_id)
                )        

    if (param.order_type=="asc"):    
        project_list = project_list.order_by(Project.project_name.asc()) \
                .offset(skip).limit(int_page_size).all()    
    elif (param.order_type=="desc"):    
        project_list = project_list.order_by(Project.project_name.desc()) \
                .offset(skip).limit(int_page_size).all()    

    print("====================end of oee_proj get_project_list" )            
    return total_cnt, project_list



if __name__ == '__main__':
    # total_cnt = get_project_list(skip=11, limit=5, keyword="insert5")
    print("__main__ total_cnt: " , total_cnt)  