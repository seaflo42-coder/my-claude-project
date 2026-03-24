# CLAUDE.md — Hanji Studio

> 이 파일은 Claude Code가 매 세션마다 읽는 프로젝트 설명서입니다.
> 반드시 이 파일을 먼저 읽고 작업을 시작하세요.

---

## 브랜드 아이덴티티

| 항목 | 내용 |
|---|---|
| 서비스명 | **Hanji Studio** |
| 태그라인 | **Korean Heritage for AI Creators** |
| 구 명칭 | 한국 문화유산 AI 이미지 프롬프트 생성기 (사용 금지) |

### 사용 규칙
- 서비스 표시명은 항상 **Hanji Studio** 로 표기
- 태그라인은 항상 **Korean Heritage for AI Creators** 로 표기
- 한국어 부제가 필요한 경우: **한국 문화유산 × AI 이미지**
- 로고/타이틀 표기: `Hanji` (Noto Serif KR, weight 700) + `Studio` (Noto Serif KR, weight 300)
- 태그라인 표기: Noto Sans KR, size-xs, letter-spacing 0.15em, --color-ink-soft

---
## 프로젝트 개요

### 서비스 구성 (2개)

| 서비스 | 도메인 | 상태 |
|---|---|---|
| Hanji Studio — AI 프롬프트 생성기 | heritage-prompt.com | 운영 중 |
| Hanji Studio — 전통문양 패턴 메이커 | pattern.heritage-prompt.com | 개발 예정 |

### 핵심 컨셉
- 국가유산청 공공데이터 API 기반 AI 이미지 프롬프트 생성기
- 공공데이터포털 전통문양 API 기반 패턴 생성 및 SVG/PNG 다운로드 툴
- 두 서비스는 독립적으로 운영되지만 미감과 브랜드는 통일

### 주요 사용자
- AI 이미지 생성 크리에이터 (Midjourney, Stable Diffusion 사용자)
- 패브릭·굿즈 제작자, 브랜드 디자이너

---

## 기술 스택

### 프론트엔드
- **언어**: 순수 HTML / CSS / JS (프레임워크 없음)
- **핵심 파일**: 단일 `index.html` (~150KB)
- **스타일**: CSS 커스텀 프로퍼티(변수) 기반
- **현재 폰트**: Pretendard + Noto Sans KR
- **전환 폰트**: Noto Serif KR (display) + Noto Sans KR (body)

### 백엔드 / 데이터
- **언어**: Python 3.10+
- **위치**: `korean_heritage_ai/` 폴더
- **역할**: 데이터 수집 + 프롬프트 생성용 CLI 도구 (서버 아님)
- **패키지**: 표준 라이브러리만 사용, 별도 패키지 없음

### 배포
- **플랫폼**: GitHub Pages (`docs/` 폴더 기반)
- **도메인**: heritage-prompt.com (`docs/CNAME` 파일로 연결)
- **진입점**: `docs/index.html` = GitHub Pages 라이브 버전
- **개발본**: `web/index.html` = 작업본

### 저장소 구조
```
korean-heritage-ai/
├── CLAUDE.md                  ← 이 파일
├── docs/
│   ├── index.html             ← GitHub Pages 배포 진입점 (라이브)
│   └── CNAME                  ← heritage-prompt.com 도메인 설정
├── web/
│   └── index.html             ← 개발 작업본
└── korean_heritage_ai/        ← Python CLI 도구 (데이터 수집용)
```

> ⚠️ 항상 `web/index.html`을 수정 → 완료 후 `docs/index.html`에 복사

---

## 외부 API

### 국가유산청 API (현재 사용)
- 공공누리 1유형 — 출처표시 조건, 상업적 이용 가능, AI 학습 가능
- 활용 방식: 문화재 메타데이터로 AI 이미지 프롬프트 텍스트 생성

### 공공데이터포털 전통문양 API (패턴 메이커용, 예정)
- 출처: data.go.kr
- 제공 데이터: 문양번호, 문양명, 섬네일 주소, 문양형태, 유형, 시대, 소장기관, 설명
- 2D / 3D 문양 모두 제공

---

## 디자인 시스템 — K-Heritage Modern

### 원칙
1. **절제된 한국성** — 전통 요소는 포인트로만, 베이스는 현대적으로
2. **도구다움** — 미술관이 아닌 작업 툴, UI가 콘텐츠를 방해하지 않는다
3. **일관성** — 두 서비스가 같은 토큰을 공유한다

### Color Tokens
```css
:root {
  --color-ground:       #F4EFE6;
  --color-ground-deep:  #EDE5D8;
  --color-ink:          #1A1814;
  --color-ink-mid:      #3D3830;
  --color-ink-soft:     #7A7068;
  --color-ink-ghost:    #C4BBB0;
  --color-accent:       #1A6B5A;   /* 단청 청록 — 메인 포인트 */
  --color-accent-light: #E8F2EF;
  --color-accent-warm:  #B5391C;   /* 단청 적색 — 보조만 */
  --color-surface:      #FFFFFF;
  --color-border:       #D9D0C5;
}
```

### Typography
```css
--font-display: 'Noto Serif KR', serif;
--font-body:    'Noto Sans KR', sans-serif;

--size-xs:   0.75rem;
--size-sm:   0.875rem;
--size-base: 1rem;
--size-md:   1.125rem;
--size-lg:   1.5rem;
--size-xl:   2rem;
--size-2xl:  3rem;
--size-3xl:  4rem;

/* 규칙 */
/* 헤딩: font-display, letter-spacing: -0.02em */
/* 본문: font-body, line-height: 1.7 */
/* 라벨: font-body, letter-spacing: 0.15em, uppercase */
```

### Spacing
```css
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
--space-6: 24px;  --space-8: 32px;  --space-12: 48px; --space-16: 64px;
```

