import psycopg2
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"

llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url=model_url,
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=None,
    temperature=0.1,
    max_new_tokens=256,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": 1},
    verbose=True,
)

db_name = "vector_db"
host = "105.53.140.229"
password = "amsdi$01"
port = "5432"
user = "vector_user"

conn = psycopg2.connect( user=user, password=password,host=host,port=port, database="postgres" )
conn.autocommit = True

fwith conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore

vector_score = PGVectorStore.from_params(
    database=db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="llama2_paper",
    embed_dim=384
)    

from pathlib import Path
from llama_index.readers.file import PyMuPDFReader

loader = PyMuPDFReader()
documents = loader.load(file_path="./data/llama2.pdf")

from llama_index.core.node_parser import SentenceSplitter

text_parser = SentenceSplitter( chunk_size=1024 )

text_chunks = []
doc_idxs = []

for doc_idx, doc in enumerate(documents):
    cur_text_chunks = text_parser.split_text( doc.text )
    text_chunks.extend(cur_text_chunks)
    doc_idxs.extend([doc_idx]*len(cur_text_chunks))

from llama_index.core.schema import TextNode

nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(
        text=text_chunk,
    )
    src_doc = documents[doc_idxs[idx]]
    node.metadata = src_doc.metadata
    nodes.append(node)

for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding

vector_score.add(nodes)

query_str = "Can you tell me about the key concepts for safety finetuning"
query_embedding = embed_model.get_query_embedding(query_str)

from llama_index.core.vector_stores import VectorStoreQuery
query_mode = "default"

vector_store_query = VectorStoreQuery(
    query_embedding=query_embedding, similarity_top_k=2, mode=query_mode
)

query_result = vector_score.query( vector_store_query )

from llama_index.core.schema import NodeWithScore
from typing import Optional

# https://docs.llamaindex.ai/en/stable/examples/low_level/oss_ingestion_retrieval.html