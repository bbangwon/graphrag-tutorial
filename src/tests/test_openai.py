# OpenAI API 연결 테스트 코드

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

llm = ChatOpenAI(base_url=OPENAI_API_BASE, api_key="", temperature=0)

response = llm.invoke("안녕하세요! 한 문장으로 자기소개 해주세요.")
print("응답: ", response.content)
