import json
import csv
import requests
import xmltodict
from langchain_core.documents import Document

class UniversalDataLoader:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'} # API 호출 시 차단 방지

    def load_data(self, source, source_type='file', data_format='json', root_key=None):
        """
        source: 파일 경로 또는 API URL
        source_type: 'file' 또는 'api'
        data_format: 'json', 'xml', 'csv'
        root_key: 데이터 리스트가 위치한 키 경로 (예: 'response.body.items.item')
        """
        raw_data = None
        
        # 1. 데이터 가져오기 (Fetch)
        if source_type == 'api':
            print(f"[API 요청] {source}")
            try:
                res = requests.get(source, headers=self.headers)
                res.raise_for_status()
                # API는 텍스트로 받아서 처리
                raw_data = res.text 
            except Exception as e:
                print(f"API 요청 실패: {e}")
                return []
        else:
            # 파일 읽기
            print(f"[파일 로드] {source}")
            encoding = 'utf-8' if data_format != 'csv' else 'utf-8-sig' # CSV 한글 깨짐 방지 시도
            try:
                with open(source, 'r', encoding=encoding) as f:
                    raw_data = f.read()
            except UnicodeDecodeError:
                with open(source, 'r', encoding='cp949') as f: # 윈도우 인코딩 대응
                    raw_data = f.read()

        # 2. 파싱 (Parsing to List of Dicts)
        items = []
        
        if data_format == 'csv':
            # CSV는 별도 처리 (문자열 -> 파이썬 리스트)
            if source_type == 'file': # 파일 객체 다시 열기 귀찮으므로 StringIO 대신 raw string 파싱
                from io import StringIO
                f = StringIO(raw_data)
                reader = csv.DictReader(f)
                items = [row for row in reader]
                
        elif data_format == 'xml':
            parsed = xmltodict.parse(raw_data)
            items = self._find_items(parsed, root_key)
            
        elif data_format == 'json':
            if isinstance(raw_data, str):
                parsed = json.loads(raw_data)
            else:
                parsed = raw_data
            items = self._find_items(parsed, root_key)

        # 3. LangChain Document 변환
        return self._to_documents(items, source, data_format)

    def _find_items(self, data, root_key):
        """복잡한 중첩 구조에서 데이터 리스트 추출"""
        if not root_key:
            return data # 키 지정 안하면 통째로 반환
        
        keys = root_key.split('.')
        current = data
        try:
            for k in keys:
                current = current[k]
            
            # 결과가 딕셔너리 하나라면 리스트로 감싸기 (XML의 경우 항목이 1개면 리스트가 아님)
            if isinstance(current, dict):
                return [current]
            return current
        except KeyError:
            print(f"키 경로를 찾을 수 없습니다: {root_key}")
            return []

    def _to_documents(self, items, source, fmt):
        """딕셔너리 리스트를 LangChain Document로 변환"""
        docs = []
        for item in items:
            # 텍스트화: 모든 키-값을 문장으로 연결
            content_parts = []
            for k, v in item.items():
                if v: # 값이 있는 경우만
                    content_parts.append(f"{k}: {v}")
            
            page_content = "\n".join(content_parts)
            
            # 메타데이터 생성
            metadata = {
                "source": source,
                "format": fmt
            }
            
            docs.append(Document(page_content=page_content, metadata=metadata))
        
        return docs

# --- 사용 예시 ---
if __name__ == "__main__":
    loader = UniversalDataLoader()
    all_docs = []

    # Case 1: 로컬 CSV 파일
    # docs_csv = loader.load_data("data/sample_data.csv", source_type='file', data_format='csv')
    # all_docs.extend(docs_csv)

    # Case 2: 공공데이터 API (XML) 예시 (실제 키 필요)
    # api_url = "http://apis.data.go.kr/...?serviceKey=인증키"
    # root_key = "response.body.items.item" # XML 구조에 따라 지정
    # docs_api = loader.load_data(api_url, source_type='api', data_format='xml', root_key=root_key)
    # all_docs.extend(docs_api)

    # print(f"총 {len(all_docs)}개의 문서가 준비되었습니다.")