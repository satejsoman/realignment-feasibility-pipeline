from hydrator import *

if __name__ == "__main__":
    blocks_hydrator = BaseHydrator("blocks", {"geom": Geometry("POLYGON")})
    blocks_hydrator.run()