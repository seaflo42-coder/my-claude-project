#!/usr/bin/env python3
"""
사용 예제: 국가유산 데이터 수집 → 구조화 → AI 프롬프트 생성

실행:
    python -m korean_heritage_ai.examples.collect_and_generate
"""

import json
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from korean_heritage_ai.api.heritage_client import HeritageAPIClient, HERITAGE_KIND_CODES
from korean_heritage_ai.data.structurer import convert_to_dataset, to_ai_dataset_entry
from korean_heritage_ai.prompts.generator import (
    generate_image_prompt,
    generate_prompt_variations,
    generate_batch_prompts,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = "output"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    client = HeritageAPIClient()

    # ────────────────────────────────────────
    # 1단계: 국보 데이터 수집 (서울 소재, 최대 5건)
    # ────────────────────────────────────────
    print("\n=== 1단계: 국보 데이터 수집 (서울) ===")
    items = client.collect_full_data(
        kind_code="11",   # 국보
        city_code="11",   # 서울
        max_items=5,
        include_images=True,
    )
    print(f"수집 완료: {len(items)}건")

    for item in items:
        print(f"  - {item.name_kr} ({item.era})")

    # ────────────────────────────────────────
    # 2단계: AI 데이터셋으로 변환
    # ────────────────────────────────────────
    print("\n=== 2단계: AI 데이터셋 변환 ===")

    # JSON 형식
    json_path = convert_to_dataset(items, f"{OUTPUT_DIR}/heritage_dataset.json", "json")
    print(f"  JSON 저장: {json_path}")

    # JSONL 형식 (파인튜닝용)
    jsonl_path = convert_to_dataset(items, f"{OUTPUT_DIR}/heritage_dataset.jsonl", "jsonl")
    print(f"  JSONL 저장: {jsonl_path}")

    # CSV 형식
    csv_path = convert_to_dataset(items, f"{OUTPUT_DIR}/heritage_dataset.csv", "csv")
    print(f"  CSV 저장: {csv_path}")

    # ────────────────────────────────────────
    # 3단계: 이미지 생성 프롬프트 생성
    # ────────────────────────────────────────
    print("\n=== 3단계: 이미지 생성 프롬프트 ===")

    if items:
        # 첫 번째 항목으로 다양한 프롬프트 생성
        sample = items[0]
        print(f"\n📌 대상: {sample.name_kr}")

        # 스타일별 변형
        variations = generate_prompt_variations(sample)
        for v in variations:
            print(f"\n  [{v['style']}]")
            print(f"  EN: {v['prompt_en'][:200]}...")
            print(f"  KO: {v['prompt_ko'][:200]}...")

        # Midjourney용 프롬프트
        mj_prompt = generate_image_prompt(
            sample, style="photorealistic", target_model="midjourney", detail_level="comprehensive"
        )
        print(f"\n  [Midjourney] {mj_prompt[:300]}...")

    # 일괄 프롬프트 생성
    print("\n=== 일괄 프롬프트 생성 ===")
    batch = generate_batch_prompts(items, target_model="general")
    with open(f"{OUTPUT_DIR}/prompts_batch.json", "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    print(f"  일괄 프롬프트 저장: {OUTPUT_DIR}/prompts_batch.json ({len(batch)}건)")

    # ────────────────────────────────────────
    # 4단계: 데이터셋 구조 미리보기
    # ────────────────────────────────────────
    if items:
        print("\n=== 데이터셋 구조 미리보기 ===")
        entry = to_ai_dataset_entry(items[0])
        print(json.dumps(entry, ensure_ascii=False, indent=2)[:1500])

    print("\n완료! output/ 디렉토리를 확인하세요.")


if __name__ == "__main__":
    main()
