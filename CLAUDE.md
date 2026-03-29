# CLAUDE.md - AI 성숙도 진단 서비스 프로젝트 가이드

## 프로젝트 개요
기업의 AI Transformation(AX) 성숙도를 진단하고 컨설팅 리포트를 제공하는 웹 서비스.
전시회/세미나 부스에서 리드 확보 목적으로 사용. 순수 HTML/CSS/JS로 구성 (프레임워크 없음).

## 파일 구조 & 역할

### index.html
- 4개 섹션(step)으로 구성: 랜딩 → 진단 → 리드폼 → 리포트
- 각 섹션은 `class="step"`으로 구분, `active` 클래스로 표시/숨김 제어
- 모든 UI는 여기에 정적으로 선언되거나 app.js에서 동적 렌더링

### questions.js
- `ASSESSMENT_DATA` 전역 객체 하나로 모든 진단 데이터 관리
- `dimensions`: 7개 진단 영역 (leadership, culture, process, capability, infra, data, measurement)
- 각 영역당 5개 선택지 (score 1~5)
- `levels`: 5단계 성숙도 레벨 (range, 설명, recommendations 포함)
- `benchmarks`: 산업 평균/상위 20% 비교 기준값

### app.js
- `CONFIG.GOOGLE_SCRIPT_URL`: Google Apps Script 배포 URL (현재 빈 문자열 → 설정 필요)
- 상태: `currentQuestion`, `answers`, `leadData`
- 핵심 함수:
  - `renderQuestion()`: 현재 질문 렌더링
  - `submitLead()`: 리드 저장 (localStorage + Google Sheets)
  - `generateReport()`: 전체 리포트 HTML 생성
  - `drawRadarChart()`: Canvas 기반 레이더 차트
  - `sendReportEmail()`: Google Apps Script로 이메일 발송 요청
  - `exportLeads()`: localStorage → CSV 다운로드 (Ctrl+Shift+E)

### styles.css
- CSS 변수 기반 디자인 시스템 (--primary: #6C5CE7)
- 반응형 (768px 브레이크포인트)
- 인쇄 스타일 포함 (@media print)

### google-apps-script.js
- Google Apps Script에 붙여넣을 코드 (프로젝트에서 직접 실행되지 않음)
- `doPost()`: saveLead (시트 저장) / sendEmail (HTML 이메일 발송)
- 설정 완료 후 배포 URL을 app.js CONFIG에 입력해야 동작

## 현재 상태 (MVP 완료)
- 진단 플로우 전체 동작 (랜딩 → 7문항 → 리드폼 → 리포트)
- 컨설팅급 리포트 (벤치마크, 갭분석, 레이더차트, 로드맵, 실행제언)
- Google Sheets / 이메일 연동 코드 작성 완료 (Apps Script URL 설정만 하면 동작)
- GitHub Pages 배포 완료

## 향후 개선 가능 영역
- 리포트 디자인 추가 개선 (애니메이션, 차트 다양화)
- 산업군별 벤치마크 데이터 세분화
- 관리자 대시보드 페이지 추가
- 진단 결과 공유 기능 (URL 공유, 카카오톡 등)
- 다국어 지원 (영문 버전)
- 커스텀 도메인 연결
- 브랜드별 커스터마이징 (로고, 색상, CTA 문구)

## 코딩 컨벤션
- 순수 JS, 프레임워크 없음. DOM 직접 조작
- 전역 함수 사용 (onclick 바인딩)
- HTML은 JS 내 템플릿 리터럴로 동적 생성
- CSS 변수 활용, BEM 미사용
- 한글 주석 사용

## 배포
- 호스팅: GitHub Pages
- URL: https://seaflo42-coder.github.io/my-claude-project/
- 배포 브랜치: claude/ai-maturity-assessment-qxAx7
- 변경사항 push하면 자동 배포됨
