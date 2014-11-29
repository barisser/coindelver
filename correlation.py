import hashlib
import db

def generate_new_id():
  return hashlib.sha256(str(random.random()))

def get_correlations_on_address(address):
    all_outputs = db.get_outputs_on_address(address, False)
    result = []
    for output in all_outputs:
        output_id = output[5]
        correlations = db.get_correlations(output_id)
        for correlation in correlations:
            weight = correlation[1]
            output_id = correlation[0]
            person_id = correlation[2]

            if person_id in result:
                result[person_id] = result[person_id] + weight
            else:
                result[person_id] = weight
    return result

def get_correlations_on_tx_inputs(input_set):
    for input in input_set:
        correlations = db.
