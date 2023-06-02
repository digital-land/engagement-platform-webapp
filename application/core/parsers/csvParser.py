# this file parses a camden conservation area csv into an entity class
# need to have some good thought about how we can make this generic, so it can import from any structure csv

import pandas
from io import StringIO

def parseCsv(contents):
    csvStringIO = StringIO(contents)
    dataColumns = pandas.read_csv(csvStringIO, sep=",", header=0, keep_default_na=False, escapechar='\\', quotechar='"')
    dataArray = dataColumns.to_dict('records')
    data = []

    for row in dataArray:
        data.append({'attributes': row, "mapData": {}, "errors": []})

    return data
