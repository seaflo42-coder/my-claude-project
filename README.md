# korean-heritage-ai-data

국가유산청 공공데이터 API를 활용하여 한국 문화유산 데이터를 수집·구조화하고,
생성형 AI 이미지 제작 시 고증에 활용할 수 있는 프롬프트 데이터셋을 만드는 도구입니다.

## 주요 기능

### 1. 데이터 수집 (`api/heritage_client.py`)
- 국가유산청 Open API를 통한 문화유산 목록/상세정보/이미지 수집
- 국보, 보물, 사적, 명승, 천연기념물 등 전 종목 지원
- 시도별/종목별 검색 및 일괄 수집

### 2. 데이터 구조화 (`data/structurer.py`)
- 시대별 정보 확장 (선사~근대, 시대별 특징 포함)
- 시각적 카테고리 분류 (건축, 불교유산, 공예, 회화 등)
- AI 학습용 데이터셋 변환 (JSON, JSONL, CSV)
- 색상 팔레트, 재료, 양식 키워드 자동 태깅

### 3. AI 프롬프트 생성 (`prompts/generator.py`)
- 문화유산 데이터 기반 이미지 생성 프롬프트 자동 생성
- 스타일별 변형 (사실적, 한국화, 일러스트, 3D)
- 모델별 최적화 (Midjourney, DALL-E, Stable Diffusion)
- 한글/영문 프롬프트 지원
- 고증 기반 상세 요소 포함 (단청, 공포, 상감기법 등)

## 프로젝트 구조

```
korean_heritage_ai/
├── api/
│   └── heritage_client.py   # 국가유산청 API 클라이언트
├── data/
│   └── structurer.py        # 데이터 구조화/변환
├── prompts/
│   └── generator.py         # AI 이미지 프롬프트 생성기
└── examples/
    ├── collect_and_generate.py  # 온라인 예제 (API 호출)
    └── offline_demo.py          # 오프라인 데모 (샘플 데이터)
```

## 빠른 시작

### 오프라인 데모 (API 키 불필요)

```bash
python -m korean_heritage_ai.examples.offline_demo
```

### 실제 API 데이터 수집

```bash
python -m korean_heritage_ai.examples.collect_and_generate
```

### 코드에서 사용

```python
from korean_heritage_ai.api.heritage_client import HeritageAPIClient
from korean_heritage_ai.data.structurer import convert_to_dataset
from korean_heritage_ai.prompts.generator import generate_image_prompt

# 1. 데이터 수집
client = HeritageAPIClient()
items = client.collect_full_data(kind_code="11", max_items=10)  # 국보 10건

# 2. 데이터셋 저장
convert_to_dataset(items, "output/dataset.json", "json")

# 3. 프롬프트 생성
for item in items:
    prompt = generate_image_prompt(
        item,
        style="photorealistic",
        target_model="midjourney",
        detail_level="comprehensive",
    )
    print(f"{item.name_kr}: {prompt}")
```

## 활용 시나리오

| 시나리오 | 설명 |
|---------|------|
| 고증 기반 이미지 생성 | 시대별·양식별 정확한 프롬프트로 역사적으로 정확한 이미지 생성 |
| 교육 콘텐츠 제작 | 문화유산 설명 + 시각 자료를 결합한 교육 콘텐츠 |
| 게임/영화 아트 레퍼런스 | 한국적 배경·소품의 정확한 고증 데이터 활용 |
| AI 모델 파인튜닝 | 한국 문화유산 특화 이미지 생성 모델 학습 데이터셋 |

## 데이터 출처

- [국가유산포털](https://www.heritage.go.kr) - 국가유산청
- [공공데이터포털](https://www.data.go.kr/data/3070426/openapi.do) - 문화재 공간 정보 API
- [국가유산공간정보서비스](https://gis-heritage.go.kr) - GIS 기반 공간정보

## 요구사항

- Python 3.10+
- 표준 라이브러리만 사용 (추가 패키지 설치 불필요)
- API 사용 시: 공공데이터포털 인증키 (일부 API에 필요)
