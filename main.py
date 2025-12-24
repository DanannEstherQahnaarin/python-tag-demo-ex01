import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def run_rag():
    if not os.path.exists("data.txt"):
        with open("data.txt", "w", encoding="utf-8") as f:
            f.write("랭체인은 LLM 애플리케이션을 개발하기 위한 프레임워크입니다.")
    
    loader = TextLoader("data.txt", encoding="utf-8")
    docs = loader.load()
    
    # 3. 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    # 4. 벡터 DB 생성
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=OpenAIEmbeddings()
    )

    # 5. RAG 체인 구성
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    prompt = ChatPromptTemplate.from_template("""
    아래 문맥만을 사용하여 질문에 답하세요:
    {context}
    
    질문: {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    # 6. 실행
    response = rag_chain.invoke({"input": "랭체인이 뭐야?"})
    print(f"\nAI 답변: {response['answer']}")

if __name__ == "__main__":
    run_rag()