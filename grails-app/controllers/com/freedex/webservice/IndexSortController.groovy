package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.IndexSort
import com.freedex.StockField
import com.freedex.SortOrder
import com.freedex.User
import com.freedex.WebserviceError


/**
 * Web service for creating sorts
 * @author jwarner
 *
 */
class IndexSortController {

    /**
     * Default does a get
     * @return
     */
    def index() {
        def resource = IndexSort.get(params.id)
        if (!resource)
            resource = WebserviceError.resourceNotFound
        render resource as JSON
    }

    /**
     * Create a new sort
     * @return
     */
    def create() {
        def indexDefinition = IndexDefinition.get(params.indexDefinition)
        def stockField = params.stockField as StockField
        def sortOrder = params.sortOrder ? params.sortOrder as SortOrder : SortOrder.descending
        def indexSort = new IndexSort(indexDefinition: indexDefinition,
            stockField: stockField, sortOrder: sortOrder)
        indexDefinition.addToIndexSorts(indexSort)
        indexSort.save()
        indexDefinition.save()
        render indexSort as JSON
    }
}
