package com.freedex

/**
 * For calculating a new index snapshot
 * @author jwarner
 *
 */
class IndexSnapshotService {
    boolean transactional = true

    def sessionFactory
    def propertyInstanceMap = org.codehaus.groovy.grails.plugins.DomainClassGrailsPlugin.PROPERTY_INSTANCE_MAP
    def grailsApplication
    final batchSize = 100

    /**
     * Helper function to flush out gorm for performance
     * @return
     */
    def cleanUpGorm() {
        def session = sessionFactory.currentSession
        session.flush()
        session.clear()
        propertyInstanceMap.get().clear()
    }

    /**
     * Assumes quote is q, stock is s
     */
    def stockFieldToHql(def stockField) {
        switch(stockField) {
            case StockField.sharePrice:
                return "q.closePrice"
            case StockField.marketCap:
                return "(q.closePrice * s.numShares)"
            case StockField.bookValue:
                return "((q.closePrice/s.priceToBook) * s.numShares)"
            case StockField.peRatio:
                return "s.priceToEarnings"
            case StockField.sector:
                return "s.sector"
            case StockField.industry:
                return "s.industry"
        }
    }

    /**
     * Create a new snapshot
     * @param indexDefinition
     * @return
     */
    def create(def indexDefinition) {
        def indexWeight = indexDefinition.indexWeight
        def query = "select s, ${stockFieldToHql(indexWeight.stockField)} AS WEIGHT "+
            "from Stock s join s.stockQuotes q "+
            "where s.numShares > 0 ";
        for (def indexFilter : indexDefinition.indexFilters) {
            def newWhere = " AND ";
            newWhere = newWhere + stockFieldToHql(indexFilter.stockField) +
                indexFilter.operation.displayName+indexFilter.value
            query = query + newWhere
        }
        query = query + " order by "
        def first = true
        for (def indexSort : indexDefinition.indexSorts) {
            if (!first) {
                query = query + ", "
            }
            query = query + stockFieldToHql(indexSort.stockField) +
                (indexSort.sortOrder == SortOrder.descending ? " DESC" : " ASC")
            first = false
        }
        def indexSelect = indexDefinition.indexSelect
        def paginationParams = [:]
        paginationParams['max'] = 9999 // HACK
        if (indexSelect.limitStocks) {
            paginationParams['max'] = indexSelect.limitStocks
        }
        if (indexSelect.offsetStocks) {
            paginationParams['offset'] = indexSelect.offsetStocks
        }
        def results = Stock.executeQuery(query, paginationParams)
        def indexSnapshot = new IndexSnapshot(indexDefinition: indexDefinition,
            snapshotDate: new Date())
        indexSnapshot.save()
        def totalWeight = results.collect { it[1] }.sum()
        def num=0
        for(def row : results) {
            def indexComponent = new IndexComponent(indexSnapshot: indexSnapshot,
                stock: row[0], weight: row[1]/totalWeight)
            //indexSnapshot.addToIndexComponents(indexComponent)
            indexComponent.save()
            if (num % batchSize == 0) {
                cleanUpGorm()
            }
            //indexSnapshot.save()
        }
        indexSnapshot.refresh() // need to fill collection
        return indexSnapshot
    }
}
