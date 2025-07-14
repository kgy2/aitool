#!/usr/bin/env python3
"""
실제 데이터 설정 자동화 스크립트
Google Drive 링크의 데이터를 다운로드하고 앱에 적용하는 스크립트
"""

import os
import sys
import shutil
from pathlib import Path
from data_uploader import RealDataUploader

def main():
    print("🚀 농촌 데이터센터 입지 추천 AI 툴 - 실제 데이터 설정")
    print("=" * 60)
    
    # 1. 환경 확인
    print("\n1️⃣ 환경 확인 중...")
    
    # 필요한 패키지 확인
    try:
        import geopandas
        import pandas
        import flask
        import folium
        print("✅ 필요한 패키지들이 설치되어 있습니다.")
    except ImportError as e:
        print(f"❌ 필요한 패키지가 누락되었습니다: {e}")
        print("다음 명령어로 설치해주세요: pip install -r requirements.txt")
        return
    
    # 2. 데이터 디렉토리 확인
    print("\n2️⃣ 데이터 디렉토리 확인 중...")
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("✅ data 폴더를 생성했습니다.")
    
    # 3. 환경 변수 설정
    print("\n3️⃣ 환경 변수 설정 확인 중...")
    env_file = Path(".env")
    if not env_file.exists():
        if Path(".env.example").exists():
            shutil.copy(".env.example", ".env")
            print("✅ .env 파일을 생성했습니다.")
            print("⚠️ .env 파일에서 KAKAO_API_KEY를 설정해주세요.")
        else:
            print("❌ .env.example 파일이 없습니다.")
    else:
        print("✅ .env 파일이 이미 존재합니다.")
    
    # 4. 실제 데이터 확인
    print("\n4️⃣ 실제 데이터 확인 중...")
    uploader = RealDataUploader()
    
    # ZIP 파일 확인
    zip_files = list(data_dir.glob("*.zip"))
    if zip_files:
        print(f"📦 ZIP 파일 발견: {len(zip_files)}개")
        for zip_file in zip_files:
            print(f"  - {zip_file.name}")
        
        # 첫 번째 ZIP 파일 추출
        latest_zip = zip_files[0]
        print(f"\n📂 {latest_zip.name} 추출 중...")
        try:
            uploader.extract_uploaded_files(str(latest_zip))
            print("✅ ZIP 파일 추출 완료!")
        except Exception as e:
            print(f"❌ ZIP 파일 추출 실패: {e}")
            return
    
    # 5. 데이터 검증
    print("\n5️⃣ 데이터 검증 중...")
    try:
        data_mapping = uploader.process_real_data()
        
        if not data_mapping:
            print("❌ 유효한 데이터 파일을 찾을 수 없습니다.")
            print("\n📋 필요한 데이터 파일들:")
            print("  📍 Shapefile: 100m격자, 건축물정보, 농업진흥지역")
            print("  📊 CSV: 점수표, 가중치표") 
            print("  📄 TXT: 격자별주택수, 변전소주소, 태양광주소")
            print("\n💡 Google Drive 링크에서 파일들을 다운로드하여")
            print("   data/ 폴더에 직접 복사하거나 ZIP으로 압축해주세요.")
            return
        
        # 6. 데이터 매핑 설정
        print("\n6️⃣ 데이터 매핑 설정 중...")
        config = uploader.create_real_data_config(data_mapping)
        
        print("\n📋 발견된 데이터 파일 매핑:")
        for key, value in config.items():
            if value:
                print(f"  ✅ {key}: {Path(value).name}")
            else:
                print(f"  ❌ {key}: 파일 없음")
        
        # 7. 완성도 검사
        print("\n7️⃣ 데이터 완성도 검사 중...")
        is_complete = uploader.validate_data_completeness(config)
        
        if is_complete:
            print("\n🎉 모든 필수 데이터가 준비되었습니다!")
            print("\n🚀 다음 단계:")
            print("  1. .env 파일에서 KAKAO_API_KEY 설정")
            print("  2. python app.py 실행")
            print("  3. http://localhost:5000 접속")
        else:
            print("\n⚠️ 일부 필수 데이터가 누락되었습니다.")
            print("real_data_guide.md 파일을 참고하여 필요한 데이터를 준비해주세요.")
            
    except Exception as e:
        print(f"❌ 데이터 검증 중 오류 발생: {e}")
        print("자세한 내용은 real_data_guide.md를 참고해주세요.")
    
    print("\n" + "=" * 60)
    print("설정 완료! 문제가 있다면 real_data_guide.md를 확인해주세요.")

if __name__ == "__main__":
    main()