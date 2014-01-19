<%-- Copyright (c) 2013-2014 Freedex, All Rights Reserved --%>
<select class=operation>
    <g:each var="op" in="${com.freedex.Operation.values()}">
        <option value="${op.toString()}">${op.displayName}</option>
    </g:each>
</select>
