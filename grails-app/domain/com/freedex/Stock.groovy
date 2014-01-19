package com.freedex

class Stock {
    // fields from fundamentals field
    String ticker
    String name
    Sector sector
    Industry industry
    double priceToEarnings
    double earningsPerShare
    double dividendYield
    long numShares
    double dps
    double priceEarningsGrowth
    double pts
    double priceToBook

    Collection stockQuotes
    static hasMany = [stockQuotes: StockQuote]

    static constraints = {
        ticker unique: true
        sector nullable: true
        industry nullable: true
    }
}
