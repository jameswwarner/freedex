// Copyright (c) 2013-2014 Freedex, All Rights Reserved

'use strict';

if (!app)
   var app = {};

app.defineIndex = {
    indexId: undefined,
    duplicate: function(event) {
        var row = $(event.target).closest('.step-row');
        var newRow = row.clone();
        newRow.insertAfter(row);
    },
    createFilters: function() {
        $('#filter-step .filter-row').each(function() {
            var elem = $(this);
            var field = elem.find('.stock-field').val();
            var op = elem.find('.operation').val();
            var val = elem.find('.row-value').val();
            if (val) {
                library.action.call('index-filter', { action: 'create',
                    params: {indexDefinition: app.defineIndex.indexId,
                             stockField: field, operation: op, value: val} });
            }
        });
    },
    createSorts: function() {
        $('#sort-step .sort-row').each(function() {
            var elem = $(this);
            var field = elem.find('.stock-field').val();
            var sortOrder = elem.find('.sort-order').val();
            library.action.call('index-sort', { action: 'create',
                params: {indexDefinition: app.defineIndex.indexId,
                         stockField: field, sortOrder: sortOrder} });
        });
    },
    handleSnapshotCreate: function(data) {
        if (!data.error) {
            // redirect to view page
            window.location = $('#base-uri').val() + 'view-index';
        }
    },
    handleWeightCreate: function(data) {
        if (!data.error) {
            // calculate holdings
            library.action.call('index-snapshot', { action: 'create',
                params: {indexDefinition: app.defineIndex.indexId},
                callback: app.defineIndex.handleSnapshotCreate });
        }
    },
    createWeight: function() {
        var weightField = $('#weight-step .stock-field').val();
        library.action.call('index-weight', { action: 'create',
            params: {indexDefinition: app.defineIndex.indexId,
                     stockField: weightField},
                     callback: app.defineIndex.handleWeightCreate });
    },
    handleSelectCreate: function(data) {
        if (!data.error) {
            app.defineIndex.createWeight();
        }
    },
    createSelect: function() {
        var limit  = $('#select-limit').val();
        var offset = $('#select-offset').val();
        library.action.call('index-select', { action: 'create',
            params: {indexDefinition: app.defineIndex.indexId,
                     limitStocks: limit, offsetStocks: offset},
                     callback: app.defineIndex.handleSelectCreate });
    },
    handleCreateIndex: function(data) {
        if (!data.error) {
            app.defineIndex.indexId = data.id;
            app.defineIndex.createFilters();
            app.defineIndex.createSorts();
            app.defineIndex.createSelect();
        }
    },
    createIndex: function() {
        var name = $('#index-name').val();
        if (name) {
            console.log("Creating index definition...")
            library.action.call('index-definition', { action: 'create',
                params: {name: name}, callback: app.defineIndex.handleCreateIndex });
        }
    },
    submit: function(event) {
        library.loading.on();
        app.defineIndex.createIndex();
    },
    setup: function() {
        if ($('#page-define-index').exists()) {
            library.ui.liveClick('.add-row', app.defineIndex.duplicate);
            library.ui.liveClick('#define-index-submit', app.defineIndex.submit);
        }
    }
};
