/**
 * ================================================================
 * Google Apps Script - AI 성숙도 진단 리드 수집 & 이메일 발송
 * ================================================================
 *
 * 🔧 설정 방법:
 *
 * 1. Google Drive에서 Google Sheets 새로 만들기
 *    - 시트 이름을 "리드" 로 변경
 *    - 첫 번째 행에 아래 헤더 입력:
 *      타임스탬프 | 회사명 | 이름 | 직책 | 부서 | 이메일 | 연락처 |
 *      임직원수 | 산업군 | 관심영역 | 총점 | 만점 | 레벨 | 레벨(한글) |
 *      리더십 | 조직문화 | 프로세스 | 역량 | 인프라 | 데이터 | 성과측정
 *
 * 2. Google Sheets 메뉴 → 확장 프로그램 → Apps Script
 *
 * 3. 아래 코드 전체를 복사하여 Apps Script 에디터에 붙여넣기
 *
 * 4. 배포 → 새 배포 → 유형: 웹 앱 선택
 *    - 실행 주체: 본인
 *    - 액세스 권한: 모든 사용자
 *    - 배포 클릭
 *
 * 5. 배포된 URL을 복사하여 app.js의 CONFIG.GOOGLE_SCRIPT_URL에 붙여넣기
 *
 * ⚠️ 주의: 처음 배포 시 Google 계정 권한 승인이 필요합니다.
 *          "고급" → "프로젝트명(안전하지 않음)으로 이동" 클릭
 * ================================================================
 */

// ─── 설정 ───
const SHEET_NAME = '리드';
const SENDER_NAME = 'AX Partners AI 성숙도 진단'; // 발신자 이름

