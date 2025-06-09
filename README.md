# 📝 온라인 쇼핑몰 크롤링

## 1. 프로젝트 폴더 구조

```plaintext
eCommerce_crawler/
├─ venv/                   # Python 가상환경
├─ requirements.txt        # Python 패키지 목록
├─ config/
│  └─ settings.py          # 환경설정 (headless, timeouts, 경로 등)
├─ core/
│  ├─ base_crawler.py      # Selenium/WebDriver 공통 관리
│  ├─ parser.py            # 공통 파싱 유틸
│  └─ utils.py             # 공통 함수/유틸리티
├─ channels/               # 각 채널(쇼핑몰)별 크롤러
│  ├─ naver_brand.py
│  ├─ naver_smartstore.py
│  ├─ naver_shopping.py
│  ├─ coupang.py
│  └─ elevenst.py
├─ services/
│  ├─ review_service.py    # 리뷰(댓글) 처리
│  ├─ price_service.py     # 가격 정보 처리
│  └─ rating_service.py    # 평점 처리
├─ api/
│  └─ controller.py        # Flask API 라우팅 (엔드포인트 집합)
├─ outputs/                # 크롤링 결과(로그, 임시 파일 등)
├─ main.py                 # 서버 진입점 (Flask 실행)
└─ README.md               # 프로젝트 소개/개요
```

- - -

## 2. 전체 아키텍처 흐름도

```plaintext
[외부 요청 (클라이언트/서버)]
         │
         ▼
   ┌──────────────────────────┐
   │      Flask API           │
   │  (api/controller.py)     │
   └──────────────────────────┘
         │
         ▼
   ┌──────────────────────────┐
   │    Service 계층          │
   │ (services/*_service.py)  │
   └──────────────────────────┘
         │
         ▼
   ┌──────────────────────────┐
   │  Channel 크롤러 계층     │
   │   (channels/*.py)        │
   └──────────────────────────┘
         │
         ▼
   ┌──────────────────────────┐
   │ Selenium/WebDriver 관리   │
   │   (core/base_crawler.py) │
   └──────────────────────────┘
         │
         ▼
   ┌──────────────────────────┐
   │    결과 파싱/정제        │
   │ (core/parser.py, utils)  │
   └──────────────────────────┘
         │
         ▼
[ JSON 결과 반환 or 외부 전송 ]
```

- - - 

## 3. 사용 모듈 환경

### Python 버전
- **Python 3.10+** (최신 안정 버전 권장, 최소 3.8 이상)

### 필수 라이브러리 (requirements.txt)
```plaintext
Flask
selenium
webdriver-manager
beautifulsoup4
pandas
python-dotenv
requests
```

- **Flask**: API 서버 및 라우팅
- **selenium**: 실제 웹드라이버(브라우저) 자동제어
- **webdriver-manager**: 크롬/파이어폭스 드라이버 자동설치 및 관리
- **beautifulsoup4**: HTML 파싱/추출 보조
- **pandas**: (선택) 표형 데이터 처리
- **python-dotenv**: 환경설정 관리(.env)
- **requests**: (선택) 외부 서버로 결과 전송 시

- - -

## 4. API 컨트롤러

| HTTP Method | Endpoint       | 설명                             | 주요 파라미터            |
| ----------- | -------------- | ------------------------------ | ------------------ |
| POST        | `/api/review`  | 지정 채널/상품URL에 대한 **리뷰(댓글) 크롤링** | `channel`, `url`   |
| POST        | `/api/price`   | 지정 채널/상품URL에 대한 **가격 정보 크롤링**  | `channel`, `url`   |
| POST        | `/api/rating`  | 지정 채널/상품URL에 대한 **평점 정보 크롤링**  | `channel`, `url`   |
| (확장)        | `/api/image` 등 | 기타 정보(상품 이미지, 상세 등) 크롤링        | `channel`, `url` 등 |

### 요청 바디 예시
```json
{
  "channel": "coupang",
  "url": "https://www.coupang.com/vp/products/8172100881"
}
```

### 응답 예시(리뷰)
```json
{
  "success": true,
  "channel": "coupang",
  "url": "...",
  "reviews": [
    {
      "user": "구매자",
      "date": "2025-06-05",
      "content": "배송 빠르고 만족합니다.",
      "rating": 5
    },
    ...
  ]
}
```
#### 실패시
```json
{
  "success": false,
  "error": "크롤링 실패: (에러 메시지)"
}
```

## 📦 요약

- Flask API 서버로 운영하며, 엔드포인트마다 JSON으로 크롤링 결과 제공
- channels/ 폴더로 **쇼핑몰별 크롤러** 분리(확장 쉬움)
- services/ 폴더에서 **정보(리뷰, 가격, 평점 등)별 서비스** 담당
- core/는 **공통 파싱, 웹드라이버 관리**
- outputs/에는 결과 또는 로그 저장
- 사용 패키지는 크로스플랫폼(윈도우/맥/리눅스) 모두 호환