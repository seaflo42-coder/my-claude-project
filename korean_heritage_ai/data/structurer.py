"""
수집된 문화유산 데이터를 생성형 AI 활용에 적합한 구조로 변환합니다.

출력 형식:
- JSON (구조화 데이터셋)
- JSONL (학습/파인튜닝용 라인별 데이터)
- CSV (스프레드시트 호환)
"""

import csv
import json
import os
from typing import Optional

from korean_heritage_ai.api.heritage_client import (
    HeritageItem,
    ERA_MAPPING,
    HERITAGE_KIND_CODES,
)


def enrich_era_info(item: HeritageItem) -> dict:
    """시대 정보를 생성형 AI가 이해할 수 있는 형태로 확장."""
    era_info = {"raw": item.era}

    for era_key, era_data in ERA_MAPPING.items():
        if era_key in item.era:
            era_info.update(era_data)
            break

    return era_info


def classify_visual_category(item: HeritageItem) -> dict:
    """
    문화유산을 시각적 카테고리로 분류합니다.
    생성형 AI 이미지 제작 시 참조할 분류 체계.
    """
    name = item.name_kr
    desc = item.description or ""
    kind = item.kind_name

    categories = {
        "primary": "",       # 주 카테고리
        "sub": "",           # 세부 카테고리
        "visual_type": "",   # 시각적 유형
        "material": [],      # 재료/재질
        "color_palette": [], # 색상 팔레트 힌트
        "style_keywords": [],# 양식 키워드
    }

    # 자연유산 (종목 기반, 최우선)
    if kind in ["천연기념물", "명승"]:
        categories["primary"] = "자연유산"
        categories["visual_type"] = "자연경관"
        categories["style_keywords"] = ["한국적 자연미", "사계절"]

    # 도자기/공예 (구체적 키워드 우선 매칭)
    elif any(kw in name or kw in desc for kw in [
        "청자", "백자", "도자", "매병", "향로", "공예", "금관",
        "장신구", "은입사", "나전칠기", "자수", "금동대향로",
    ]):
        categories["primary"] = "공예"
        if "청자" in name or "청자" in desc:
            categories["sub"] = "청자"
            categories["color_palette"] = ["비색(비취색)", "회청색"]
            categories["style_keywords"] = ["상감기법", "운학문", "당초문"]
        elif "백자" in name or "백자" in desc:
            categories["sub"] = "백자"
            categories["color_palette"] = ["순백색", "청화색"]
            categories["style_keywords"] = ["순백미", "달항아리", "청화백자"]
        else:
            categories["style_keywords"] = ["전통공예", "정교한 세공"]
        categories["material"] = ["도자기", "유약"] if "자" in name else ["금속", "보석"]
        categories["visual_type"] = "전통공예"

    # 불교 조각/유산 (반가사유상, 불상, 석굴 등)
    elif any(kw in name or kw in desc for kw in [
        "반가", "사유상", "불상", "보살", "석굴", "석불", "마애",
        "범종", "사리", "광배", "여래", "관음", "비로자나",
    ]):
        categories["primary"] = "불교유산"
        categories["sub"] = "불상/조각"
        categories["visual_type"] = "불교조각"
        categories["material"] = ["금동", "석재", "목재"]
        categories["color_palette"] = ["금색", "녹청색", "주홍색"]
        categories["style_keywords"] = ["불교미술", "연꽃문양", "광배", "대좌"]

    # 불교 건축 (탑, 사찰)
    elif any(kw in name for kw in ["탑", "사찰", "석등"]) or \
         any(kw in desc for kw in ["석탑", "전탑", "사찰", "승탑"]):
        categories["primary"] = "불교유산"
        categories["sub"] = "석탑/사찰건축"
        categories["visual_type"] = "석조건축물"
        categories["material"] = ["화강암", "석재"]
        categories["style_keywords"] = ["불교미술", "연꽃문양", "옥개석", "기단부"]

    # 회화/서예 (구체적 키워드)
    elif any(kw in name or kw in desc for kw in [
        "그림", "산수화", "초상화", "불화", "민화", "서첩",
        "필적", "서예", "화첩", "풍속화", "겸재", "단원",
    ]):
        categories["primary"] = "회화/서예"
        categories["visual_type"] = "전통회화"
        categories["material"] = ["비단", "종이", "먹"]
        categories["color_palette"] = ["수묵(흑백)", "채색(오방색)"]
        categories["style_keywords"] = ["산수화", "인물화", "화조화", "민화"]

    # 건축물 (궁궐, 성문, 전각 등)
    elif any(kw in name for kw in ["궁", "궁궐", "문루", "성문", "객사"]) or \
         any(kw in name + desc for kw in [
             "숭례문", "흥인지문", "광화문", "경복궁", "창덕궁",
             "창경궁", "덕수궁", "종묘", "한옥", "기와", "단청",
             "팔작지붕", "겹처마", "공포",
         ]):
        categories["primary"] = "건축"
        categories["visual_type"] = "전통건축"
        categories["material"] = ["목재", "기와", "석재", "단청"]
        categories["color_palette"] = ["단청 오방색(청, 적, 황, 백, 흑)", "기와 회색", "목재 갈색"]
        categories["style_keywords"] = ["팔작지붕", "겹처마", "공포", "기단"]

    # 기본
    if not categories["primary"]:
        categories["primary"] = "문화유산"
        categories["visual_type"] = "기타"

    return categories


