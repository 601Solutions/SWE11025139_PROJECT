#====================================================
# Author: 601 Solutions
# Title: main.py
# FastAPI를 통한 http 통신 형식 및 규범 정의
#====================================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from typing import Optional, List
from contextlib import asynccontextmanager

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels to reach project root
sys.path.append(project_root)

# Now we can import from LLM directory
from LLM.llm_rag.retriver.retriever import get_rag_retriever
from LLM.llm_rag.llm.llm_response import generate_response
from LLM.llm_rag.utils.dog_profile import get_dog_profile, format_dog_profile_for_prompt
from LLM.llm_rag import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행되는 lifespan 핸들러"""
    # 시작 시 실행
    print("Retriever 초기화 중...")
    try:
        retriever = get_rag_retriever()
        if retriever is None:
            raise RuntimeError("Retriever 초기화 실패!")
        app.state.retriever = retriever  # app.state에 저장
        print("Retriever 준비 완료!")
    except Exception as e:
        print(f"초기화 실패: {e}")
        raise
    
    yield
    
    # 종료 시 실행 (필요시)
    print("리소스 정리 중...")

# FastAPI 앱 초기화
app = FastAPI(
    title="펫 헬스케어 AI 챗봇 API",
    description="RAG 기반 반려동물 건강 상담 챗봇 (개인화 지원)",
    version="2.0.0",
    lifespan=lifespan  # lifespan 핸들러 등록
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Pydantic 모델 =====

class MessageRequest(BaseModel):
    """사용자 질문 요청 (강아지 정보 포함)"""
    message: str
    owner_id: Optional[int] = None  # 사용자 ID (강아지 정보 조회용)
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "우리 강아지 관절에 좋은 영양제 추천해주세요",
                "owner_id": 1
            }
        }


class MessageResponse(BaseModel):
    """AI 응답"""
    message: str
    retrieved_docs: Optional[int] = None
    dog_name: Optional[str] = None  # 강아지 이름


class DetailedResponse(BaseModel):
    """상세 응답"""
    answer: str
    retrieved_documents: List[dict]
    question: str
    dog_profile: Optional[dict] = None  # 강아지 프로필 정보


# ===== API 엔드포인트 =====

@app.get("/")
async def get_root(request: Request):
    return {
        "status": "running",
        "retriever_initialized": hasattr(request.app.state, "retriever"),
        "message": "펫 헬스케어 AI 챗봇 API 서버"
    }

@app.post("/conversation", response_model=MessageResponse)
async def post_message(request_data: MessageRequest, request: Request):
    """사용자 질문에 대한 AI 응답 생성"""
    print(f"받은 질문: {request_data.message}")
    print(f"Owner ID: {request_data.owner_id}")
    
    # app.state에서 retriever 가져오기
    if not hasattr(request.app.state, "retriever"):
        raise HTTPException(
            status_code=503, 
            detail="Retriever가 초기화되지 않았습니다. 서버를 재시작해주세요."
        )
    
    retriever = request.app.state.retriever
    
    try:
        # 1. 강아지 프로필 가져오기
        dog_profile_dict = None
        dog_profile_text = ""
        dog_name = None
        
        if request_data.owner_id:
            dog_profile_dict = get_dog_profile(request_data.owner_id)
            if dog_profile_dict:
                dog_profile_text = format_dog_profile_for_prompt(dog_profile_dict)
                dog_name = dog_profile_dict.get('name', 'My Dog')
                print(f"강아지 정보 로드: {dog_name}")
        
        # 2. 관련 문서 검색
        print("문서 검색 중...")
        retrieved_docs = retriever.invoke(request_data.message)
        print(f"{len(retrieved_docs)}개 문서 검색 완료")
        
        # 3. Context 생성
        context = "\n\n".join([doc.page_content for doc in retrieved_docs[:5]])
        
        # 4. LLM 응답 생성
        print("AI 응답 생성 중...")
        answer = generate_response(
            context=context,
            question=request_data.message,
            dog_profile=dog_profile_text
        )
        print("응답 생성 완료")
        
        return {
            "message": answer,
            "retrieved_docs": len(retrieved_docs),
            "dog_name": dog_name
        }
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"응답 생성 중 오류: {str(e)}")

@app.post("/conversation/detailed", response_model=DetailedResponse)
async def post_message_detailed(request_data: MessageRequest, request: Request):
    """상세 응답"""
    print(f"받은 질문: {request_data.message}")
    
    # app.state에서 retriever 가져오기
    if not hasattr(request.app.state, "retriever"):
        raise HTTPException(
            status_code=503, 
            detail="Retriever가 초기화되지 않았습니다."
        )
    
    retriever = request.app.state.retriever
    
    try:
        # 1. 강아지 프로필 가져오기
        dog_profile_dict = None
        dog_profile_text = ""
        
        if request_data.owner_id:
            dog_profile_dict = get_dog_profile(request_data.owner_id)
            if dog_profile_dict:
                dog_profile_text = format_dog_profile_for_prompt(dog_profile_dict)
                print(f"강아지 정보 로드: {dog_profile_dict['name']}")
        
        # 2. 문서 검색
        print("문서 검색 중...")
        retrieved_docs = retriever.invoke(request_data.message)
        
        # 3. Context 생성
        context = "\n\n".join([doc.page_content for doc in retrieved_docs[:5]])
        
        # 4. LLM 응답 생성
        print("AI 응답 생성 중...")
        answer = generate_response(
            context=context,
            question=request_data.message,
            dog_profile=dog_profile_text
        )
        
        # 5. 문서 정보 포맷팅
        doc_list = [
            {
                "content": doc.page_content[:500],
                "metadata": doc.metadata
            }
            for doc in retrieved_docs[:5]
        ]
        
        return {
            "answer": answer,
            "retrieved_documents": doc_list,
            "question": request_data.message,
            "dog_profile": dog_profile_dict
        }
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"응답 생성 중 오류: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("펫 헬스케어 AI 챗봇 API 서버 v2.0")
    print("=" * 60)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
