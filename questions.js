const ASSESSMENT_DATA = {
    dimensions: [
        {
            id: "leadership",
            title: "리더십 & 전략",
            icon: "🎯",
            description: "경영진의 AI 비전과 전략적 방향성",
            question: "우리 조직의 AI 활용에 대한 리더십의 관여 수준은?",
            options: [
                { score: 1, label: "AI에 대한 관심이 거의 없거나 일회성 언급에 그침" },
                { score: 2, label: "AI 도입 필요성은 인식하나 구체적 전략이 없음" },
                { score: 3, label: "AI 활용 방향은 있으나 부서별로 산발적으로 진행" },
                { score: 4, label: "전사 AI 전략이 수립되어 있고 실행 로드맵이 존재함" },
                { score: 5, label: "경영진이 AI-First 비전을 주도하며 조직 전체에 내재화" }
            ]
        },
        {
            id: "culture",
            title: "조직문화 & 수용도",
            icon: "🧬",
            description: "구성원들의 AI 활용 태도와 문화적 수용성",
            question: "구성원들의 업무 중 AI 도구 활용 수준은?",
            options: [
                { score: 1, label: "대부분의 구성원이 AI 도구를 사용하지 않음" },
                { score: 2, label: "일부 얼리어답터만 개인적으로 ChatGPT 등을 사용" },
                { score: 3, label: "팀 단위로 AI 도구를 업무에 시범 활용하고 있음" },
                { score: 4, label: "대부분의 부서에서 AI를 일상 업무에 활용하고 있음" },
                { score: 5, label: "AI 활용이 조직 문화로 정착, 자발적 실험과 공유가 활발" }
            ]
        },
        {
            id: "process",
            title: "업무 프로세스 & 적용",
            icon: "⚙️",
            description: "실제 업무 프로세스에 AI가 통합된 수준",
            question: "AI가 핵심 업무 프로세스에 통합된 정도는?",
            options: [
                { score: 1, label: "업무 프로세스에 AI가 전혀 반영되어 있지 않음" },
                { score: 2, label: "단순 반복 업무(번역, 요약 등)에만 부분적으로 활용" },
                { score: 3, label: "주요 업무 일부에 AI 워크플로우가 도입되어 있음" },
                { score: 4, label: "핵심 비즈니스 프로세스에 AI가 체계적으로 통합됨" },
                { score: 5, label: "AI 기반으로 업무 프로세스 자체가 재설계(BPR)되었음" }
            ]
        },
        {
            id: "capability",
            title: "역량 & 교육 체계",
            icon: "📚",
            description: "AI 역량 개발을 위한 교육 및 학습 체계",
            question: "조직의 AI 역량 개발 및 교육 체계 수준은?",
            options: [
                { score: 1, label: "AI 관련 교육이 전무하거나 계획이 없음" },
                { score: 2, label: "외부 특강이나 일회성 교육을 진행한 적 있음" },
                { score: 3, label: "직무별 AI 교육 프로그램이 운영 중이나 체계 부족" },
                { score: 4, label: "체계적인 AI 역량 프레임워크와 교육 로드맵이 존재" },
                { score: 5, label: "AI 학습이 조직 내 자생적으로 이루어지는 학습 생태계 구축" }
            ]
        },
        {
            id: "infra",
            title: "인프라 & 거버넌스",
            icon: "🔐",
            description: "AI 활용을 위한 기술 인프라와 정책 체계",
            question: "AI 활용을 위한 인프라와 거버넌스 수준은?",
            options: [
                { score: 1, label: "AI 관련 인프라나 정책이 전혀 없음" },
                { score: 2, label: "개인별 무료 도구 사용, 보안/정책 가이드 부재" },
                { score: 3, label: "기업용 AI 도구 도입, 기본적인 사용 가이드라인 존재" },
                { score: 4, label: "AI 플랫폼 구축, 보안/윤리 정책 및 거버넌스 체계 운영" },
                { score: 5, label: "자체 AI 플랫폼과 데이터 파이프라인, 고도화된 거버넌스 운영" }
            ]
        }
    ],

    levels: [
        {
            range: [5, 8],
            level: 1,
            name: "Unaware",
            nameKo: "미인지 단계",
            color: "#E74C3C",
            summary: "AI 도입의 필요성에 대한 조직적 인식이 부족한 상태입니다.",
            description: "조직 내 AI 활용이 거의 이루어지지 않고 있으며, AI 전환에 대한 전략과 비전이 부재합니다. 빠르게 변화하는 비즈니스 환경에서 경쟁력 약화가 우려됩니다.",
            recommendations: [
                "경영진 대상 AI 트렌드 및 비즈니스 임팩트 워크숍 진행",
                "경쟁사 및 산업 내 AI 활용 사례 벤치마킹 실시",
                "AI 전환 필요성에 대한 조직 내 공감대 형성 캠페인",
                "Quick Win이 가능한 소규모 AI 파일럿 프로젝트 선정"
            ]
        },
        {
            range: [9, 12],
            level: 2,
            name: "Exploring",
            nameKo: "탐색 단계",
            color: "#E67E22",
            summary: "AI에 대한 관심은 있으나 체계적인 접근이 부족한 상태입니다.",
            description: "일부 구성원이 개인적으로 AI 도구를 활용하고 있으나, 조직 차원의 전략과 체계가 없어 산발적으로 진행되고 있습니다. AI 교육이 일회성에 그치고 있어 지속적 역량 개발이 필요합니다.",
            recommendations: [
                "전사 AI 전환 비전 및 로드맵 수립",
                "부서별 AI 활용 니즈 파악 및 우선순위 도출",
                "기업용 AI 도구 도입 및 사용 가이드라인 마련",
                "AI 챔피언 그룹 구성을 통한 내부 전파 체계 구축"
            ]
        },
        {
            range: [13, 16],
            level: 3,
            name: "Experimenting",
            nameKo: "실험 단계",
            color: "#F1C40F",
            summary: "AI 활용이 시작되었으나 전사적 확산이 필요한 단계입니다.",
            description: "팀 단위로 AI를 업무에 적용하기 시작했고, 부분적인 성과가 나타나고 있습니다. 그러나 부서 간 편차가 크고, 체계적인 교육과 프로세스 통합이 과제입니다.",
            recommendations: [
                "성공 사례 기반 전사 확산 전략 수립",
                "직무별 맞춤형 AI 역량 프레임워크 설계",
                "AI 활용 성과 측정 KPI 및 대시보드 구축",
                "부서 간 AI 활용 베스트 프랙티스 공유 체계 마련"
            ]
        },
        {
            range: [17, 20],
            level: 4,
            name: "Integrating",
            nameKo: "통합 단계",
            color: "#2ECC71",
            summary: "AI가 업무 프로세스에 체계적으로 통합되고 있는 단계입니다.",
            description: "대부분의 부서에서 AI를 활용하고 있으며, 핵심 비즈니스 프로세스에 AI가 통합되어 있습니다. 체계적인 교육과 거버넌스가 운영되고 있어 조직 전반의 AI 역량이 고르게 성장하고 있습니다.",
            recommendations: [
                "AI 기반 업무 프로세스 재설계(BPR) 추진",
                "고급 AI 활용 역량(프롬프트 엔지니어링, AI 에이전트 등) 교육",
                "AI 활용 내재화를 위한 인센티브 및 인정 체계 도입",
                "산업 특화 AI 솔루션 개발 및 적용"
            ]
        },
        {
            range: [21, 25],
            level: 5,
            name: "Transforming",
            nameKo: "전환 단계",
            color: "#6C5CE7",
            summary: "AI가 조직의 DNA로 내재화된 선도적 단계입니다.",
            description: "AI 활용이 조직 문화로 완전히 정착되어 있으며, 구성원들이 자발적으로 AI를 실험하고 공유합니다. AI 기반으로 비즈니스 모델 자체가 혁신되고 있으며, 자생적 학습 생태계가 구축되어 있습니다.",
            recommendations: [
                "AI 기반 신규 비즈니스 모델 및 수익원 발굴",
                "산업 내 AI 리더십 포지셔닝 강화",
                "AI 혁신 랩 운영 및 사내 벤처 프로그램 활성화",
                "외부 AI 생태계(스타트업, 학계 등) 협업 확대"
            ]
        }
    ]
};
