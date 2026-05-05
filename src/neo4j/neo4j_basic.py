"""neo4j 기본 연결"""

from neo4j import GraphDatabase

# 연결 정보
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")  # 사용자 이름과 비밀번호

# 드라이버 생성
driver = GraphDatabase.driver(URI, auth=AUTH)

# 연결 확인
driver.verify_connectivity()
print("Neo4j 연결 성공!")

# 드라이버 종료
driver.close()
