// ============================================================
// CONFIG - Google Apps Script Web App URL
// 아래 URL을 Google Apps Script 배포 URL로 교체하세요
// ============================================================
const CONFIG = {
    // Google Apps Script 웹 앱 URL (설정 방법은 google-apps-script.js 참고)
    GOOGLE_SCRIPT_URL: '',
    // 회사 브랜드명
    BRAND_NAME: 'AX Partners',
};

// ─── State ───
let currentQuestion = 0;
let answers = {};
let leadData = {};

// ─── Navigation ───
function showStep(stepId) {
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    document.getElementById(stepId).classList.add('active');
    window.scrollTo(0, 0);
}

function startAssessment() {
    showStep('step-assessment');
    renderQuestion();
}

// ─── Assessment ───
function renderQuestion() {
    const dim = ASSESSMENT_DATA.dimensions[currentQuestion];
    const totalQ = ASSESSMENT_DATA.dimensions.length;

    const pct = ((currentQuestion + 1) / totalQ) * 100;
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = `${currentQuestion + 1} / ${totalQ}`;

    document.getElementById('btnPrev').style.visibility = currentQuestion === 0 ? 'hidden' : 'visible';
    const isLast = currentQuestion === totalQ - 1;
    document.getElementById('btnNext').innerHTML = isLast
        ? '완료 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg>'
        : '다음 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';

    const selected = answers[dim.id];
    document.getElementById('questionArea').innerHTML = `
        <div class="question-header">
            <span class="question-icon">${dim.icon}</span>
            <span class="question-dimension">${dim.title}</span>
        </div>
        <h2 class="question-text">${dim.question}</h2>
        <p class="question-desc">${dim.description}</p>
        <div class="options-list">
            ${dim.options.map(opt => `
                <button class="option-btn ${selected === opt.score ? 'selected' : ''}"
                        onclick="selectOption('${dim.id}', ${opt.score}, this)">
                    <span class="option-level">Lv.${opt.score}</span>
                    <span class="option-text">${opt.label}</span>
                </button>
            `).join('')}
        </div>
    `;

    document.getElementById('btnNext').disabled = !selected;
}

function selectOption(dimensionId, score, el) {
    answers[dimensionId] = score;
    document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
    el.classList.add('selected');
    document.getElementById('btnNext').disabled = false;
}

function nextQuestion() {
    const totalQ = ASSESSMENT_DATA.dimensions.length;
    if (currentQuestion < totalQ - 1) {
        currentQuestion++;
        renderQuestion();
    } else {
        showStep('step-lead');
    }
}

function prevQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        renderQuestion();
    }
}

// ─── Lead Form ───
function submitLead(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> 리포트 생성 중...';

    leadData = {
        company: document.getElementById('companyName').value,
        name: document.getElementById('userName').value,
        position: document.getElementById('userPosition').value,
        department: document.getElementById('department').value,
        email: document.getElementById('userEmail').value,
        phone: document.getElementById('userPhone').value,
        employeeCount: document.getElementById('employeeCount').value,
        industry: document.getElementById('industry').value,
        interest: document.getElementById('interest').value,
        timestamp: new Date().toISOString(),
        answers: { ...answers }
    };

    // Save to localStorage as backup
    const leads = JSON.parse(localStorage.getItem('ax_leads') || '[]');
    leads.push(leadData);
    localStorage.setItem('ax_leads', JSON.stringify(leads));

    // Send to Google Sheets
    sendToGoogleSheets(leadData);

    // Generate report immediately (don't wait for network)
    setTimeout(() => generateReport(), 600);
}

