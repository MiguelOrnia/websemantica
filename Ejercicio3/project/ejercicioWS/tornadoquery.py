class TornadoQuery:
    def __init__(self, begindate, county, duration):
        self.begindate = begindate
        self.county = county
        self.duration = duration

    def getQuery(self):
        query = self.begindate.split(" ")[0].split("-")[0] + " " + self.county + " tornado"
        return query
