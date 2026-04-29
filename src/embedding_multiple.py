import os

from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

load_dotenv()


# 환경 변수 로드
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 여러 텍스트를 한 번에 임베딩
texts = [
    "오늘 날씨가 정말 좋습니다.",
    "화창한 하늘이 아름답네요.",
    "파이썬 프로그래밍을 배우고 있습니다.",
    "맛있는 저녁을 먹었습니다.",
]

# embed_documents는 여러 텍스트를 한 번에 처리
vectors = hf_embeddings.embed_documents(texts)

print(f"입력 텍스트 수: {len(texts)}")
print(f"벡터 수: {len(vectors)}")
print(f"각 벡터의 차원: {len(vectors[0])}")
