# 간단한 데이터 추가 테스트

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    # 노드 생성
    session.run("""
                CREATE (p:Person {name: '김철수', age: 30})
                CREATE (c:Company {name: 'AI 스타트업'})
                CREATE (p)-[:WORKS_AT]->(c)                
                """)
    print("데이터 추가 완료!")

    # 데이터 조회
    result = session.run("""
                MATCH (p:Person)-[:WORKS_AT]->(c:Company)
                RETURN p.name AS person, c.name AS company
                """)

    for record in result:
        print(f"{record['person']}님은 {record['company']}에서 근무합니다.")

driver.close()
