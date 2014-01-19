
import grails.converters.JSON

import com.freedex.WebserviceError
import com.freedex.IndexSnapshot
import com.freedex.IndexComponent
import com.freedex.Stock

class BootStrap {

    def init = { servletContext ->
        //Default timezone
        TimeZone.setDefault(TimeZone.getTimeZone("America/Los_Angeles"))

        //Web Services
        JSON.registerObjectMarshaller(WebserviceError) {
            return [
               error: true,
               code:  it.code,
               msg:   it.msg
            ]
        }

        JSON.registerObjectMarshaller(IndexSnapshot) {
            return [
                id: it.id,
                indexDefinition: [id: it.indexDefinition.id, name: it.indexDefinition.name],
                snapshotDate: it.snapshotDate,
                indexComponents: it.indexComponents.sort({-it.weight}).collect {
                    [id: it.id, stock: [id: it.stock.id, ticker: it.stock.ticker, name: it.stock.name],
                     weight: it.weight]
                }
             ]
        }
    }
    def destroy = {
    }
}
