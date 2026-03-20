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
    # ── 회화/서예 ──────────────────────────────────
    {
        "name": "김홍도 풍속화첩",
        "name_en": "Danwon Genre Paintings by Kim Hong-do",
        "type": "국보",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (국립중앙박물관)",
        "description": "조선 후기 화원 김홍도(단원)가 그린 풍속화첩. 서당, 씨름, 무동, 빨래터 등 서민의 일상을 생동감 있게 포착한 25점의 풍속 장면. 간결하면서도 힘찬 필선과 여백의 미가 돋보이는 조선 회화의 걸작.",
        "visual": {
            "style": ["수묵담채", "여백 중심 구도", "간결한 필선", "원형 또는 대각선 구도", "인물 군상 배치"],
            "colors": ["수묵 먹색", "담채 연갈색", "옅은 청색", "연한 녹색", "화선지 미색"],
            "materials": ["화선지(한지)", "수묵", "담채 안료", "모필(붓)"],
            "atmosphere": "해학적인, 서민적 활기, 생동감 넘치는, 소박하고 따뜻한",
        },
    },
    {
        "name": "신윤복 미인도",
        "name_en": "Portrait of a Beauty by Shin Yun-bok",
        "type": "보물",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (간송미술관)",
        "description": "조선 후기 화원 신윤복(혜원)이 그린 여인 초상. 얹은머리에 트레머리를 한 기녀의 전신상으로, 자주색 치마와 연두색 저고리의 색감 대비가 돋보이며, 섬세한 필치로 여인의 우아한 자태와 내면의 감정을 표현한 걸작.",
        "visual": {
            "style": ["전신 입상 초상", "섬세한 세필 묘사", "S자형 자태", "얹은머리(기녀 머리)", "여백 배경"],
            "colors": ["자주색 치마", "연두색 저고리", "흰색 속치마", "검은 머리카락", "살색 피부", "화선지 미색"],
            "materials": ["비단(견본)", "수묵", "채색 안료", "세필(가는 붓)"],
            "atmosphere": "우아한, 고혹적인, 단아한 아름다움, 내밀한 정취",
        },
    },
    {
        "name": "정선 인왕제색도",
        "name_en": "After Rain at Mt. Inwang by Jeong Seon",
        "type": "국보",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (삼성미술관 리움)",
        "description": "조선 후기 겸재 정선이 1751년 비 온 뒤 인왕산의 모습을 실경으로 그린 진경산수화의 대표작. 먹을 흠뻑 적셔 화강암 바위의 질감을 표현한 적묵법과, 비 개인 뒤 산에 걸린 안개와 구름의 생동감이 압도적인 걸작.",
        "visual": {
            "style": ["진경산수화", "적묵법(젖은 먹 기법)", "대담한 구도", "화강암 바위 질감 표현", "운무(구름·안개) 묘사"],
            "colors": ["짙은 먹색(화강암 바위)", "옅은 먹색(안개·구름)", "담묵 회색 그라데이션", "화선지 미색"],
            "materials": ["화선지(한지)", "수묵", "대필(큰 붓)", "농묵·담묵"],
            "atmosphere": "웅장한, 비 개인 뒤의 청량함, 압도적 자연의 힘, 숭고한",
        },
    },
    {
        "name": "추사 세한도",
        "name_en": "Wintertime by Chusa Kim Jeong-hui",
        "type": "국보",
        "category": "서예/회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (국립중앙박물관)",
        "description": "조선 후기 추사 김정희가 제주 유배 시절인 1844년에 그린 문인화. 메마른 소나무와 잣나무, 단출한 집 한 채로 세한(歲寒)의 절개를 표현. 군더더기 없는 간결한 필치와 극도의 여백이 문인 정신의 극치를 보여주는 작품.",
        "visual": {
            "style": ["문인화(선비 그림)", "극도의 여백 구도", "마른 붓질(갈필)", "간결한 수묵 필선", "두루마리 형식(권축)"],
            "colors": ["수묵 먹색", "갈필 마른 먹색", "화선지 미색", "담묵 회색"],
            "materials": ["화선지(한지)", "수묵", "갈필(마른 붓)", "먹"],
            "atmosphere": "고독한, 절제된, 선비의 지조와 절개, 겨울의 쓸쓸함, 담백한",
        },
    },
    {
        "name": "안견 몽유도원도",
        "name_en": "Dream Journey to the Peach Blossom Land by An Gyeon",
        "type": "국보",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "일본 덴리대학교 도서관",
        "description": "조선 초기 화원 안견이 1447년 안평대군의 도원 꿈 이야기를 듣고 3일 만에 완성한 산수화. 현실 세계에서 이상향 도원으로 이행하는 장면을 두루마리 형식으로 펼쳐낸 작품으로, 북송 곽희파 화풍을 조선적으로 재해석한 걸작.",
        "visual": {
            "style": ["산수화(두루마리 횡권)", "곽희파 화풍", "게발(蟹爪) 나뭇가지 표현", "운두준법(구름 머리 준법)", "복숭아꽃 도원 묘사"],
            "colors": ["수묵 먹색", "담채 연녹색", "연분홍 복숭아꽃", "담청색 원산", "비단 미색 바탕"],
            "materials": ["비단(견본)", "수묵", "담채 안료", "모필(붓)"],
            "atmosphere": "몽환적인, 이상향의 신비로움, 유토피아적, 서사적 여정",
        },
    },
    {
        "name": "강세황 영통동구도",
        "name_en": "View of Yeongtonggok Valley by Kang Se-hwang",
        "type": "보물",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (국립중앙박물관)",
        "description": "조선 후기 표암 강세황이 개성 영통사 골짜기의 실경을 서양 투시법과 전통 산수화법을 결합하여 그린 진경산수화. 원근법적 시점과 사실적 수목 묘사가 돋보이며, 조선 회화에 서양 화법을 수용한 선구적 작품.",
        "visual": {
            "style": ["진경산수화", "서양식 원근 투시법 도입", "사실적 수목 묘사", "계곡 공간감 표현", "담채 산수"],
            "colors": ["수묵 먹색", "담채 녹색(수목)", "갈색(바위·토산)", "옅은 청색(원경)", "화선지 미색"],
            "materials": ["화선지(한지)", "수묵", "담채 안료", "모필(붓)"],
            "atmosphere": "사실적인, 탐구적인, 학자적 관찰, 자연의 깊이감",
        },
    },
    {
        "name": "이암 화조구자도",
        "name_en": "Puppies and Flowers by Yi Am",
        "type": "보물",
        "category": "회화",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 (국립중앙박물관)",
        "description": "조선 전기 왕족 출신 화가 이암이 그린 화조영모화. 들판에서 나비와 꽃 사이를 뛰노는 강아지들의 천진한 모습을 세밀하고 부드러운 필치로 묘사. 털의 질감 표현과 자연스러운 동세가 뛰어난 영모화의 백미.",
        "visual": {
            "style": ["영모화(동물 그림)", "세필 묘사", "몰골법(윤곽선 없는 기법)", "자연 배경 속 동물 배치", "사실적 모피 질감 표현"],
            "colors": ["흰색·갈색·검은색(강아지 털)", "연분홍(꽃)", "녹색(풀·잎)", "담채 자연색", "비단 미색 바탕"],
            "materials": ["비단(견본)", "수묵", "채색 안료", "세필(가는 붓)"],
            "atmosphere": "천진난만한, 따뜻한, 생기 넘치는, 목가적인, 사랑스러운",
        },
    },
    {
        "name": "고려불화 수월관음도",
        "name_en": "Goryeo Buddhist Water-Moon Avalokitesvara",
        "type": "국보",
        "category": "불화/회화",
        "era": "고려",
        "era_en": "Goryeo Dynasty (918-1392)",
        "location": "일본·미국·유럽 등 해외 소장 다수",
        "description": "고려시대 제작된 수월관음보살도. 투명한 사라(紗羅) 천의를 걸친 관음보살이 바위 위에 반가좌로 앉아 선재동자를 맞이하는 장면. 금니(金泥) 문양의 정교함, 투명 직물의 세밀한 표현, 화려한 영락 장식이 세계적으로 인정받는 고려 불교 회화의 정수.",
        "visual": {
            "style": ["불교 도상(보살 반가좌)", "금니(金泥) 세밀 문양", "투명 사라 직물 표현", "보타락가산 배경", "원형 두광·신광", "선재동자 배치"],
            "colors": ["금색(금니 문양·영락 장식)", "짙은 녹색·비색(배경)", "붉은색(영락·산호)", "백색(피부·달빛)", "감청색(바다)", "비단 바탕색"],
            "materials": ["비단(견본)", "금니(금가루 안료)", "석채(광물성 안료)", "세필(가는 붓)", "아교"],
            "atmosphere": "경건한, 신비로운, 자비로운, 극도로 정교한, 초월적 아름다움",
        },
    },
    {
        "name": "불국사",
        "name_en": "Bulguksa Temple",
        "type": "국보/세계유산",
        "category": "건축/사찰",
        "era": "통일신라",
        "era_en": "Unified Silla Dynasty (668-935)",
        "location": "경상북도 경주시",
        "description": "751년 김대성이 창건한 통일신라 불교 예술의 정수. 석축 기단 위에 목조 전각을 배치하고, 청운교·백운교 석계를 통해 대웅전에 이르는 구조. 다보탑과 석가탑이 대웅전 앞에 대칭 배치되어 있으며, 극락전·비로전 등 다수의 전각이 회랑으로 연결된 가람배치.",
        "visual": {
            "style": ["팔작지붕", "다포식 공포", "석축 기단(stone terrace)", "석계(stone stairway)", "회랑(corridor)", "가람배치(temple layout)"],
            "colors": ["단청 오방색(청·적·황·백·흑)", "기와 회흑색", "석축 화강암 회백색", "목재 적갈색"],
            "materials": ["목재", "기와", "화강암 석재", "단청"],
            "atmosphere": "장엄한, 신성한, 통일신라 불교 문화의 극치, 산중 사찰의 고요함과 웅장함",
        },
    },
    {
        "name": "수원화성",
        "name_en": "Hwaseong Fortress, Suwon",
        "type": "세계유산",
        "category": "건축/성곽",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "경기도 수원시",
        "description": "1794-1796년 정조의 명으로 정약용이 설계한 성곽. 거중기 등 신기술을 활용하여 축조. 총 길이 약 5.7km의 성벽에 장안문·팔달문·화서문·창룡문 4대문과 공심돈·봉돈·치성·포루·암문 등 48개 방어 시설을 갖춘 동서양 축성술의 융합체.",
        "visual": {
            "style": ["성벽(fortress wall)", "치성(bastion)", "공심돈(hollow guard tower)", "봉돈(beacon mound)", "누각식 성문(gate pavilion)", "옹성(barbican)"],
            "colors": ["성벽 석재 회백색", "벽돌 적갈색", "기와 회흑색", "단청 오방색", "목재 갈색"],
            "materials": ["화강암 석재", "벽돌", "목재", "기와", "단청"],
            "atmosphere": "웅장한, 견고한, 실학 정신의 과학적 설계, 조선 후기 개혁 군주의 의지",
        },
    },
    {
        "name": "종묘",
        "name_en": "Jongmyo Royal Ancestral Shrine",
        "type": "세계유산",
        "category": "건축/제례",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 종로구",
        "description": "조선 역대 왕과 왕비의 신위를 모신 유교 사당. 정전은 19칸의 긴 수평 건물로 세계에서 가장 긴 단일 목조 건축물 중 하나. 맞배지붕의 절제된 형태에 장엄한 비례미를 갖추고 있으며, 영녕전과 함께 유교적 제례 공간의 정수를 보여줌.",
        "visual": {
            "style": ["맞배지붕(gable roof)", "익공식 공포", "장대한 수평 구성(elongated horizontal form)", "월대(raised stone platform)", "신로(spirit path)"],
            "colors": ["단청 최소화, 절제된 적·녹색", "기와 회흑색", "목재 짙은 갈색", "월대 화강암 회백색"],
            "materials": ["목재", "기와", "화강암 석재", "단청(절제된)"],
            "atmosphere": "엄숙한, 절제된, 유교적 경건함, 장대한 수평적 비례의 숭고미",
        },
    },
    {
        "name": "부석사 무량수전",
        "name_en": "Muryangsujeon Hall, Buseoksa Temple",
        "type": "국보",
        "category": "건축/사찰",
        "era": "고려",
        "era_en": "Goryeo Dynasty (918-1392)",
        "location": "경상북도 영주시",
        "description": "676년 의상대사가 창건한 부석사의 본전으로 현존하는 한국 최고(最古)의 목조 건축물 중 하나(1376년 중수). 정면 5칸 측면 3칸의 주심포 양식 건물로, 배흘림 기둥과 단아한 팔작지붕이 고려시대 건축의 우아함을 보여줌.",
        "visual": {
            "style": ["팔작지붕", "주심포식 공포(column-top bracket)", "배흘림기둥(entasis column)", "활주(inclined support)", "기단(stone platform)"],
            "colors": ["단청 퇴색된 고풍스러운 적·녹색", "기와 회흑색", "목재 풍화된 짙은 갈색", "기단 자연석 회갈색"],
            "materials": ["목재", "기와", "자연석", "단청"],
            "atmosphere": "고즈넉한, 단아한, 고려 건축의 우아한 절제미, 소백산 자락의 탈속적 고요함",
        },
    },
    {
        "name": "안동 하회마을",
        "name_en": "Hahoe Folk Village, Andong",
        "type": "세계유산",
        "category": "건축/전통마을",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "경상북도 안동시",
        "description": "낙동강이 마을을 감싸 도는 물돌이 지형에 자리한 풍산 류씨 동성마을. 양진당·충효당 등 양반 가옥과 초가 서민 가옥이 유교적 신분 질서에 따라 배치. 배산임수의 풍수 원리를 따르며, 하회별신굿 탈놀이의 발상지.",
        "visual": {
            "style": ["기와집(tile-roofed house)", "초가집(thatched-roof house)", "사랑채·안채 구분(outer/inner quarters)", "토담(earthen wall)", "배산임수 배치(mountain-back water-front layout)"],
            "colors": ["기와 회흑색", "흙벽 황토색", "목재 자연 갈색", "초가 짚 황금색", "토담 황갈색"],
            "materials": ["목재", "기와", "짚", "황토", "자연석"],
            "atmosphere": "소박한, 평온한, 유교적 전통 질서, 낙동강과 어우러진 전원적 풍경",
        },
    },
    {
        "name": "경회루",
        "name_en": "Gyeonghoeru Pavilion, Gyeongbokgung Palace",
        "type": "국보",
        "category": "건축/궁궐",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "서울특별시 종로구",
        "description": "경복궁 내 연못 위에 세워진 2층 누각으로, 국가 연회와 외국 사신 접대에 사용된 조선 최대의 정자 건축. 정면 7칸 측면 5칸, 48개의 석주가 1층을 지탱하고 2층은 목조 누마루. 주역의 음양오행 원리에 따라 내·외진 기둥 배치.",
        "visual": {
            "style": ["팔작지붕", "겹처마", "다포식 공포", "석주(stone pillars)", "2층 누각(two-story pavilion)", "방형 연못(square pond)", "3개 석교(stone bridges)"],
            "colors": ["단청 오방색(청·적·황·백·흑)", "기와 회흑색", "석주 화강암 회백색", "연못 수면 반사광"],
            "materials": ["목재", "기와", "화강암 석재", "단청"],
            "atmosphere": "화려한, 웅장한, 수면 위의 장대한 누각, 조선 왕실의 위엄과 풍류",
        },
    },
    {
        "name": "다보탑",
        "name_en": "Dabotap Pagoda, Bulguksa Temple",
        "type": "국보",
        "category": "건축/석탑",
        "era": "통일신라",
        "era_en": "Unified Silla Dynasty (668-935)",
        "location": "경상북도 경주시",
        "description": "751년 불국사 대웅전 앞 동쪽에 건립된 석탑. 법화경의 다보여래를 상징하며, 서쪽 석가탑의 단순미와 대비되는 화려하고 복잡한 구조. 사각·팔각·원형의 평면이 층층이 변화하며, 석재로 목조 건축의 세부를 정교하게 재현한 독창적 조형.",
        "visual": {
            "style": ["사각 기단(square base)", "팔각 중층(octagonal middle)", "계단식 구성(stepped structure)", "석조 난간(stone railing)", "사자상(lion sculptures)", "목조 모방 석조(wood-imitating stonework)"],
            "colors": ["화강암 회백색", "풍화된 석재 연갈색", "이끼 녹색 부분 부착"],
            "materials": ["화강암"],
            "atmosphere": "정교한, 화려한, 통일신라 석조 예술의 극치, 종교적 장엄함과 기술적 경이",
        },
    },
    {
        "name": "첨성대",
        "name_en": "Cheomseongdae Observatory",
        "type": "국보",
        "category": "건축/과학",
        "era": "신라",
        "era_en": "Silla Dynasty (57 BCE-935 CE)",
        "location": "경상북도 경주시",
        "description": "632-647년경 선덕여왕 때 축조된 동아시아 최고(最古)의 천문 관측대. 높이 약 9.17m, 362개(음력 1년의 날수 상징)의 가공 석재를 27단(선덕여왕이 27대 왕)으로 원통형 쌓기. 중간부 남쪽에 정(井)자형 창구부, 상부에 정(井)자형 정상석 배치.",
        "visual": {
            "style": ["원통형 병 모양(bottle-shaped cylinder)", "정자형 창구부(square window opening)", "정자형 정상석(square top frame)", "곡선 외벽(curved outer wall)"],
            "colors": ["화강암 회백색~연갈색", "풍화 석재 황갈색", "이끼 녹색 부분 부착"],
            "materials": ["화강암 가공석"],
            "atmosphere": "신비로운, 고대 과학의 지혜, 경주 평야 위의 고요한 위엄, 천문과 건축의 조화",
        },
    },
    {
        "name": "하회탈과 하회별신굿탈놀이",
        "name_en": "Hahoe Mask Dance Drama",
        "type": "무형유산",
        "category": "탈춤/공연",
        "era": "고려~조선",
        "era_en": "Goryeo to Joseon Dynasty (12th–19th century)",
        "location": "경상북도 안동시 하회마을",
        "description": "12세기경 하회마을에서 시작된 별신굿탈놀이. 양반, 선비, 초랭이, 이매, 부네, 중, 백정, 할미 등 탈을 쓰고 마당에서 펼치는 마을굿 연희. 양반과 선비의 위선을 풍자하고 서민의 삶을 해학적으로 표현. 국보 제121호 하회탈은 나무를 깎아 만든 한국 대표 가면.",
        "visual": {
            "style": ["하회탈(나무 조각 가면, 턱이 분리되어 움직임)", "도포·갓 착용 양반탈", "승복 입은 중탈", "마당놀이(야외 원형 공연장)", "농악대 반주"],
            "colors": ["탈: 옅은 살구색 나무 바탕에 검은 눈썹·수염", "양반 의상: 흰색·남색 도포", "초랭이: 붉은색·황색 의상", "부네: 연분홍·연두 치마저고리"],
            "materials": ["오리나무(탈 조각)", "옻칠", "삼베·무명(의상)", "짚·한지(소도구)"],
            "atmosphere": "해학적인, 풍자적인, 마을 축제의 흥겨움, 탈의 신비로운 표정 변화",
        },
    },
    {
        "name": "판소리",
        "name_en": "Pansori Epic Chant",
        "type": "무형유산",
        "category": "공연예술",
        "era": "조선",
        "era_en": "Joseon Dynasty (18th–19th century)",
        "location": "전라도 중심, 전국",
        "description": "소리꾼 한 명이 고수의 북 반주에 맞춰 창(노래), 아니리(사설), 너름새(몸짓)로 긴 이야기를 엮어가는 한국 전통 음악극. 춘향가, 심청가, 흥보가, 수궁가, 적벽가의 다섯 마당이 전승. 2003년 유네스코 인류무형문화유산 등재. 진양조, 중모리, 자진모리 등 다양한 장단 활용.",
        "visual": {
            "style": ["소리꾼(부채 들고 서서 공연)", "고수(북 앞에 앉아 반주)", "합죽선(접는 부채) 활용 동작", "소리꾼 한 명의 독무대", "추임새(얼씨구, 좋지)"],
            "colors": ["소리꾼: 흰색 또는 옥색 한복, 남색·갈색 두루마기", "고수: 흰색 바지저고리", "부채: 대나무색·흰색 한지", "돗자리: 황토색"],
            "materials": ["합죽선(대나무·한지 부채)", "소리북(소가죽·나무통)", "돗자리", "병풍(배경)"],
            "atmosphere": "비장한, 애절한, 흥겨운, 한(恨)과 흥(興)의 교차, 소리꾼의 격정적 몰입",
        },
    },
    {
        "name": "강강술래",
        "name_en": "Ganggangsullae Circle Dance",
        "type": "무형유산",
        "category": "민속놀이",
        "era": "조선",
        "era_en": "Joseon Dynasty (16th century origin)",
        "location": "전라남도 해남·진도·완도 일대",
        "description": "추석 보름달 아래 여성들이 손을 잡고 원을 그리며 도는 민속 원무. 선소리꾼이 앞소리를 메기면 나머지가 '강강술래'를 후렴으로 받으며 춤을 춘다. 느린 진강강술래에서 빠른 자진강강술래로 점차 빨라짐. 덕석몰기, 청어엮기, 기와밟기, 남생아놀아라 등 놀이 포함. 2009년 유네스코 인류무형문화유산 등재.",
        "visual": {
            "style": ["여성들 손잡고 큰 원형 대형", "보름달 아래 야외 춤", "치마저고리 차림", "덕석몰기(소용돌이 대형)", "청어엮기(지그재그 대형)"],
            "colors": ["흰색·옥색 저고리", "남색·감색 치마", "보름달 은백색 달빛", "가을밤 어둠 속 흰 옷의 대비"],
            "materials": ["무명·삼베 한복", "맨발 또는 짚신", "달빛(자연 조명)"],
            "atmosphere": "보름달 아래 신비로운, 여성적 연대와 흥겨움, 느림에서 빠름으로의 고조, 한가위 축제 분위기",
        },
    },
    {
        "name": "나전칠기",
        "name_en": "Najeonchilgi - Mother-of-Pearl Lacquerware",
        "type": "무형유산",
        "category": "공예",
        "era": "고려~조선",
        "era_en": "Goryeo to Joseon Dynasty (10th–19th century)",
        "location": "통영, 원주, 전국",
        "description": "전복, 소라 등 조개껍데기의 진주층을 얇게 갈아 문양을 오려 붙이고 옻칠로 마감하는 전통 공예. 고려시대 나전칠기는 세계 최고 수준으로 국화, 모란, 학, 구름 등 정교한 문양이 특징. 끊음질(가는 실 모양 자개를 끊어 붙이는 기법)은 한국 고유 기법. 함, 경상, 문갑, 빗접 등 생활 가구에 활용.",
        "visual": {
            "style": ["자개 끊음질(가는 자개 실로 기하학 문양)", "자개 줄음질(자개를 오려 형태 표현)", "옻칠 표면에 박힌 무지개빛 자개", "국화당초문·포도덩굴문·학문양", "문갑·함·경대·빗접 형태"],
            "colors": ["칠흑색 옻칠 바탕", "자개의 무지개빛 광택(청록·분홍·보라·금빛)", "대모(거북등) 복채색", "붉은 주칠 안쪽면"],
            "materials": ["전복껍데기·소라껍데기(자개)", "옻칠(천연 도료)", "삼베·한지(초벌 바탕)", "목재(소나무·피나무 골격)", "아교"],
            "atmosphere": "칠흑 속에 빛나는 무지개빛, 정교한 장인정신, 고려·조선의 귀족적 우아함",
        },
    },
    {
        "name": "전통 매듭공예",
        "name_en": "Maedeup - Traditional Korean Decorative Knot Craft",
        "type": "무형유산",
        "category": "공예",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392–1897)",
        "location": "전국",
        "description": "한 올의 끈을 맺고 조여 장식적 매듭을 만드는 전통 공예. 도래매듭, 나비매듭, 국화매듭, 생쪽매듭, 잠자리매듭 등 38가지 이상의 기본 매듭법이 전승. 노리개, 주머니, 선추, 유소(깃발 장식) 등에 활용. 매듭 아래에 술(다회)을 달아 완성. 왕실 의례용부터 일상 장신구까지 폭넓게 사용.",
        "visual": {
            "style": ["도래매듭(둥근 대칭형)", "나비매듭(나비 형상)", "국화매듭(꽃 형상)", "노리개(매듭+술+장식 결합)", "유소(의례용 긴 매듭 장식)"],
            "colors": ["오방색(빨강·파랑·노랑·흰색·검정)", "자주·분홍·연두 배색", "금색 술 장식", "색실 혼합 그라데이션"],
            "materials": ["명주실(꼰 끈)", "면사·인조사", "구슬·옥·밀화(호박) 장식", "금속 장식(은·놋쇠)"],
            "atmosphere": "섬세한 손끝 예술, 색실의 화려한 조화, 한국적 장식미의 정수",
        },
    },
    {
        "name": "전통 자수",
        "name_en": "Jasu - Traditional Korean Embroidery",
        "type": "무형유산",
        "category": "공예",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392–1897)",
        "location": "전국 (궁중 및 민간)",
        "description": "비단이나 모시 위에 색실로 문양을 수놓는 전통 공예. 궁수(궁중 자수)는 용, 봉황, 모란 등 화려한 도안이 특징이고, 민수(민간 자수)는 십장생, 화조, 문자(복·수·강녕) 등 소박한 도안이 특징. 평수, 이음수, 자릿수, 징금수 등 다양한 수법 사용. 병풍, 베갯모, 수저집, 활옷, 흉배 등에 활용.",
        "visual": {
            "style": ["자수 병풍(십장생도·화조도)", "흉배(관복 가슴 장식, 학·호랑이 문양)", "베갯모(양끝 자수 장식)", "활옷(혼례복 자수)", "수보(보자기 자수)"],
            "colors": ["오색실(빨강·파랑·노랑·초록·보라)", "금사·은사(궁중용)", "비단 바탕(남색·붉은색·흰색)", "자연색 그라데이션 표현"],
            "materials": ["명주실·면사(수실)", "금사·은사(궁수용)", "비단·모시·무명(바탕천)", "자수틀(둥근 나무틀)", "수침(자수 바늘)"],
            "atmosphere": "정교한 바늘 한 땀의 예술, 궁중의 화려함과 민간의 소박한 아름다움, 한국 여성의 솜씨와 정성",
        },
    },
    {
        "name": "가야금",
        "name_en": "Gayageum - Korean Twelve-String Zither",
        "type": "무형유산",
        "category": "악기",
        "era": "가야~삼국",
        "era_en": "Gaya to Three Kingdoms Period (6th century origin)",
        "location": "가야(경남 고령), 이후 신라·고려·조선 전국",
        "description": "6세기 가야국 가실왕이 만들었다고 전해지는 한국 대표 현악기. 오동나무 공명판 위에 12줄(또는 산조가야금은 비단줄)을 걸고 안족(기러기발 모양 받침)으로 음높이를 조절. 정악가야금은 넓고 긴 형태로 궁중음악에, 산조가야금은 작고 좁은 형태로 민속음악에 사용. 농현(줄을 흔드는 기법)으로 깊은 여운 표현.",
        "visual": {
            "style": ["긴 직사각 오동나무 울림통", "12개 명주줄(또는 비단줄)", "안족(기러기발 모양 나무 받침대, 줄마다 하나)", "양이두(머리 장식, 양의 귀 모양)", "연주자 좌식 자세, 무릎 위에 놓고 오른손 탄주·왼손 농현"],
            "colors": ["오동나무 연한 황갈색 몸체", "명주줄 미색·흰색", "안족 밤나무 갈색", "뒤판 밤나무 짙은 갈색"],
            "materials": ["오동나무(앞판 공명판)", "밤나무(뒤판·안족)", "명주실(줄, 꼬아서 사용)", "부들(줄 감는 장식)"],
            "atmosphere": "맑고 청아한 울림, 한국 전통 선율의 깊은 여운, 농현의 깊은 떨림과 서정성",
        },
    },
    {
        "name": "봉산탈춤",
        "name_en": "Bongsan Mask Dance",
        "type": "무형유산",
        "category": "탈춤/공연",
        "era": "조선",
        "era_en": "Joseon Dynasty (18th–19th century)",
        "location": "황해도 봉산군 (현 전승지: 서울·전국)",
        "description": "황해도 봉산 지역에서 단오날 밤에 횃불을 밝히고 펼치던 탈춤. 사상좌춤, 팔목중춤, 사당춤, 노장춤, 사자춤, 양반춤, 미얄춤 등 7과장으로 구성. 파계승의 타락, 양반의 허세, 처첩 갈등 등을 풍자. 역동적이고 활달한 춤사위가 특징이며 해서탈춤 계열의 대표격. 국가무형문화재 제17호.",
        "visual": {
            "style": ["봉산탈(바가지·종이로 만든 큰 탈)", "먹중 검은 장삼 차림 역동적 춤", "양반탈(비뚤어진 입·큰 코)", "사자탈(두 사람이 한 몸)", "횃불 아래 야외 마당 공연", "팔목중의 과장된 동작"],
            "colors": ["먹중: 검은 장삼·붉은 가사", "양반: 흰 도포·검은 갓", "사당: 화려한 치마저고리", "탈: 붉은색·검은색·흰색 도채", "횃불 주황빛 조명"],
            "materials": ["바가지(탈 몸체)", "한지·옻칠(탈 표면)", "먹물·안료(탈 채색)", "무명·삼베(의상)", "짚·나무(소도구)"],
            "atmosphere": "횃불 아래 역동적인, 과장된 해학과 통렬한 풍자, 민중의 신명과 해방감",
        },
    },
    {
        "name": "김치와 김장 문화",
        "name_en": "Kimchi and Kimjang Culture",
        "type": "음식문화",
        "category": "세계무형유산",
        "era": "조선/전시대",
        "era_en": "Joseon Dynasty & All Periods",
        "location": "전국",
        "description": "초겨울 온 가족과 이웃이 모여 월동 김치를 대량으로 담그는 김장 문화. 배추·무를 소금에 절이고, 고춧가루·젓갈·마늘·생강 등으로 만든 양념소를 버무려 항아리에 켜켜이 담가 땅속에 묻어 저장하였다. 2013년 유네스코 인류무형문화유산 등재.",
        "visual": {
            "style": ["대가족 마당 작업", "큰 함지박·양푼", "배추 절이기", "양념소 버무리기", "옹기 항아리"],
            "colors": ["배추 연두색", "고춧가루 선홍색", "젓갈 갈색", "옹기 적갈색", "짚 노란색"],
            "materials": ["옹기", "짚", "소금", "배추", "고춧가루"],
            "atmosphere": "협동적인, 정겨운, 초겨울 찬 공기 속 활기찬 노동",
        },
    },
    {
        "name": "한정식 궁중요리",
        "name_en": "Royal Court Cuisine - Hanjeongsik",
        "type": "음식문화",
        "category": "무형유산",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "한양(서울)",
        "description": "조선 궁중에서 왕에게 올리던 수라상. 12첩 반상을 기본으로 탕·찌개·전골·구이·전·회·편육·나물·젓갈·김치 등이 놋그릇과 백자에 담겨 격식 있게 차려졌다. 주원료의 오방색(五方色) 배치와 음양오행 사상이 반영된 의례적 식문화.",
        "visual": {
            "style": ["12첩 반상차림", "놋그릇·백자 식기", "소반(小盤)", "수라간 궁녀", "붉은 칠기 상"],
            "colors": ["놋쇠 금색", "백자 흰색", "오방색(적·청·황·백·흑)", "칠기 주홍색"],
            "materials": ["놋쇠", "백자", "옻칠 목기", "은수저"],
            "atmosphere": "엄숙한, 격조 높은, 정갈하고 화려한 궁중의 위엄",
        },
    },
    {
        "name": "전통 혼례",
        "name_en": "Traditional Korean Wedding Ceremony",
        "type": "생활문화",
        "category": "의례",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "조선시대 유교식 전통 혼례. 신부 집 마당에 초례청을 설치하고, 전안례(기러기 드리기)·교배례(맞절)·합근례(표주박 술잔 나누기)의 절차를 거쳤다. 신랑은 사모관대, 신부는 원삼·족두리·연지곤지를 갖추었다.",
        "visual": {
            "style": ["초례청(병풍·돗자리)", "기러기 나무 조각", "표주박 술잔", "사모관대 신랑", "원삼·족두리 신부"],
            "colors": ["신부 원삼 홍색·남색", "신랑 관복 청색", "초례상 붉은 보자기", "소나무·대나무 녹색"],
            "materials": ["비단", "나무 기러기", "표주박", "병풍", "돗자리"],
            "atmosphere": "경건한, 화사한, 가문의 경사로 들뜬 정중한 분위기",
        },
    },
    {
        "name": "전통 장독대",
        "name_en": "Traditional Jangdokdae - Sauce Jar Platform",
        "type": "생활문화",
        "category": "생활/음식",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "한옥 뒤뜰 양지바른 곳에 크고 작은 옹기 항아리를 늘어놓아 된장·간장·고추장·젓갈·김치 등을 발효·저장하던 공간. 장독 뚜껑은 소금을 얹어 잡귀를 막고, 볏짚 새끼줄에 고추·숯을 꿰어 금줄을 쳤다. 한국 발효 식문화의 핵심 공간.",
        "visual": {
            "style": ["양지바른 뒤뜰 돌단", "크고 작은 옹기 항아리", "소금 올린 뚜껑", "금줄(새끼줄·고추·숯)", "한옥 담장 배경"],
            "colors": ["옹기 적갈색·흑갈색", "돌담 회색", "소금 흰색", "고추 붉은색", "된장 갈색"],
            "materials": ["옹기", "화강석", "볏짚", "소금", "숯"],
            "atmosphere": "고즈넉한, 정갈한, 어머니의 손맛과 세월이 담긴 생활 공간",
        },
    },
    {
        "name": "서낭당과 장승",
        "name_en": "Village Guardian Totem Poles - Jangseung",
        "type": "민속문화",
        "category": "민속/신앙",
        "era": "조선",
        "era_en": "Joseon Dynasty (1392-1897)",
        "location": "전국",
        "description": "마을 입구에 세워 잡귀와 역병을 막고 마을의 안녕을 기원하던 나무·돌 장승. '천하대장군' '지하여장군'을 한 쌍으로 세우고, 돌무더기(서낭당)와 신목(神木)에 오색 천을 묶어 마을 수호신으로 삼았다. 정월 대보름에 장승제를 지냈다.",
        "visual": {
            "style": ["나무 장승 한 쌍(남·여)", "투박하게 깎은 얼굴", "벙거지·갓 형태 머리", "서낭당 돌무더기", "신목에 걸린 오색 천"],
            "colors": ["나무 원목 갈색", "먹 글씨 검정", "오색 천(빨·파·노·흰·녹)", "돌무더기 회색"],
            "materials": ["소나무 원목", "자연석", "먹", "삼베·무명 천"],
            "atmosphere": "토속적인, 주술적인, 마을 공동체의 외경과 안도감",
        },
    },
    {
        "name": "온돌",
        "name_en": "Ondol - Korean Underfloor Heating System",
        "type": "생활문화",
        "category": "건축/생활",
        "era": "고구려/전시대",
        "era_en": "Goguryeo Origins & All Periods",
        "location": "전국",
        "description": "아궁이에서 땔감을 때면 뜨거운 연기가 바닥 밑 구들장 사이의 고래(연도)를 지나 굴뚝으로 빠지며 방바닥을 데우는 한국 고유의 난방 방식. 고구려 시대 쪽구들에서 발전하여 조선시대 전면 온돌로 완성되었다. 2023년 유네스코 인류무형문화유산 등재.",
        "visual": {
            "style": ["아궁이 불길", "납작한 구들장 단면도", "고래(연도) 구조", "황토 마감 바닥", "굴뚝"],
            "colors": ["아궁이 불 주황색", "구들장 청회색", "황토 바닥 누런색", "굴뚝 연기 회색"],
            "materials": ["화강석 구들장", "황토", "진흙", "짚", "땔나무"],
            "atmosphere": "따뜻한, 은은한, 겨울밤 아랫목의 포근함과 안온함",
        },
    },
    {
        "name": "한지 제조",
        "name_en": "Hanji - Traditional Korean Paper Making",
        "type": "전통공예",
        "category": "공예",
        "era": "고려/조선",
        "era_en": "Goryeo to Joseon Dynasty",
        "location": "전주, 원주, 가평 등",
        "description": "닥나무 껍질을 채취하여 삶고 두드려 닥풀(황촉규 뿌리 점액)과 섞은 뒤, 대나무 발(簾)로 앞뒤·좌우로 흔들어 떠내는 외발뜨기(유렴법) 기법의 전통 제지술. 천년 이상 보존되는 내구성으로 '지천년 견오백(紙千年 絹五百)'이라 불렸다.",
        "visual": {
            "style": ["닥나무 껍질 삶기", "돌 위에서 닥 두드리기", "외발뜨기(대나무 발)", "널빤지 건조", "한지 완성품"],
            "colors": ["닥풀 미색·유백색", "물 투명", "대나무 발 연갈색", "삶은 닥 크림색"],
            "materials": ["닥나무 껍질", "황촉규 뿌리", "대나무 발", "가마솥", "잿물"],
            "atmosphere": "고요한, 장인의 집중, 물소리와 규칙적인 손동작의 반복",
        },
    },
    {
        "name": "씨름",
        "name_en": "Ssireum - Korean Traditional Wrestling",
        "type": "민속문화",
        "category": "세계무형유산",
        "era": "삼국시대/전시대",
        "era_en": "Three Kingdoms Period & All Periods",
        "location": "전국",
        "description": "두 선수가 샅바(허리·다리에 감는 천 띠)를 잡고 모래판 위에서 상대를 넘기는 한국 전통 경기. 고구려 고분벽화(각저총)에 씨름 장면이 묘사되어 있으며, 단오·추석 축제의 핵심 행사로 우승자에게 황소를 부상으로 수여하였다. 2018년 유네스코 인류무형문화유산 등재.",
        "visual": {
            "style": ["원형 모래판", "샅바 잡은 두 선수", "상투·맨몸 차림", "구경꾼 원형 배치", "우승 황소"],
            "colors": ["모래판 황토색", "샅바 남색·붉은색", "선수 피부색", "구경꾼 흰 옷(백의)"],
            "materials": ["모래", "삼베 샅바", "짚자리", "흙"],
            "atmosphere": "역동적인, 힘찬, 환호와 북소리 속 축제의 열기",
        },
    },
]

