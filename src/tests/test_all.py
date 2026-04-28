import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from neo4j import GraphDatabase

# 환경변수 로드
load_dotenv()

print("=" * 50)
print("GraphRAG 환경 통합 테스트")
print("=" * 50)

# 1. Noe4j 연결 테스트
print("\n[1] Neo4j 연결 테스트")
try:
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")),
    )
    driver.verify_connectivity()
    print("Neo4j 연결 성공!")
    driver.close()
except Exception as e:
    print(f"Neo4j 연결 실패: {e}")

# 2 OpenAI 연결 테스트
print("\n[2] OpenAI 연결 테스트")
try:
    llm = ChatOpenAI(
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )
    response = llm.invoke("1+1=?")
    print(f"LLM 응답: {response}")
except Exception as e:
    print(f"LLM 연결 실패: {e}")

# 3 HuggingFace 임베딩 테스트
print("\n[3] HuggingFace 임베딩 테스트")
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="dragonkue/snowflake-arctic-embed-l-v2.0-ko"
    )
    vector = embeddings.embed_query("테스트")
    print(f"임베딩 생성 성공! (차원: {len(vector)})")
except Exception as e:
    print(f"임베딩 생성 실패: {e}")

# 4. LangChain + Neo4j 통합 테스트
print("\n[4] LangChain + Neo4j 통합 테스트")
try:
    from langchain_neo4j import Neo4jGraph

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USER"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    # 스키마 정보 조회
    schema = graph.get_schema
    print("Neo4j Graph 연결 성공!")
    print(f"현재 스키마: {schema[:100]}..." if schema else "스키마: 비어있음")
except Exception as e:
    print(f"통합 실패: {e}")

print("\n" + "=" * 50)
print("테스트 완료!")
print("=" * 50)
