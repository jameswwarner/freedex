<%-- Copyright (c) 2013-2014 Freedex, All Rights Reserved --%>
<select class=sort-order>
    <g:each var="sortOrder" in="${com.freedex.SortOrder.values()}">
        <option value="${sortOrder.toString()}">${sortOrder.toString()}</option>
    </g:each>
</select>
