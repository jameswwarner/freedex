package com.freedex

/**
 * Represents which stocks from the list to take
 * @author jwarner
 *
 */
class IndexSelect {
    int limitStocks
    int offsetStocks

    static belongsTo = [indexDefinition : IndexDefinition]

    static constraints = {
        limitStocks nullable: true
        offsetStocks nullable: true
    }
}