// ─── POST 요청 처리 ───
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    if (data.action === 'saveLead') {
      return saveLead(data);
    } else if (data.action === 'sendEmail') {
      return sendEmail(data);
    }

    return ContentService.createTextOutput(JSON.stringify({ success: false, error: 'Unknown action' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ─── GET 요청 (테스트용) ───
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: 'ok', message: 'AX Assessment API is running' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── 리드 저장 ───
function saveLead(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

  // 헤더가 없으면 추가
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      '타임스탬프', '회사명', '이름', '직책', '부서', '이메일', '연락처',
      '임직원수', '산업군', '관심영역', '총점', '만점', '레벨', '레벨(한글)',
      '리더십', '조직문화', '프로세스', '역량', '인프라', '데이터', '성과측정'
    ]);
  }

  sheet.appendRow([
    data.timestamp || new Date().toISOString(),
    data.company || '',
    data.name || '',
    data.position || '',
    data.department || '',
    data.email || '',
    data.phone || '',
    data.employeeCount || '',
    data.industry || '',
    data.interest || '',
    data.totalScore || 0,
    data.maxScore || 35,
    data.level || '',
    data.levelKo || '',
    data.score_leadership || 0,
    data.score_culture || 0,
    data.score_process || 0,
    data.score_capability || 0,
    data.score_infra || 0,
    data.score_data || 0,
    data.score_measurement || 0,
  ]);

  return ContentService.createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── 이메일 발송 ───
function sendEmail(data) {
  const subject = `[AI 성숙도 진단] ${data.company} 분석 리포트`;

  const dimensionRows = data.dimensionScores.map(d => `
    <tr>
      <td style="padding:10px 16px;border-bottom:1px solid #F1F5F9;font-size:14px;">
        ${d.icon} ${d.title}
      </td>
      <td style="padding:10px 16px;border-bottom:1px solid #F1F5F9;">
        <div style="background:#F1F5F9;border-radius:6px;height:10px;width:100%;">
          <div style="background:${getBarColor(d.score)};border-radius:6px;height:10px;width:${(d.score/5)*100}%;"></div>
        </div>
      </td>
      <td style="padding:10px 16px;border-bottom:1px solid #F1F5F9;font-weight:700;text-align:center;font-size:14px;">
        ${d.score}/5
      </td>
    </tr>
  `).join('');

  const recRows = data.recommendations.map((rec, i) => `
    <tr>
      <td style="padding:14px 16px;border-bottom:1px solid #F1F5F9;vertical-align:top;width:36px;">
        <div style="width:28px;height:28px;background:#6C5CE7;color:#fff;border-radius:6px;text-align:center;line-height:28px;font-weight:700;font-size:13px;">${i+1}</div>
      </td>
      <td style="padding:14px 16px;border-bottom:1px solid #F1F5F9;">
        <strong style="font-size:15px;color:#1E293B;">${rec.title}</strong><br>
        <span style="font-size:13px;color:#64748B;line-height:1.6;">${rec.desc}</span>
      </td>
    </tr>
  `).join('');

  const html = `
  <!DOCTYPE html>
  <html>
  <head><meta charset="UTF-8"></head>
  <body style="margin:0;padding:0;background:#F8FAFC;font-family:'Apple SD Gothic Neo','Malgun Gothic',sans-serif;">
    <div style="max-width:640px;margin:0 auto;background:#fff;">

      <!-- Header -->
      <div style="background:linear-gradient(135deg,#6C5CE7,#A29BFE);padding:40px 32px;text-align:center;color:#fff;">
        <div style="font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">AI MATURITY CONSULTING REPORT</div>
        <h1 style="margin:0;font-size:26px;font-weight:900;">${data.company}</h1>
        <p style="margin:8px 0 0;font-size:16px;opacity:0.9;">AI 성숙도 진단 리포트</p>
        <p style="margin:8px 0 0;font-size:13px;opacity:0.7;">${data.name}님 | ${new Date().toLocaleDateString('ko-KR')}</p>
      </div>

      <!-- Score -->
      <div style="padding:32px;text-align:center;border-bottom:1px solid #F1F5F9;">
        <div style="display:inline-block;width:120px;height:120px;border-radius:50%;border:8px solid ${data.levelColor};text-align:center;line-height:104px;">
          <span style="font-size:36px;font-weight:900;color:#1E293B;">${data.totalScore}</span>
          <span style="font-size:14px;color:#64748B;">/${data.maxScore}</span>
        </div>
        <div style="margin-top:16px;">
          <span style="display:inline-block;padding:4px 16px;background:${data.levelColor};color:#fff;border-radius:50px;font-size:13px;font-weight:700;">
            ${data.levelName}
          </span>
        </div>
        <h2 style="margin:12px 0 8px;font-size:22px;font-weight:800;color:#1E293B;">${data.levelNameKo}</h2>
        <p style="font-size:15px;color:#64748B;line-height:1.7;max-width:480px;margin:0 auto;">${data.summary}</p>
      </div>

      <!-- Key Insight -->
      <div style="padding:24px 32px;background:#F5F3FF;border-left:4px solid #6C5CE7;margin:24px 32px;border-radius:8px;">
        <div style="font-size:11px;font-weight:700;color:#6C5CE7;letter-spacing:1px;margin-bottom:6px;">KEY INSIGHT</div>
        <p style="font-size:14px;color:#1E293B;line-height:1.7;margin:0;">${data.keyInsight}</p>
      </div>

      <!-- Analysis -->
      <div style="padding:0 32px 24px;">
        <h3 style="font-size:16px;font-weight:700;color:#1E293B;border-bottom:2px solid #E2E8F0;padding-bottom:10px;">종합 분석</h3>
        <p style="font-size:14px;color:#64748B;line-height:1.8;">${data.description}</p>
      </div>

      <!-- Dimension Scores -->
      <div style="padding:0 32px 24px;">
        <h3 style="font-size:16px;font-weight:700;color:#1E293B;border-bottom:2px solid #E2E8F0;padding-bottom:10px;">영역별 상세 진단</h3>
        <table style="width:100%;border-collapse:collapse;">
          ${dimensionRows}
        </table>
      </div>

      <!-- Recommendations -->
      <div style="padding:0 32px 24px;">
        <h3 style="font-size:16px;font-weight:700;color:#1E293B;border-bottom:2px solid #E2E8F0;padding-bottom:10px;">맞춤형 실행 제언</h3>
        <table style="width:100%;border-collapse:collapse;">
          ${recRows}
        </table>
      </div>

      <!-- CTA -->
      <div style="background:linear-gradient(135deg,#6C5CE7,#E040FB);padding:32px;text-align:center;color:#fff;margin:0 32px 32px;border-radius:12px;">
        <h3 style="margin:0 0 8px;font-size:18px;font-weight:800;">AI Transformation, DNA를 바꾸는 여정</h3>
        <p style="margin:0;font-size:14px;opacity:0.9;line-height:1.7;">
          조직의 AI 성숙도를 한 단계 끌어올리는<br>맞춤형 AX 프로그램에 대해 상담해보세요.
        </p>
      </div>

      <!-- Footer -->
      <div style="padding:24px 32px;background:#F8FAFC;text-align:center;border-top:1px solid #E2E8F0;">
        <p style="font-size:12px;color:#94A3B8;margin:0;">
          본 리포트는 ${data.brandName || 'AX Partners'} AI 성숙도 진단 서비스에 의해 자동 생성되었습니다.
        </p>
      </div>
    </div>
  </body>
  </html>
  `;

  MailApp.sendEmail({
    to: data.email,
    subject: subject,
    htmlBody: html,
    name: SENDER_NAME,
  });

  return ContentService.createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── 유틸 ───
function getBarColor(score) {
  const colors = ['#E74C3C', '#E67E22', '#F1C40F', '#2ECC71', '#6C5CE7'];
  return colors[score - 1] || colors[0];
}
