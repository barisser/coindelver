import hashlib

def correlation_to_string(correlation_vector):
  #[[address, fraction]]
  answer = ''
  for x in correlation_vector:
    answer = answer + "_"+x[0]
    answer = answer + ";"+str(x[1])
  return answer

def string_to_correlation(correlation_string):
  answer = []
  sets = correlation_string.split('_')
  sets = sets[1:len(sets)]
  for x in sets:
    temp = []
    ss = x.split(';')
    temp.append(ss[0])
    temp.append(float(ss[1]))
    answer.append(temp)
  return answer

def generate_new_id():
  return hashlib.sha256(str(random.random()))

a=[['first',0.3], ['second', 3232]]
