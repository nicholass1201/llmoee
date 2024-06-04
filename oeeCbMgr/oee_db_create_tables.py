from oee_db_conn import EngineConn
import oee_chatbot_models as models

engine_conn = EngineConn()
engine = engine_conn.engine

print( models.Base )
models.Base.metadata.create_all(bind=engine)