// ─── Google Sheets Integration ───
function sendToGoogleSheets(data) {
    if (!CONFIG.GOOGLE_SCRIPT_URL) {
        console.log('[INFO] Google Script URL not configured. Lead saved to localStorage only.');
        return;
    }

    const totalScore = Object.values(data.answers).reduce((a, b) => a + b, 0);
    const maxScore = ASSESSMENT_DATA.dimensions.length * 5;
    const level = ASSESSMENT_DATA.levels.find(l => totalScore >= l.range[0] && totalScore <= l.range[1]);

    const payload = {
        action: 'saveLead',
        company: data.company,
        name: data.name,
        position: data.position,
        department: data.department,
        email: data.email,
        phone: data.phone,
        employeeCount: data.employeeCount,
        industry: data.industry,
        interest: data.interest,
        timestamp: data.timestamp,
        totalScore: totalScore,
        maxScore: maxScore,
        level: level ? level.name : '',
        levelKo: level ? level.nameKo : '',
        // Individual dimension scores
        score_leadership: data.answers.leadership || 0,
        score_culture: data.answers.culture || 0,
        score_process: data.answers.process || 0,
        score_capability: data.answers.capability || 0,
        score_infra: data.answers.infra || 0,
        score_data: data.answers.data || 0,
        score_measurement: data.answers.measurement || 0,
    };

    fetch(CONFIG.GOOGLE_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).catch(err => console.warn('Google Sheets 전송 실패 (localStorage에 백업됨):', err));
}

