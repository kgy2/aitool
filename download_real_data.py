#!/usr/bin/env python3
"""
Google Drive에서 실제 데이터를 다운로드하는 스크립트
"""

import os
import sys
from pathlib import Path

def download_google_drive_folder():
    """Google Drive 폴더의 파일들을 다운로드하는 안내"""
    
    print("📥 Google Drive 실제 데이터 다운로드 가이드")
    print("=" * 50)
    
    drive_link = "https://drive.google.com/drive/folders/1CTZWeh_QHPRpc5qUEwwLMwVG8ctAlLpk?usp=drive_link"
    
    print(f"\n📂 Google Drive 링크:")
    print(f"   {drive_link}")
    
    print(f"\n🔧 수동 다운로드 방법:")
    print(f"   1. 위 링크를 클릭하여 Google Drive 폴더에 접속")
    print(f"   2. 모든 파일을 선택 (Ctrl+A 또는 Cmd+A)")
    print(f"   3. 우클릭 → '다운로드' 선택")
    print(f"   4. ZIP 파일로 자동 압축되어 다운로드됨")
    print(f"   5. 다운로드된 ZIP 파일을 이 프로젝트의 data/ 폴더에 복사")
    
    print(f"\n💡 자동 처리:")
    print(f"   - ZIP 파일을 data/ 폴더에 넣은 후")
    print(f"   - python setup_real_data.py 실행")
    print(f"   - 자동으로 압축 해제 및 데이터 검증")
    
    # data 디렉토리 확인
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 data 폴더 상태:")
    files = list(data_dir.iterdir())
    if files:
        for file in files:
            print(f"   📄 {file.name}")
    else:
        print(f"   📭 비어있음 - Google Drive에서 파일들을 다운로드해주세요")
    
    print(f"\n🚀 다음 단계:")
    print(f"   1. Google Drive에서 데이터 다운로드")
    print(f"   2. ZIP 파일을 data/ 폴더에 복사")
    print(f"   3. python setup_real_data.py 실행")
    print(f"   4. .env 파일에서 KAKAO_API_KEY 설정")
    print(f"   5. python app.py 실행")

def try_sample_demo():
    """샘플 데이터로 데모 실행해보기"""
    print(f"\n🎯 샘플 데이터 데모:")
    print(f"   실제 데이터가 없어도 샘플 데이터로 앱 기능을 확인할 수 있습니다.")
    print(f"   python app.py 실행 후 http://localhost:5000 접속")
    
    # 샘플 데이터 확인
    sample_files = [
        "data/sample_score_table.csv",
        "data/sample_weight_table.csv", 
        "data/sample_housing_data.txt"
    ]
    
    print(f"\n📋 샘플 데이터 확인:")
    for file_path in sample_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")

if __name__ == "__main__":
    download_google_drive_folder()
    try_sample_demo()