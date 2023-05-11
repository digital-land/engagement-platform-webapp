class points:
    
    def __init__(self, pointsString):
        # remove polygon string from start
        formattedString = pointsString.replace('POLYGON ((', '').replace('))', '')
        pointsStringArray = formattedString.split(',')
        self.pointsArray = []
        for pointString in pointsStringArray:
            pointStringSplit = pointString.strip(' ').split(' ')
            pointValues = [float(pointStringSplit[0]), float(pointStringSplit[1])]
            self.pointsArray.append(pointValues)

    def getViewportSettings(self):
        # need to get min x min y width height
        self.minX = 361
        self.minY = 361
        self.maxX = -361
        self.maxY = -361
        for point in self.pointsArray:
            if(point[0] < self.minX):
                self.minX = point[0]
            if(point[1] < self.minY):
                self.minY = point[1]
            if(point[0] > self.maxX):
                self.maxX = point[0]
            if(point[1] > self.maxY):
                self.maxY = point[1]

        height = self.maxY - self.minY
        width = self.maxX - self.minX

        return str(self.minX) + ' ' + str(self.minY) + ' ' + str((width)) + ' ' + str((height))
    
    def getPolygonPoints(self):
        returnString = ''
        for point in self.pointsArray:
            returnString += str(point[0]) + ',' + str(point[1]) + ' '
        return returnString
    
    def getStrokeWidth(self):
        estimateArea = (self.maxX - self.minX) + (self.maxY - self.minY)
        lineFactor = 0.003
        return estimateArea * lineFactor
