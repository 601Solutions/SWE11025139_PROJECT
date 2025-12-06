import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# test_llm.py가 있는 경로를 path에 추가하여 임포트 가능하게 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 테스트 대상 함수 임포트
from test_llm import interactive_mode

@pytest.fixture
def mock_dependencies():
    """
    외부 의존성(Retriever, LLM Response)을 Mocking하는 Fixture
    """
    with patch('test_llm.get_rag_retriever') as mock_get_retriever, \
         patch('test_llm.generate_response') as mock_gen_response:
        
        # 1. Retriever가 반환할 가짜 문서 객체 설정
        mock_retriever_instance = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "강아지 관절에는 글루코사민이 좋습니다."
        mock_retriever_instance.invoke.return_value = [mock_doc]
        
        mock_get_retriever.return_value = mock_retriever_instance
        
        # 2. LLM이 반환할 가짜 답변 설정
        mock_gen_response.return_value = "AI 답변: 글루코사민 제품을 추천합니다."
        
        yield mock_get_retriever, mock_gen_response

def test_interactive_mode_flow(mock_dependencies):
    """
    시나리오: 사용자가 질문을 1회 입력하고 답변을 받은 뒤 종료하는 흐름 테스트
    """
    mock_get_retriever, mock_gen_response = mock_dependencies
    
    # input() 함수가 호출될 때마다 반환할 값의 리스트 (순서대로)
    # 첫 번째 호출: 질문 입력 / 두 번째 호출: 종료 명령어
    user_inputs = ["강아지 관절 영양제 추천", "quit"]
    
    with patch('builtins.input', side_effect=user_inputs) as mock_input, \
         patch('builtins.print') as mock_print:
        
        # 테스트 대상 함수 실행
        interactive_mode()
        
        # [검증 1] input이 정확히 2번 호출되었는지 확인
        assert mock_input.call_count == 2
        
        # [검증 2] RAG 파이프라인(답변 생성)이 1번 실행되었는지 확인 (quit 입력 시는 실행 안 됨)
        mock_gen_response.assert_called_once()
        
        # [검증 3] 생성된 답변이 출력되었는지 확인 (print 호출 인자 검사)
        # 모든 print 호출 중 우리가 기대한 답변이 포함되어 있는지 확인
        printed_args = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert any("AI 답변: 글루코사민 제품을 추천합니다." in str(arg) for arg in printed_args)

def test_interactive_mode_exit_immediately(mock_dependencies):
    """
    시나리오: 시작하자마자 'exit'를 입력하여 즉시 종료하는지 테스트
    """
    mock_get_retriever, mock_gen_response = mock_dependencies
    
    with patch('builtins.input', side_effect=["exit"]):
        interactive_mode()
        
        # 질문을 하지 않았으므로 생성 함수는 호출되지 않아야 함
        mock_gen_response.assert_not_called()

def test_interactive_mode_empty_input(mock_dependencies):
    """
    시나리오: 빈 값(엔터)을 입력했을 때 에러 없이 다시 입력을 받는지 테스트
    """
    mock_get_retriever, mock_gen_response = mock_dependencies
    
    # 빈 문자열 -> 질문 -> 종료
    user_inputs = ["", "고양이 사료는?", "quit"]
    
    with patch('builtins.input', side_effect=user_inputs):
        interactive_mode()
        
        # 빈 입력은 무시되고 유효한 질문 1개에 대해서만 응답 생성 호출
        assert mock_gen_response.call_count == 1    