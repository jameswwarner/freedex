package com.freedex.webservice

import grails.converters.JSON

import com.freedex.IndexDefinition
import com.freedex.User
import com.freedex.WebserviceError


/**
 * Webservice for getting, creating index definitions
 * @author jwarner
 *
 */
class IndexDefinitionController {

    /**
     * Default does a get
     * @return
     */
    def index() {
        def resource = IndexDefinition.get(params.id)
        if (!resource)
            resource = WebserviceError.resourceNotFound
        render resource as JSON
    }

    /**
     * Create a new index definition, giving a name
     * @return
     */
    def create() {
        def name = params.name
        def user = User.get(session.userId)
        def definition = new IndexDefinition(name: name, user: user)
        definition.save()
        render definition as JSON
    }
}
