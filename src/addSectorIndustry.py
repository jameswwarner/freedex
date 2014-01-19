#!/usr/bin/env python
import MySQLdb as db
import os,sys


def cleanupSectorIndustry(fields):
    for i in [2,3]:
        if not fields[i]: fields[i] = "Unknown"
    pass

def lines(fName, skipLines, cleanup=None):
    toSkip = skipLines
    for line in open(fName):
        fields = line.strip().split("\t")
        if cleanup: cleanup(fields)
        if toSkip:
            #print fields
            toSkip -= 1
            continue
        yield fields
    pass
def grabMeta(fName):
    sectorList = []
    industryList = []
    for fields in lines(fName, 1, cleanupSectorIndustry):
        if len(fields) < 4: continue
        if fields[2]: sectorList.append(fields[2])
        if fields[3]: industryList.append(fields[3])        
        pass
    sectorList = sorted(list(set(sectorList)))
    industryList = sorted(list(set(industryList)))
    return (sectorList, industryList)

class MetaImporter:
    def __init__(self, fList):
        self.fList = fList
        self.sectorSet = set()
        self.industrySet = set()
        self.dbName = "freedex"

    def importFromFile(self, fName):
        print "importing from", fName
        sectorList = []
        industryList = []
        for fields in lines(fName, 1, cleanupSectorIndustry):
            if len(fields) < 4: continue
            if fields[2]: sectorList.append(fields[2])
            if fields[3]: industryList.append(fields[3])        
            pass
        self.sectorSet.update(sectorList)
        self.industrySet.update(industryList)

    def doImport(self):
        for f in self.fList: 
            self.importFromFile(f)

    def insertOnly(self, conn, vList, tableName):
        vList = map(conn.escape_string, vList)
        cur = conn.cursor()
        tuples = ",".join(map(lambda s:"(0,'%s')" %s, vList))
        q = "INSERT INTO %s (%s) VALUES %s;" % (tableName, 
                                                "`version`,`name`", tuples)
        cur.execute(q);
        print cur.rowcount, "rows inserted" 
        cur.close()
        pass

    def pushIdxs(self):
        sectorList = sorted(list(self.sectorSet))
        industryList = sorted(list(set(self.industrySet)))
        conn = db.connect(db=self.dbName, user="appuser", passwd="freedex")
        self.insertOnly(conn, sectorList, "sector")
        conn.commit()
        self.insertOnly(conn, industryList, "industry")
        conn.commit()

# every argument is a file to be scanned for sector and industry
if __name__ == "__main__":
    mi = MetaImporter(sys.argv[1:])
    mi.doImport()
    mi.pushIdxs()

# example:  src/addSectorIndustry.py AMEX.txt NASDAQ.txt NYSE.txt

### refresh everything:
"""
truncate stock_quote;
delete from stock; alter table stock auto_increment=1;
delete from sector; alter table sector auto_increment=1;
delete from industry;  alter table industry auto_increment=1;
"""
