# 🐶 내 손안의 반려동물 지키미, '찌낌이'

> **SWE11025139_PROJECT** > **LLM + RAG 기반 강아지 헬스케어 서비스**

![Python](https://img.shields.io/badge/Python-3.12.10-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=flat-square)

---
![main](main.png)

## 📖 Introduction

'찌낌이'는 대규모 언어 모델(LLM)과 검색 증강 생성(RAG) 기술을 결합하여 개발된 **강아지 전용 헬스케어 서비스**입니다. 

반려견의 증상을 입력하면 AI가 상태를 분석하여 적절한 조언을 제공하고, 증상에 맞는 의약품을 추천해주는 **맞춤형 복약 지도 시스템**을 통해 소중한 반려동물의 건강을 지켜드립니다.

### ✨ Key Features
* **🩺 AI 건강 상담:** RAG 기술을 활용하여 검증된 수의학 정보를 바탕으로 챗봇 상담을 제공합니다.
* **💊 복약 지도 시스템:** 반려견의 상태와 증상에 따라 최적의 의약품을 추천하고 주의사항을 안내합니다.

---

## 👨‍💻 Team Members

| 이름 | 역할 | 담당 업무 |
|:---:|:---:|:---|
| **정준혁** | Team Lead, PM | 프로젝트 총괄, 기획 및 일정 관리 |
| **전혁건** | Scrum Master, DM | 스크럼 진행, 문서화 및 리포트 관리 |
| **문기준** | Platform Engineer | 서비스 아키텍처 설계 및 백엔드/프론트엔드 구현 |
| **김도원** | LLM Engineer | LLM 튜닝, RAG 파이프라인 구축 및 프롬프트 엔지니어링 |

---

## 🛠️ Tech Stack

### Environment
* **Language:** Python 3.12.10
* **Virtual Env:** venv

### Platform & Framework
* **Frontend:** Streamlit
* **Backend:** FastAPI

### Database & AI
* **Vector DB:** ChromaDB
* **RDBMS:** SQLite
* **Technique:** RAG (Retrieval-Augmented Generation), LLM

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.12.10** 버전이 설치되어 있어야 합니다.

### 2. Installation

Repository를 클론하고 프로젝트 폴더로 이동합니다.
```bash
git clone [레포지토리 URL을 입력하세요]
cd [프로젝트 폴더명]
```

가상 환경(Virtual Environment)을 생성하고 활성화합니다.

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
```

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

필요한 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

### 3. Run Application
#### Backend (FastAPI) 실행
```bash
python3 main.py
```
#### Frontend (Streamlit) 실행
```bash
streamlit run main_ui.py
```
