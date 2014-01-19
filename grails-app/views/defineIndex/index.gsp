<%-- Copyright (c) 2013-2014 Freedex, All Rights Reserved --%>
<html>
<head>
    <meta name="layout" content="key">
    <meta property="og:title" content="Freedex - Define an index">
    <%-- meta property="og:image" content="http:${resource(dir: 'images/key', file: 'share-thumb.jpg')}" --%>
    <%-- meta property="og:description" content="${com.freedex.Configuration.lookup("og-description")}" --%>
    <%-- meta name="description" content="${com.freedex.Configuration.lookup("og-description")}" --%>
</head>
<body id="page-define-index">

<g:render template="/includes/subNav" model="[pageName:'defineIndex']" />

<h1>Define an index</h1>

<label class=name-area>Index Name:
    <input type=text id=index-name>
</label>

<div class=define-step id=filter-step>
    <div class=step-num><span>1</span></div>
    <div class=step-input>
        <div class=step-header>
            <div class=step-name>Filters</div>
            <div class=step-description>
                Please give information about what stocks you would like to exclude from your universe.
            </div>
        </div>
        <div class="filter-row step-row">
            <g:render template="/includes/fieldSelect" />
            <g:render template="/includes/operationSelect" />
            <input type=text class=row-value name=filter-value>
            <span class=add-row>+</span>
        </div>
    </div>
</div>
<div class=define-step id=sort-step>
    <div class=step-num><span>2</span></div>
    <div class=step-input>
        <div class=step-header>
            <div class=step-name>Sort</div>
            <div class=step-description>
                You may sort the stocks by the fields selected.
            </div>
        </div>
        <div class="sort-row step-row">
            <g:render template="/includes/fieldSelect" />
            <g:render template="/includes/sortOrderSelect" />
            <span class=add-row>+</span>
        </div>
    </div>
</div>
<div class=define-step id=select-step>
    <div class=step-num><span>3</span></div>
    <div class=step-input>
        <div class=step-header>
            <div class=step-name>Select</div>
            <div class=step-description>
                Specify and offset and limit for the stocks you want to select.
            </div>
        </div>
        <label>
            <span>Limit</span>
            <input type=text id=select-limit>
        </label>
        <label>
            <span>Offset</span>
            <input type=text id=select-offset>
        </label>
    </div>
</div>
<div class=define-step id=weight-step>
    <div class=step-num><span>4</span></div>
    <div class=step-input>
        <div class=step-header>
            <div class=step-name>Weight</div>
            <div class=step-description>
                Specify the field you would like to use to weight the index.
            </div>
        </div>
        <g:render template="/includes/fieldSelect" />
    </div>
</div>
<div class=button-holder>
    <div id=define-index-submit>Submit</div>
</div>

</body>
</html>
