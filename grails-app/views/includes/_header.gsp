<%-- Copyright (c) 2013-2014 James W. Warner, All Rights Reserved --%>
<div id=section-header>

    <div id=top-bar-intro>
        <g:link controller="page" action="gateway">
            <g:img class="intro-logo" uri="/images/key/freedex-logo.png" alt="Logo" />
        </g:link>
        <g:render template="/includes/socialFollowButtons" model="['hideTumblr': true]" />
    </div>

    <div id=top-bar-define class="header-menu-item" data-page=define>
        <g:link controller="defineIndex">Define Index</g:link>
    </div>

    <div id=top-bar-view class="header-menu-item" data-page=view>
        <g:link controller="viewIndex">View Index</g:link>
    </div>

</div>
