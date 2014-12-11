class Outputs:
    def __init__(self, output_id):
        self.output_id = output_id

    def load(self):
        dbstring = "select * from outputs where output_id = '"+str(self.output_id)+"';"
        results = db.dbexecute(dbstring, True)
        if len(results)>0:
            self.value = results[0][6]
            self.spent = results[0][5]
            self.transaction_hash = results[0][2]
            self.destination_address = results[0][8]
            self.person_id = results[0][1]

    def load_correlations(self):
        dbstring = "select * from correlations where from_person_id ='"+self.person_id+"';"
        results = db.dbexecute(dbstring, True)
        return results

    def correlations(self):
        correlations = self.load_correlations()
        results = []
        for correlation in correlations:
            to_person_id = correlation[1]
            weight = correlation[2]
            item = {}
            item[to_person_id] = weight
            results.append(item)
        return results
