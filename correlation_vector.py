import db
import math

class CorrelationVector:
    def __init__(self, from_person_id):
        self.from_person_id = from_person_id
        self.vector = []

    def add_component_to_vector(self, to_person_id, weight):
        present = False
        for i, x in enumerate(self.vector):
            if x[0] == to_person_id:
                present=True
                self.vector[i][1] = self.vector[i][1]+weight
        if not present:
            self.vector.append([to_person_id, float(weight)])
        self.normalize_vector()

    def normalize_vector(self):
        magnitude = 0
        for x in self.vector:
            magnitude = magnitude + x[1]*x[1]
        magnitude = math.sqrt(magnitude)
        if magnitude > 0:
            for i in range(0, len(self.vector)):
                self.vector[i][1] = float(self.vector[i][1]) / float(magnitude)

    def scale_vector(self, scalar):
        for i in range(0, len(self.vector)):
            self.vector[i][1] = self.vector[i][1]*float(scalar)

    def load_from_db(self):
        correlations = db.get_correlations(self.from_person_id)
        self.vector = []
        for c in correlations:
            self.vector.append([c[0], c[1]])
        self.normalize_vector()

    def save_to_db(self):
        for v in self.vector:
            weight = v[1]
            to_person_id = v[0]
            from_person_id = self.from_person_id
            dbstring = "insert into correlations values ('"+str(from_person_id)+"', '"+str(to_person_id)+"', "+str(weight)+");"
            db.dbexecute(dbstring, False)
