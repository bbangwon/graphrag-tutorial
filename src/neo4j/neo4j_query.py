from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

driver = GraphDatabase.driver(URI, auth=AUTH)


# 읽기 쿼리 실행
def get_movies(tx, limit=5):
    query = """
    MATCH (m:Movie)
    RETURN m.title AS title, m.released AS year
    LIMIT $limit
    """
    result = tx.run(query, limit=limit)
    return [{"title": record["title"], "year": record["year"]} for record in result]


# 세션으로 실행
with driver.session() as session:
    movies = session.execute_read(get_movies, limit=5)

    print("영화 목록:")
    for movie in movies:
        print(f"  - {movie['title']} ({movie['year']})")

# 드라이버 종료
driver.close()
