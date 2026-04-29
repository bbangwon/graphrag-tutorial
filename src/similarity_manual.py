import os

import numpy as np
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

# 환경 변수 로드
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"


def cosine_similarity(vec1, vec2):
    """두 벡터의 코사인 유사도 계산"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# 임베딩 모델 초기화
hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 테스트 문장들
sentences = [
    "오늘 날씨가 정말 좋습니다.",
    "화창한 하늘이 아름답네요.",
    "파이썬 프로그래밍을 배우고 있습니다.",
    "비가 많이 내립니다.",
]

# 모든 문장 임베딩
vectors = hf_embeddings.embed_documents(sentences)

# 첫번째 문장과 나머지 비교
print("기준: ", sentences[0])
print("-" * 50)

for i in range(1, len(sentences)):
    similarity = cosine_similarity(vectors[0], vectors[i])
    print(f"{sentences[i]}")
    print(f"       -> 유사도: {similarity:.4f}")
    print()
