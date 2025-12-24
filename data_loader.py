import json
from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document

def load_public_data(file_path):
    # 1. JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 필요한 데이터 추출 (공공데이터 구조에 따라 경로가 다름)
    # 예: response -> body -> items
    items = data['response']['body']['items']
    
    documents = []
    for item in items:
        # 3. 검색에 사용할 텍스트 구성 (이름 + 주소 + 소개)
        content = f"시설명: {item['facltNm']}\n주소: {item['addr1']}\n소개: {item['intro']}\n예약방법: {item['resveCl']}"
        
        # 4. 메타데이터와 함께 문서 객체 생성
        doc = Document(
            page_content=content,
            metadata={"source": "public_data", "name": item['facltNm']}
        )
        documents.append(doc)
        
    return documents

if __name__ == "__main__":
    docs = load_public_data("data/sample_data.json")
    print(f"총 {len(docs)}개의 데이터가 로드되었습니다.")
    print(docs[0].page_content)