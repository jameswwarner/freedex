<%-- Copyright (c) 2013-2014 Freedex, All Rights Reserved --%>
<html>
<head>
    <meta name="layout" content="key">
    <meta property="og:title" content="Freedex - View an index">
    <%-- meta property="og:image" content="http:${resource(dir: 'images/key', file: 'share-thumb.jpg')}" --%>
    <%-- meta property="og:description" content="${com.freedex.Configuration.lookup("og-description")}" --%>
    <%-- meta name="description" content="${com.freedex.Configuration.lookup("og-description")}" --%>
</head>
<body id="page-view-index">

<g:render template="/includes/subNav" model="[pageName:'viewIndex']" />

<h1>View Indexes</h1>

<h2>Available Indexes</h2>
<ul class=available-indexes>
    <g:each var="index" in="${com.freedex.IndexDefinition.list()}">
        <li class=available-index data-id=${index.id}><span>${index.name}</span></li>
    </g:each>
</ul>

<div class=hide-me id=index-holdings>
    <h2>Index Holdings: <span class=index-name><%-- name put here by JS --%></span></h2>
    <table>
        <tr><th>Ticker</th><th>Name</th><th>Weight in index</th></tr>
        <tbody>
            <%-- rows shoved here by js --%>
        </tbody>
    </table>
</div>

</body>
</html>
