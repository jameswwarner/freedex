#!/usr/bin/env python
import itertools
import os,sys
import MySQLdb as db

#eoddata schema

## stock_quote schema
  # `id` bigint(20) NOT NULL AUTO_INCREMENT,
  # `version` bigint(20) NOT NULL,
  # `close_price` double NOT NULL,
  # `high_price` double NOT NULL,
  # `low_price` double NOT NULL,
  # `open_price` double NOT NULL,
  # `quote_date` datetime NOT NULL,
  # `stock_id` bigint(20) NOT NULL,
  # `volume` int(11) NOT NULL,
class StockIdx:
    def __init__(self, dbName):
        self.dbName = dbName
        self.idxTable = "stock";
        self._buildCache()
        pass
    def lookupId(self, symbol):
        return self.stocks[symbol]
        return 1
    def _buildCache(self):
        conn = db.connect(db=self.dbName, user="appuser", passwd="freedex")
        cur = conn.cursor()
        cur.execute("SELECT ticker, id FROM %s" % self.idxTable);
        rows = cur.fetchall()
        self.stocks = dict(itertools.imap(lambda t: (t[0],int(t[1])), rows))
        cur.close()
        conn.commit()

        pass
    pass
        
class QuoteImporter:
    def __init__(self):
        # schema column, column idx in input, conversion function
        self.columnList = [('version',None , lambda : 0),
                           ('stock_id', 0, self.lookupStock),
                           ('quote_date', 1, self.convertDate), 
                           ('open_price', 2, lambda f:f), 
                           ('high_price', 3, lambda f:f),
                           ('low_price', 4, lambda f:f),
                           ('close_price', 5, lambda f:f),
                           ('volume', 6, lambda f:f)]
        self.stockIdx = None
        self.template = "INSERT INTO %s (%s) VALUES %s;"
        self.columnStr = ",".join(map(lambda t: "`%s`" % t[0], 
                                      self.columnList))
        self.dbName = "freedex"
        self.quoteTableName = "stock_quote"
        self.conn = None
        self.cur = None
        pass

    def lookupStock(self, ticker):
        "Return id in stock table"
        if not self.stockIdx: self.stockIdx = StockIdx(self.dbName)
        return self.stockIdx.lookupId(ticker)

    def convertDate(self, eoddate):
        "Convert date from eod format to sql date"
        y = eoddate[:4]
        m = eoddate[4:6]
        d = eoddate[6:]        
        return "%s-%s-%s" %(y,m,d)

    def _readInFile(self, fName):
        for line in open(fName):
            rFields = line.strip().split(",")
            fields = []
            for n,i,f in self.columnList:
                if i == None:
                    fields.append(f())
                else:
                    fields.append(f(rFields[i]))
                pass
            yield fields

    def pushRows(self, batch):
        if not (self.conn and self.cur):
            self.conn = db.connect(db=self.dbName, 
                                   user="appuser", passwd="freedex")
            self.cur = self.conn.cursor()
        q = self.template % (self.quoteTableName, self.columnStr, 
                             ",".join(batch))
        #print "executing q", q
        self.cur.execute(q)
        self.cur.fetchall() # ignore result
        self.conn.commit()
        self.cur = self.conn.cursor()

    def importFields(self, fName):
        batchSize = 100
        buf = []
        
        for fields in self._readInFile(fName):
            val = "(%s)" % ",".join(map(lambda s: "'%s'" % str(s), fields))
            buf.append(val)
            if len(buf) >= batchSize:
                self.pushRows(buf)
                buf = []
                #break
        if buf:
            self.pushRows(buf)
########################################################################

filename=sys.argv[1]
print "importing from", filename        
qi = QuoteImporter()
qi.importFields(filename)
                

            
                
