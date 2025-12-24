import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 환경설정 로드
load_dotenv()

def run_rag_system(question):
    # 1. LLM 및 임베딩 모델 설정
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 2. Pinecone Vector Store 연결 (이미 데이터가 업로드된 상태)
    index_name = os.getenv("PINECONE_INDEX_NAME")
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    
    # 3. Retriever(검색기) 설정
    # k=3 : 가장 유사한 문서 3개를 가져옴
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 4. 프롬프트 템플릿 작성 (System Prompt)
    template = """
    당신은 공공데이터 기반의 친절한 안내원입니다.
    아래의 [Context]를 바탕으로 사용자의 질문에 답변하세요.
    정보가 없다면 "제공된 데이터에는 해당 정보가 없습니다"라고 정중히 말하세요.
    
    [Context]
    {context}
    
    질문: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 5. LangChain 파이프라인 구축 (LCEL 문법)
    # chain = (검색 -> 프롬프트 주입 -> LLM -> 문자열 변환)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 6. 실행 및 결과 출력
    print(f"\n[질문]: {question}")
    print("[답변 생성 중...]")
    response = chain.invoke(question)
    print(f"[답변]: {response}\n")

if __name__ == "__main__":
    # 테스트 질문
    user_question = "부산에 있는 캠핑장이나 숙소 좀 추천해줘. 오션뷰였으면 좋겠어."
    run_rag_system(user_question)