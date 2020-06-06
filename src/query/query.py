from pathlib import Path
from typing import Any, Dict, Sequence

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import shapely.geometry
import shapely.wkt
from geoalchemy2 import Geometry, WKTElement
from mrjob.job import MRJob, MRStep
from sqlalchemy import create_engine


# fake credentials for github
username = "user"
password = "blorp"
domain   = "public-db-url.rds.amazonaws.com"
port     = 5432
db_name  = "database-1"
BASE_URL = f"postrgresql://{username}:{password}@{domain}:{port}/{db_name}"

def is_feasible(block: shapely.geometry.Polygon, buildings: Sequence[shapely.geometry.Polygon]) -> bool:
    min_area_rects = (list(p.minimum_rotated_rectangle.exterior.coords) for p in buildings)
    return block.length > sum(min(shapely.geometry.LineString(rectangle[i:i+2]).length for i in range(len(rectangle)-1)) for rectangle in min_area_rects)

def query(block_ids, _): 
    engine = create_engine(BASE_URL)

    blocks = gpd.GeoDataFrame.from_postgis(
        f"""
        select 
            blocks.block_id, 
            blocks.geom      as block_geom, 
            buildings.geom   as geometry_buildings
        from 
            blocks, 
            buildings
        where 
            blocks.block_id in {block_ids} and 
            ST_Contains(block_geom, geometry_buildings)
        """, 
        engine, index_col="block_id")\
    .groupby("block_id").agg(list) # client side aggregation to make conversion to Python types cleaner
    engine.dispose()
    return { 
        block_id: is_feasible(block, buildings) 
        for (block_id, block, buildings) 
        in blocks[["block_geom", "geometry_buildings"]].itertuples()
    }