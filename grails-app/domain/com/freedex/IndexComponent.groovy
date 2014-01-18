package com.freedex

class IndexComponent {
    Stock stock
    Double weight

    static belongsTo = [indexSnapshot : IndexSnapshot]
}
