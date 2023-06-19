from components.models.entity import Entity
from shapely.geometry import mapping
import shapely.wkt
import json


class Entity_MapData(Entity):
    def __init__(self, *args):
        if type(args[0]) is Entity:
            self.__dict__ = args[0].__dict__.copy()
        else:
            super(Entity_MapData, self).__init__(*args)

        self.mapData = {}
        self.shapely = {}

        try:
            polygon = shapely.wkt.loads(self.Geometry)
            polygons = mapping(polygon)["coordinates"]
            self.Geometry = json.dumps(polygons)
            self.mapData["bounds"] = [
                [polygon.bounds[1], polygon.bounds[0]],
                [polygon.bounds[3], polygon.bounds[2]],
            ]
            self.shapely["polygon"] = polygon
        except Exception as e:
            print("Unable to load polygon: %s", str(e))

        # convert the xy coordinates to lat/long
        try:
            if self.Point is not None:
                point = shapely.wkt.loads(self.Point)
                self.Point = [point.x, point.y]
                self.shapely["point"] = point
        except Exception as e:
            print("Unable to load point: %s", str(e))

    def serialize(self):
        attributes = vars(self).copy()
        mapData = attributes.pop("mapData")
        attributes.pop("shapely")
        mapping = attributes.pop("mapping")
        return {
            "attributes": attributes,
            "mapData": mapData,
            "mapping": mapping,
        }
