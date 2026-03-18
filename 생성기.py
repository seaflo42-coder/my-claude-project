#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   한국 문화유산 AI 이미지 프롬프트 생성기     ║
║                                              ║
║   실행 방법: python 생성기.py                 ║
╚══════════════════════════════════════════════╝

코드를 몰라도 됩니다!
번호만 선택하면 생성형 AI용 프롬프트가 자동으로 만들어집니다.
"""

import json
import os
import sys

# ──────────────────────────────────────────────
# 한국 문화유산 데이터베이스 (내장)
# ──────────────────────────────────────────────

HERITAGE_DB = [
    {
        "name": "숭례문",
        "name_en": "Sungnyemun Gate",
        "type": "국보",
        "category": "건축",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시",
        "description": "조선시대 한양도성의 남쪽 정문. 2층 누각 형태의 문루와 석축 기단, 팔작지붕에 다포식 공포, 장엄한 단청.",
        "visual": {
            "style": ["팔작지붕", "겹처마", "공포(bracket system)", "기단(stone platform)", "문루(gate pavilion)"],
            "colors": ["단청 오방색(청·적·황·백·흑)", "기와 회색", "목재 갈색"],
            "materials": ["목재", "기와", "석재", "단청"],
            "atmosphere": "장엄한, 위풍당당한, 조선 왕조의 위엄",
        },
    },
    {
        "name": "경복궁 근정전",
        "name_en": "Geunjeongjeon Hall, Gyeongbokgung Palace",
        "type": "국보",
        "category": "건축",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시",
        "description": "조선 왕조의 법궁인 경복궁의 정전. 왕의 즉위식과 외국 사신 접견이 이루어진 곳. 이중 기단 위 중층 건물.",
        "visual": {
            "style": ["중층 팔작지붕", "이중 월대(기단)", "답도(踏道)", "드므(화재방지 물항아리)", "어좌(옥좌)"],
            "colors": ["단청 오방색", "금색 용 장식", "홍색 기둥", "회색 화강암 기단"],
            "materials": ["목재", "화강암", "기와", "금박"],
            "atmosphere": "왕실의 권위, 유교적 질서, 장엄한 궁궐 공간",
        },
    },
    {
        "name": "창덕궁 부용정",
        "name_en": "Buyongjeong Pavilion, Changdeokgung Palace",
        "type": "보물",
        "category": "건축",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시",
        "description": "창덕궁 후원의 부용지 위에 세워진 정자. 십자형 평면에 이익공 양식, 연못에 비친 모습이 아름답다.",
        "visual": {
            "style": ["십자형 정자", "이익공 양식", "연못 위 누각", "후원 정원"],
            "colors": ["단청 채색", "연못 비취색", "주변 녹음"],
            "materials": ["목재", "석재", "기와"],
            "atmosphere": "고요한, 운치 있는, 선비의 풍류, 자연과 조화",
        },
    },
    {
        "name": "석굴암 본존불",
        "name_en": "Seokguram Grotto Main Buddha",
        "type": "국보",
        "category": "불교 조각",
        "era": "통일신라",
        "era_en": "Unified Silla (668-935)",
        "location": "경상북도 경주",
        "description": "토함산 중턱 인공 석굴 안의 본존불. 화강암을 깎아 만든 항마촉지인의 석가여래좌상. 불교미술의 최고 걸작.",
        "visual": {
            "style": ["항마촉지인(손 모양)", "광배(둥근 후광)", "연화대좌(연꽃 받침)", "석굴 돔 천장"],
            "colors": ["화강암 회백색", "은은한 자연광"],
            "materials": ["화강암"],
            "atmosphere": "숭고한, 명상적, 고요한 불교적 성스러움",
        },
    },
    {
        "name": "금동미륵보살반가사유상",
        "name_en": "Gilt-bronze Pensive Maitreya Bodhisattva",
        "type": "국보",
        "category": "불교 조각",
        "era": "삼국시대",
        "era_en": "Three Kingdoms Period (BC 57-AD 668)",
        "location": "국립중앙박물관",
        "description": "반가부좌로 깊은 사유에 잠긴 보살상. 부드러운 미소, 유려한 옷주름, 자연스러운 자세. 한국 불교 조각의 백미.",
        "visual": {
            "style": ["반가부좌 자세", "삼산관(머리장식)", "천의(얇은 옷)", "자연스러운 미소"],
            "colors": ["금동색(황금빛 청동)", "녹청색 녹"],
            "materials": ["금동(도금 청동)"],
            "atmosphere": "명상적, 신비로운 미소, 우아한 곡선미",
        },
    },
    {
        "name": "고려청자 상감운학문매병",
        "name_en": "Goryeo Celadon Maebyeong with Inlaid Cloud and Crane",
        "type": "국보",
        "category": "도자기",
        "era": "고려",
        "era_en": "Goryeo Dynasty (918-1392)",
        "location": "국립중앙박물관",
        "description": "고려청자의 대표작. 매병 형태에 구름과 학 문양을 상감기법으로 시문. 고려 특유의 비색 유약.",
        "visual": {
            "style": ["매병(梅甁) 형태", "상감기법(inlay)", "운학문(구름+학)", "당초문 띠"],
            "colors": ["비색(翡色, jade-green)", "백토 상감 흰색", "자토 상감 검은색"],
            "materials": ["도자기", "비색 유약"],
            "atmosphere": "우아한, 고려의 세련된 귀족 미학",
        },
    },
    {
        "name": "조선백자 달항아리",
        "name_en": "Joseon White Porcelain Moon Jar",
        "type": "국보",
        "category": "도자기",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "국립중앙박물관",
        "description": "조선 후기 백자의 대표작. 보름달처럼 크고 둥근 형태. 순백의 유약, 약간의 비대칭이 주는 자연스러운 아름다움.",
        "visual": {
            "style": ["완전한 구형(보름달)", "약간의 비대칭", "무문(장식 없음)", "넉넉한 크기"],
            "colors": ["순백색(유백색)", "약간의 회청색 빛"],
            "materials": ["백자", "순백 유약"],
            "atmosphere": "담백한, 소박한, 조선 선비의 미학, 달빛 같은 온화함",
        },
    },
    {
        "name": "팔만대장경 장경판전",
        "name_en": "Janggyeongpanjeon, Haeinsa Temple",
        "type": "국보/세계유산",
        "category": "건축",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "경상남도 합천",
        "description": "해인사의 팔만대장경 보관 건물. 자연 환기 시스템으로 700년간 경판을 보존. 과학적 건축의 걸작.",
        "visual": {
            "style": ["긴 목조 건물", "크기가 다른 창문(환기용)", "경판 보관 선반", "산중 사찰"],
            "colors": ["고목 갈색", "기와 회색", "주변 녹음"],
            "materials": ["목재", "기와", "대장경 목판"],
            "atmosphere": "경건한, 고즈넉한, 지혜의 보고, 산사의 고요함",
        },
    },
    {
        "name": "조선 궁중 혼례",
        "name_en": "Joseon Royal Wedding Ceremony",
        "type": "무형유산/의례",
        "category": "생활문화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "궁궐",
        "description": "조선시대 왕실의 가례(嘉禮). 붉은 원삼과 족두리, 활옷을 입은 왕비와 곤룡포의 왕. 화려한 궁중 의례.",
        "visual": {
            "style": ["원삼(圓衫)", "족두리", "활옷", "곤룡포", "가마", "대례상", "청사홍사 초"],
            "colors": ["홍색(원삼)", "남색(치마)", "금색 자수", "청색·홍색 초"],
            "materials": ["비단", "금사자수", "칠보장식"],
            "atmosphere": "화려한, 장엄한, 왕실의 격식, 경사스러운",
        },
    },
    {
        "name": "한복 (여성 전통 한복)",
        "name_en": "Hanbok - Traditional Korean Women's Dress",
        "type": "무형유산",
        "category": "복식",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "저고리와 치마로 구성된 여성 한복. 짧은 저고리의 직선미와 풍성한 치마의 곡선미가 조화. 고름, 동정, 깃 등 세부 요소.",
        "visual": {
            "style": ["저고리(짧은 상의)", "치마(긴 하의)", "고름(매듭끈)", "동정(흰 깃)", "버선(흰 버선)"],
            "colors": ["색동(오방색 줄무늬)", "연두·분홍·노랑 배색", "흰색 동정"],
            "materials": ["비단(명주)", "모시", "삼베"],
            "atmosphere": "우아한, 단아한, 한국 여성의 곡선미",
        },
    },
    {
        "name": "조선 선비의 사랑방",
        "name_en": "Joseon Scholar's Sarangbang Study Room",
        "type": "생활문화",
        "category": "건축/실내",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국 한옥",
        "description": "조선시대 선비의 서재. 문방사우(붓·먹·벼루·종이), 책장, 서안(書案), 병풍, 소나무 분재 등으로 꾸민 검소하고 격조 높은 공간.",
        "visual": {
            "style": ["한옥 온돌방", "서안(낮은 책상)", "문방사우", "사방탁자(책장)", "먹그림 병풍", "한지 창호"],
            "colors": ["한지 미색", "목재 갈색", "먹색", "옅은 자연색"],
            "materials": ["한지", "목재(소나무·오동나무)", "돌(벼루)", "먹"],
            "atmosphere": "고즈넉한, 학문적, 검소하면서 격조 높은, 선비의 풍류",
        },
    },
    {
        "name": "한옥마을 풍경",
        "name_en": "Traditional Hanok Village Scenery",
        "type": "문화경관",
        "category": "건축/마을",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국 (전주, 경주, 안동 등)",
        "description": "기와지붕이 물결치듯 이어지는 한옥마을. 돌담길, 장독대, 대청마루, 안마당 등 한국 전통 주거 풍경.",
        "visual": {
            "style": ["기와지붕 곡선", "돌담길", "장독대", "대청마루", "안마당", "굴뚝"],
            "colors": ["기와 회흑색", "흙담 황토색", "장독 갈색", "하늘색"],
            "materials": ["기와", "흙", "돌", "목재", "한지"],
            "atmosphere": "정겨운, 평화로운, 한국적 향수, 사계절의 아름다움",
        },
    },
    {
        "name": "고구려 무용총 벽화",
        "name_en": "Goguryeo Muyongchong Tomb Mural",
        "type": "국보",
        "category": "벽화",
        "era": "고구려",
        "era_en": "Goguryeo Kingdom (BC 37-AD 668)",
        "location": "중국 지린성 (원본) / 국내 모사본",
        "description": "고구려 고분벽화. 사냥하는 무사, 춤추는 인물, 사신도(청룡·백호·주작·현무) 등 역동적 장면.",
        "visual": {
            "style": ["사냥 장면", "무용 장면", "사신도(四神圖)", "연회 장면", "역동적 구도"],
            "colors": ["주홍색", "황토색", "먹색", "녹색", "청색"],
            "materials": ["석회 벽면", "광물 안료"],
            "atmosphere": "역동적, 힘찬, 고구려의 진취적 기상",
        },
    },
    {
        "name": "신라 금관",
        "name_en": "Silla Gold Crown",
        "type": "국보",
        "category": "금속공예",
        "era": "신라",
        "era_en": "Silla Kingdom (BC 57-AD 935)",
        "location": "국립경주박물관",
        "description": "신라 왕릉에서 출토된 순금 금관. 나뭇가지(出)와 사슴뿔 모양 장식, 곡옥(曲玉)과 금 드리개.",
        "visual": {
            "style": ["출자형(出字形) 세움장식", "사슴뿔 장식", "곡옥 달림장식", "금실 드리개"],
            "colors": ["순금색", "비취색(곡옥)", "은빛"],
            "materials": ["순금", "비취(곡옥)", "금실"],
            "atmosphere": "화려한, 신비로운, 신라 왕실의 권위와 화려함",
        },
    },
    {
        "name": "백제 금동대향로",
        "name_en": "Baekje Gilt-bronze Incense Burner",
        "type": "국보",
        "category": "금속공예",
        "era": "백제",
        "era_en": "Baekje Kingdom (BC 18-AD 660)",
        "location": "국립부여박물관",
        "description": "백제 예술의 극치. 용이 받치고 봉황이 올라앉은 향로. 뚜껑에 산악 신선세계, 몸체에 연꽃잎 표현.",
        "visual": {
            "style": ["용(받침)", "봉황(꼭대기)", "산악 신선세계(뚜껑)", "연꽃잎(몸체)", "74개 산봉우리와 인물"],
            "colors": ["금동색(황금빛)", "녹청색(녹)", "세밀한 세부 묘사"],
            "materials": ["금동(도금 청동)"],
            "atmosphere": "신비로운, 정교한, 백제의 섬세한 예술 세계",
        },
    },
    {
        "name": "조선 갑옷 무장",
        "name_en": "Joseon Dynasty Armored Warrior",
        "type": "군사문화",
        "category": "복식/군사",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "조선시대 무관의 갑옷 차림. 두정갑(철 못 박은 갑옷), 투구, 목가리개, 환도(칼), 활과 화살통.",
        "visual": {
            "style": ["두정갑(studded armor)", "철 투구", "목가리개(목 보호대)", "환도(칼)", "각궁(활)", "전립(모자)"],
            "colors": ["철 은회색", "가죽 갈색", "홍색 전포(겉옷)"],
            "materials": ["철", "가죽", "비단", "대나무(활)"],
            "atmosphere": "위풍당당한, 무인의 기상, 전투 준비된",
        },
    },
    {
        "name": "조선 시장 풍경",
        "name_en": "Joseon Traditional Market Scene",
        "type": "생활문화",
        "category": "풍속",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "조선시대 오일장(5일장). 보부상, 엿장수, 약재상, 떡전, 포목전 등이 늘어선 활기찬 시장 풍경.",
        "visual": {
            "style": ["초가 가게(움막)", "보부상(등짐 장수)", "떡살·엿가위", "가마솥", "멍석·자리"],
            "colors": ["황토색 흙바닥", "짚 노란색", "다양한 식재료 색"],
            "materials": ["짚", "목재", "흙", "무명천"],
            "atmosphere": "활기찬, 정겨운, 서민 생활의 활력",
        },
    },
    {
        "name": "제주 돌하르방",
        "name_en": "Jeju Dolhareubang Stone Statue",
        "type": "민속문화재",
        "category": "석조",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "제주특별자치도",
        "description": "제주도 성문 앞에 세운 수호신 석상. 큰 눈, 주먹코, 양손을 배에 올린 특유의 자세. 현무암으로 제작.",
        "visual": {
            "style": ["벙거지 모자", "튀어나온 큰 눈", "주먹코", "배 위에 올린 두 손", "투박한 조각"],
            "colors": ["현무암 검회색", "이끼 녹색"],
            "materials": ["현무암(제주 화산석)"],
            "atmosphere": "수호자의 위엄, 소박한 해학, 제주의 바람과 돌",
        },
    },
]

# 시대별 보조 정보
ERA_CONTEXT = {
    "고구려": "강렬하고 역동적인 기상. 벽화 중심. 기마 문화, 전투 장면, 사신도가 대표적.",
    "백제": "부드럽고 섬세한 곡선미. '백제의 미소'로 대표되는 온화한 예술 세계.",
    "신라": "화려한 금속공예. 금관, 귀걸이, 곡옥 등 호화로운 장신구 문화.",
    "통일신라": "불교미술의 전성기. 석굴암, 불국사. 세련되고 이상적인 불교 조각.",
    "고려": "청자와 불화의 시대. 귀족적 세련미. 비색 청자, 상감기법이 대표적.",
    "조선": "유교 문화. 검소함 속의 격조. 백자, 한옥, 한복, 궁궐 건축이 대표적.",
    "삼국시대": "고구려·백제·신라 각각의 개성 있는 문화. 고분, 금속공예, 토기가 대표적.",
}


# ──────────────────────────────────────────────
# 프롬프트 생성 엔진
# ──────────────────────────────────────────────

def make_prompt_photorealistic(item):
    """사실적 사진 스타일 프롬프트"""
    v = item["visual"]
    parts = [
        f'{item["name_en"]}, {item["era_en"]}',
        f'featuring: {", ".join(v["style"][:4])}',
        f'color palette: {", ".join(v["colors"])}',
        f'materials: {", ".join(v["materials"])}',
        f'{v["atmosphere"]}',
        "photorealistic, highly detailed, 8K resolution, dramatic natural lighting",
    ]
    return ", ".join(parts)


def make_prompt_painting(item):
    """전통 한국화 스타일 프롬프트"""
    v = item["visual"]
    parts = [
        f'{item["name_en"]}, {item["era_en"]}',
        f'depicted in traditional Korean painting (Hanguk-hwa) style',
        f'elements: {", ".join(v["style"][:3])}',
        f'color tones: {", ".join(v["colors"][:2])}',
        "ink wash and mineral pigment on hanji paper, visible brush strokes",
        "contemplative, artistic, traditional East Asian aesthetic",
    ]
    return ", ".join(parts)


def make_prompt_illustration(item):
    """세밀 일러스트 스타일 프롬프트"""
    v = item["visual"]
    parts = [
        f'{item["name_en"]}, {item["era_en"]}',
        f'detailed illustration showing: {", ".join(v["style"])}',
        f'palette: {", ".join(v["colors"])}',
        f'materials depicted: {", ".join(v["materials"])}',
        f'{v["atmosphere"]}',
        "editorial illustration, clean lines, rich detail, cultural accuracy",
    ]
    return ", ".join(parts)


def make_prompt_3d(item):
    """3D 렌더링 스타일 프롬프트"""
    v = item["visual"]
    parts = [
        f'{item["name_en"]}, {item["era_en"]}',
        f'3D render with: {", ".join(v["style"][:4])}',
        f'realistic materials: {", ".join(v["materials"])}',
        f'color: {", ".join(v["colors"][:2])}',
        "cinematic lighting, physically based rendering, octane render, museum quality",
    ]
    return ", ".join(parts)


def make_prompt_korean(item, style_name):
    """한글 프롬프트"""
    v = item["visual"]
    style_map = {
        "사실적 사진": "사실적 사진 스타일, 고해상도 8K, 자연광",
        "전통 한국화": "전통 한국화 스타일, 한지 위 수묵채색, 붓터치",
        "세밀 일러스트": "세밀한 일러스트레이션, 정확한 고증, 깨끗한 선",
        "3D 렌더링": "3D 렌더링, 사실적 재질 표현, 시네마틱 조명",
    }
    parts = [
        f'한국 {item["category"]}: {item["name"]}',
        f'시대: {item["era"]} ({item["era_en"]})',
        f'주요 요소: {", ".join(v["style"])}',
        f'색감: {", ".join(v["colors"])}',
        f'재질: {", ".join(v["materials"])}',
        f'분위기: {v["atmosphere"]}',
        f'스타일: {style_map.get(style_name, style_name)}',
        "고증에 충실한 역사적 표현",
    ]
    return ". ".join(parts)


def make_midjourney(item):
    """Midjourney 전용 프롬프트"""
    prompt = make_prompt_photorealistic(item)
    return f"{prompt} --ar 16:9 --q 2 --style raw --v 6"


def make_dalle(item):
    """DALL-E 전용 프롬프트"""
    v = item["visual"]
    return (
        f'Create a historically accurate, detailed image of {item["name_en"]} '
        f'from the {item["era_en"]}. '
        f'It should show: {", ".join(v["style"][:4])}. '
        f'The color palette should include {", ".join(v["colors"][:2])}. '
        f'Made of {", ".join(v["materials"])}. '
        f'The mood should be {v["atmosphere"]}. '
        f'Ensure period-appropriate historical accuracy.'
    )


def make_stable_diffusion(item):
    """Stable Diffusion 전용 프롬프트"""
    prompt = make_prompt_photorealistic(item)
    return f"{prompt}, masterpiece, best quality, ultra detailed, sharp focus"


STYLE_GENERATORS = {
    "1": ("사실적 사진", make_prompt_photorealistic),
    "2": ("전통 한국화", make_prompt_painting),
    "3": ("세밀 일러스트", make_prompt_illustration),
    "4": ("3D 렌더링", make_prompt_3d),
}

MODEL_GENERATORS = {
    "1": ("Midjourney", make_midjourney),
    "2": ("DALL-E", make_dalle),
    "3": ("Stable Diffusion", make_stable_diffusion),
}


# ──────────────────────────────────────────────
# 화면 출력 함수들
# ──────────────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║                                                      ║")
    print("║    한국 문화유산 AI 이미지 프롬프트 생성기  v1.0     ║")
    print("║                                                      ║")
    print("║    국가유산청 데이터 기반 · 고증 자동 반영           ║")
    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()


def print_divider():
    print("─" * 56)


def show_main_menu():
    print_header()
    print("  무엇을 하시겠습니까?")
    print()
    print("  [1] 문화유산 선택해서 프롬프트 만들기")
    print("  [2] 전체 문화유산 한번에 프롬프트 만들기")
    print("  [3] 문화유산 목록 보기")
    print("  [4] 사용법 안내")
    print("  [0] 종료")
    print()


def show_heritage_list():
    """문화유산 목록 표시"""
    print()
    print("  ┌─ 문화유산 목록 ─────────────────────────────────┐")
    print()
    for i, item in enumerate(HERITAGE_DB, 1):
        print(f"  [{i:2d}] {item['name']}")
        print(f"       {item['type']} | {item['era']} | {item['category']}")
        print()
    print("  └────────────────────────────────────────────────────┘")


def show_heritage_detail(item):
    """문화유산 상세 정보 표시"""
    print()
    print_divider()
    print(f"  ■ {item['name']} ({item['name_en']})")
    print_divider()
    print(f"  분류: {item['type']} | {item['category']}")
    print(f"  시대: {item['era']} ({item['era_en']})")
    print(f"  위치: {item['location']}")
    print()
    print(f"  설명: {item['description']}")
    print()
    print(f"  시각 요소:")
    print(f"    양식: {', '.join(item['visual']['style'])}")
    print(f"    색감: {', '.join(item['visual']['colors'])}")
    print(f"    재질: {', '.join(item['visual']['materials'])}")
    print(f"    분위기: {item['visual']['atmosphere']}")
    if item["era"] in ERA_CONTEXT:
        print()
        print(f"  [{item['era']}시대 참고]")
        print(f"    {ERA_CONTEXT[item['era']]}")
    print_divider()


def show_style_menu():
    """스타일 선택 메뉴"""
    print()
    print("  이미지 스타일을 선택하세요:")
    print()
    print("  [1] 사실적 사진 스타일 (포토리얼리스틱)")
    print("  [2] 전통 한국화 스타일 (수묵·채색)")
    print("  [3] 세밀 일러스트 스타일")
    print("  [4] 3D 렌더링 스타일")
    print("  [5] 전부 다 만들기 (4가지 스타일 모두)")
    print()


def show_model_menu():
    """AI 모델 선택 메뉴"""
    print()
    print("  어떤 AI 모델용 프롬프트를 만들까요?")
    print()
    print("  [1] Midjourney")
    print("  [2] DALL-E (ChatGPT)")
    print("  [3] Stable Diffusion")
    print("  [4] 범용 (아무 모델에나 사용 가능)")
    print("  [5] 전부 다 만들기")
    print()


def print_prompt_box(title, prompt):
    """프롬프트를 박스 안에 표시"""
    print()
    print(f"  ┌─ {title} ─{'─' * max(0, 48 - len(title))}┐")
    print()
    # 프롬프트를 적절한 길이로 줄바꿈
    words = prompt.split()
    line = "    "
    for word in words:
        if len(line) + len(word) + 1 > 72:
            print(line)
            line = "    " + word
        else:
            line = line + " " + word if line.strip() else "    " + word
    if line.strip():
        print(line)
    print()
    print(f"  └{'─' * 54}┘")


# ──────────────────────────────────────────────
# 메인 기능들
# ──────────────────────────────────────────────

def generate_single():
    """단일 문화유산 선택 → 프롬프트 생성"""
    show_heritage_list()
    print("  문화유산 번호를 입력하세요 (0: 뒤로가기): ", end="")
    try:
        choice = int(input().strip())
    except (ValueError, EOFError):
        return
    if choice == 0 or choice > len(HERITAGE_DB):
        return

    item = HERITAGE_DB[choice - 1]
    show_heritage_detail(item)

    show_style_menu()
    print("  스타일 번호: ", end="")
    try:
        style_choice = input().strip()
    except EOFError:
        return

    show_model_menu()
    print("  AI 모델 번호: ", end="")
    try:
        model_choice = input().strip()
    except EOFError:
        return

    print()
    print("=" * 56)
    print(f"  ■ {item['name']} 프롬프트 생성 결과")
    print("=" * 56)

    # 스타일별 프롬프트 생성
    if style_choice == "5":
        styles_to_gen = ["1", "2", "3", "4"]
    else:
        styles_to_gen = [style_choice] if style_choice in STYLE_GENERATORS else ["1"]

    for sid in styles_to_gen:
        style_name, gen_func = STYLE_GENERATORS[sid]
        prompt_en = gen_func(item)
        prompt_ko = make_prompt_korean(item, style_name)
        print_prompt_box(f"영문 - {style_name}", prompt_en)
        print_prompt_box(f"한글 - {style_name}", prompt_ko)

    # AI 모델별 프롬프트 생성
    if model_choice == "5":
        models_to_gen = ["1", "2", "3"]
    elif model_choice == "4":
        models_to_gen = []  # 범용은 위에서 이미 생성
    else:
        models_to_gen = [model_choice] if model_choice in MODEL_GENERATORS else []

    for mid in models_to_gen:
        model_name, gen_func = MODEL_GENERATORS[mid]
        prompt = gen_func(item)
        print_prompt_box(f"{model_name} 전용", prompt)

    # 파일 저장 제안
    print()
    print("  파일로 저장할까요? (y/n): ", end="")
    try:
        save = input().strip().lower()
    except EOFError:
        save = "n"

    if save == "y":
        save_prompts(item, styles_to_gen, models_to_gen)


def generate_all():
    """전체 문화유산 일괄 프롬프트 생성"""
    print()
    print("  전체 문화유산에 대해 프롬프트를 생성합니다.")
    print(f"  총 {len(HERITAGE_DB)}개 항목")
    print()

    show_model_menu()
    print("  AI 모델 번호: ", end="")
    try:
        model_choice = input().strip()
    except EOFError:
        return

    results = []
    for item in HERITAGE_DB:
        entry = {
            "name": item["name"],
            "name_en": item["name_en"],
            "type": item["type"],
            "era": item["era"],
            "category": item["category"],
            "prompts": {},
        }

        # 4가지 스타일
        for sid, (style_name, gen_func) in STYLE_GENERATORS.items():
            entry["prompts"][f"영문_{style_name}"] = gen_func(item)
            entry["prompts"][f"한글_{style_name}"] = make_prompt_korean(item, style_name)

        # AI 모델별
        if model_choice == "5":
            for mid, (model_name, gen_func) in MODEL_GENERATORS.items():
                entry["prompts"][model_name] = gen_func(item)
        elif model_choice in MODEL_GENERATORS:
            model_name, gen_func = MODEL_GENERATORS[model_choice]
            entry["prompts"][model_name] = gen_func(item)

        results.append(entry)
        print(f"  ✓ {item['name']} 완료")

    # 저장
    os.makedirs("output", exist_ok=True)
    output_path = "output/전체_프롬프트.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 읽기 쉬운 텍스트 버전도 저장
    txt_path = "output/전체_프롬프트.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for entry in results:
            f.write(f"{'=' * 60}\n")
            f.write(f"{entry['name']} ({entry['name_en']})\n")
            f.write(f"{entry['type']} | {entry['era']} | {entry['category']}\n")
            f.write(f"{'=' * 60}\n\n")
            for prompt_name, prompt_text in entry["prompts"].items():
                f.write(f"[{prompt_name}]\n")
                f.write(f"{prompt_text}\n\n")
            f.write("\n")

    print()
    print_divider()
    print(f"  저장 완료!")
    print(f"  JSON: {output_path}")
    print(f"  텍스트: {txt_path}")
    print_divider()
    print()
    print("  output/ 폴더의 파일을 열어서")
    print("  원하는 프롬프트를 복사해 사용하세요!")


def save_prompts(item, styles, models):
    """단일 항목 프롬프트를 파일로 저장"""
    os.makedirs("output", exist_ok=True)

    safe_name = item["name"].replace(" ", "_")
    txt_path = f"output/{safe_name}_프롬프트.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"{item['name']} ({item['name_en']})\n")
        f.write(f"{item['type']} | {item['era']} | {item['category']}\n")
        f.write(f"{'=' * 60}\n\n")

        for sid in styles:
            style_name, gen_func = STYLE_GENERATORS[sid]
            f.write(f"[영문 - {style_name}]\n")
            f.write(f"{gen_func(item)}\n\n")
            f.write(f"[한글 - {style_name}]\n")
            f.write(f"{make_prompt_korean(item, style_name)}\n\n")

        for mid in models:
            if mid in MODEL_GENERATORS:
                model_name, gen_func = MODEL_GENERATORS[mid]
                f.write(f"[{model_name} 전용]\n")
                f.write(f"{gen_func(item)}\n\n")

    print()
    print(f"  저장 완료: {txt_path}")
    print(f"  이 파일을 열어서 프롬프트를 복사해 사용하세요!")


def show_help():
    """사용법 안내"""
    print()
    print_divider()
    print("  ■ 사용법 안내")
    print_divider()
    print()
    print("  이 도구는 한국 문화유산 데이터를 바탕으로")
    print("  생성형 AI 이미지 프롬프트를 자동으로 만들어 줍니다.")
    print()
    print("  ┌─ 사용 순서 ──────────────────────────────────┐")
    print("  │                                                │")
    print("  │  1. 문화유산을 선택합니다 (숭례문, 석굴암 등)  │")
    print("  │  2. 이미지 스타일을 선택합니다                 │")
    print("  │     (사진/한국화/일러스트/3D)                  │")
    print("  │  3. AI 모델을 선택합니다                       │")
    print("  │     (Midjourney/DALL-E/Stable Diffusion)       │")
    print("  │  4. 생성된 프롬프트를 복사해서 사용!           │")
    print("  │                                                │")
    print("  └────────────────────────────────────────────────┘")
    print()
    print("  ┌─ 프롬프트 사용법 ────────────────────────────┐")
    print("  │                                                │")
    print("  │  Midjourney: Discord에서 /imagine 뒤에 붙여넣기│")
    print("  │  DALL-E:     ChatGPT에 프롬프트 그대로 입력    │")
    print("  │  SD:         WebUI의 Prompt란에 붙여넣기       │")
    print("  │                                                │")
    print("  │  한글 프롬프트는 한글 지원 모델에서 사용하세요 │")
    print("  │  (예: DALL-E, 일부 한글 지원 SD 모델)          │")
    print("  │                                                │")
    print("  └────────────────────────────────────────────────┘")
    print()
    print("  ┌─ 고증 정보 ──────────────────────────────────┐")
    print("  │                                                │")
    print("  │  각 프롬프트에는 다음 고증 정보가 포함됩니다:  │")
    print("  │  - 정확한 시대와 연도                          │")
    print("  │  - 건축/공예 양식 (팔작지붕, 상감기법 등)      │")
    print("  │  - 전통 색상 (단청 오방색, 비색 등)            │")
    print("  │  - 재료 (화강암, 금동, 비단 등)                │")
    print("  │  - 시대별 분위기와 미학                        │")
    print("  │                                                │")
    print("  │  출처: 국가유산청 (heritage.go.kr)              │")
    print("  │                                                │")
    print("  └────────────────────────────────────────────────┘")
    print()


# ──────────────────────────────────────────────
# 메인 루프
# ──────────────────────────────────────────────

def main():
    while True:
        show_main_menu()
        print("  번호 입력: ", end="")
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  종료합니다. 감사합니다!")
            break

        if choice == "1":
            generate_single()
        elif choice == "2":
            generate_all()
        elif choice == "3":
            show_heritage_list()
        elif choice == "4":
            show_help()
        elif choice == "0":
            print("\n  종료합니다. 감사합니다!")
            break
        else:
            print("\n  올바른 번호를 입력하세요.")

        if choice in ("1", "2", "3", "4"):
            print()
            print("  Enter를 누르면 메인 메뉴로 돌아갑니다...")
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                break


if __name__ == "__main__":
    main()
