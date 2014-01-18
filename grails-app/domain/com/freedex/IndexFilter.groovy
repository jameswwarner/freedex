package com.freedex

class IndexFilter {

    StockField stockField
    Operation operation
    Double value

    static belongsTo = [indexDefinition : IndexDefinition]
}
