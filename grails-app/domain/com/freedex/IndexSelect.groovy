package com.freedex

/**
 * Represents which stocks from the list to take
 * @author jwarner
 *
 */
class IndexSelect {
    Integer limitStocks
    Integer offsetStocks

    static belongsTo = [indexDefinition : IndexDefinition]

    static constraints = {
        limitStocks nullable: true
        offsetStocks nullable: true
    }
}
