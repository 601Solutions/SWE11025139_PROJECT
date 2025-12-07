# llm_rag/utils/dog_profile.py

import sqlite3
import os
from typing import Optional, Dict
from pathlib import Path

def get_db_path():
    """
    실제 DB 파일 경로 찾기
    project_root/pet_healthcare.db
    """
    # 1. 스크립트를 실행하는 현재 위치의 절대 경로 (Current Working Directory)
    # 예: SWE11025139_PROJECT
    execution_path = Path.cwd()
    
    print(f"현재 실행 경로(CWD): {execution_path}")

    # 2. 목표 DB 경로 설정 (OS 호환성을 위해 pathlib의 / 연산자 사용)
    # 실행 경로 하위의 Platform -> UI -> pet_healthcare.db
    target_db_path = execution_path / "pet_healthcare.db"
    # 가능한 경로들 (우선순위순)
# 3. 경로 존재 여부 및 테이블 확인
    if target_db_path.exists():
        abs_path = target_db_path.resolve()
        print(f"DB 파일 발견: {abs_path}")
        
        try:
            # dogs 테이블 확인
            conn = sqlite3.connect(str(abs_path))
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogs'")
            has_dogs_table = c.fetchone() is not None
            conn.close()
            
            if has_dogs_table:
                print(f"dogs 테이블 확인됨")
                return str(abs_path)
            else:
                print(f"경고: DB 파일은 있으나 dogs 테이블이 없습니다.")
                return str(abs_path) # 파일은 있으므로 경로는 반환
                
        except Exception as e:
            print(f"DB 연결 중 오류 발생: {e}")
            return None
    else:
        print(f"오류: DB 파일을 찾을 수 없습니다.")
        print(f"탐색 경로: {target_db_path}")
        print("프로젝트 최상위 폴더(SWE11025139_PROJECT)에서 스크립트를 실행했는지 확인해주세요.")
        return None

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
