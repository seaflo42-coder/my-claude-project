"""
생성형 AI 이미지 프롬프트 생성기.

수집된 문화유산 데이터를 기반으로 고증에 충실한 이미지 생성 프롬프트를 만듭니다.
DALL-E, Midjourney, Stable Diffusion 등 다양한 모델에 활용할 수 있습니다.
"""

from typing import Optional

from korean_heritage_ai.api.heritage_client import HeritageItem, ERA_MAPPING
from korean_heritage_ai.data.structurer import classify_visual_category, enrich_era_info


# 한국 전통 양식별 프롬프트 템플릿
STYLE_TEMPLATES = {
    "건축": {
        "base": "Korean traditional architecture ({name}), {era_desc}",
        "details": [
            "dancheong (단청) colorful paintwork on wooden beams",
            "giwa (기와) curved ceramic roof tiles",
            "gongpo (공포) bracket system under eaves",
            "gidan (기단) stone platform foundation",
            "traditional Korean palatial architecture style",
        ],
        "atmosphere": "majestic, serene, historically accurate Korean setting",
    },
    "불교유산": {
        "base": "Korean Buddhist heritage ({name}), {era_desc}",
        "details": [
            "lotus motif ornaments",
            "gwangbae (광배) mandorla halo",
            "daejwa (대좌) pedestal base",
            "Buddhist iconography in Korean Silla/Goryeo/Joseon style",
        ],
        "atmosphere": "spiritual, meditative, sacred Korean Buddhist aesthetic",
    },
    "공예": {
        "base": "Korean traditional craft artwork ({name}), {era_desc}",
        "details": [
            "intricate traditional Korean patterns",
            "sanggam (상감) inlay technique" if "청자" else "",
            "traditional Korean ceramic aesthetic",
        ],
        "atmosphere": "elegant, refined, museum-quality Korean craftsmanship",
    },
    "회화/서예": {
        "base": "Korean traditional painting ({name}), {era_desc}",
        "details": [
            "sumuk (수묵) ink wash technique",
            "traditional Korean paper (hanji) texture",
            "Korean literati painting style",
        ],
        "atmosphere": "contemplative, artistic, traditional Korean brush painting aesthetic",
    },
    "자연유산": {
        "base": "Korean natural heritage site ({name}), {era_desc}",
        "details": [
            "Korean landscape scenery",
            "four seasons beauty",
        ],
        "atmosphere": "breathtaking Korean natural beauty, documentary style",
    },
}

DEFAULT_TEMPLATE = {
    "base": "Korean cultural heritage ({name}), {era_desc}",
    "details": ["traditional Korean aesthetic", "historically accurate depiction"],
    "atmosphere": "authentic Korean cultural heritage, detailed and respectful",
}


def generate_image_prompt(
    item: HeritageItem,
    style: str = "photorealistic",
    language: str = "en",
    detail_level: str = "detailed",
    target_model: str = "general",
) -> str:
    """
    문화유산 데이터로부터 생성형 AI 이미지 프롬프트를 생성합니다.

    Args:
        item: 문화유산 데이터
        style: "photorealistic", "painting", "illustration", "3d_render"
        language: "en" (영문), "ko" (한글)
        detail_level: "simple", "detailed", "comprehensive"
        target_model: "general", "midjourney", "dalle", "stable_diffusion"

    Returns:
        생성형 AI용 프롬프트 문자열
    """
    visual_cat = classify_visual_category(item)
    era_info = enrich_era_info(item)
    primary_cat = visual_cat.get("primary", "문화유산")

    template = STYLE_TEMPLATES.get(primary_cat, DEFAULT_TEMPLATE)

    # 시대 설명 구성
    era_desc = ""
    if era_info.get("period"):
        era_desc = f"{era_info['period']} period ({era_info.get('years', '')})"
    elif item.era:
        era_desc = f"{item.era} period"

    # 기본 프롬프트
    base = template["base"].format(name=item.name_kr or item.name_en, era_desc=era_desc)

    # 상세 요소
    details = [d for d in template["details"] if d]
    if visual_cat.get("color_palette"):
        details.append(f"color palette: {', '.join(visual_cat['color_palette'])}")
    if visual_cat.get("material"):
        details.append(f"materials: {', '.join(visual_cat['material'])}")

    # 스타일 지시자
    style_map = {
        "photorealistic": "photorealistic, high detail, 8K resolution",
        "painting": "traditional Korean painting style, brush strokes visible",
        "illustration": "detailed illustration, Korean artistic style",
        "3d_render": "3D render, realistic materials and lighting",
    }
    style_desc = style_map.get(style, style)

    # 분위기
    atmosphere = template.get("atmosphere", "")

    # 프롬프트 조합
    if detail_level == "simple":
        prompt = f"{base}, {style_desc}"
    elif detail_level == "detailed":
        detail_str = ", ".join(details[:4])
        prompt = f"{base}, {detail_str}, {atmosphere}, {style_desc}"
    else:  # comprehensive
        detail_str = ", ".join(details)
        prompt = f"{base}, {detail_str}, {atmosphere}, {style_desc}"

        # 고증 관련 추가 지시
        if era_info.get("characteristics"):
            prompt += f", era-specific characteristics: {era_info['characteristics']}"
        if item.description:
            # 설명문에서 핵심 키워드 추출 (간단히 앞부분)
            desc_hint = item.description[:200].replace("\n", " ")
            prompt += f", reference: {desc_hint}"

    # 타겟 모델별 최적화
    if target_model == "midjourney":
        prompt = prompt + " --ar 16:9 --q 2 --style raw"
    elif target_model == "dalle":
        prompt = f"I NEED to create a historically accurate image of {prompt}. Please ensure period-appropriate details."
    elif target_model == "stable_diffusion":
        prompt = prompt + ", masterpiece, best quality, highly detailed"

    # 한글 프롬프트
    if language == "ko":
        prompt = _to_korean_prompt(item, visual_cat, era_info, style)

    return prompt.strip()


