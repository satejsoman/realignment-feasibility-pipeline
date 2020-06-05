import geopandas as gpd
import pandas as pd
from geoalchemy2 import Geometry, WKTElement
from mrjob.job import MRJob, MRStep
from sqlalchemy import create_engine


class BaseHydrator(MRJob):
    def __init__(self, table_name: str, s3_prefix: str, *args, **kwargs):
        super(BaseHydrator, self).__init__(*args, **kwargs)
        self.table_name = table_name 
        self.s3_prefix = s3_prefix
        self.engine = None

    def mapper_init(self):
        self.engine = create_engine("postrgresql://postgres:blorpblorp@:5432/database-1")

    def mapper_raw(self, path, uri):
        gpd.read_file(path).to_sql(
            self.table_name
        )

    def mapper_final(self):
        self.engine.dispose()

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init, mapper_raw=self.mapper_raw, mapper_final=self.mapper_final)]
