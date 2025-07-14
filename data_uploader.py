import os
import shutil
import zipfile
from pathlib import Path
import pandas as pd
import geopandas as gpd

class RealDataUploader:
    """실제 데이터 업로드 및 처리를 위한 클래스"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def extract_uploaded_files(self, uploaded_zip_path: str):
        """업로드된 ZIP 파일에서 데이터 추출"""
        with zipfile.ZipFile(uploaded_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.data_dir)
        print(f"파일들이 {self.data_dir}에 추출되었습니다.")
        
    def process_real_data(self):
        """실제 데이터 파일들을 처리하고 검증"""
        results = {}
        
        # 1. Shapefile 검증
        shapefiles = list(self.data_dir.glob("*.shp"))
        print(f"발견된 Shapefile: {len(shapefiles)}개")
        
        for shp in shapefiles:
            try:
                gdf = gpd.read_file(shp)
                print(f"✓ {shp.name}: {len(gdf)}개 피처, CRS: {gdf.crs}")
                results[shp.stem] = {
                    'type': 'shapefile',
                    'path': str(shp),
                    'count': len(gdf),
                    'columns': list(gdf.columns)
                }
            except Exception as e:
                print(f"✗ {shp.name} 로딩 실패: {e}")
        
        # 2. CSV 파일 검증
        csv_files = list(self.data_dir.glob("*.csv"))
        print(f"\n발견된 CSV 파일: {len(csv_files)}개")
        
        for csv in csv_files:
            try:
                df = pd.read_csv(csv)
                print(f"✓ {csv.name}: {len(df)}행, 컬럼: {list(df.columns)}")
                results[csv.stem] = {
                    'type': 'csv',
                    'path': str(csv),
                    'shape': df.shape,
                    'columns': list(df.columns)
                }
            except Exception as e:
                print(f"✗ {csv.name} 로딩 실패: {e}")
        
        # 3. TXT 파일 검증
        txt_files = list(self.data_dir.glob("*.txt"))
        print(f"\n발견된 TXT 파일: {len(txt_files)}개")
        
        for txt in txt_files:
            try:
                with open(txt, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"✓ {txt.name}: {len(lines)}행")
                results[txt.stem] = {
                    'type': 'text',
                    'path': str(txt),
                    'lines': len(lines)
                }
            except Exception as e:
                print(f"✗ {txt.name} 로딩 실패: {e}")
        
        return results
    
    def create_real_data_config(self, data_mapping: dict):
        """실제 데이터 파일 매핑 설정 생성"""
        config = {
            "grid_shapefile": None,
            "building_shapefile": None, 
            "agricultural_shapefile": None,
            "housing_data": None,
            "score_table": None,
            "weight_table": None,
            "substation_addresses": None,
            "solar_addresses": None
        }
        
        # 파일명 패턴 매칭으로 자동 분류
        for filename, info in data_mapping.items():
            path = info['path']
            
            # 격자 데이터 식별
            if any(keyword in filename.lower() for keyword in ['격자', 'grid', '100m']):
                config["grid_shapefile"] = path
                
            # 건축물 데이터 식별  
            elif any(keyword in filename.lower() for keyword in ['건축물', 'building', '건물']):
                config["building_shapefile"] = path
                
            # 농업진흥지역 식별
            elif any(keyword in filename.lower() for keyword in ['농업', 'agricultural', '진흥']):
                config["agricultural_shapefile"] = path
                
            # 주택수 데이터 식별
            elif any(keyword in filename.lower() for keyword in ['주택', 'housing', '인구']):
                config["housing_data"] = path
                
            # 점수표 식별
            elif any(keyword in filename.lower() for keyword in ['점수', 'score']):
                config["score_table"] = path
                
            # 가중치표 식별
            elif any(keyword in filename.lower() for keyword in ['가중', 'weight']):
                config["weight_table"] = path
                
            # 변전소 주소 식별
            elif any(keyword in filename.lower() for keyword in ['변전소', 'substation']):
                config["substation_addresses"] = path
                
            # 태양광 주소 식별
            elif any(keyword in filename.lower() for keyword in ['태양광', 'solar']):
                config["solar_addresses"] = path
        
        return config
    
    def validate_data_completeness(self, config: dict):
        """필수 데이터 완성도 검사"""
        required_files = [
            "grid_shapefile", "building_shapefile", "agricultural_shapefile",
            "housing_data", "score_table", "weight_table"
        ]
        
        missing_files = []
        for req_file in required_files:
            if not config.get(req_file):
                missing_files.append(req_file)
        
        if missing_files:
            print(f"⚠️ 누락된 필수 파일: {missing_files}")
            return False
        else:
            print("✅ 모든 필수 데이터 파일이 준비되었습니다!")
            return True

if __name__ == "__main__":
    uploader = RealDataUploader()
    print("실제 데이터 업로드 준비 완료!")
    print("\n사용 방법:")
    print("1. Google Drive에서 모든 데이터 파일을 ZIP으로 압축")
    print("2. ZIP 파일을 data/ 폴더에 업로드")
    print("3. uploader.extract_uploaded_files('data/your_data.zip') 실행")
    print("4. uploader.process_real_data() 실행하여 데이터 검증")