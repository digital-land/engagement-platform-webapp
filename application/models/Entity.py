#!/usr/bin/env python3

commonColumnsAlias = {
    'reference': ['reference'],
    'point': ['point'],
    'geometry': ['geometry'],
    'name': ['name'],
}



class EntityFactory:
    # params:
    #   row: dictionary {header: value}
    def makeFromCsvRow(row: dict):
        foundColumns = {}

        for column, aliases in commonColumnsAlias.items():
            for alias in aliases:
                if alias in map(lambda x: x.lower(), row.keys()):
                    foundColumns[column] = row.pop(alias)

        attributes = row

        return Entity(foundColumns['reference'], foundColumns['name'], foundColumns['geometry'], foundColumns['point'], attributes)


class Entity:
    def __init__(self, reference, name, geometry, point, attributes):
        self.reference = reference
        self.name = name
        self.geometry = geometry
        self.point = point
        self.attributes = attributes
