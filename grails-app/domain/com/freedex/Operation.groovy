package com.freedex

enum Operation {
    greaterThan(">"),
    greaterOrEqual(">="),
    lessThan("<"),
    lessOrEqual("<="),
    equal("=")

    String displayName

    Operation(String displayName) {
        this.displayName = displayName
    }

}
