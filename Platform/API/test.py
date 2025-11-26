#====================================================
# Author: 601 Solutions
# Title: API_test_case.py
# FastAPI 테스트케이스 코드
#====================================================

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