// ─── Send Email via Google Apps Script ───
function sendReportEmail() {
    if (!CONFIG.GOOGLE_SCRIPT_URL) {
        alert('이메일 발송 기능 설정이 필요합니다.\ngoogle-apps-script.js 파일을 참고하여 Google Apps Script를 설정해주세요.');
        return;
    }

    const emailBtn = document.getElementById('emailBtn');
    emailBtn.disabled = true;
    emailBtn.innerHTML = '<span class="spinner"></span> 발송 중...';

    const totalScore = Object.values(answers).reduce((a, b) => a + b, 0);
    const maxScore = ASSESSMENT_DATA.dimensions.length * 5;
    const level = ASSESSMENT_DATA.levels.find(l => totalScore >= l.range[0] && totalScore <= l.range[1]);

    const dimensionScores = ASSESSMENT_DATA.dimensions.map(dim => ({
        title: dim.title,
        icon: dim.icon,
        score: answers[dim.id] || 0
    }));

    const payload = {
        action: 'sendEmail',
        email: leadData.email,
        name: leadData.name,
        company: leadData.company,
        totalScore: totalScore,
        maxScore: maxScore,
        levelName: level.name,
        levelNameKo: level.nameKo,
        levelColor: level.color,
        summary: level.summary,
        description: level.description,
        keyInsight: level.keyInsight,
        recommendations: level.recommendations,
        dimensionScores: dimensionScores,
        brandName: CONFIG.BRAND_NAME
    };

    fetch(CONFIG.GOOGLE_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(() => {
        emailBtn.innerHTML = '✓ 이메일 발송 완료';
        emailBtn.classList.add('btn-success');
    }).catch(() => {
        emailBtn.innerHTML = '발송 실패 - 다시 시도';
        emailBtn.disabled = false;
    });
}

// ─── Report Generation ───
function generateReport() {
    const totalScore = Object.values(answers).reduce((a, b) => a + b, 0);
    const level = ASSESSMENT_DATA.levels.find(l => totalScore >= l.range[0] && totalScore <= l.range[1]);
    const maxScore = ASSESSMENT_DATA.dimensions.length * 5;
    const overallPct = Math.round((totalScore / maxScore) * 100);

    const dimensionScores = ASSESSMENT_DATA.dimensions.map(dim => ({
        ...dim,
        score: answers[dim.id] || 0
    }));

    const sorted = [...dimensionScores].sort((a, b) => b.score - a.score);
    const strongest = sorted[0];
    const weakest = sorted[sorted.length - 1];

    // Benchmark comparison
    const benchAvg = ASSESSMENT_DATA.benchmarks.average;
    const benchTop = ASSESSMENT_DATA.benchmarks.top20;
    const vsBenchmark = totalScore - benchAvg;
    const benchmarkText = vsBenchmark > 0
        ? `산업 평균 대비 <strong>+${vsBenchmark}점</strong> 높은 수준`
        : vsBenchmark === 0
            ? `산업 평균과 <strong>동일한</strong> 수준`
            : `산업 평균 대비 <strong>${vsBenchmark}점</strong> 낮은 수준`;

    const dateStr = new Date().toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' });

    document.getElementById('reportContainer').innerHTML = `
        <div class="report-header">
            <div class="report-badge">AI MATURITY CONSULTING REPORT</div>
            <h1>${leadData.company}</h1>
            <h2 class="report-header-sub">AI 성숙도 진단 리포트</h2>
            <p class="report-date">${dateStr} | ${leadData.name}${leadData.position ? ' ' + leadData.position : ''}</p>
        </div>

        <!-- Executive Summary -->
        <div class="report-card report-executive">
            <div class="card-label">EXECUTIVE SUMMARY</div>
            <h3>진단 결과 요약</h3>
            <div class="executive-grid">
                <div class="score-circle-wrap">
                    <div class="score-circle" style="--score-pct: ${overallPct}; --score-color: ${level.color}">
                        <div class="score-inner">
                            <span class="score-number">${totalScore}</span>
                            <span class="score-max">/ ${maxScore}</span>
                        </div>
                    </div>
                    <div class="score-label">${overallPct}%</div>
                </div>
                <div class="score-info">
                    <div class="level-badge" style="background: ${level.color}">Level ${level.level} — ${level.name}</div>
                    <h2 class="level-name">${level.nameKo}</h2>
                    <p class="level-summary">${level.summary}</p>
                    <div class="benchmark-bar">
                        <div class="benchmark-label">${benchmarkText}</div>
                        <div class="benchmark-track">
                            <div class="benchmark-marker benchmark-avg" style="left: ${(benchAvg / maxScore) * 100}%">
                                <span>산업 평균</span>
                            </div>
                            <div class="benchmark-marker benchmark-top" style="left: ${(benchTop / maxScore) * 100}%">
                                <span>상위 20%</span>
                            </div>
                            <div class="benchmark-you" style="left: ${Math.min(overallPct, 100)}%">
                                <span>귀사</span>
                            </div>
                            <div class="benchmark-fill" style="width: ${overallPct}%; background: ${level.color}"></div>
                        </div>
                        <p class="benchmark-note">${ASSESSMENT_DATA.benchmarks.description}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Key Insight -->
        <div class="report-card insight-card">
            <div class="insight-icon">💡</div>
            <div class="insight-content">
                <div class="card-label">KEY INSIGHT</div>
                <p>${level.keyInsight}</p>
            </div>
        </div>

        <!-- Overall Analysis -->
        <div class="report-card">
            <div class="card-label">ANALYSIS</div>
            <h3>종합 분석</h3>
            <p>${level.description}</p>
        </div>

        <!-- Dimension Detail -->
        <div class="report-card">
            <div class="card-label">DIMENSION ANALYSIS</div>
            <h3>7대 영역별 상세 진단</h3>
            <div class="dimension-bars">
                ${dimensionScores.map(dim => `
                    <div class="dim-bar-row">
                        <div class="dim-bar-label">
                            <span class="dim-bar-icon">${dim.icon}</span>
                            <span>${dim.title}</span>
                        </div>
                        <div class="dim-bar-track">
                            <div class="dim-bar-fill" style="width: ${(dim.score / 5) * 100}%; background: ${getBarColor(dim.score)}"></div>
                        </div>
                        <span class="dim-bar-score">${dim.score}<small>/5</small></span>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Radar Chart -->
        <div class="report-card">
            <div class="card-label">COMPETENCY MAP</div>
            <h3>AI 역량 레이더 차트</h3>
            <div class="radar-wrap">
                <canvas id="radarChart" width="420" height="420"></canvas>
            </div>
        </div>

        <!-- Gap Analysis -->
        <div class="report-card">
            <div class="card-label">GAP ANALYSIS</div>
            <h3>성숙도 갭 분석</h3>
            <p class="card-desc">현재 수준과 목표 수준(Level 4 통합 단계) 간의 갭을 분석합니다.</p>
            <div class="gap-chart">
                ${dimensionScores.map(dim => {
                    const gap = 4 - dim.score;
                    const gapClass = gap > 2 ? 'gap-critical' : gap > 0 ? 'gap-moderate' : 'gap-good';
                    return `
                    <div class="gap-row ${gapClass}">
                        <div class="gap-label">${dim.icon} ${dim.title}</div>
                        <div class="gap-visual">
                            <div class="gap-current" style="width: ${(dim.score / 5) * 100}%"></div>
                            <div class="gap-target" style="left: ${(4 / 5) * 100}%"></div>
                        </div>
                        <div class="gap-info">
                            ${gap > 0 ? `<span class="gap-value">Gap: ${gap}</span>` : '<span class="gap-achieved">달성</span>'}
                        </div>
                    </div>`;
                }).join('')}
            </div>
        </div>

        <!-- Strength & Weakness -->
        <div class="report-highlights">
            <div class="highlight-card strength">
                <div class="highlight-icon">${strongest.icon}</div>
                <div class="highlight-badge">핵심 강점 영역</div>
                <h4>${strongest.title}</h4>
                <p><strong>${strongest.score}/5</strong> — 이 영역의 강점을 레버리지하여 타 영역의 성장을 견인하는 전략을 권고합니다. ${strongest.title} 역량은 조직 내 AI 전환의 앵커 포인트로 활용할 수 있습니다.</p>
            </div>
            <div class="highlight-card weakness">
                <div class="highlight-icon">${weakest.icon}</div>
                <div class="highlight-badge">우선 개선 영역</div>
                <h4>${weakest.title}</h4>
                <p><strong>${weakest.score}/5</strong> — 이 영역의 우선적 개선이 전체 AI 성숙도 향상의 핵심 레버입니다. 단기 집중 투자를 통해 가장 큰 성숙도 향상 효과를 기대할 수 있습니다.</p>
            </div>
        </div>

        <!-- Maturity Roadmap -->
        <div class="report-card">
            <div class="card-label">MATURITY ROADMAP</div>
            <h3>AI 성숙도 로드맵</h3>
            <p class="card-desc">귀사의 현재 위치와 AX 전환까지의 여정을 보여드립니다.</p>
            <div class="roadmap">
                ${ASSESSMENT_DATA.levels.map(l => `
                    <div class="roadmap-step ${l.level === level.level ? 'roadmap-current' : ''} ${l.level < level.level ? 'roadmap-done' : ''}">
                        <div class="roadmap-dot" style="background: ${l.level <= level.level ? l.color : '#E2E8F0'}"></div>
                        <div class="roadmap-content">
                            <div class="roadmap-level" style="color: ${l.color}">Level ${l.level}</div>
                            <div class="roadmap-name">${l.name}</div>
                            <div class="roadmap-name-ko">${l.nameKo}</div>
                            ${l.level === level.level ? '<div class="roadmap-you">← 현재 위치</div>' : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Recommendations -->
        <div class="report-card">
            <div class="card-label">ACTION PLAN</div>
            <h3>맞춤형 실행 제언</h3>
            <p class="card-desc">귀사의 현재 성숙도 단계에 맞는 우선순위 높은 실행 과제입니다.</p>
            <div class="recommendations">
                ${level.recommendations.map((rec, i) => `
                    <div class="rec-item">
                        <div class="rec-header">
                            <span class="rec-number">${i + 1}</span>
                            <h4 class="rec-title">${rec.title}</h4>
                        </div>
                        <p class="rec-desc">${rec.desc}</p>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- CTA -->
        <div class="report-cta">
            <h3>AI Transformation,<br>교육이 아닌 DNA를 바꾸는 여정</h3>
            <p>우리는 단순한 AI 교육을 넘어, 조직의 일하는 방식 자체를 변화시키는<br><strong>AX(AI Transformation) 프로그램</strong>을 제공합니다.</p>
            <div class="cta-features">
                <div class="cta-feature">
                    <span class="cta-icon">🎯</span>
                    <div>
                        <strong>AX 전략 컨설팅</strong>
                        <span>맞춤형 AI 전환 로드맵</span>
                    </div>
                </div>
                <div class="cta-feature">
                    <span class="cta-icon">🧬</span>
                    <div>
                        <strong>DNA 체인지 프로그램</strong>
                        <span>조직문화 내재화</span>
                    </div>
                </div>
                <div class="cta-feature">
                    <span class="cta-icon">📊</span>
                    <div>
                        <strong>성과 기반 교육</strong>
                        <span>ROI 측정 가능한 역량 개발</span>
                    </div>
                </div>
            </div>
            <p class="cta-contact">자세한 상담은 부스 담당자에게 문의해주세요</p>
        </div>

        <!-- Actions -->
        <div class="report-actions">
            <button class="btn-secondary" onclick="restartAssessment()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                새로운 진단
            </button>
            <button class="btn-primary" id="emailBtn" onclick="sendReportEmail()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 4l-10 8L2 4"/></svg>
                이메일로 리포트 받기
            </button>
            <button class="btn-secondary" onclick="window.print()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                PDF 저장
            </button>
        </div>
    `;

    showStep('step-report');
    setTimeout(() => drawRadarChart(dimensionScores), 150);
}

function getBarColor(score) {
    const colors = ['#E74C3C', '#E67E22', '#F1C40F', '#2ECC71', '#6C5CE7'];
    return colors[score - 1] || colors[0];
}

// ─── Radar Chart (pure canvas) ───
function drawRadarChart(dimensions) {
    const canvas = document.getElementById('radarChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const size = 420;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width = size + 'px';
    canvas.style.height = size + 'px';
    ctx.scale(dpr, dpr);

    const cx = size / 2;
    const cy = size / 2;
    const maxR = 155;
    const n = dimensions.length;
    const angleStep = (Math.PI * 2) / n;
    const startAngle = -Math.PI / 2;

    // Background rings
    for (let ring = 1; ring <= 5; ring++) {
        const r = (ring / 5) * maxR;
        ctx.beginPath();
        for (let i = 0; i <= n; i++) {
            const angle = startAngle + i * angleStep;
            const x = cx + r * Math.cos(angle);
            const y = cy + r * Math.sin(angle);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = ring % 2 === 0 ? '#F8FAFC' : '#F1F5F9';
        ctx.fill();
        ctx.strokeStyle = '#E2E8F0';
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    // Axis lines & labels
    dimensions.forEach((dim, i) => {
        const angle = startAngle + i * angleStep;
        const x = cx + maxR * Math.cos(angle);
        const y = cy + maxR * Math.sin(angle);
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(x, y);
        ctx.strokeStyle = '#E2E8F0';
        ctx.lineWidth = 1;
        ctx.stroke();

        const lx = cx + (maxR + 30) * Math.cos(angle);
        const ly = cy + (maxR + 30) * Math.sin(angle);
        ctx.font = '12px "Noto Sans KR", sans-serif';
        ctx.fillStyle = '#475569';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const shortTitle = dim.title.length > 8 ? dim.title.substring(0, 8) + '..' : dim.title;
        ctx.fillText(shortTitle, lx, ly);
    });

    // Data polygon
    ctx.beginPath();
    dimensions.forEach((dim, i) => {
        const angle = startAngle + i * angleStep;
        const r = (dim.score / 5) * maxR;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.closePath();

    const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, maxR);
    gradient.addColorStop(0, 'rgba(108, 92, 231, 0.3)');
    gradient.addColorStop(1, 'rgba(108, 92, 231, 0.08)');
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.strokeStyle = '#6C5CE7';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Data points with score labels
    dimensions.forEach((dim, i) => {
        const angle = startAngle + i * angleStep;
        const r = (dim.score / 5) * maxR;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);

        // Glow
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(108, 92, 231, 0.2)';
        ctx.fill();

        // Point
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#6C5CE7';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

// ─── Restart ───
function restartAssessment() {
    currentQuestion = 0;
    answers = {};
    leadData = {};
    document.getElementById('leadForm').reset();
    showStep('step-landing');
}

// ─── Admin: Export Leads from localStorage ───
function exportLeads() {
    const leads = JSON.parse(localStorage.getItem('ax_leads') || '[]');
    if (leads.length === 0) { alert('저장된 리드가 없습니다.'); return; }

    const headers = ['timestamp', 'company', 'name', 'position', 'department', 'email', 'phone', 'employeeCount', 'industry', 'interest',
        'leadership', 'culture', 'process', 'capability', 'infra', 'data', 'measurement', 'totalScore'];

    const rows = leads.map(l => {
        const total = l.answers ? Object.values(l.answers).reduce((a, b) => a + b, 0) : 0;
        return [l.timestamp, l.company, l.name, l.position, l.department || '', l.email, l.phone,
            l.employeeCount, l.industry || '', l.interest || '',
            l.answers?.leadership || 0, l.answers?.culture || 0, l.answers?.process || 0,
            l.answers?.capability || 0, l.answers?.infra || 0, l.answers?.data || 0, l.answers?.measurement || 0,
            total
        ].map(v => `"${v}"`).join(',');
    });

    const csv = [headers.join(','), ...rows].join('\n');
    const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `ax_leads_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
}

// Ctrl+Shift+E to export leads (admin shortcut)
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.shiftKey && e.key === 'E') exportLeads();
});
