import os

from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()  # .env 파일에서 환경 변수 로드

# Neo4j 연결 (환경 변수 또는 직접 지정)
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# 스키마 확인
print("데이터 베이스 스키마:")
print(graph.schema)
