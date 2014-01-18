package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.IndexWeight
import com.freedex.StockField
import com.freedex.User
import com.freedex.WebserviceError

class IndexWeightController {

    /**
     * Default does a get
     * @return
     */
    def index() {
        def resource = IndexWeight.get(params.id)
        if (!resource)
            resource = WebserviceError.resourceNotFound
        render resource as JSON
    }

    /**
     * Create a new index weight
     * @return
     */
    def create() {
        def indexDefinition = IndexDefinition.get(params.indexDefinition)
        def stockField = params.stockField as StockField
        def indexWeight = new IndexWeight(indexDefinition: indexDefinition,
            stockField: stockField)
        indexWeight.save()
        render indexWeight as JSON
    }
}
