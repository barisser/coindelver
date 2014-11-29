import db
import blocks

class Meta:
    def __init__(self):
        dbstring = "select lastblockdone from meta;"
        lastblockdone = db.dbexecute(dbstring, True)[0][0]
        self.lastblockdone = lastblockdone

    def update(self, lastblockdone):
        dbstring = "update meta set lastblockdone = "+str(lastblockdone)+";"
        db.dbexecute(dbstring, False)
        self.lastblockdone = lastblockdone

    def process_blocks(self, blockn):
        for i in range(self.lastblockdone+1, blockn+self.lastblockdone+1):
            block = blocks.Blocks(i)
            block.download_data()
            block.process()
            del block
            self.update(i)


main = Meta()
