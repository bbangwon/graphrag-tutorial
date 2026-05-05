from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

driver = GraphDatabase.driver(URI, auth=AUTH)


def create_person(tx, name, born):
    query = """
    MERGE (p:Person {name: $name})
    ON CREATE SET p.born = $born
    RETURN p    
    """
    result = tx.run(query, name=name, born=born)
    return result.single()


# 쓰기는 execute_write로 실행
with driver.session() as session:
    result = session.execute_write(create_person, "테스트인물", 2000)
    print(f"생성됨: {result}")

driver.close()
