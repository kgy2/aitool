import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np
from data_processor import SpatialDataProcessor
from score_calculator import ScoreCalculator

"""
run_sample.py
-------------
A lightweight, self-contained demo that uses the three sample data files shipped in
`data/` to exercise the SpatialDataProcessor and ScoreCalculator classes without
requiring any external GIS layers or a Kakao API key.

Usage:
    python run_sample.py
It will print summary statistics and write `output/sample_scored_grids.geojson`.
"""

# ---------------------------------------------------------------------------
# 1. Input paths
# ---------------------------------------------------------------------------
DATA_DIR = "data"
HOUSING_PATH = f"{DATA_DIR}/sample_housing_data.txt"
SCORE_TABLE_PATH = f"{DATA_DIR}/sample_score_table.csv"
WEIGHT_TABLE_PATH = f"{DATA_DIR}/sample_weight_table.csv"

# ---------------------------------------------------------------------------
# 2. Instantiate helpers
# ---------------------------------------------------------------------------
# We pass a dummy Kakao key because the demo does not call any geocoding APIs.
processor = SpatialDataProcessor(kakao_api_key="DUMMY_KEY")
calculator = ScoreCalculator(SCORE_TABLE_PATH, WEIGHT_TABLE_PATH)

# ---------------------------------------------------------------------------
# 3. Load housing counts (tab-separated)
# ---------------------------------------------------------------------------
housing_df = processor.load_housing_data(HOUSING_PATH)

if housing_df is None:
    raise RuntimeError("Failed to read sample_housing_data.txt — aborting demo.")

# ---------------------------------------------------------------------------
# 4. Build a synthetic 100 m-grid layer
# ---------------------------------------------------------------------------
#  For the purpose of this sample we create one square polygon per row with a
#  nominal size of ≈500 m (0.005 degrees) laid out in a simple east-west line.
polygons = []
for i in range(len(housing_df)):
    x0 = i * 0.01            # 0.01° ≈ 1.11 km spacing — prevents overlap
    y0 = 0.0
    poly = Polygon([
        (x0, y0),
        (x0, y0 + 0.005),
        (x0 + 0.005, y0 + 0.005),
        (x0 + 0.005, y0)
    ])
    polygons.append(poly)

grid_gdf = gpd.GeoDataFrame({
    "grid_id": housing_df["grid_id"].values
}, geometry=polygons, crs="EPSG:4326")

# Attach the synthetic grid layer to the processor so downstream helper
# functions (filter_buildable_grids, etc.) can operate.
processor.grid_gdf = grid_gdf

# ---------------------------------------------------------------------------
# 5. Skip exclusion layers (buildings/agricultural) — none in this demo
# ---------------------------------------------------------------------------
buildable_grids = processor.filter_buildable_grids(exclusion_types=[])  # no exclusions

# ---------------------------------------------------------------------------
# 6. Create minimal sets of facility points
# ---------------------------------------------------------------------------
#  One dummy substation ~1 km west of the first grid, one dummy solar plant ~1 km
#  east of the last grid.
substation_gdf = gpd.GeoDataFrame(geometry=[Point(-0.01, 0.0025)], crs="EPSG:4326")
solar_gdf = gpd.GeoDataFrame(geometry=[Point(polygons[-1].centroid.x + 0.01, 0.0025)], crs="EPSG:4326")

# ---------------------------------------------------------------------------
# 7. Align housing counts with `buildable_grids`
# ---------------------------------------------------------------------------
#  Ensure we have housing counts in the same row order as `buildable_grids`.
housing_counts = housing_df.set_index("grid_id").loc[buildable_grids["grid_id"], "housing_count"].values

# ---------------------------------------------------------------------------
# 8. Calculate scores
# ---------------------------------------------------------------------------
score_dict = calculator.calculate_total_score(
    grid_gdf=buildable_grids,
    substation_gdf=substation_gdf,
    solar_gdf=solar_gdf,
    housing_counts=housing_counts
)

scored_gdf = calculator.create_scored_geodataframe(buildable_grids, score_dict)

# ---------------------------------------------------------------------------
# 9. Persist and report
# ---------------------------------------------------------------------------
OUTPUT_DIR = "output"
OUTPUT_PATH = f"{OUTPUT_DIR}/sample_scored_grids.geojson"
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)
calculator.export_results_to_geojson(scored_gdf, OUTPUT_PATH)

print("\nTop-5 candidate grid cells based on total score:\n")
print(scored_gdf[["grid_id", "total_score", "score_grade"]]
      .sort_values("total_score", ascending=False)
      .head(5)
      .to_string(index=False))

print(f"\nFull GeoJSON with scores written to {OUTPUT_PATH}")