
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정: 모든 출처에서 오는 요청을 허용합니다.
# 이렇게 하면 로컬에서 파일을 직접 여는 file:// 프로토콜에서도 API 요청이 가능해집니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 랭킹 데이터를 저장할 파일
RANKING_FILE = "ranking.json"

# 요청 본문의 형식을 정의합니다 (플레이어 이름과 점수).
class ScoreItem(BaseModel):
    name: str
    score: float

def read_ranking():
    """ranking.json 파일에서 랭킹 데이터를 읽어옵니다."""
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_ranking(data):
    """랭킹 데이터를 ranking.json 파일에 저장합니다."""
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.post("/add_score")
def add_score(item: ScoreItem):
    """게임에서 새로운 점수를 받아 랭킹에 추가합니다."""
    ranking = read_ranking()
    
    # 새 점수 추가
    ranking.append({"name": item.name, "score": int(item.score)})
    
    # 점수를 기준으로 내림차순 정렬
    ranking.sort(key=lambda x: x["score"], reverse=True)
    
    # 상위 100명만 저장 (원하는 만큼 조절 가능)
    write_ranking(ranking[:100])
    
    return {"message": "Score added successfully"}

@app.get("/get_ranking")
def get_ranking():
    """저장된 랭킹 데이터를 반환합니다."""
    return read_ranking()

# 서버를 실행하려면 터미널에 uvicorn server:app --reload 라고 입력하세요.
