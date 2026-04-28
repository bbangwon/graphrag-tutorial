# 임베딩 모델 테스트 코드
import os

from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 테스트 텍스트
text = "GraphRAG는 그래프와 RAG를 결합한 기술입니다."

# 임베딩 생성
vector = hf_embeddings.embed_query(text)

print(f"임베딩 차원 : {len(vector)}")
print(f"처음 5개 값 : {vector[:5]}")
