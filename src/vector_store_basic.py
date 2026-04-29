import os

from dotenv import load_dotenv
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

load_dotenv()

# 임베딩 모델
HF_TOKEN = os.getenv("HF_TOKEN")
model_name = "dragonkue/snowflake-arctic-embed-l-v2.0-ko"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name, huggingfacehub_api_token=HF_TOKEN
)

# 벡터 저장소 생성
vector_store = InMemoryVectorStore(hf_embeddings)

# 문서 추가
documents = [
    "세종대왕은 한글을 창제한 조선의 왕입니다.",
    "이순신 장군은 임진왜란에서 왜군을 물리쳤습니다.",
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "서울은 대한민국의 수도입니다.",
    "김치는 한국의 전통 발효 음식입니다.",
    "훈민정음은 1443년에 창제되었습니다.",
]

vector_store.add_texts(documents)
print(f"총 문서 수: {len(documents)}")

# 검색
query = "한글을 만든 왕은 누구인가요?"
results = vector_store.similarity_search_with_score(query, k=3)

print(f"\n질문: {query}\n")
for i, (doc, score) in enumerate(results, 1):
    print(f"{i}. {doc.page_content} (유사도: {score:.4f})")
