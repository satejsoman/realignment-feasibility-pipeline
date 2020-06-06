from typing import Any, Dict

import geopandas as gpd
import pandas as pd
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


class BaseHydrator(MRJob):
    def __init__(self, table_name: str, schema: Dict[str, Any], *args, **kwargs):
        super(BaseHydrator, self).__init__(*args, **kwargs)
        self.table_name = table_name 
        self.schema     = schema
        self.engine     = None

    def mapper_init(self):
        self.engine = create_engine(BASE_URL)

    def mapper_raw(self, path, _):
        gdf = gpd.read_file(path)
        gdf["geom"] = gdf["geometry"].apply(WKTElement)
        gdf.drop('geometry', 1, inplace=True)
        gdf.to_sql(self.table_name, self.engine, if_exists='append', index=True, dtype=self.schema)

    def mapper_final(self):
        self.engine.dispose()

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init, mapper_raw=self.mapper_raw, mapper_final=self.mapper_final)]
