"""
국가유산청 Open API 클라이언트.

문화재청(현 국가유산청)의 공공데이터 API를 통해
문화유산 목록, 상세정보, 이미지 데이터를 수집합니다.

API 문서: https://www.khs.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0201.jsp
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
import time
import logging

logger = logging.getLogger(__name__)

# 문화재 종목 코드
HERITAGE_KIND_CODES = {
    "11": "국보",
    "12": "보물",
    "13": "사적",
    "14": "사적및명승",
    "15": "명승",
    "16": "천연기념물",
    "17": "국가무형문화재",
    "18": "국가민속문화재",
    "21": "시도유형문화재",
    "22": "시도무형문화재",
    "23": "시도기념물",
    "24": "시도민속문화재",
    "25": "시도등록문화재",
    "31": "문화재자료",
    "79": "등록문화재(국가등록유산)",
    "80": "이북5도 무형문화재",
}

# 시도 코드
CITY_CODES = {
    "11": "서울특별시",
    "21": "부산광역시",
    "22": "대구광역시",
    "23": "인천광역시",
    "24": "광주광역시",
    "25": "대전광역시",
    "26": "울산광역시",
    "45": "세종특별자치시",
    "31": "경기도",
    "32": "강원특별자치도",
    "33": "충청북도",
    "34": "충청남도",
    "35": "전북특별자치도",
    "36": "전라남도",
    "37": "경상북도",
    "38": "경상남도",
    "50": "제주특별자치도",
    "ZZ": "전국(해외포함)",
}

# 시대 코드 매핑 (고증용)
ERA_MAPPING = {
    "선사시대": {"period": "선사시대", "years": "~BC 2333", "characteristics": "빗살무늬토기, 돌도끼, 고인돌"},
    "삼국시대": {"period": "삼국시대", "years": "BC 57~AD 668", "characteristics": "고구려 벽화, 백제 미소, 신라 금관"},
    "고구려": {"period": "고구려", "years": "BC 37~AD 668", "characteristics": "강렬한 벽화, 무용총, 석조 건축"},
    "백제": {"period": "백제", "years": "BC 18~AD 660", "characteristics": "부드러운 곡선미, 서산마애삼존불, 백제금동대향로"},
    "신라": {"period": "신라", "years": "BC 57~AD 935", "characteristics": "금관, 첨성대, 불국사, 석굴암"},
    "통일신라": {"period": "통일신라", "years": "668~935", "characteristics": "불교미술 전성기, 석굴암, 다보탑"},
    "고려": {"period": "고려", "years": "918~1392", "characteristics": "청자, 불화, 팔만대장경, 금속활자"},
    "조선": {"period": "조선", "years": "1392~1897", "characteristics": "유교문화, 한글, 백자, 궁궐건축, 한옥"},
    "대한제국": {"period": "대한제국", "years": "1897~1910", "characteristics": "근대화, 서양식 건축 혼합"},
    "일제강점기": {"period": "일제강점기", "years": "1910~1945", "characteristics": "근대건축, 문화유산 수난"},
}


@dataclass
class HeritageItem:
    """문화유산 항목 데이터."""
    kind_code: str = ""           # 종목코드 (ccbaKdcd)
    city_code: str = ""           # 시도코드 (ccbaCtcd)
    asset_no: str = ""            # 지정번호 (ccbaAsno)
    manage_no: str = ""           # 관리번호 (ccbaCpno)
    name_kr: str = ""             # 국문명 (ccbaMnm1)
    name_hanja: str = ""          # 한자명 (ccbaMnm2)
    name_en: str = ""             # 영문명 (ccbaEnm)
    kind_name: str = ""           # 종목명
    city_name: str = ""           # 시도명
    detail_address: str = ""      # 소재지 상세
    era: str = ""                 # 시대
    description: str = ""         # 설명문
    content: str = ""             # 내용
    image_url: str = ""           # 대표 이미지 URL
    image_urls: list = field(default_factory=list)  # 추가 이미지 URL 목록
    longitude: str = ""           # 경도
    latitude: str = ""            # 위도
    category: str = ""            # 분류 (유형)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}


# 기본 API 베이스 URL (국가유산청 개편에 따라 변경될 수 있음)
BASE_URL = "http://www.cha.go.kr/cha"
# 국가유산포털 API (신규)
HERITAGE_PORTAL_URL = "https://www.heritage.go.kr/heri"


class HeritageAPIClient:
    """국가유산청 Open API 클라이언트."""

    def __init__(self, base_url: str = BASE_URL, api_key: Optional[str] = None):
        """
        Args:
            base_url: API 베이스 URL. 기본값은 문화재청 기존 URL.
                      국가유산청 개편 후 URL이 변경될 수 있으므로 설정 가능.
            api_key: 공공데이터포털 API 인증키 (일부 API에 필요).
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._request_interval = 0.5  # API 호출 간격 (초)
        self._last_request_time = 0.0

    def _throttle(self):
        """API 호출 속도 제한."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._request_interval:
            time.sleep(self._request_interval - elapsed)
        self._last_request_time = time.time()

    def _fetch_xml(self, url: str) -> Optional[ET.Element]:
        """URL에서 XML 데이터를 가져와 파싱."""
        self._throttle()
        logger.info(f"API 요청: {url}")

        for attempt in range(3):
            try:
                req = Request(url, headers={"User-Agent": "KoreanHeritageAI/0.1"})
                with urlopen(req, timeout=30) as response:
                    data = response.read()
                    return ET.fromstring(data)
            except (URLError, ET.ParseError) as e:
                logger.warning(f"요청 실패 (시도 {attempt + 1}/3): {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
        return None

    def search_heritage_list(
        self,
        kind_code: str = "",
        city_code: str = "",
        page_unit: int = 10,
        page_index: int = 1,
    ) -> list[HeritageItem]:
        """
        문화유산 종목별 목록을 검색합니다.

        Args:
            kind_code: 종목 코드 (예: "11"=국보, "12"=보물)
            city_code: 시도 코드 (예: "11"=서울)
            page_unit: 페이지당 건수
            page_index: 페이지 번호

        Returns:
            HeritageItem 목록
        """
        params = {
            "pageUnit": page_unit,
            "pageIndex": page_index,
        }
        if kind_code:
            params["ccbaKdcd"] = kind_code
        if city_code:
            params["ccbaCtcd"] = city_code

        url = f"{self.base_url}/SearchKindOpenapiList.do?{urlencode(params)}"
        root = self._fetch_xml(url)

        if root is None:
            logger.error("문화유산 목록 조회 실패")
            return []

        items = []
        for item_elem in root.iter("item"):
            item = HeritageItem(
                kind_code=self._text(item_elem, "ccbaKdcd"),
                city_code=self._text(item_elem, "ccbaCtcd"),
                asset_no=self._text(item_elem, "ccbaAsno"),
                manage_no=self._text(item_elem, "ccbaCpno"),
                name_kr=self._text(item_elem, "ccbaMnm1"),
                name_hanja=self._text(item_elem, "ccbaMnm2"),
                name_en=self._text(item_elem, "ccbaEnm"),
                kind_name=self._text(item_elem, "ccbaKdNm", ""),
                city_name=self._text(item_elem, "ccbaCtcdNm", ""),
                longitude=self._text(item_elem, "longitude"),
                latitude=self._text(item_elem, "latitude"),
            )
            # 코드로부터 이름 매핑
            if not item.kind_name and item.kind_code in HERITAGE_KIND_CODES:
                item.kind_name = HERITAGE_KIND_CODES[item.kind_code]
            if not item.city_name and item.city_code in CITY_CODES:
                item.city_name = CITY_CODES[item.city_code]
            items.append(item)

        logger.info(f"목록 조회 완료: {len(items)}건")
        return items

    def get_heritage_detail(self, item: HeritageItem) -> HeritageItem:
        """
        개별 문화유산의 상세정보를 조회합니다.

        Args:
            item: 기본 정보가 담긴 HeritageItem

        Returns:
            상세정보가 추가된 HeritageItem
        """
        params = {
            "ccbaKdcd": item.kind_code,
            "ccbaAsno": item.asset_no,
            "ccbaCtcd": item.city_code,
        }
        url = f"{self.base_url}/SearchKindOpenapiDeatil.do?{urlencode(params)}"
        root = self._fetch_xml(url)

        if root is None:
            logger.warning(f"상세정보 조회 실패: {item.name_kr}")
            return item

        for detail_elem in root.iter("item"):
            item.content = self._text(detail_elem, "content")
            item.era = self._text(detail_elem, "ccceName")
            item.detail_address = self._text(detail_elem, "ccbaLcad")
            item.image_url = self._text(detail_elem, "imageUrl")
            # 설명문
            desc = self._text(detail_elem, "ccbaTextDscrt")  # 기술 설명
            if not desc:
                desc = self._text(detail_elem, "content")
            item.description = desc

        return item

    def get_heritage_images(self, item: HeritageItem) -> list[str]:
        """
        문화유산의 이미지 URL 목록을 조회합니다.

        Args:
            item: HeritageItem

        Returns:
            이미지 URL 리스트
        """
        params = {
            "ccbaKdcd": item.kind_code,
            "ccbaAsno": item.asset_no,
            "ccbaCtcd": item.city_code,
        }
        url = f"{self.base_url}/SearchImageOpenapi.do?{urlencode(params)}"
        root = self._fetch_xml(url)

        image_urls = []
        if root is not None:
            for img_elem in root.iter("imageUrl"):
                if img_elem.text and img_elem.text.strip():
                    image_urls.append(img_elem.text.strip())

        item.image_urls = image_urls
        return image_urls

    def collect_full_data(
        self,
        kind_code: str = "",
        city_code: str = "",
        max_items: int = 50,
        include_images: bool = True,
    ) -> list[HeritageItem]:
        """
        목록 조회 → 상세정보 → 이미지를 한번에 수집합니다.

        Args:
            kind_code: 종목 코드
            city_code: 시도 코드
            max_items: 최대 수집 건수
            include_images: 이미지 URL 수집 여부

        Returns:
            완전한 HeritageItem 리스트
        """
        items = []
        page = 1
        page_size = min(max_items, 100)

        while len(items) < max_items:
            batch = self.search_heritage_list(
                kind_code=kind_code,
                city_code=city_code,
                page_unit=page_size,
                page_index=page,
            )
            if not batch:
                break

            for item in batch:
                if len(items) >= max_items:
                    break
                item = self.get_heritage_detail(item)
                if include_images:
                    self.get_heritage_images(item)
                items.append(item)
                logger.info(f"[{len(items)}/{max_items}] {item.name_kr} 수집 완료")

            page += 1

        return items

    @staticmethod
    def _text(elem: ET.Element, tag: str, default: str = "") -> str:
        """XML 엘리먼트에서 텍스트 추출."""
        child = elem.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return default
