package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.IndexSnapshot
import com.freedex.IndexComponent
import com.freedex.WebserviceError


/**
 * Viewing and creating index snapshots
 * @author jwarner
 *
 */
class IndexSnapshotController {

    def indexSnapshotService

    /**
     * Default does a get
     * @return
     */
    def index() {
        def indexSnapshot
        if (params.id) {
            indexSnapshot = IndexSnapshot.get(params.id)
        }
        else {
            // better pass the index definition id
            def indexDefinition = IndexDefinition.get(params.indexDefinition)
            indexSnapshot = IndexSnapshot.findAllByIndexDefinition(indexDefinition).last()
        }

        if (!indexSnapshot) {
            render WebserviceError.resourceNotFound as JSON
            return
        }

        render indexSnapshot as JSON
    }

    /**
     * Create a new snapshot
     * @return
     */
    def create() {
        def indexDefinition = IndexDefinition.get(params.indexDefinition)
        def indexSnapshot = indexSnapshotService.create(indexDefinition)
        render indexSnapshot as JSON
    }
}
