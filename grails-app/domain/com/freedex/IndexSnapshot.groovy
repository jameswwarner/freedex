package com.freedex

class IndexSnapshot {
    IndexDefinition indexDefinition
    Date snapshotDate

    Collection indexComponents
    static hasMany = [indexComponents: IndexComponent]
}
