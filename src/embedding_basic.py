import os

from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

# 환경 변수 로드
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 텍스트를 임베딩으로 변환
text = "오늘 날씨가 정말 좋습니다."
vector = hf_embeddings.embed_query(text)

# 결과 확인
print(f"입력 텍스트: {text}")
print(f"임베딩 차원: {len(vector)}")
print(f"처음 5개 값: {vector[:5]}")
