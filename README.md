# RAG Demo 프로젝트

이 프로젝트는 LangChain을 활용한 RAG(Retrieval-Augmented Generation) 시스템 데모입니다.

## 프로젝트 구조

```
Rag Demo/
├── main.py                    # ChromaDB를 사용한 기본 RAG 예제
├── main_rag.py               # Pinecone을 사용한 RAG 예제
├── ingest_data.py            # 데이터 수집 및 벡터 DB 업로드
├── data_loader.py            # 기본 데이터 로더
├── data_loader_universal.py  # 범용 데이터 로더 (JSON, XML, CSV 지원)
├── csv_loader.py             # CSV 전용 로더
├── data/                     # 데이터 파일 디렉토리
├── data.txt                  # 샘플 텍스트 데이터
├── requirements.txt          # Python 패키지 의존성
└── README.md                 # 프로젝트 설명서
```

## 사전 요구사항

- Python 3.8 이상
- Git

## 설치 및 설정 절차

### 1. 저장소 클론 (또는 Pull)

```bash
git clone <저장소 URL>
cd "Rag Demo"
```

또는 기존 저장소를 업데이트하는 경우:

```bash
git pull origin main
```

### 2. 가상 환경(Virtual Environment) 생성

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. 가상 환경 활성화

**Windows (Git Bash 또는 PowerShell):**
```bash
source venv/Scripts/activate
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

활성화가 성공하면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.

### 4. 필요한 라이브러리 설치

가상 환경이 활성화된 상태에서 다음 명령어를 실행합니다:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 API 키를 설정합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_index_name_here
```

**주의:** `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다. 각 개발자는 자신의 API 키를 별도로 설정해야 합니다.

## 사용 방법

### 기본 RAG 예제 실행 (ChromaDB 사용)

```bash
python main.py
```

### Pinecone을 사용한 RAG 예제 실행

```bash
python main_rag.py
```

### 데이터 수집 및 벡터 DB 업로드

```bash
python ingest_data.py
```

## 가상 환경 비활성화

작업이 끝난 후 가상 환경을 비활성화하려면:

```bash
deactivate
```

## 문제 해결

### 가상 환경 활성화가 안 되는 경우

- Python이 올바르게 설치되어 있는지 확인: `python --version`
- venv 모듈이 설치되어 있는지 확인: `python -m venv --help`
- 가상 환경이 제대로 생성되었는지 확인: `ls venv` (macOS/Linux) 또는 `dir venv` (Windows)

### 라이브러리 설치 오류

- pip가 최신 버전인지 확인: `pip install --upgrade pip`
- 인터넷 연결 확인
- 특정 패키지 설치 오류 시 해당 패키지의 공식 문서 확인

### API 키 관련 오류

- `.env` 파일이 프로젝트 루트에 있는지 확인
- 환경 변수 이름이 정확한지 확인 (대소문자 구분)
- API 키가 유효한지 확인

## 참고 사항

- 이 프로젝트는 `venv` 폴더를 Git에서 제외하도록 설정되어 있습니다.
- 각 개발자는 로컬에서 가상 환경을 생성하고 필요한 라이브러리를 설치해야 합니다.
- `requirements.txt` 파일을 업데이트한 경우, 다른 개발자들에게 알려주고 `git pull` 후 `pip install -r requirements.txt`를 다시 실행하도록 안내하세요.

