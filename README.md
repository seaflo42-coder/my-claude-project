# AI 성숙도 진단 서비스 (AX Assessment)

기업의 AI Transformation(AX) 성숙도를 진단하고, 맞춤형 컨설팅 리포트를 제공하는 웹 서비스입니다.

## 서비스 목적
- 전시회/세미나 부스에서 방문자가 3분 내 진단 완료
- 리드(잠재고객) 정보 확보 → Google Spreadsheet 자동 저장
- 컨설팅급 리포트를 화면에서 확인 + 이메일 발송

## 현재 상태 (MVP)
- [x] 랜딩 페이지
- [x] 7개 영역 진단 문항 (컨설팅급)
- [x] 리드 입력 폼 (회사명, 이름, 이메일, 연락처, 부서, 산업군, 관심영역)
- [x] 컨설팅 리포트 (벤치마크 비교, 갭분석, 레이더차트, 성숙도 로드맵, 실행제언)
- [x] Google Sheets 연동 코드 (Apps Script)
- [x] 이메일 리포트 발송 기능
- [x] PDF 저장 (브라우저 인쇄)
- [x] GitHub Pages 배포

## 파일 구조

```
├── index.html              # 메인 HTML (랜딩, 진단, 리드폼, 리포트 4개 섹션)
├── styles.css              # 전체 스타일 (반응형, 인쇄 스타일 포함)
├── questions.js            # 진단 데이터 (7개 영역, 5단계 레벨, 벤치마크)
├── app.js                  # 앱 로직 (진단, 리포트 생성, Google Sheets/이메일 연동)
├── google-apps-script.js   # Google Apps Script 코드 (시트 저장 + 이메일 발송)
├── CLAUDE.md               # 클로드 코드 작업 가이드
└── README.md               # 프로젝트 설명
```

## 기술 스택
- 순수 HTML/CSS/JavaScript (프레임워크 없음)
- Google Apps Script (리드 저장 & 이메일 발송 백엔드)
- GitHub Pages (호스팅)

## 배포
- GitHub Pages: `https://seaflo42-coder.github.io/my-claude-project/`
- 브랜치: `claude/ai-maturity-assessment-qxAx7`

## Google Sheets 연동 설정
1. Google Sheets 생성
2. 확장 프로그램 → Apps Script
3. `google-apps-script.js` 내용을 붙여넣기
4. 웹 앱으로 배포
5. 배포 URL을 `app.js`의 `CONFIG.GOOGLE_SCRIPT_URL`에 입력

## 관리자 기능
- `Ctrl + Shift + E`: localStorage의 리드 데이터 CSV 다운로드 (오프라인 백업)
