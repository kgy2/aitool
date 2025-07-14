# 🚀 실제 데이터 적용 가이드

## 📋 필요한 실제 데이터 파일들

Google Drive 링크 (https://drive.google.com/drive/folders/1CTZWeh_QHPRpc5qUEwwLMwVG8ctAlLpk?usp=drive_link) 에서 다음 파일들을 다운로드해야 합니다:

### 📍 공간 데이터 (Shapefile)
- **100m 격자 지도** (*.shp + 관련 파일들)
  - 역할: 경상남도를 100m 단위로 나눈 분석 단위
  - 필수 컬럼: grid_id (격자 고유 번호)

- **건축물 정보** (*.shp + 관련 파일들)
  - 역할: 기존 건축물이 있는 곳은 건설 불가능 지역으로 제외
  - 필수 컬럼: geometry (건물 위치)

- **농업진흥지역도** (*.shp + 관련 파일들)
  - 역할: 농업 보호구역은 건설 제한 지역으로 제외
  - 필수 컬럼: zone_type (지역 구분)

### 📊 텍스트 데이터
- **격자별 주택수** (*.txt 또는 *.csv)
  - 역할: D항 (농촌인구밀도) 평가에 사용
  - 형식: `grid_id\thousing_count` (탭 구분)

- **점수표** (*.csv)
  - 역할: 각 평가 항목별 거리/조건에 따른 점수 기준
  - 컬럼: category, criteria, distance_km, score

- **가중치표** (*.csv)
  - 역할: 평가 항목별 중요도 설정
  - 컬럼: category, weight, description

### 🏢 주소 데이터
- **변전소 주소 목록** (*.txt)
  - 역할: A항 (변전소 접근성) 평가에 사용
  - 형식: 한 줄에 하나씩 주소

- **태양광 발전소 주소 목록** (*.txt)
  - 역할: B항 (태양광 발전소 접근성) 평가에 사용
  - 형식: 한 줄에 하나씩 주소

## 🔧 실제 데이터 적용 방법

### 1단계: 데이터 다운로드 및 준비
```bash
# 1. Google Drive에서 모든 데이터 파일 다운로드
# 2. 모든 파일을 하나의 폴더에 모음
# 3. ZIP 파일로 압축 (예: real_data.zip)
```

### 2단계: 데이터 업로드
```bash
# ZIP 파일을 프로젝트의 data/ 폴더에 복사
cp real_data.zip /workspace/data/

# 또는 직접 파일들을 data/ 폴더에 복사
cp -r downloaded_files/* /workspace/data/
```

### 3단계: 환경 설정
```bash
# 환경 변수 파일 생성
cp .env.example .env

# .env 파일 편집하여 카카오 API 키 입력
# KAKAO_API_KEY=your_actual_api_key_here
```

### 4단계: 데이터 검증 및 처리
```python
# Python 스크립트 실행
python data_uploader.py

# 또는 직접 검증
from data_uploader import RealDataUploader

uploader = RealDataUploader()
# ZIP 파일이 있는 경우
uploader.extract_uploaded_files('data/real_data.zip')

# 데이터 검증
data_mapping = uploader.process_real_data()
config = uploader.create_real_data_config(data_mapping)
uploader.validate_data_completeness(config)
```

### 5단계: 앱 실행
```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# Flask 앱 실행
python app.py

# 브라우저에서 접속
# http://localhost:5000
```

## 📈 평가 항목별 데이터 역할

### A항: 변전소 접근성 (25%)
- **목적**: 데이터센터 전력 공급 용이성 평가
- **데이터**: 변전소 주소 → 좌표 변환 → 각 격자까지 거리 계산
- **점수**: 1km 이내(10점) ~ 10km 초과(2점)

### B항: 태양광 발전소 접근성 (25%)
- **목적**: 신재생에너지 연계 가능성 평가
- **데이터**: 태양광 발전소 주소 → 좌표 변환 → 각 격자까지 거리 계산
- **점수**: 2km 이내(10점) ~ 15km 초과(2점)

### C항: 용수 공급원 접근성 (0%)
- **목적**: 데이터센터 냉각용 용수 공급 평가
- **현재 상태**: 데이터 없음으로 가중치 0%
- **향후 확장**: 하천, 지하수 데이터 추가 시 활성화

### D항: 농촌인구밀도 (25%)
- **목적**: 인력 수급 및 지역 발전 효과 평가
- **데이터**: 격자별 주택수 → 인구밀도 추정
- **점수**: 50가구 이상(10점) ~ 10가구 미만(2점)

### E항: 교통 접근성 (25%)
- **목적**: 물류 및 접근성 평가
- **현재**: 임시 랜덤 점수 (도로 네트워크 데이터 없음)
- **향후 확장**: 도로망 데이터 추가 시 실제 거리 계산

## 🎯 결과 해석

### 점수 체계
- **총점**: 100점 만점 (각 항목 10점 × 가중치)
- **등급**: A(90-100) > B(80-89) > C(70-79) > D(60-69) > E(50-59) > F(50 미만)

### 지도 시각화
- **히트맵**: 점수가 높을수록 파란색, 낮을수록 빨간색
- **팝업**: 각 격자 클릭시 상세 점수 정보 표시
- **범례**: 등급별 색상 가이드 제공

### 상위 후보지
- **순위**: 총점 기준 상위 20개 격자
- **좌표**: 위경도 정보 제공
- **상세 점수**: 항목별 점수 및 등급 표시

## 🔧 문제 해결

### 데이터 로딩 오류
1. **Shapefile 오류**: .shp, .shx, .dbf, .prj 파일이 모두 있는지 확인
2. **인코딩 오류**: CSV/TXT 파일이 UTF-8로 저장되었는지 확인
3. **좌표계 오류**: Shapefile이 올바른 좌표계(EPSG:4326 권장)인지 확인

### API 오류
1. **카카오 API**: 유효한 API 키인지 확인
2. **요청 제한**: API 호출 횟수 제한 확인
3. **주소 형식**: 주소가 정확한 형식인지 확인

### 성능 최적화
1. **대용량 데이터**: 격자 수가 많은 경우 처리 시간 고려
2. **메모리 사용량**: 큰 Shapefile 처리 시 메모리 모니터링
3. **배치 처리**: 주소→좌표 변환을 배치로 처리하여 API 효율성 향상