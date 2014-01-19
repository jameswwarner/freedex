package com.freedex

/**
 * This represents a definition for an index
 * @author jwarner
 *
 */
class IndexDefinition {
    User user
    String name
    Date created = new Date()

    Collection indexFilters
    List indexSorts
    Collection indexSnapshots
    static hasMany = [indexFilters: IndexFilter, indexSorts: IndexSort,
        indexSnapshots: IndexSnapshot]

    static hasOne = [indexSelect: IndexSelect, indexWeight: IndexWeight]

    static constraints = {
        user nullable: true
        indexSelect nullable: true
        indexWeight nullable: true
    }
}
