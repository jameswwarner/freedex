package com.freedex

enum StockField {
    sharePrice("Share Price"),
    marketCap("Market Cap"),
    bookValue("Book Value"),
    peRatio("P/E Ratio"),
    sector("Sector"),
    industry("Industry")

    String displayName

    StockField(String displayName) {
        this.displayName = displayName
    }
}
