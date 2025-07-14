# 🚀 실제 데이터 적용 완전 가이드

## 📋 프로젝트 개요

이 **농촌 데이터센터 건설 입지 추천 AI 툴**은 경상남도를 대상으로 100m 격자 단위에서 최적의 데이터센터 건설 후보지를 추천하는 시스템입니다.

### 🎯 평가 항목
- **A항 (25%)**: 변전소 접근성 - 전력 공급 용이성
- **B항 (25%)**: 태양광 발전소 접근성 - 신재생에너지 연계
- **C항 (0%)**: 용수 공급원 접근성 - 현재 데이터 없음
- **D항 (25%)**: 농촌인구밀도 - 인력 수급 및 지역 발전 효과
- **E항 (25%)**: 교통 접근성 - 물류 및 접근성

## 📊 Google Drive 실제 데이터 분석

### 📂 Google Drive 링크
```
https://drive.google.com/drive/folders/1CTZWeh_QHPRpc5qUEwwLMwVG8ctAlLpk?usp=drive_link
```

### 📁 예상 데이터 파일들과 역할

#### 1. 공간 데이터 (Shapefile 형태)
```
🗺️ 100m_격자_경상남도.shp (+ .shx, .dbf, .prj)
   역할: 분석 대상 격자 구역 정의
   컬럼: grid_id, geometry
   
🏗️ 건축물정보_경상남도.shp (+ 관련 파일들)
   역할: 건설 불가능 지역 제외
   컬럼: building_type, geometry
   
🌾 농업진흥지역도_경상남도.shp (+ 관련 파일들)
   역할: 농업 보호구역 제외
   컬럼: zone_type, geometry
```

#### 2. 텍스트 데이터
```
📊 격자별_주택수.txt 또는 .csv
   역할: D항 농촌인구밀도 계산
   형식: grid_id    housing_count
   
📈 점수표.csv
   역할: 거리/조건별 점수 기준
   컬럼: category, criteria, distance_km, score
   
⚖️ 가중치표.csv
   역할: 평가 항목별 중요도
   컬럼: category, weight, description
```

#### 3. 주소 데이터
```
⚡ 변전소_주소목록.txt
   역할: A항 변전소 접근성 평가
   형식: 한 줄에 하나씩 주소
   
☀️ 태양광발전소_주소목록.txt
   역할: B항 태양광 접근성 평가
   형식: 한 줄에 하나씩 주소
```

## 🔧 실제 데이터 적용 단계별 가이드

### 1단계: 데이터 다운로드
```bash
# 1. Google Drive 링크 접속
# 2. 폴더 내 모든 파일 선택 (Ctrl+A)
# 3. 우클릭 → "다운로드"
# 4. ZIP 파일 자동 생성
```

### 2단계: 프로젝트 환경 준비
```bash
# 프로젝트 폴더로 이동
cd /workspace

# 다운로드 가이드 실행
python3 download_real_data.py

# data 폴더에 ZIP 파일 복사
# (다운로드된 파일을 data/ 폴더에 넣기)
```

### 3단계: 실제 데이터 설정
```bash
# 자동 설정 스크립트 실행
python3 setup_real_data.py

# 또는 수동으로
python3 data_uploader.py
```

### 4단계: 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 카카오 API 키 입력
# KAKAO_API_KEY=your_actual_api_key_here
```

### 5단계: 앱 실행
```bash
# 의존성 설치 (가상환경 권장)
pip install -r requirements.txt

# Flask 앱 실행
python3 app.py

# 브라우저에서 접속
# http://localhost:5000
```

## 📈 데이터 처리 흐름

### 🔄 처리 순서
1. **Shapefile 로딩**: 격자, 건축물, 농업진흥지역 데이터 로드
2. **건설 가능 격자 필터링**: 기존 건축물과 농업보호구역 제외
3. **주소→좌표 변환**: 카카오 API로 변전소/태양광 주소를 좌표로 변환
4. **거리 계산**: 각 격자에서 시설까지의 최단거리 계산
5. **점수 계산**: 거리 기반 점수 매기기
6. **가중치 적용**: 항목별 중요도 반영
7. **결과 시각화**: 지도와 상위 후보지 표시

### ⚙️ 핵심 알고리즘
```python
# A항: 변전소 접근성
scores_A = calculate_distance_scores(grid_centroids, substation_points)

# B항: 태양광 접근성  
scores_B = calculate_distance_scores(grid_centroids, solar_points)

# D항: 농촌인구밀도
scores_D = map_housing_counts_to_scores(housing_data)

# E항: 교통 접근성 (현재는 임시)
scores_E = generate_random_scores() # TODO: 도로 데이터 연동

