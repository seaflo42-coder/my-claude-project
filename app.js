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

    // Progress
    const pct = ((currentQuestion + 1) / totalQ) * 100;
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = `${currentQuestion + 1} / ${totalQ}`;

    // Navigation buttons
    document.getElementById('btnPrev').style.visibility = currentQuestion === 0 ? 'hidden' : 'visible';
    const isLast = currentQuestion === totalQ - 1;
    document.getElementById('btnNext').innerHTML = isLast
        ? '완료 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg>'
        : '다음 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';

    // Question content
    const selected = answers[dim.id];
    document.getElementById('questionArea').innerHTML = `
        <div class="question-header">
            <span class="question-icon">${dim.icon}</span>
            <span class="question-dimension">${dim.title}</span>
        </div>
        <h2 class="question-text">${dim.question}</h2>
        <p class="question-desc">${dim.description}</p>
        <div class="options-list">
            ${dim.options.map((opt, i) => `
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
    leadData = {
        company: document.getElementById('companyName').value,
        name: document.getElementById('userName').value,
        position: document.getElementById('userPosition').value,
        email: document.getElementById('userEmail').value,
        phone: document.getElementById('userPhone').value,
        employeeCount: document.getElementById('employeeCount').value,
        timestamp: new Date().toISOString(),
        answers: { ...answers }
    };

    // Save to localStorage as simple lead DB
    const leads = JSON.parse(localStorage.getItem('ax_leads') || '[]');
    leads.push(leadData);
    localStorage.setItem('ax_leads', JSON.stringify(leads));

    generateReport();
}

// ─── Report ───
function generateReport() {
    const totalScore = Object.values(answers).reduce((a, b) => a + b, 0);
    const level = ASSESSMENT_DATA.levels.find(l => totalScore >= l.range[0] && totalScore <= l.range[1]);
    const maxScore = ASSESSMENT_DATA.dimensions.length * 5;
    const overallPct = Math.round((totalScore / maxScore) * 100);

    const dimensionScores = ASSESSMENT_DATA.dimensions.map(dim => ({
        ...dim,
        score: answers[dim.id] || 0
    }));

    // Find strongest and weakest
    const sorted = [...dimensionScores].sort((a, b) => b.score - a.score);
    const strongest = sorted[0];
    const weakest = sorted[sorted.length - 1];

    document.getElementById('reportContainer').innerHTML = `
        <div class="report-header">
            <div class="report-badge">AI MATURITY REPORT</div>
            <h1>${leadData.company}의<br>AI 성숙도 진단 리포트</h1>
            <p class="report-date">${new Date().toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
        </div>

        <div class="report-score-section">
            <div class="score-circle-wrap">
                <div class="score-circle" style="--score-pct: ${overallPct}; --score-color: ${level.color}">
                    <div class="score-inner">
                        <span class="score-number">${totalScore}</span>
                        <span class="score-max">/ ${maxScore}</span>
                    </div>
                </div>
            </div>
            <div class="score-info">
                <div class="level-badge" style="background: ${level.color}">${level.name}</div>
                <h2 class="level-name">${level.nameKo}</h2>
                <p class="level-summary">${level.summary}</p>
            </div>
        </div>

        <div class="report-card">
            <h3>종합 분석</h3>
            <p>${level.description}</p>
        </div>

        <div class="report-card">
            <h3>영역별 상세 진단</h3>
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
                        <span class="dim-bar-score">${dim.score}/5</span>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="report-card">
            <h3>레이더 차트</h3>
            <div class="radar-wrap">
                <canvas id="radarChart" width="400" height="400"></canvas>
            </div>
        </div>

        <div class="report-highlights">
            <div class="highlight-card strength">
                <div class="highlight-icon">${strongest.icon}</div>
                <div class="highlight-badge">강점 영역</div>
                <h4>${strongest.title}</h4>
                <p>이 영역에서 상대적으로 높은 성숙도를 보이고 있습니다. 이 강점을 레버리지하여 다른 영역의 성장을 견인하세요.</p>
            </div>
            <div class="highlight-card weakness">
                <div class="highlight-icon">${weakest.icon}</div>
                <div class="highlight-badge">개선 영역</div>
                <h4>${weakest.title}</h4>
                <p>이 영역의 우선적 개선이 전체 AI 성숙도 향상의 핵심 레버가 될 수 있습니다.</p>
            </div>
        </div>

        <div class="report-card">
            <h3>맞춤 실행 제언</h3>
            <div class="recommendations">
                ${level.recommendations.map((rec, i) => `
                    <div class="rec-item">
                        <span class="rec-number">${i + 1}</span>
                        <span class="rec-text">${rec}</span>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="report-cta">
            <h3>AI Transformation, 교육이 아닌 DNA를 바꾸는 여정</h3>
            <p>우리는 단순한 AI 교육을 넘어, 조직의 일하는 방식 자체를 변화시키는<br><strong>AX(AI Transformation) 프로그램</strong>을 제공합니다.</p>
            <div class="cta-features">
                <div class="cta-feature">
                    <span class="cta-icon">🎯</span>
                    <span>맞춤형 AX 전략 수립</span>
                </div>
                <div class="cta-feature">
                    <span class="cta-icon">🧬</span>
                    <span>조직 DNA 변화 프로그램</span>
                </div>
                <div class="cta-feature">
                    <span class="cta-icon">📊</span>
                    <span>성과 기반 컨설팅</span>
                </div>
            </div>
            <p class="cta-contact">자세한 상담은 부스 담당자에게 문의해주세요</p>
        </div>

        <div class="report-actions">
            <button class="btn-secondary" onclick="restartAssessment()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                새로운 진단
            </button>
            <button class="btn-primary" onclick="downloadReport()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                리포트 저장
            </button>
        </div>
    `;

    showStep('step-report');

    // Draw radar chart after DOM update
    setTimeout(() => drawRadarChart(dimensionScores), 100);
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
    const size = 400;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width = size + 'px';
    canvas.style.height = size + 'px';
    ctx.scale(dpr, dpr);

    const cx = size / 2;
    const cy = size / 2;
    const maxR = 150;
    const n = dimensions.length;
    const angleStep = (Math.PI * 2) / n;
    const startAngle = -Math.PI / 2;

    // Background grid
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
        ctx.strokeStyle = ring === 5 ? '#cbd5e1' : '#e2e8f0';
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
        ctx.strokeStyle = '#e2e8f0';
        ctx.stroke();

        // Label
        const lx = cx + (maxR + 28) * Math.cos(angle);
        const ly = cy + (maxR + 28) * Math.sin(angle);
        ctx.font = '13px "Noto Sans KR", sans-serif';
        ctx.fillStyle = '#475569';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(dim.title, lx, ly);
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
    ctx.fillStyle = 'rgba(108, 92, 231, 0.2)';
    ctx.fill();
    ctx.strokeStyle = '#6C5CE7';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Data points
    dimensions.forEach((dim, i) => {
        const angle = startAngle + i * angleStep;
        const r = (dim.score / 5) * maxR;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#6C5CE7';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

// ─── Download Report as Image ───
function downloadReport() {
    const el = document.getElementById('reportContainer');
    // Simple print fallback
    window.print();
}

// ─── Restart ───
function restartAssessment() {
    currentQuestion = 0;
    answers = {};
    leadData = {};
    document.getElementById('leadForm').reset();
    showStep('step-landing');
}
