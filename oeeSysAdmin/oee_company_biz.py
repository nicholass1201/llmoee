import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print("======company_biz path: ", os.path.dirname(__file__) )
print("======company_biz path: ", os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from oeeCbMgr.oee_db_conn import EngineConn
from oeeSysAdmin.oee_sys_admin_models import Company
from oeeSysAdmin.oee_company_schema import *


engine = EngineConn()
# session  = engine.sessionmaker()

def get_company_list(param : CompanySrchParam):
    print("company_biz start==========")
    print("company_biz start==========param: ", param)    

    int_page_num = int(param.page_num) 
    int_page_num=int_page_num-1
    int_page_size = int(param.count_per_page)
    skip = int_page_num * int_page_size 

    # param.project_name = "insert3"
    session  = engine.sessionmaker()    
    total_cnt = session.query(Company).count()
    print("company_biz get_company_list company_cnt:" , total_cnt)    

    company_list = session.query(Company)

    if ((param.company_id.strip() )==""):
        print("company_biz if param.project_id is null")      
        company_list = company_list \
            .filter(Company.company_name.ilike('%' + param.company_name + '%') 
                )                  
    else:
        print("company_biz if param.company_id:", param.company_id)                        
        company_list = company_list \
            .filter(Company.company_id == param.company_id 
                )        
    print("company_biz get_company_list company_list:" , company_list)    

    company_list = company_list.order_by(Company.company_name.asc()) \
            .offset(skip).limit(int_page_size).all()    

    print("====================end of company_biz get_company_list" )            
    return total_cnt, company_list

if __name__ == '__main__':
    # total_cnt = get_project_list_old(skip=11, limit=5, keyword="insert5")
    total_cnt = 0
    print("__main__ total_cnt: " , total_cnt)  