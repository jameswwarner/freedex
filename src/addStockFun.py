#!/usr/bin/env python
import os,sys
import MySQLdb as db
import fdxUtil

columns = ["version", "ticker", "name", "sector_id", 
           "industry_id",  "price_to_earnings", "earnings_per_share",  
           "dividend_yield",    "num_shares",  "dps", 
           "price_earnings_growth", "pts", "price_to_book", 
           "price_per_share"]

def fixInt(intString):
    # Try as integer first.
    try: return int(filter(lambda c: c != ',', intString))
    except: return 0

class StockFunImporter:
    def __init__(self, fList):
        self.fList = fList
        self.sectorIdx = None
        self.industryIdx = None
        self.dbName = "freedex"
        self.funTableName = "stock"
        self.columnList = ",".join(columns)

        self.conn = db.connect(db=self.dbName, user="appuser", passwd="freedex")
        self.initIdxs()
        pass

    def grabIdx(self, cur, tableName):
        q = "SELECT name, id FROM %s;" % (tableName)
        print q
        cur.execute(q);
        vals = cur.fetchall()
        #vals looks like: ((5L, 'hello'), (6L, 'foo'))
        #invert the list.
        return vals

    def initIdxs(self):
        cur = self.conn.cursor()
        self.sectorIdx = dict(self.grabIdx(cur, "sector"))
        self.industryIdx = dict(self.grabIdx(cur, "industry"))
        #print self.sectorIdx.items()[:10]


    def _fundReader(self, fName):
        for fields in fdxUtil.lines(fName, 1, fdxUtil.cleanupSectorIndustry):
            #print fields
            try:
                fields[2]  = self.sectorIdx[fields[2]]
                fields[3] = self.industryIdx[fields[3]]
                fields[7] = fixInt(fields[7])
                yield [0] + fields + [0]
   
            except Exception, e:
                print e
                print "Error handling:", fields, "skipping..."
        pass

    def _tupleGen(self, fundGen):
        for f in fundGen:            
            f[2] = self.conn.escape_string(f[2])
            yield "(%s)" % (",".join(map(lambda s: "'%s'" %s, f)))

    def pushTuple(self, cur, tList):
        q = "INSERT IGNORE INTO %s (%s) VALUES %s;" % (self.funTableName, 
                                                       self.columnList, 
                                                       ",".join(tList))
        cur.execute(q)
        print cur.rowcount, "rows inserted into", self.funTableName
        cur.fetchall() # ignore result

    def importFromFile(self, fName):
        print "importing from", fName
        buf = []
        batchSize = 100
        cur = self.conn.cursor()
        for t in self._tupleGen(self._fundReader(fName)):
            buf.append(t)
            if len(buf) >= batchSize:
                self.pushTuple(cur, buf)
                self.conn.commit()
                buf = []
        if buf:
            self.pushTuple(cur, buf)
            self.conn.commit()

    def doImport(self):
        for f in self.fList: 
            self.importFromFile(f)

if __name__ == "__main__":
    sfi = StockFunImporter(sys.argv[1:])
    sfi.doImport()
