import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print("======sys admin path: ", os.path.dirname(__file__) )
print("======sys admin path: ", os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from oeeCbMgr.oee_db_conn import EngineConn
import oee_sys_admin_models as models

engine_conn = EngineConn()
engine = engine_conn.engine

print( models.Base )
models.Base.metadata.create_all(bind=engine)