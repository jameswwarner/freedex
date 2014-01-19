class UrlMappings {

	static mappings = {
        def maintenanceMode = false
        final controllers = [
            page: ["page", "define-index", "view-index"],
            rest: ["configuration", "event-log", "index-definition",
                "image", "auth", "index-filter", "index-select", "index-sort", "index-weight"],
            admin: ["data-hub", "mktg-hub", "ops-hub"]
        ]
        "/robots.txt" (controller: "page", action: "robots")
        name admin: "/admin/$controller/$action?" {
            constraints {
                controller inList: controllers.admin
            }
        }
        if (maintenanceMode) {
            "/**" (controller: "page", action: "maintenance")
        }
        else {
            "/" (controller: "page", action: "gateway")
            name rest: "/rest/$controller/$action/$id?" {
                constraints {
                    controller inList: controllers.rest
                    action matches: "[a-z][0-9a-z-]+"
                    id matches: "[0-9]+"
                }
            }
            name rest: "/rest/$controller/$id?" {  //simple get resource (default action)
                constraints {
                    controller inList: controllers.rest
                    id matches: "[0-9]+"
                }
            }
            "/$controller/$action?/$id?"{
                constraints {
                    controller inList: controllers.page
                    id matches: "[0-9]+"
                }
            }
            "404" (controller: "page", action: "not-found")
            "500" (controller: "page", action: "error")
        }
	}
}