def to_ai_dataset_entry(item: HeritageItem) -> dict:
    """
    단일 HeritageItem을 생성형 AI 학습/활용용 데이터셋 엔트리로 변환.

    Returns:
        구조화된 딕셔너리
    """
    era_info = enrich_era_info(item)
    visual_category = classify_visual_category(item)

    return {
        "id": f"{item.kind_code}_{item.city_code}_{item.asset_no}",
        "name": {
            "korean": item.name_kr,
            "hanja": item.name_hanja,
            "english": item.name_en,
        },
        "classification": {
            "heritage_type": item.kind_name,
            "heritage_code": item.kind_code,
            "location": {
                "city": item.city_name,
                "detail": item.detail_address,
                "coordinates": {
                    "latitude": item.latitude,
                    "longitude": item.longitude,
                } if item.latitude and item.longitude else None,
            },
        },
        "historical_context": {
            "era": era_info,
            "description": item.description[:2000] if item.description else "",
        },
        "visual_reference": {
            "category": visual_category,
            "primary_image": item.image_url,
            "additional_images": item.image_urls,
        },
        "ai_generation_hints": {
            "style_keywords": visual_category.get("style_keywords", []),
            "color_palette": visual_category.get("color_palette", []),
            "materials": visual_category.get("material", []),
            "visual_type": visual_category.get("visual_type", ""),
        },
    }


def convert_to_dataset(
    items: list[HeritageItem],
    output_path: str,
    output_format: str = "json",
) -> str:
    """
    HeritageItem 리스트를 데이터셋 파일로 저장.

    Args:
        items: 문화유산 항목 리스트
        output_path: 출력 파일 경로
        output_format: "json", "jsonl", "csv" 중 택1

    Returns:
        저장된 파일 경로
    """
    entries = [to_ai_dataset_entry(item) for item in items]

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if output_format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                {"metadata": {"version": "0.1", "total_count": len(entries), "source": "국가유산청 Open API"},
                 "items": entries},
                f, ensure_ascii=False, indent=2,
            )

    elif output_format == "jsonl":
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    elif output_format == "csv":
        if not entries:
            return output_path
        flat_rows = []
        for entry in entries:
            flat_rows.append({
                "id": entry["id"],
                "name_kr": entry["name"]["korean"],
                "name_en": entry["name"]["english"],
                "heritage_type": entry["classification"]["heritage_type"],
                "city": entry["classification"]["location"]["city"],
                "era": entry["historical_context"]["era"].get("raw", ""),
                "era_period": entry["historical_context"]["era"].get("period", ""),
                "era_years": entry["historical_context"]["era"].get("years", ""),
                "visual_type": entry["ai_generation_hints"]["visual_type"],
                "style_keywords": "|".join(entry["ai_generation_hints"]["style_keywords"]),
                "color_palette": "|".join(entry["ai_generation_hints"]["color_palette"]),
                "materials": "|".join(entry["ai_generation_hints"]["materials"]),
                "primary_image": entry["visual_reference"]["primary_image"],
                "description": entry["historical_context"]["description"][:500],
            })
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=flat_rows[0].keys())
            writer.writeheader()
            writer.writerows(flat_rows)

    return output_path
