import os

from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

# .env 파일에서 환경 변수 로드
load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# 읽기 쿼리
result = graph.query("""
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    RETURN p.name AS actor, m.title AS movie
    LIMIT 5
""")

print("영화와 배우 목록:")
for row in result:
    print(f"  - {row['actor']} -> {row['movie']}")

# 매개변수가 있는 쿼리
result = graph.query(
    """
    MATCH (p:Person {name: $name})-[:ACTED_IN]->(m:Movie)
    RETURN m.title AS movie
    """,
    params={"name": "Tom Hanks"},
)

print("Tom Hanks가 출연한 영화:")
for row in result:
    print(f"  - {row['movie']}")
