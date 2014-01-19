#!/usr/bin/env python
# prerequisites: NYSE.txt in current working directory, 
# downloaded from eoddata.com
import itertools
import MySQLdb as db
## schema:
# `id` bigint(20) NOT NULL AUTO_INCREMENT,
# `version` bigint(20) NOT NULL,
# `dividend_yield` double NOT NULL,
# `dps` double NOT NULL,
# `earnings_per_share` double NOT NULL,
# `industry_id` bigint(20) NOT NULL,
# `name` varchar(255) NOT NULL,
# `num_shares` int(11) NOT NULL,
# `price_earnings_growth` double NOT NULL,
# `price_per_share` double NOT NULL,
# `price_to_book` double NOT NULL,
# `price_to_earnings` double NOT NULL,
# `pts` double NOT NULL,
# `sector_id` bigint(20) NOT NULL,
# `ticker` varchar(255) NOT NULL

###  color scheme
# blue r 1b, g 75, b bb
# grey a7 a9 ab

# fundamental columns:
#Symbol	Name	Sector	Industry	PE	EPS	DivYield	Shares	DPS	PEG	PtS	PtB

columns = ["version", "ticker", "name", "sector_id", 
           "industry_id",  "price_to_earnings", "earnings_per_share",  
           "dividend_yield",    "num_shares",  "dps", 
           "price_earnings_growth", "pts", "price_to_book", 
           "price_per_share"]


vTemplate = "()"

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


#sectors = dict(zip(sectorList, itertools.count()))
#industries = dict(zip(industryList, itertools.count()))


def grabInverted(cur, tableName):
    q = "SELECT id, name FROM %s;" % (tableName)
    print q
    cur.execute(q);
    vals = cur.fetchall()
    #vals looks like: ((5L, 'hello'), (6L, 'foo'))
    #invert the list.
    inverted = map(lambda t: (t[1],t[0]), vals)
    return inverted

def insertOnly(conn, vList, tableName):
    vList = map(conn.escape_string, vList)
    cur = conn.cursor()
    tuples = ",".join(map(lambda s:"(0,'%s')" %s, vList))
    q = "INSERT INTO %s (%s) VALUES %s;" % (tableName, 
                                              "`version`,`name`", tuples)
    cur.execute(q);
    print cur.rowcount, "rows inserted" 
    cur.close()
    pass

def insertGrab(vList, dbName, tableName):
    conn = db.connect(db=dbName, user="appuser", passwd="freedex")
    insertOnly(conn, vList, tableName)
    conn.commit()
    cur = conn.cursor()
    idx = grabInverted(cur, tableName)
    conn.commit()
    return idx
def fixInt(intString):
    # Try as integer first.
    try: return int(filter(lambda c: c != ',', intString))
    except: return 0

def grabFundies(fName, sectors, industries): 
    stocks = []
    for fields in lines(fName, 1, cleanupSectorIndustry):
        #print fields
        try:
            fields[2]  = sectors[fields[2]]
            fields[3] = industries[fields[3]]
            fields[7] = fixInt(fields[7])
            yield fields
            #val = "(%s)" % (",".join(map(lambda v: "'%s'"%str(v), fields)))
            #yield val
        except Exception, e:
            print e
            print "Error handling:", fields, "skipping..."
        pass

def makeFundTuple(fields):
    # version 0 (col 0)
    # price per share 0 ( last col)
    out = [0] + list(fields) + [0]
    return out
    
def insertFundies(conn, tableName, fieldsIterable):
    """tuples is the iterable output from grabFundies and makeFundTuple"""
    columnList = ",".join(columns)
    tuples = []
    skip = 0
    
    for f in fieldsIterable:
        if skip: 
            skip -= 1
            continue
        #2 is column idx of company name
        f[2] = conn.escape_string(f[2])
        tuples.append("(%s)" % (",".join(map(lambda s: "'%s'" %s, f))))

            
        #break #debugging..
    cur = conn.cursor()
    off = 0
    while tuples:
        subset = tuples[:100]
        q = "INSERT INTO %s (%s) VALUES %s;" % (tableName, 
                                                columnList, 
                                                ",".join(subset))
        tuples = tuples[100:]
        print "Executing (%d): " %off
        cur.execute(q)
        print cur.rowcount, "rows inserted into", tableName
        off += 100
    cur.close()
    pass

def processFundies(fName, dbName, tableName, sectors, industries):
    conn = db.connect(db=dbName, user="appuser", passwd="freedex")
    insertFundies(conn, tableName, itertools.imap(makeFundTuple, 
                                                 grabFundies(fName, 
                                                             sectors, 
                                                             industries)))
    conn.commit()
    pass

(secList, indList) = grabMeta("NYSE.txt")

# Refresh:
# delete from industry; alter table industry auto_increment=1;
# delete from sector; alter table sector auto_increment=1;

secIdx = insertGrab(secList, "freedex", "sector")
indIdx = insertGrab(indList, "freedex", "industry")
sectors = dict(secIdx)
industries = dict(indIdx)

processFundies("NYSE.txt", "freedex", "stock", sectors, industries)

#print "sector index:", secIdx
#print "industry index:", indIdx

    


