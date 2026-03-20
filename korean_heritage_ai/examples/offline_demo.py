#!/usr/bin/env python3
"""
오프라인 데모: API 호출 없이 샘플 데이터로 프롬프트 생성 과정을 시연합니다.

실행:
    python -m korean_heritage_ai.examples.offline_demo
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from korean_heritage_ai.api.heritage_client import HeritageItem
from korean_heritage_ai.data.structurer import to_ai_dataset_entry, convert_to_dataset
from korean_heritage_ai.prompts.generator import (
    generate_image_prompt,
    generate_prompt_variations,
)

# 샘플 문화유산 데이터 (API 호출 없이 사용)
SAMPLE_HERITAGE_ITEMS = [
    HeritageItem(
        kind_code="11", city_code="11", asset_no="00010000",
        name_kr="숭례문", name_hanja="崇禮門", name_en="Sungnyemun Gate",
        kind_name="국보", city_name="서울특별시",
        era="조선",
        description="숭례문은 조선시대 한양도성의 남쪽 정문으로, 1398년(태조 7)에 처음 세워졌다. "
                    "현존하는 서울의 가장 오래된 목조 건축물로, 2층 누각 형태의 문루와 석축 기단으로 구성되어 있다. "
                    "팔작지붕에 다포식 공포를 갖추고 있으며, 장엄한 단청으로 장식되어 있다.",
        image_url="https://www.heritage.go.kr/unisearch/images/national_treasure/1611086.jpg",
        detail_address="서울특별시 중구 세종대로 40",
    ),
    HeritageItem(
        kind_code="11", city_code="37", asset_no="00240000",
        name_kr="석굴암 석굴", name_hanja="石窟庵石窟", name_en="Seokguram Grotto",
        kind_name="국보", city_name="경상북도",
        era="통일신라",
        description="석굴암은 경주 토함산 중턱에 위치한 통일신라시대의 대표적 석굴사원이다. "
                    "화강암을 다듬어 인공적으로 조성한 석굴 안에 본존불을 중심으로 보살상, 천왕상, 나한상 등 "
                    "40구의 불상이 조화롭게 배치되어 있다. 불교미술의 최고 걸작으로 평가받는다.",
        image_url="https://www.heritage.go.kr/unisearch/images/national_treasure/1611100.jpg",
        detail_address="경상북도 경주시 불국로 873-243",
    ),
    HeritageItem(
        kind_code="12", city_code="11", asset_no="18680000",
        name_kr="청자 상감운학문 매병", name_hanja="靑磁象嵌雲鶴文梅甁",
        name_en="Celadon Maebyeong with Inlaid Cloud and Crane Design",
        kind_name="보물", city_name="서울특별시",
        era="고려",
        description="고려시대 상감청자의 대표작으로, 매병(梅甁) 형태의 청자에 "
                    "구름과 학 문양을 상감 기법으로 시문하였다. "
                    "고려 특유의 비색(翡色) 유약과 정교한 상감 기법이 돋보이는 작품이다.",
        image_url="https://www.heritage.go.kr/unisearch/images/treasure/1621100.jpg",
    ),
    HeritageItem(
        kind_code="11", city_code="11", asset_no="00830000",
        name_kr="반가사유상", name_hanja="半跏思惟像",
        name_en="Gilt-bronze Pensive Bodhisattva",
        kind_name="국보", city_name="서울특별시",
        era="삼국시대",
        description="삼국시대에 제작된 금동반가사유상으로, 반가부좌 자세로 깊은 사유에 잠긴 보살의 모습을 표현하였다. "
                    "부드러운 미소와 유려한 옷주름, 자연스러운 자세가 조화를 이루며, "
                    "한국 불교 조각의 백미로 평가된다.",
        image_url="https://www.heritage.go.kr/unisearch/images/national_treasure/1611058.jpg",
    ),
    HeritageItem(
        kind_code="15", city_code="36", asset_no="00010000",
        name_kr="명승 제1호 명주 청학동 소금강", name_en="Sogeumgang Valley",
        kind_name="명승", city_name="강원특별자치도",
        era="",
        description="오대산 동쪽 기슭에 위치한 소금강은 기암괴석과 폭포, 계곡이 어우러진 절경으로, "
                    "금강산의 축소판이라 하여 소금강이라 불린다. "
                    "사계절 아름다운 자연경관을 자랑하는 한국의 대표적 명승지이다.",
    ),
]


def main():
    print("=" * 60)
    print("  한국 국가유산 → 생성형 AI 데이터 변환 데모")
    print("  (오프라인 모드 - 샘플 데이터 사용)")
    print("=" * 60)

    # ── 1. 데이터셋 구조 확인 ──
    print("\n\n━━━ 1. AI 데이터셋 구조화 ━━━")
    for item in SAMPLE_HERITAGE_ITEMS[:2]:
        entry = to_ai_dataset_entry(item)
        print(f"\n▶ {item.name_kr} ({item.kind_name})")
        print(json.dumps(entry, ensure_ascii=False, indent=2))

    # ── 2. 프롬프트 생성 ──
    print("\n\n━━━ 2. 이미지 생성 프롬프트 ━━━")
    for item in SAMPLE_HERITAGE_ITEMS:
        print(f"\n{'─' * 50}")
        print(f"▶ {item.name_kr} ({item.kind_name}, {item.era or '자연유산'})")

        # 영문 프롬프트 (Midjourney 스타일)
        prompt_en = generate_image_prompt(
            item, style="photorealistic", language="en",
            detail_level="comprehensive", target_model="midjourney",
        )
        print(f"\n  [Midjourney 프롬프트]")
        print(f"  {prompt_en}")

        # 한글 프롬프트
        prompt_ko = generate_image_prompt(
            item, style="painting", language="ko",
            detail_level="detailed",
        )
        print(f"\n  [한글 프롬프트 - 회화 스타일]")
        print(f"  {prompt_ko}")

    # ── 3. 스타일 변형 ──
    print(f"\n\n━━━ 3. 스타일 변형 (숭례문) ━━━")
    variations = generate_prompt_variations(SAMPLE_HERITAGE_ITEMS[0])
    for v in variations:
        print(f"\n  [{v['style']}]")
        print(f"  EN: {v['prompt_en']}")
        print(f"  KO: {v['prompt_ko']}")

    # ── 4. 데이터셋 파일 저장 ──
    print(f"\n\n━━━ 4. 데이터셋 파일 저장 ━━━")
    os.makedirs("output", exist_ok=True)
    for fmt in ["json", "jsonl", "csv"]:
        path = convert_to_dataset(
            SAMPLE_HERITAGE_ITEMS,
            f"output/sample_dataset.{fmt}",
            fmt,
        )
        print(f"  저장됨: {path}")

    print("\n\n완료! output/ 디렉토리에서 생성된 파일을 확인하세요.")
    print("이 데이터를 생성형 AI 이미지 모델의 프롬프트/학습 데이터로 활용할 수 있습니다.")


if __name__ == "__main__":
    main()
