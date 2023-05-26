# this file parses a camden conservation area csv into an entity class
# need to have some good thought about how we can make this generic, so it can import from any structure csv

import pandas
from io import StringIO
from application.models.Entity import Entity, EntityFactory

def parseCsv(contents):
    csvStringIO = StringIO(contents)
    dataColumns = pandas.read_csv(csvStringIO, sep=",", header=0)
    dataArray = dataColumns.to_dict('records')
    data = []

    for row in dataArray:
        row =  {k.lower(): v for k, v in row.items()}
        data.append(EntityFactory.makeFromCsvRow(row))

    return data
