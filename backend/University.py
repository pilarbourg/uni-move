class University:

    # Constructor, initalizing class

    def __init__(self, name: str, degree: str, ranking: int):
        self.name = name
        self.degree = degree
        self.ranking = ranking



    def __repr__(self):
        return f"{self.name} (Degree: {self.degree}, Ranking: {self.ranking})"


