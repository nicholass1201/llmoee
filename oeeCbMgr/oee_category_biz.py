from oee_db_conn import EngineConn
from oee_chatbot_models import Category
from oee_category_schema import *

engine = EngineConn()

def get_category_list(param : CategorySrchParam):
    print("====================category_biz get_category_list start==========")

    int_page_num = int(param.page_num) 
    int_page_num=int_page_num-1
    int_page_size = int(param.count_per_page)
    skip = int_page_num * int_page_size

    session  = engine.sessionmaker()
    total_cnt = session.query(Category).count()
    print("category_biz get_category_list project_cnt: " , total_cnt)    

    result_list = session.query(Category)

    sParent_category_id = param.parent_category_id
    sCategory_id = param.category_id    
    if ((str(sParent_category_id).strip() )!=""):    
        result_list = result_list \
                .filter(
                        Category.company_id == param.company_id ,
                        Category.project_id == int(param.project_id),
                        Category.parent_category_id == int(param.parent_category_id),
                        Category.category_name.ilike('%' + param.category_name + '%') ,                        
                        )

    elif ((str(sCategory_id).strip() )!=""):
        result_list = result_list \
                .filter(
                        Category.company_id == param.company_id ,
                        Category.project_id == int(param.project_id),
                        Category.category_id == int(param.category_id)                
                        )

    else:
        result_list = result_list \
                .filter(Category.category_name.ilike('%' + param.category_name + '%') ,
                        Category.company_id == param.company_id ,
                        Category.project_id == int(param.project_id),
                        )
    if (param.order_type=="asc"):    
        result_list = result_list.order_by(Category.category_name.asc()) \
                .offset(skip).limit(int_page_size).all()    
    elif (param.order_type=="desc"):    
        result_list = result_list.order_by(Category.category_name.desc()) \
                .offset(skip).limit(int_page_size).all()    


    print("====================category_biz get_category_list  end==========")
    return total_cnt, result_list