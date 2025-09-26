class University:

    # Constructor, initalizing class

    def __init__(self, name: str, degree: str, ranking: int, latitude: float = None, longitude: float = None):
        self.name = name
        self.degree = degree
        self.ranking = ranking
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"{self.name} (Degree: {self.degree}, Ranking: {self.ranking})"

    def to_dict(self):
        return {
            "name": self.name,
            "degree": self.degree,
            "ranking": self.ranking,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


