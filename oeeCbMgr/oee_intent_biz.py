import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from oeeCbMgr.oee_db_conn import EngineConn
from oeeCbMgr.oee_chatbot_models import Intent
from oeeCbMgr.oee_intent_schema  import *

engine = EngineConn()

def get_intent_list(param : IntentSrchParam):
    print("====================intent_biz get_intent_list start==========")
    print("====================intent_biz get_intent_list param: " , param)    

    int_page_num = int(param.page_num) 
    int_page_num=int_page_num-1
    int_page_size = int(param.count_per_page)
    skip = int_page_num * int_page_size

    session  = engine.sessionmaker()
    intent_list_for_totalCnt = session.query(Intent) \
        .filter(
                Intent.company_id == param.company_id,
                Intent.project_id == int(param.project_id)                
                ).all()      
    # total_cnt = session.query(Intent).count()
    total_cnt = len(intent_list_for_totalCnt)     
    print("intent_biz get_intent_list project_cnt: " , total_cnt)    
    print("intent_biz get_intent_list param.intent_id: " , param.intent_id)        
    print("intent_biz get_intent_list param.intent_id.strip(): " , param.intent_id.strip())            

    if ((param.intent_id.strip() )==""):
        result_list = session.query(Intent)
        result_list = result_list \
                .filter(Intent.intent_name.ilike('%' + param.intent_name + '%') ,
                        Intent.required_entity_names.ilike('%' + param.required_entity_names + '%') ,        
                        Intent.company_id == param.company_id ,
                        Intent.project_id == int(param.project_id)
                        )
        result_list = result_list.order_by(Intent.intent_name.asc()) \
                .offset(skip).limit(int_page_size).all()    

    else:
        result_list = session.query(Intent)
        result_list = result_list \
                .filter(                         
                        Intent.company_id == param.company_id ,
                        Intent.project_id == int(param.project_id),
                        Intent.intent_id == int(param.intent_id)                        
                        )
        result_list = result_list.order_by(Intent.intent_name.asc()) \
                .offset(skip).limit(int_page_size).all()    

    print("====================intent_biz get_intent_list  end==========")
    return total_cnt, result_list