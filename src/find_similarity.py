import os

import numpy as np
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"


def cosine_similarity(vec1, vec2):
    """두 벡터의 코사인 유사도 계산"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 문서 데이터베이스 (실제로는 파일이나 DB에서 로드)

documents = [
    "세종대왕은 한글을 창제한 조선의 왕입니다.",
    "이순신 장군은 임진왜란에서 왜군을 물리쳤습니다.",
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "서울은 대한민국의 수도입니다.",
    "김치는 한국의 전통 발효 음식입니다.",
    "훈민정음은 1443년에 창제되었습니다.",
]

# 모든 문서 임베딩 (미리 계산)
doc_vectors = hf_embeddings.embed_documents(documents)


# 검색 함수
def search(query, top_k=3):
    """질문과 가장 비슷한 문서 top_k개 반환"""
    query_vector = hf_embeddings.embed_query(query)

    # 모든 문서와 유사도 계산
    similaritys = []
    for i, doc_vec in enumerate(doc_vectors):
        sim = cosine_similarity(query_vector, doc_vec)
        similaritys.append((i, sim))

    # 유사도 순으로 정렬
    similaritys.sort(key=lambda x: x[1], reverse=True)

    # 상위 k개 반환
    results = []
    for idx, sim in similaritys[:top_k]:
        results.append(
            {
                "document": documents[idx],
                "similarity": sim,
            }
        )

    return results


# 테스트
query = "한글을 만든 왕은 누구인가요?"
print(f"질문: {query}\n")

results = search(query, top_k=3)
for i, result in enumerate(results):
    print(f"{i}. [{result['similarity']:.4f}] {result['document']}")
