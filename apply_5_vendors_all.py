import os
import re

# 폴더/파일명 한글 매핑 딕셔너리
NAME_MAP = {
    "seoul": "서울", "gangnam": "강남구", "seocho": "서초구", "songpa": "송파구", "gangdong": "강동구",
    "mapo": "마포구", "yongsan": "용산구", "seodaemun": "서대문구", "eunpyeong": "은평구",
    "jongno": "종로구", "junggu": "중구", "jungnang": "중랑구", "seongbuk": "성북구",
    "gangbuk": "강북구", "dobong": "도봉구", "nowon": "노원구", "seongdong": "성동구",
    "gwangjin": "광진구", "dongdaemun": "동대문구", "yeongdeungpo": "영등포구",
    "guro": "구로구", "geumcheon": "금천구", "yangcheon": "양천구", "gangse": "강서구",
    "gangseo": "강서구", "dongjak": "동작구", "gwanak": "관악구",
    "incheon_bupyeong": "인천 부평구", "incheon_namdong": "인천 남동구", "incheon_yeonsu": "인천 연수구",
    "incheon_michuhol": "인천 미추홀구", "incheon_seogu": "인천 서구", "incheon_gyeyang": "인천 계양구",
    "incheon_junggu": "인천 중구", "incheon_donggu": "인천 동구",
    "suwon": "수원시", "suwon_paldal": "수원 팔달구", "suwon_yeongtong": "수원 영통구", "suwon_jangan": "수원 장안구", "suwon_gwonseon": "수원 권선구",
    "seongnam": "성남시", "seongnam_bundang": "성남 분당구", "seongnam_sujeong": "성남 수정구", "seongnam_jungwon": "성남 중원구",
    "goyang": "고양시", "goyang_ilsandong": "고양 일산동구", "goyang_ilsanseo": "고양 일산서구", "goyang_deogyang": "고양 덕양구",
    "yongin": "용인시", "yongin_suji": "용인 수지구", "yongin_giheung": "용인 기흥구", "yongin_cheoin": "용인 처인구",
    "anyang": "안양시", "anyang_dongan": "안양 동안구", "anyang_manan": "안양 만안구",
    "ansan": "안산시", "ansan_danwon": "안산 단원구", "ansan_sangnok": "안산 상록구",
    "bucheon": "부천시", "hwaseong": "화성시", "pyeongtaek": "평택시", "siheung": "시흥시",
    "gimpo": "김포시", "paju": "파주시", "namyangju": "남양주시", "uijeongbu": "의정부시",
    "hanam": "하남시", "gwangmyeong": "광명시", "gunpo": "군포시", "guri": "구리시",
    "osan": "오산시", "gwangju_gyeonggi": "경기 광주시", "icheon": "이천시", "yangju": "양주시",
    "uiwang": "의왕시", "anseong": "안성시"
}