### Border Radius
```css
--radius-sm: 2px; --radius-md: 4px; --radius-lg: 8px; --radius-full: 9999px;
```

### 텍스처
- `body::before`에 SVG noise grain 적용 (opacity: 0.03)

---

## 컴포넌트 규칙

### 버튼
- `btn-primary`: bg `--color-ink`, hover bg `--color-accent`
- `btn-accent`: bg `--color-accent`
- `btn-outline`: border `--color-border`, hover border `--color-ink`
- `btn-ghost`: no border, color `--color-ink-soft`
- 공통: padding `space-3 × space-6`, radius `radius-sm`, font-body size-sm weight-500

### 카드
- bg `--color-surface`, border `1px --color-border`, radius `--radius-lg`
- hover: `box-shadow: 0 4px 24px rgba(26,24,20,0.08)`

### Badge
- radius `--radius-full`
- 시대: ground-deep bg / ink-mid 텍스트
- 카테고리: accent-light bg / accent 텍스트

---

## 두 서비스 연결

- 패턴 메이커 → "이 문양으로 AI 프롬프트 만들기" → heritage-prompt.com
- 프롬프트 생성기 → "관련 전통문양 패턴 보기" → pattern.heritage-prompt.com
- 데이터 전달: URL 파라미터 방식

---

## 금지 사항

- ❌ Inter, Roboto, Arial, Pretendard 신규 사용 금지
- ❌ 보라색 그라디언트 금지
- ❌ `--color-accent-warm` 메인 포인트 사용 금지
- ❌ 인라인 스타일에 색상값 직접 입력 금지 (CSS 변수만 사용)
- ❌ `docs/index.html` 직접 수정 금지 (항상 web/ 먼저)
- ❌ API 키 코드 직접 노출 금지

---

## 작업 시 참고

- 오너: 디자이너 백그라운드, 개발 비전공자
- 기술 용어 최소화, 변경 사항은 항상 설명과 함께
- 주요 결정 포인트에서 반드시 확인 후 진행
- 작업 완료 후 `web/index.html` → `docs/index.html` 복사 필수
- 커밋 메시지 한국어 가능

---

## 브랜드 아이덴티티

### 서비스명
```
Hanji Studio
Korean Heritage for AI Creators
```

### 적용 위치
- 브라우저 탭 타이틀: `Hanji Studio — [페이지명]`
- meta description: `Korean Heritage for AI Creators`
- 헤더 로고: `Hanji Studio` (Noto Serif KR, font-weight 600)
- 로고 아래 tagline: `Korean Heritage for AI Creators` (Noto Sans KR, size-xs, letter-spacing 0.1em, color: --color-ink-soft)
- OG 이미지 텍스트, footer 등 모든 브랜드 노출 지점에 통일 적용

### 톤
- 영어 기반, 글로벌 크리에이터 타겟
- 권위 있되 접근하기 쉬운 톤
- "전통을 도구로 만든다"는 관점 유지

---

## 핵심 기능 V2 — 고증 × 감도 프롬프트 생성기

### 컨셉
문화유산의 고증 정보 위에 현대적 씬(패션/인물/제품)과 감도(에디토리얼/시네마틱/캠페인)를 레이어로 얹어, 두 요소가 자연스럽게 어우러진 프롬프트를 생성한다.

### 기존과의 차이
- 기존: 유산 선택 → 스타일 → AI 모델 → 프롬프트
- V2: 유산 선택 → 씬 타입 → 감도 → 자유입력 → (고급설정) → 프롬프트

### UI 구조 — 스마트 모드 (기본 + 고급)

#### 기본 모드 (항상 노출)
1. **유산 선택** — 기존 고증 데이터 유지
2. **씬 타입 선택** — 패션/브랜드 캠페인 · 인물/포트레이트 · 제품 사진
3. **자유 입력** — "나이키 런웨이", "버버리 코트" 등 핵심 키워드
4. **감도 선택** — 에디토리얼 · 시네마틱 · 캠페인

#### 고급 설정 (접기/펼치기)
- 카메라 앵글 (정면 · 측면 · 오버헤드 · 로우앵글)
- 렌즈 (35mm · 50mm · 85mm · 광각)
- 조명 (골든아워 · 블루아워 · 스튜디오 · 자연광 · 무드)
- 계절 (봄 · 여름 · 가을 · 겨울)
- 시간대 (새벽 · 오전 · 오후 · 야간)
- 추가 디렉션 자유입력

### 감도별 프롬프트 출력 방식

#### 에디토리얼 (보그 느낌)
```
[유산 고증 정보], [씬], Vogue editorial, [렌즈]mm lens,
shallow depth of field, dramatic lighting, high fashion photography,
[계절/시간대], [추가 디렉션]
```

#### 시네마틱
```
[유산 고증 정보], [씬], cinematic composition, anamorphic lens,
film grain, [조명], [시간대], movie still, [감독 레퍼런스 스타일],
[추가 디렉션]
```

#### 캠페인
```
[유산 고증 정보], [씬], advertising campaign, [브랜드 느낌],
commercial photography, [조명], clean composition,
[추가 디렉션]
```

### 핵심 원칙
- 고증 정보는 항상 프롬프트 앞부분에 위치 (절대 생략 금지)
- 감도 레이어는 고증을 덮지 않고 자연스럽게 이어지도록 연결
- 자유입력 키워드는 씬 타입과 감도 사이에 자연스럽게 삽입
- 고급 설정은 기본값이 있어야 함 (사용자가 안 건드려도 작동)

### 고급 설정 기본값
- 카메라: 정면
- 렌즈: 85mm
- 조명: 골든아워
- 계절: 지정 안 함
- 시간대: 지정 안 함
