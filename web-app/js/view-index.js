// Copyright (c) 2013-2014 Freedex, All Rights Reserved

'use strict';

if (!app)
   var app = {};

app.viewIndex = {
    handleViewIndex: function(data) {
        if (!data.error) {
            console.log(data);
            var name = data.indexDefinition.name;
            $('#index-holdings .index-name').text(name);
            var destElem = $('#index-holdings tbody');
            for (var i = 0; i < data.indexComponents.length; i++) {
                var component = data.indexComponents[i];
                var stock = component.stock;
                var newRow = $("<tr><td>"+component.stock.ticker+"</td><td>"+
                        component.stock.name+"</td><td>"+
                        (component.weight * 100).toFixed(2)+"%</td></tr>");
                newRow.appendTo(destElem);
            }
            $('#index-holdings').fadeIn();
        }
        library.loading.off();
    },
    displayIndex: function(event) {
        library.loading.on();
        var elem = $(event.target).closest('.available-index');
        var id = elem.data('id');
        if (id) {
            library.action.call('index-snapshot', {
                params: {indexDefinition: id}, callback: app.viewIndex.handleViewIndex });
            $('#index-holdings tbody').empty();
        }
    },
    setup: function() {
        if ($('#page-view-index').exists()) {
            library.ui.liveClick('.available-index', app.viewIndex.displayIndex);
        }
    }
}