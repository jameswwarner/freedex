package com.freedex

class IndexDefinition {
    User user
    Date created = new Date()

    static constraints = {
        user nullable: true
    }
}
