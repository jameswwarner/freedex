package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.IndexFilter
import com.freedex.StockField
import com.freedex.Operation
import com.freedex.User
import com.freedex.WebserviceError


/**
 * Web service for creating, getting index filters
 * @author jwarner
 *
 */
class IndexFilterController {

    /**
     * Default does a get
     * @return
     */
    def index() {
        def resource = IndexFilter.get(params.id)
        if (!resource)
            resource = WebserviceError.resourceNotFound
        render resource as JSON
    }

    /**
     * Create a new index filter
     * @return
     */
    def create() {
        def indexDefinition = IndexDefinition.get(params.indexDefinition)
        def stockField = params.stockField as StockField
        def operation  = params.operation as Operation
        def value      = params.value
        def indexFilter = new IndexFilter(indexDefinition: indexDefinition, stockField: stockField,
            operation: operation, value: value)
        indexFilter.save()
        render indexFilter as JSON
    }
}