def _to_korean_prompt(
    item: HeritageItem,
    visual_cat: dict,
    era_info: dict,
    style: str,
) -> str:
    """한글 프롬프트 생성 (한글 지원 모델용)."""
    parts = []

    parts.append(f"한국 {visual_cat.get('primary', '문화유산')}: {item.name_kr}")

    if era_info.get("period"):
        parts.append(f"시대: {era_info['period']} ({era_info.get('years', '')})")

    if visual_cat.get("style_keywords"):
        parts.append(f"양식: {', '.join(visual_cat['style_keywords'])}")

    if visual_cat.get("color_palette"):
        parts.append(f"색감: {', '.join(visual_cat['color_palette'])}")

    if visual_cat.get("material"):
        parts.append(f"재질: {', '.join(visual_cat['material'])}")

    style_ko = {
        "photorealistic": "사실적 사진 스타일, 고해상도",
        "painting": "전통 한국화 스타일, 붓터치",
        "illustration": "세밀한 일러스트레이션",
        "3d_render": "3D 렌더링, 사실적 재질",
    }
    parts.append(f"스타일: {style_ko.get(style, style)}")
    parts.append("고증에 충실한 역사적 표현")

    return ". ".join(parts)


def generate_prompt_variations(
    item: HeritageItem,
    count: int = 4,
) -> list[dict]:
    """
    하나의 문화유산에 대해 다양한 스타일의 프롬프트 변형을 생성합니다.

    Returns:
        [{"style": ..., "prompt_en": ..., "prompt_ko": ...}, ...]
    """
    styles = ["photorealistic", "painting", "illustration", "3d_render"]
    variations = []

    for i, style in enumerate(styles[:count]):
        variations.append({
            "style": style,
            "prompt_en": generate_image_prompt(
                item, style=style, language="en", detail_level="detailed"
            ),
            "prompt_ko": generate_image_prompt(
                item, style=style, language="ko", detail_level="detailed"
            ),
        })

    return variations


def generate_batch_prompts(
    items: list[HeritageItem],
    style: str = "photorealistic",
    target_model: str = "general",
) -> list[dict]:
    """
    여러 문화유산에 대해 일괄 프롬프트를 생성합니다.

    Returns:
        [{"name": ..., "id": ..., "prompt": ..., "metadata": ...}, ...]
    """
    results = []
    for item in items:
        prompt = generate_image_prompt(
            item,
            style=style,
            language="en",
            detail_level="comprehensive",
            target_model=target_model,
        )
        results.append({
            "name": item.name_kr,
            "id": f"{item.kind_code}_{item.asset_no}",
            "heritage_type": item.kind_name,
            "era": item.era,
            "prompt": prompt,
            "metadata": {
                "source": "국가유산청 Open API",
                "image_ref": item.image_url,
            },
        })
    return results
