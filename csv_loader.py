import csv
from langchain_core.documents import Document

def load_csv_data(file_path):
    documents = []
    
    # [중요] 공공데이터 CSV는 'utf-8' 또는 'cp949(euc-kr)' 인코딩이 많습니다.
    # 에러가 나면 encoding='cp949'로 변경해서 시도해보세요.
    try:
        f = open(file_path, 'r', encoding='utf-8')
        reader = csv.DictReader(f)
        # 데이터를 읽으려 시도 (인코딩 체크용)
        next(reader) 
        f.seek(0) # 파일 포인터 초기화
        next(f)   # 헤더 건너뛰기
    except UnicodeDecodeError:
        print("UTF-8 로드 실패, CP949로 재시도합니다.")
        f = open(file_path, 'r', encoding='cp949')
        reader = csv.DictReader(f)

    # csv.DictReader를 통해 행(Row)별로 데이터를 읽습니다.
    for row in reader:
        # 데이터가 비어있는 경우 건너뛰기
        if not row.get('시설명'): 
            continue

        # 1. 검색(LLM)에 제공할 텍스트 구성
        # 단순히 값을 나열하는 것보다, 설명하는 문장 형태로 만드는 것이 RAG 성능에 좋습니다.
        content = (
            f"시설명은 '{row.get('시설명')}'입니다. "
            f"주소는 '{row.get('주소')}'에 위치해 있습니다. "
            f"특징 및 소개: {row.get('소개')}. "
            f"운영시간은 {row.get('운영시간')}이며, "
            f"전화번호는 {row.get('전화번호')}입니다."
        )
        
        # 2. 메타데이터 구성 (출처 표기용)
        metadata = {
            "source": "public_data_csv",
            "name": row.get('시설명'),
            "category": "숙박/캠핑"
        }
        
        # 3. Document 객체 생성
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
    
    f.close()
    return documents

if __name__ == "__main__":
    docs = load_csv_data("data/sample_data.csv")
    print(f"총 {len(docs)}개의 데이터가 로드되었습니다.")
    print("\n--- 첫 번째 데이터 미리보기 ---")
    print(docs[0].page_content)