def get_loc_name(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    if len(parts) == 2 and parts[1] == "index.html":
        folder = parts[0]
        return NAME_MAP.get(folder, folder.capitalize())
    else:
        folder = parts[0]
        file_name = parts[-1].replace(".html", "")
        folder_kr = NAME_MAP.get(folder, folder.capitalize())
        file_kr = NAME_MAP.get(file_name, file_name.capitalize())
        return f"{folder_kr} {file_kr}" if folder_kr != file_kr else folder_kr

FIVE_VENDORS_HTML = """
        <!-- 1번 업체: 스파루나 프리미엄 -->
        <div class="vendor-card">
            <img src="/images/vendor1.jpg" alt="{loc} 테라피" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge">추천 01</span>
                        <span class="vendor-title">스파루나 프리미엄 홈케어</span>
                    </div>
                    <div class="vendor-tagline">★ {loc} 전 지역 30분 내 신속 방문 보장</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">시그니처 건식 타이, 감성 아로마 릴렉싱, 딥티슈 집중 케어</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">24시간 연중무휴, 100% 후불제 안심 결제, 1회용 위생용품 완비</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>

        <!-- 2번 업체: VIP 프라이빗 바디 테라피 -->
        <div class="vendor-card">
            <img src="/images/vendor2.jpg" alt="{loc} 스웨디시" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge gold">추천 02</span>
                        <span class="vendor-title">루나 VIP 프라이빗 바디 테라피</span>
                    </div>
                    <div class="vendor-tagline">★ 호텔식 최고급 에센셜 오일 & 림프 순환 케어</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">프리미엄 스웨디시, 림프 드레니쉬, 전신 바디 밸런싱 케어</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">철저한 1:1 맞춤 테라피, 단골 고객 만족도 1위 검증 매장</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>

        <!-- 3번 업체: 달빛 힐링 아로마 -->
        <div class="vendor-card">
            <img src="/images/vendor3.jpg" alt="{loc} 홈타이" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge blue">추천 03</span>
                        <span class="vendor-title">달빛 힐링 아로마 테라피</span>
                    </div>
                    <div class="vendor-tagline">★ 야간·새벽 직장인 맞춤 힐링 & 스트레스 완화</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">타이 + 아로마 스페셜 콤보 코스 (90분/120분)</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">투명한 정찰제 요금 운영, 친절한 베테랑 관리사 상시 대기</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>

        <!-- 4번 업체: 힐링터치 감성 에스테틱 -->
        <div class="vendor-card">
            <img src="/images/vendor4.jpg" alt="{loc} 감성 테라피" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge purple">추천 04</span>
                        <span class="vendor-title">힐링터치 감성 에스테틱</span>
                    </div>
                    <div class="vendor-tagline">★ 섬세한 압 조절과 전신 림프 부종 케어 전문</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">감성 로드 스웨디시, 전신 릴렉싱 스트레칭, 스페셜 풋 케어</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">고객 맞춤형 강약 압 조절, 2030 인기 감성 힐링 샵</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>

        <!-- 5번 업체: 24시 명품 전통 홈타이 -->
        <div class="vendor-card">
            <img src="/images/vendor5.jpg" alt="{loc} 출장 마사지" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge green">추천 05</span>
                        <span class="vendor-title">24시 명품 전통 홈타이</span>
                    </div>
                    <div class="vendor-tagline">★ 뭉친 근육을 시원하게 풀어주는 정통 건식 테라피</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">오리지널 정통 타이, 등/어깨 집중 케어, 전신 아로마 힐링</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">선입금 없는 100% 현장 결제, 신속한 실시간 배차 시스템</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>
"""

updated_files = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if not file.endswith(".html"):
            continue
        
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, ".").replace("\\", "/")
        
        # 메인 루트 index.html 은 제외
        if rel_path == "index.html":
            continue
        
        loc_name = get_loc_name(rel_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 업체 카드 영역을 탐색하여 통째로 5개짜리로 교체
        if '<div class="vendor-card">' in content:
            # 섹션 타이틀 변경
            content = re.sub(r'<h2 class="section-title">.*?</h2>', f'<h2 class="section-title">{loc_name} 추천 테라피 매장 TOP 5</h2>', content, count=1)
            
            # 첫 번째 vendor-card 부터 마지막 vendor-card 닫는 div 태그까지 치환
            vendors_replacement = FIVE_VENDORS_HTML.format(loc=loc_name)
            pattern = re.compile(r'<div class="vendor-card">.*?</div>\s*</div>(?=\s*(?:<h2|<div class="gu-grid"|</div>\s*<footer>|<footer>))', re.DOTALL)
            
            if pattern.search(content):
                content = pattern.sub(vendors_replacement.strip(), content)
            else:
                # 패턴이 안 맞을 경우 기존 vendor-card 전체를 치환
                content = re.sub(r'(<div class="vendor-card">.*</div>\s*</a>\s*</div>)', vendors_replacement.strip(), content, flags=re.DOTALL)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            updated_files += 1

print(f"🎉 총 {updated_files}개 모든 지역 페이지(서울/경기/인천 전체)에 추천 업체 5개(TOP 5)가 완벽하게 적용되었습니다.")
