import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from uuid import uuid4

# 1. 데이터 로더 함수 임포트 (Step 2 파일에서)
from data_loader_step1 import load_public_data # 파일명을 실제 파일명으로 변경 필요

# 환경변수 로드
load_dotenv()

def ingest_data():
    # 1. 데이터 로드
    docs = load_public_data("data/sample_data.json")
    
    # 2. 임베딩 모델 설정 (OpenAI text-embedding-3-small 등)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 3. Pinecone 인덱스 이름
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    print("Pinecone에 데이터를 업로드 중입니다...")
    
    # 4. 벡터 저장소 생성 및 문서 업로드
    # from_documents를 사용하면 임베딩 변환 및 업로드를 한 번에 처리
    vectorstore = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=index_name
    )
    
    print("업로드 완료!")

if __name__ == "__main__":
    ingest_data()