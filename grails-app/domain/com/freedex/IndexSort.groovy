package com.freedex

enum SortOrder {
    descending,
    ascending,
}

class IndexSort {
    StockField stockField
    SortOrder sortOrder = SortOrder.descending

    static belongsTo = [indexDefinition : IndexDefinition]
}