# 시대별 보조 정보
ERA_CONTEXT = {
    "고구려": "강렬하고 역동적인 기상. 벽화 중심. 기마 문화, 전투 장면, 사신도가 대표적.",
    "백제": "부드럽고 섬세한 곡선미. '백제의 미소'로 대표되는 온화한 예술 세계.",
    "신라": "화려한 금속공예. 금관, 귀걸이, 곡옥 등 호화로운 장신구 문화.",
    "통일신라": "불교미술의 전성기. 석굴암, 불국사. 세련되고 이상적인 불교 조각.",
    "고려": "청자와 불화의 시대. 귀족적 세련미. 비색 청자, 상감기법, 나전칠기가 대표적.",
    "고려~조선": "고려의 세련미에서 조선의 절제미로 전환. 나전칠기, 탈춤 등이 양 시대에 걸쳐 발전.",
    "조선": "유교 문화. 검소함 속의 격조. 백자, 한옥, 한복, 궁궐 건축, 풍속화가 대표적.",
    "삼국시대": "고구려·백제·신라 각각의 개성 있는 문화. 고분, 금속공예, 토기가 대표적.",
    "삼국시대/전시대": "고대부터 이어온 한민족의 생활문화. 씨름, 놀이 등 토착 전통.",
    "가야~삼국": "가야의 독자적 문화. 철기, 토기, 가야금 등 독창적 예술 세계.",
    "고구려/전시대": "고구려에서 비롯된 온돌 등 한국 고유의 생활 기술. 실용적 지혜의 전통.",
    "고려/조선": "고려에서 조선으로 이어진 장인 문화. 한지, 나전칠기 등 정교한 공예 전통.",
    "조선/전시대": "조선시대에 체계화된 한국 전통 발효 식문화. 김치, 장류 등.",
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


def make_nano_banana(item):
    """나노바나나(Gemini) 전용 프롬프트 - 한국어 자연어 서술형, 최대한 구체적"""
    v = item["visual"]
    era_ctx = ERA_CONTEXT.get(item["era"], "")

    prompt = (
        f'다음 한국 문화유산을 극도로 사실적이고 세밀하게 묘사한 이미지를 생성해 주세요.\n\n'
        f'【피사체】 {item["era"]} 시대({item["era_en"]})의 {item["name"]} ({item["name_en"]})\n'
        f'【위치】 {item["location"]}\n'
        f'【상세 설명】 {item["description"]}\n\n'
        f'【구조와 양식】 다음 요소들을 정확하게 포함해 주세요: {", ".join(v["style"])}. '
        f'각 요소의 비례와 배치가 역사적 고증에 맞아야 합니다.\n\n'
        f'【색상 팔레트】 {", ".join(v["colors"])}. '
        f'색상 간의 대비와 조화를 자연스럽게 표현하고, 시대 특유의 색감을 반영해 주세요.\n\n'
        f'【재질 묘사】 {", ".join(v["materials"])}의 질감을 극도로 사실적으로 표현해 주세요. '
        f'표면의 미세한 결, 광택, 풍화 흔적, 세월의 흔적까지 보여야 합니다.\n\n'
        f'【분위기와 감성】 {v["atmosphere"]}. '
    )
    if era_ctx:
        prompt += f'{item["era"]}시대의 문화적 맥락: {era_ctx}\n\n'
    prompt += (
        f'【촬영 스타일】 전문 건축/문화재 사진작가가 골든아워(일출 직후 또는 일몰 직전)에 '
        f'풀프레임 카메라와 고급 렌즈로 촬영한 듯한 느낌. 자연광이 피사체를 부드럽게 감싸며, '
        f'적절한 명암 대비로 입체감을 살려 주세요. 배경은 {item["location"]}의 실제 환경을 반영하되, '
        f'피사체에 시선이 집중되도록 약간의 보케(배경 흐림) 효과를 적용해 주세요.\n\n'
        f'【금지 사항】 현대적 요소(전선, 자동차, 현대 건물)가 보이면 안 됩니다. '
        f'AI 특유의 부자연스러운 질감이나 왜곡 없이 깨끗하게 표현해 주세요.'
    )
    return prompt


def make_nano_banana_en(item):
    """나노바나나(Gemini) 전용 영문 프롬프트 - 자연어 서술형, 최대한 구체적"""
    v = item["visual"]
    era_ctx = ERA_CONTEXT.get(item["era"], "")

    prompt = (
        f'Create an extremely detailed and photorealistic image of the following Korean cultural heritage.\n\n'
        f'【Subject】 {item["name_en"]} from the {item["era_en"]}\n'
        f'【Location】 {item["location"]}\n'
        f'【Description】 {item["description"]}\n\n'
        f'【Structure & Style】 Accurately depict these architectural/artistic elements: '
        f'{", ".join(v["style"])}. Proportions and placement must be historically accurate.\n\n'
        f'【Color Palette】 {", ".join(v["colors"])}. '
        f'Render natural contrast and harmony between colors, reflecting the period-specific aesthetic.\n\n'
        f'【Material Textures】 Show ultra-realistic textures of {", ".join(v["materials"])}. '
        f'Include fine grain, patina, subtle weathering, and signs of age on surfaces.\n\n'
        f'【Mood & Atmosphere】 {v["atmosphere"]}. '
    )
    if era_ctx:
        prompt += f'Cultural context of the {item["era"]} era: {era_ctx}\n\n'
    prompt += (
        f'【Photography Style】 Shot as if by a professional heritage photographer during golden hour '
        f'(just after sunrise or before sunset) with a full-frame camera and premium lens. '
        f'Soft natural light wraps around the subject with balanced contrast for three-dimensionality. '
        f'Background reflects the actual environment of {item["location"]} with subtle bokeh '
        f'to draw focus to the main subject.\n\n'
        f'【Restrictions】 No modern elements (power lines, cars, modern buildings). '
        f'Clean rendering without AI artifacts or unnatural textures.'
    )


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
    "4": ("나노바나나(한글)", make_nano_banana),
    "5": ("나노바나나(영문)", make_nano_banana_en),
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
    print("  [4] 나노바나나 - 한글 (Gemini, 구체적 서술형)")
    print("  [5] 나노바나나 - 영문 (Gemini, 구체적 서술형)")
    print("  [6] 범용 (아무 모델에나 사용 가능)")
    print("  [7] 전부 다 만들기")
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
    if model_choice == "7":
        models_to_gen = ["1", "2", "3", "4", "5"]
    elif model_choice == "6":
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
        if model_choice == "7":
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
    print("  │     (Midjourney/DALL-E/SD/나노바나나)          │")
    print("  │  4. 생성된 프롬프트를 복사해서 사용!           │")
    print("  │                                                │")
    print("  └────────────────────────────────────────────────┘")
    print()
    print("  ┌─ 프롬프트 사용법 ────────────────────────────┐")
    print("  │                                                │")
    print("  │  Midjourney: Discord에서 /imagine 뒤에 붙여넣기│")
    print("  │  DALL-E:     ChatGPT에 프롬프트 그대로 입력    │")
    print("  │  SD:         WebUI의 Prompt란에 붙여넣기       │")
    print("  │  나노바나나: Gemini 앱에서 이미지 생성 선택 후 │")
    print("  │              프롬프트를 그대로 붙여넣기         │")
    print("  │                                                │")
    print("  │  한글 프롬프트는 한글 지원 모델에서 사용하세요 │")
    print("  │  (예: DALL-E, 나노바나나, 일부 SD 모델)        │")
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
