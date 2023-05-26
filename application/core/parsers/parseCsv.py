# this file parses a camden conservation area csv into an entity class
# need to have some good thought about how we can make this generic, so it can import from any structure csv

import pandas
from io import StringIO
from application.models.Entity import Entity

def parseCsv(contents):
    csvStringIO = StringIO(contents)
    dataColumns = pandas.read_csv(csvStringIO, sep=",", header=None)

    data = []

    for rowNumber, row in enumerate(dataColumns.values):
        row = row.tolist()
        if rowNumber == 0:
            continue
        point = row.pop(6)
        geometry = row.pop(2)
        name = row.pop(1)
        reference = row.pop(0)
        attributes = row
        data.append(Entity(reference, name, geometry, point, row))

    return data
