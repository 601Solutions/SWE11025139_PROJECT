# llm_rag/utils/dog_profile.py

import sqlite3
import os
from typing import Optional, Dict
from pathlib import Path

def get_db_path():
    """
    실제 DB 파일 경로 찾기
    Platform/API/proto/pet_healthcare.db
    """
    current_file = Path(__file__)
    
    # 가능한 경로들 (우선순위순)
    possible_paths = [
        # 1. UI 폴더의 DB (진짜 DB)
        current_file.parent.parent.parent.parent / "Platform" / "UI" / "pet_healthcare.db",
        
        # 2. UI 폴더의 DB
        current_file.parent.parent.parent.parent / "Platform" / "UI" / "pet_healthcare.db",
        
        # 3. 현재 작업 디렉토리 기준
        Path.cwd() / "UI" / "pet_healthcare.db",
        Path.cwd() / "pet_healthcare.db",
        
    ]
    
    for path in possible_paths:
        if path.exists():
            abs_path = path.resolve()
            print(f"DB 파일 발견: {abs_path}")
            
            # dogs 테이블 확인
            try:
                conn = sqlite3.connect(str(abs_path))
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogs'")
                has_dogs_table = c.fetchone() is not None
                
                if has_dogs_table:
                    print(f"dogs 테이블 확인됨")
                    conn.close()
                    return str(abs_path)
                else:
                    print(f"dogs 테이블 없음, 다음 경로 확인...")
                    conn.close()
            except Exception as e:
                print(f"DB 확인 중 오류: {e}")
                continue
    
    # 기본값 (proto 폴더)
    default_path = Path("proto/pet_healthcare.db")
    print(f"DB를 찾지 못함. 기본 경로 사용: {default_path}")
    return str(default_path)

DB_PATH = get_db_path()

def get_dog_profile(owner_id: int) -> Optional[Dict]:
    """
    강아지 프로필 정보 가져오기
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT name, breed, age, weight, health
        FROM dogs
        WHERE owner_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (owner_id,))
    
    result = c.fetchone()
    conn.close()
    
    if result is None:
        return None
    
    return {
        "name": result[0],
        "breed": result[1],
        "age": result[2],
        "weight": result[3],
        "health": result[4]
    }


def format_dog_profile_for_prompt(profile: Dict) -> str:
    """
    강아지 프로필을 프롬프트용 텍스트로 변환
    """
    if not profile:
        return ""
    
    profile_text = f"""
반려견 정보:
- 이름: {profile['name']}
- 견종: {profile['breed']}
- 나이: {profile['age']}세
- 체중: {profile['weight']}kg
"""

    if profile.get('health'):
        profile_text += f"- 건강: {profile['health']}\n"

    return profile_text.strip()
