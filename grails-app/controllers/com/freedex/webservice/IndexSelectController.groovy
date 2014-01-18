package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.IndexSelect
import com.freedex.User
import com.freedex.WebserviceError


/**
 * Web service for getting, creating index selects
 * @author jwarner
 *
 */
class IndexSelectController {

    /**
     * Default does a get
     * @return
     */
    def index() {
        def resource = IndexSelect.get(params.id)
        if (!resource)
            resource = WebserviceError.resourceNotFound
        render resource as JSON
    }

    /**
     * Create an index select
     * @return
     */
    def create() {
        def indexDefinition = IndexDefinition.get(params.indexDefinition)
        def limitStocks  = params.limitStocks
        def offsetStocks = params.offsetStocks
        def indexSelect = new IndexSelect(indexDefinition: indexDefinition,
            limitStocks: limitStocks, offsetStocks: offsetStocks)
        indexSelect.save()
        render indexSelect as JSON
    }
}
