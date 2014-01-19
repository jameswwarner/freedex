<%-- Copyright (c) 2013-2014 Freedex, All Rights Reserved --%>
<select class=stock-field>
    <g:each var="field" in="${com.freedex.StockField.values()}">
        <option value="${field.toString()}">${field.displayName}</option>
    </g:each>
</select>
