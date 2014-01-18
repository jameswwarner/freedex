// Copyright (c) 2013-2014 James W. Warner, All Rights Reserved

package com.freedex.webservice

import grails.converters.JSON
import com.freedex.EventLoggingService


class EventLogController {
    EventLoggingService eventLoggingService

    static allowedMethods = [index: "POST"]

    def index() {
        def jsonPayload = request.JSON
        eventLoggingService.logJson(session.id, request.token, jsonPayload)
        render ([status: "ok"] as JSON)
    }

    def error() {
        log.error(params.msg)
        render ([status: "ok", msg: params.msg] as JSON)
    }

}
