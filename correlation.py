import hashlib
import db

def generate_new_id():
  return hashlib.sha256(str(random.random()))

def add_correlations(correlation1, correlation2):
    newvector = []
    for x in correlation1.vector:
        for y in correlation2.vector:
            if x[0] == y[0]:
                newvector.append([x[0], x[1]+y[1]])
