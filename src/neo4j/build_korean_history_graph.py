import os

from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()  # .env 파일에서 환경 변수 로드

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD"),
)
# 데이터 정의
people = [
    {"name": "세종대왕", "born": 1397, "died": 1450, "role": "왕"},
    {"name": "장영실", "born": 1390, "role": "과학자"},
    {"name": "신숙주", "born": 1417, "died": 1475, "role": "학자"},
    {"name": "정조", "born": 1752, "died": 1800, "role": "왕"},
    {"name": "정약용", "born": 1762, "died": 1836, "role": "학자"},
]

achievements = [
    {"name": "훈민정음", "year": 1443, "type": "문자"},
    {"name": "측우기", "year": 1441, "type": "발명"},
    {"name": "수원화성", "year": 1796, "type": "건축"},
]

organizations = [
    {"name": "집현전", "type": "학술기관"},
    {"name": "규장각", "type": "학술기관"},
]

# 인물 생성
for person in people:
    graph.query(
        """
        MERGE (p:Person {name: $name})
        SET p.born = $born,
            p.died = $died,
            p.role = $role
        """,
        params={
            "name": person["name"],
            "born": person.get("born"),
            "died": person.get("died"),
            "role": person.get("role"),
        },
    )

print(f"{len(people)}명의 인물이 생성되었습니다.")

# 업적 생성
for ach in achievements:
    graph.query(
        """
    MERGE (a:Achievement {name: $name})
    SET a.year = $year, a.type = $type
    """,
        params=ach,
    )

print(f"{len(achievements)}개의 업적이 생성되었습니다.")

# 기관 생성
for org in organizations:
    graph.query(
        """
    MERGE (o:Organization {name: $name})
    SET o.type = $type
    """,
        params=org,
    )

print(f"{len(organizations)}개의 기관이 생성되었습니다.")

# 관계 생성
relationships = [
    ("세종대왕", "CREATED", "훈민정음"),
    ("세종대왕", "ESTABLISHED", "집현전"),
    ("세종대왕", "COLLABORATED_WITH", "장영실"),
    ("장영실", "INVENTED", "측우기"),
    ("신숙주", "WORKED_AT", "집현전"),
    ("정조", "ESTABLISHED", "규장각"),
    ("정조", "ORDERED", "수원화성"),
    ("정조", "APPOINTED", "정약용"),
    ("정약용", "WORKED_AT", "규장각"),
]

for source, rel_type, target in relationships:
    graph.query(
        f"""
    MATCH (a {{name: $source}})
    MATCH (b {{name: $target}})
    MERGE (a)-[:{rel_type}]->(b)
""",
        params={"source": source, "target": target},
    )

print(f"{len(relationships)}개의 관계가 생성되었습니다.")
print("한국 역사 그래프가 성공적으로 구축되었습니다.")

# 세종대왕 관련 모든 정보
result = graph.query("""
    MATCH (sejong:Person {name: "세종대왕"})-[r]->(related)
    RETURN type(r) AS 관계, labels(related) AS 유형, related.name AS 대상
""")

print("세종대왕과 관련된 정보:")
for row in result:
    print(f"  - 관계: {row['관계']}, 유형: {row['유형']}, 대상: {row['대상']}")

# 2단계 관계 탐색
result = graph.query("""
    MATCH (sejong:Person {name: "세종대왕"})-[:ESTABLISHED]->(org:Organization)<-[:WORKED_AT]-(scholar:Person)
    RETURN org.name AS 기관, scholar.name AS 학자
""")

print("세종대왕이 설립한 기관에서 일한 학자:")
for row in result:
    print(f"  - 기관: {row['기관']}, 학자: {row['학자']}")