# 총점 계산
total_score = (scores_A * 0.25) + (scores_B * 0.25) + 
              (scores_D * 0.25) + (scores_E * 0.25)
```

## 🎯 결과 해석 및 활용

### 📊 점수 체계
- **90-100점 (A등급)**: 최우수 후보지
- **80-89점 (B등급)**: 우수 후보지
- **70-79점 (C등급)**: 양호 후보지
- **60-69점 (D등급)**: 보통 후보지
- **50-59점 (E등급)**: 미흡 후보지
- **50점 미만 (F등급)**: 부적합 후보지

### 🗺️ 지도 시각화
- **히트맵**: 점수별 색상 구분 (빨강→노랑→초록→파랑)
- **팝업 정보**: 격자 클릭시 상세 점수 표시
- **범례**: 등급별 색상 가이드

### 📈 상위 후보지 리스트
- **순위**: 총점 기준 상위 20개
- **좌표**: 위경도 정보
- **항목별 점수**: A, B, D, E항 개별 점수
- **등급**: 최종 등급 분류

## 🔧 실제 데이터 활용 예시 코드

### 📁 데이터 로딩
```python
from data_processor import SpatialDataProcessor
from score_calculator import ScoreCalculator

# 카카오 API 키 설정
processor = SpatialDataProcessor("your_kakao_api_key")

# Shapefile 로딩
grid_gdf = processor.load_grid_data("data/100m_격자_경상남도.shp")
buildings_gdf = processor.load_building_data("data/건축물정보_경상남도.shp")
agricultural_gdf = processor.load_agricultural_zones("data/농업진흥지역도_경상남도.shp")

# 텍스트 데이터 로딩
housing_data = pd.read_csv("data/격자별_주택수.csv", sep='\t')
```

### 🏗️ 점수 계산
```python
# 점수 계산기 초기화
calculator = ScoreCalculator("data/점수표.csv", "data/가중치표.csv")

# 주소를 좌표로 변환
substation_addresses = open("data/변전소_주소목록.txt").readlines()
solar_addresses = open("data/태양광발전소_주소목록.txt").readlines()

substation_coords = processor.convert_addresses_to_coordinates(substation_addresses)
solar_coords = processor.convert_addresses_to_coordinates(solar_addresses)

# 점수 계산
scores = calculator.calculate_total_score(
    grid_gdf, substation_gdf, solar_gdf, housing_counts
)
```

### 🎨 결과 시각화
```python
# 점수 적용된 GeoDataFrame 생성
scored_gdf = calculator.create_scored_geodataframe(grid_gdf, scores)

# 지도 생성
import folium
map_center = [35.2, 128.2]  # 경상남도 중심
m = folium.Map(location=map_center, zoom_start=9)

# 히트맵 추가
for _, row in scored_gdf.iterrows():
    color = get_color_by_score(row['total_score'])
    folium.CircleMarker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        radius=5,
        color=color,
        popup=f"점수: {row['total_score']:.1f} (등급: {row['grade']})"
    ).add_to(m)

# 지도 저장
m.save("output/result_map.html")
```

## 🚀 확장 가능성

### 🌟 추가 평가 요소
- **C항 용수 공급**: 하천, 지하수 데이터 추가
- **지형 조건**: 경사도, 고도 데이터 연동
- **환경 규제**: 보호구역, 생태 지역 고려
- **경제성**: 토지 비용, 개발 비용 분석

### 🔬 기술적 개선
- **머신러닝**: 과거 성공 사례 학습으로 예측 정확도 향상
- **실시간 데이터**: 교통, 전력 현황 실시간 연동
- **3D 시각화**: Three.js 등을 활용한 입체적 표현
- **모바일 지원**: 반응형 웹 또는 네이티브 앱

### 📊 분석 고도화
- **민감도 분석**: 가중치 변화에 따른 결과 변화 분석
- **시나리오 분석**: 다양한 조건하에서의 최적 입지 분석
- **클러스터링**: 유사한 특성의 격자 그룹화
- **예측 모델링**: 미래 환경 변화 고려

## 📞 지원 및 문의

### 🔧 문제 해결
- **데이터 로딩 오류**: real_data_guide.md 참고
- **API 오류**: 카카오 API 키 및 호출 한도 확인
- **성능 이슈**: 대용량 데이터 처리 최적화

### 📚 추가 자료
- `README.md`: 전체 프로젝트 개요
- `DEMO_GUIDE.md`: 데모 실행 가이드
- `real_data_guide.md`: 상세 데이터 가이드

---

**🏆 실제 데이터를 적용하여 더욱 정확하고 실용적인 입지 추천을 경험해보세요!**