from hydrator import *

if __name__ == "__main__":
    buildings_hydrator = BaseHydrator("buildings", {"geom": Geometry("POLYGON")})
    buildings_hydrator.run()