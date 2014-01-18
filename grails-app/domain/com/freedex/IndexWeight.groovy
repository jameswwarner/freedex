package com.freedex

class IndexWeight {
    StockField stockField
    boolean isEqual = false

    static belongsTo = [indexDefinition : IndexDefinition]

    static constraints = {
        stockField nullable: true
    }
}
