from oee_db_conn import EngineConn
from oee_chatbot_models import Project

engine = EngineConn()
session  = engine.sessionmaker()

def get_project_list(skip: int=0, limit:int=10, keyword:str=''):
    print("oee_project_crud start==========")
    total_cnt = session.query(Project).count()
    print("project_cnt: " , total_cnt)    
    print("skip: " , skip)            
    print("limit: " , limit)        
    print("keyword: " , keyword)     
    project_list = session.query(Project)
    project_list = project_list.filter(Project.project_name.ilike(keyword))
    project_list = project_list.order_by(Project.project_name.asc()).all()
    print("====================project_list: " , project_list)            
    return total_cnt, project_list

def get_project_list_old(skip: int=0, limit:int=10, keyword:str=''):
    print("oee_project_crud start==========")
    total_cnt = session.query(Project).count()
    print("project_cnt: " , total_cnt)  
    print("skip: " , skip)            
    print("limit: " , limit)        
    print("keyword: " , keyword)        
    project_list = session.query(Project)
    print("project_list: " , project_list)        

    return total_cnt    

if __name__ == '__main__':
    total_cnt = get_project_list(skip=11, limit=5, keyword="insert5")
    print("__main__ total_cnt: " , total_cnt)  