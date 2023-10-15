<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta name="robots" content="noindex,nofollow"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="generator" content="0.10 (f6047b328bd2)"/>
    <link rel="icon" href="/source/default/img/icon.png" type="image/png"/>
    <link rel="stylesheet" type="text/css" href="/source/default/style.css?v=f6047b328bd2"/>
    <link rel="stylesheet" type="text/css" href="/source/default/print.css?v=f6047b328bd2" media="print" />

    <link rel="stylesheet" type="text/css" href="/source/default/jquery.tooltip.css?v=f6047b328bd2" />

    <link rel="alternate stylesheet" type="text/css" media="all" title="Paper White" href="/source/default/print.css?v=f6047b328bd2"/>
    <link rel="search" href="/source/opensearch" type="application/opensearchdescription+xml" title="OpenGrok Search for current project(s)" />
    <title>Cross Reference: /SAS_10.20/OPSWrhn_import/bin/cdn_import.py</title>
</head>

<body style="overflow:hidden;">
<script type="text/javascript" src="/source/jquery-1.4.2.min.js"></script>
<script type="text/javascript">/* <![CDATA[ */
function get_annotations() {
    link="/source/xref/SAS_10.20/OPSWrhn_import/bin/cdn_import.py?a=true&r=dffa5290aebf56202c0b13cb10ed3d44264989ec";
    hash="&h="+window.location.hash.substring(1,window.location.hash.length);
    window.location=link+hash;
}
    $().ready(function() {
     h="null";
     if (!window.location.hash) {
         if (h!=null && h!="null")  { window.location.hash=h; }
             else { $('#content').focus(); }
      }
} );
/* ]]> */</script>

<div id="page">
<div id="whole_header" >
<form action="/source/search">
    <div id="header">

<a href="/source/"><span id="MastheadLogo"></span></a>

        <div id="pagetitle"><b id="filename">Cross Reference: cdn_import.py</b></div>
    </div>
    <div id="Masthead"><tt><a href="/source/xref/">xref</a>: /<a href="/source/xref/SAS_10.20">SAS_10.20</a>/<a href="/source/xref/SAS_10.20/OPSWrhn_import">OPSWrhn_import</a>/<a href="/source/xref/SAS_10.20/OPSWrhn_import/bin">bin</a>/<a href="/source/xref/SAS_10.20/OPSWrhn_import/bin/cdn_import.py">cdn_import.py</a></tt></div>
    <div id="bar"><a href="/source/" id="home">Home</a> |
        <a id="history" href="/source/history/SAS_10.20/OPSWrhn_import/bin/cdn_import.py">History</a> | <a href="#" onclick="javascript:get_annotations(); return false;">Annotate</a> | <a href="#" onclick="javascript:lntoggle();return false;" title="Show or hide line numbers (might be slower if file has more than 10 000 lines).">Line #</a> | <a href="#" onclick="javascript:lsttoggle();return false;" title="Show or hide symbol list.">Navigate</a> | <a id="download" href="/source/raw/SAS_10.20/OPSWrhn_import/bin/cdn_import.py?r=dffa5290aebf56202c0b13cb10ed3d44264989ec">Download</a> | <input id="search" name="q" class="q"/>
        <input type="submit" value="Search" class="submit"/>
        <input type="hidden" name="project" value="SAS_10.20"/><input type="checkbox" name="path" value="/SAS_10.20/OPSWrhn_import/bin"/> only in <b>bin</b>
</div></form></div>
        <div id="content">


<script type="text/javascript">/* <![CDATA[ */
function lntoggle() {
   $("a").each(function() {
      if (this.className == 'l' || this.className == 'hl') {
         this.className=this.className+'-hide';
         this.setAttribute("tmp", this.innerHTML);
         this.innerHTML='';
      }
      else if (this.className == 'l-hide' || this.className == 'hl-hide') {
          this.innerHTML=this.getAttribute("tmp");
          this.className=this.className.substr(0,this.className.indexOf('-'));
      }
     }
    );
}

function get_sym_list_contents()
{
    var contents = "";

    //contents += "<input id=\"input_highlight\" name=\"input_highlight\" class=\"q\"/>";
    //contents += "&nbsp;&nbsp;";
    //contents += "<b><a href=\"#\" onclick=\"javascript:add_highlight();return false;\" title=\"Add highlight\">Highlight</a></b><br>";
    contents += "<a href=\"#\" onclick=\"javascript:lsttoggle();\">[Close]</a><br>"

    var symbol_classes = get_sym_list();
    for (var i = 0; i < symbol_classes.length; i++) {
        if (i > 0) {
            contents += "<br/>";
        }
        var symbol_class = symbol_classes[i];
        contents += "<b>" + symbol_class[0] + "</b><br/>";

        var class_name = symbol_class[1];

        var symbols = symbol_class[2];

        for (var j = 0; j < symbols.length; j++) {
            var symbol = symbols[j][0];
            var line = symbols[j][1];
            contents +=
                "<a href=\"#" + line + "\" class=\"" + class_name + "\">" +
                escape_html(symbol) + "</a><br/>";
        }
    }

    return contents;
}

function escape_html(string) {
    return string
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;");
}

// Initial value
document.sym_div_width = 240;
document.sym_div_height_max = 480;
document.sym_div_top = 100;
document.sym_div_left_margin = 40;
document.sym_div_height_margin = 40;

function get_sym_div_left()
{
    document.sym_div_left = $(window).width() - (document.sym_div_width + document.sym_div_left_margin);
    return document.sym_div_left;
}

function get_sym_div_height()
{
    document.sym_div_height = $(window).height() - document.sym_div_top - document.sym_div_height_margin;

    if (document.sym_div_height > document.sym_div_height_max)
        document.sym_div_height = document.sym_div_height_max;

    return document.sym_div_height;
}

function get_sym_div_top()
{
    return document.sym_div_top;
}

function get_sym_div_width()
{
    return document.sym_div_width;
}

function lsttoggle()
{
    if (document.sym_div == null)
    {
        document.sym_div = document.createElement("div");
        document.sym_div.id = "sym_div";

        document.sym_div.className = "sym_list_style";
        document.sym_div.style.margin = "0px auto";
        document.sym_div.style.width = get_sym_div_width() + "px";
        document.sym_div.style.height = get_sym_div_height() + "px";
        document.sym_div.style.top = get_sym_div_top() + "px";
        document.sym_div.style.left = get_sym_div_left() + "px";

        document.sym_div.innerHTML = get_sym_list_contents();

        document.body.appendChild(document.sym_div);
        document.sym_div_shown = 1;
    }
    else
    {
        if (document.sym_div_shown == 1)
        {
            document.sym_div.className = "sym_list_style_hide";
            document.sym_div_shown = 0;
        }
        else
        {
            document.sym_div.style.height = get_sym_div_height() + "px";
            document.sym_div.style.width = get_sym_div_width() + "px";
            document.sym_div.style.top = get_sym_div_top() + "px";
            document.sym_div.style.left = get_sym_div_left() + "px";
            document.sym_div.className = "sym_list_style";
            document.sym_div_shown = 1;
        }
    }
}

$(window).resize(
    function()
    {
        if (document.sym_div_shown == 1)
        {
            document.sym_div.style.left = get_sym_div_left() + "px";
            document.sym_div.style.height = get_sym_div_height() + "px";
        }
    }
);

// Highlighting
/*
// This will replace link's href contents as well, be careful
function HighlightKeywordsFullText(keywords)
{
    var el = $("body");

    $(keywords).each(
        function()
        {
            var pattern = new RegExp("("+this+")", ["gi"]);
            var rs = "<span style='background-color:#FFFF00;font-weight: bold;'>$1</span>";
            el.html(el.html().replace(pattern, rs));
        }
    );
}
//HighlightKeywordsFullText(["nfstcpsock"]);
*/

document.highlight_count = 0;
// This only changes matching tag's style
function HighlightKeyword(keyword)
{
    var high_colors=[
        "#ffff66",
        "#ffcccc",
        "#ccccff",
        "#99ff99",
        "#cc66ff"];

    var pattern = "a:contains('" + keyword + "')";
    $(pattern).css({
        'text-decoration' : 'underline',
        'background-color' : high_colors[document.highlight_count % high_colors.length],
        'font-weight' : 'bold'
    });

    document.highlight_count++;
}

//HighlightKeyword('timeval');

function add_highlight()
{
    var tbox = document.getElementById('input_highlight');
    HighlightKeyword(tbox.value);
}

/* ]]> */
</script>

<div id="src"><span class="pagetitle">cdn_import.py revision dffa5290aebf56202c0b13cb10ed3d44264989ec </span><pre><a class="l" name="1" href="#1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1&nbsp;</a><a href="/source/s?defs=__author__&amp;project=SAS_10.20">__author__</a> = <span class="s">'fauri'</span>
<a class="l" name="2" href="#2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;</a>
<a class="l" name="3" href="#3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3&nbsp;</a><b>import</b> <a href="/source/s?defs=datetime&amp;project=SAS_10.20">datetime</a>
<a class="l" name="4" href="#4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4&nbsp;</a><b>import</b> <a href="/source/s?defs=collections&amp;project=SAS_10.20">collections</a>
<a class="l" name="5" href="#5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5&nbsp;</a><b>import</b> <a href="/source/s?defs=urllib&amp;project=SAS_10.20">urllib</a>
<a class="l" name="6" href="#6">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6&nbsp;</a><b>import</b> <a href="/source/s?defs=os&amp;project=SAS_10.20">os</a>
<a class="l" name="7" href="#7">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7&nbsp;</a><b>import</b> <a href="/source/s?defs=re&amp;project=SAS_10.20">re</a>
<a class="l" name="8" href="#8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8&nbsp;</a><b>import</b> <a href="/source/s?defs=string&amp;project=SAS_10.20">string</a>
<a class="l" name="9" href="#9">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9&nbsp;</a><b>import</b> <a href="/source/s?defs=time&amp;project=SAS_10.20">time</a>
<a class="hl" name="10" href="#10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10&nbsp;</a>
<a class="l" name="11" href="#11">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;11&nbsp;</a><b>from</b> <a href="/source/s?defs=commons&amp;project=SAS_10.20">commons</a> <b>import</b> <a href="/source/s?defs=ShortCircuit&amp;project=SAS_10.20">ShortCircuit</a>, <a href="/source/s?defs=RHN_HOSTNAME&amp;project=SAS_10.20">RHN_HOSTNAME</a>, <a href="/source/s?defs=unwrap&amp;project=SAS_10.20">unwrap</a>
<a class="l" name="12" href="#12">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;12&nbsp;</a><b>from</b> <a href="/source/s?defs=redhat_import&amp;project=SAS_10.20">redhat_import</a> <b>import</b> <a href="/source/s?defs=MetaChannel&amp;project=SAS_10.20">MetaChannel</a>, <a href="/source/s?defs=MetaErratum&amp;project=SAS_10.20">MetaErratum</a>, <a href="/source/s?defs=PathDictionary&amp;project=SAS_10.20">PathDictionary</a>, <a href="/source/s?defs=AbstractRedHatDownload&amp;project=SAS_10.20">AbstractRedHatDownload</a>
<a class="l" name="13" href="#13">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13&nbsp;</a><b>from</b> <a href="/source/s?defs=rpm_compare&amp;project=SAS_10.20">rpm_compare</a> <b>import</b> <a href="/source/s?defs=label_compare&amp;project=SAS_10.20">label_compare</a>
<a class="l" name="14" href="#14">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;14&nbsp;</a><b>from</b> <a href="/source/s?defs=config&amp;project=SAS_10.20">config</a> <b>import</b> <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>
<a class="l" name="15" href="#15">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;15&nbsp;</a><b>from</b> <a href="/source/s?defs=cdnrepo&amp;project=SAS_10.20">cdnrepo</a> <b>import</b> <a href="/source/s?defs=RedHatCDNRepo&amp;project=SAS_10.20">RedHatCDNRepo</a>
<a class="l" name="16" href="#16">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;16&nbsp;</a><b>from</b> <a href="/source/s?defs=cdnentitlement&amp;project=SAS_10.20">cdnentitlement</a> <b>import</b> <a href="/source/s?defs=CDNEntitlement&amp;project=SAS_10.20">CDNEntitlement</a>
<a class="l" name="17" href="#17">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;17&nbsp;</a><b>from</b> <a href="/source/s?defs=redhat_import_exceptions&amp;project=SAS_10.20">redhat_import_exceptions</a> <b>import</b> <a href="/source/s?defs=InvalidContentName&amp;project=SAS_10.20">InvalidContentName</a>, <a href="/source/s?defs=RHNDownloadVerificationError&amp;project=SAS_10.20">RHNDownloadVerificationError</a>, <a href="/source/s?defs=Retry&amp;project=SAS_10.20">Retry</a>, <a href="/source/s?defs=retry&amp;project=SAS_10.20">retry</a>, <a href="/source/s?defs=Error&amp;project=SAS_10.20">Error</a>
<a class="l" name="18" href="#18">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;18&nbsp;</a><b>from</b> <a href="/source/s?defs=rhn_logger&amp;project=SAS_10.20">rhn_logger</a> <b>import</b> <a href="/source/s?defs=RHNLogger&amp;project=SAS_10.20">RHNLogger</a>, <a href="/source/s?defs=ProgressBar&amp;project=SAS_10.20">ProgressBar</a>
<a class="l" name="19" href="#19">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;19&nbsp;</a><b>from</b> <a href="/source/s?defs=xmlparser&amp;project=SAS_10.20">xmlparser</a>.<a href="/source/s?defs=repomdparser&amp;project=SAS_10.20">repomdparser</a> <b>import</b> <a href="/source/s?defs=RepomdXMLParser&amp;project=SAS_10.20">RepomdXMLParser</a>
<a class="hl" name="20" href="#20">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;20&nbsp;</a><b>from</b> <a href="/source/s?defs=xmlparser&amp;project=SAS_10.20">xmlparser</a>.<a href="/source/s?defs=primaryparser&amp;project=SAS_10.20">primaryparser</a> <b>import</b> <a href="/source/s?defs=PrimaryXMLParser&amp;project=SAS_10.20">PrimaryXMLParser</a>
<a class="l" name="21" href="#21">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;21&nbsp;</a><b>from</b> <a href="/source/s?defs=xmlparser&amp;project=SAS_10.20">xmlparser</a>.<a href="/source/s?defs=updateinfoparser&amp;project=SAS_10.20">updateinfoparser</a> <b>import</b> <a href="/source/s?defs=UpdateInfoXMLParser&amp;project=SAS_10.20">UpdateInfoXMLParser</a>
<a class="l" name="22" href="#22">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;22&nbsp;</a>
<a class="l" name="23" href="#23">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;23&nbsp;</a><a href="/source/s?defs=log&amp;project=SAS_10.20">log</a> = <a href="/source/s?defs=RHNLogger&amp;project=SAS_10.20">RHNLogger</a>()
<a class="l" name="24" href="#24">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;24&nbsp;</a><a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a> = <a href="/source/s?defs=ShortCircuit&amp;project=SAS_10.20">ShortCircuit</a>()
<a class="l" name="25" href="#25">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;25&nbsp;</a>
<a class="l" name="26" href="#26">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;26&nbsp;</a>
<a class="l" name="27" href="#27">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;27&nbsp;</a><b>class</b> <a href="/source/s?defs=CDNErratum&amp;project=SAS_10.20">CDNErratum</a>(<a href="/source/s?defs=MetaErratum&amp;project=SAS_10.20">MetaErratum</a>):
<a class="l" name="28" href="#28">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;28&nbsp;</a>    <a href="/source/s?defs=__date_pattern&amp;project=SAS_10.20">__date_pattern</a> = <a href="/source/s?defs=re&amp;project=SAS_10.20">re</a>.<a href="/source/s?defs=compile&amp;project=SAS_10.20">compile</a>(<span class="s">"[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+"</span>)
<a class="l" name="29" href="#29">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;29&nbsp;</a>
<a class="hl" name="30" href="#30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;30&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>, <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>):
<a class="l" name="31" href="#31">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;31&nbsp;</a>        <a href="/source/s?defs=super&amp;project=SAS_10.20">super</a>(<a href="/source/s?defs=CDNErratum&amp;project=SAS_10.20">CDNErratum</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>).<a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>, {})
<a class="l" name="32" href="#32">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;32&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_advisory'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'id'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="33" href="#33">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;33&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_synopsis'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'title'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="34" href="#34">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;34&nbsp;</a>
<a class="l" name="35" href="#35">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;35&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_topic'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'summary'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="36" href="#36">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;36&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_update_date'</span>] = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_custom_date_format&amp;project=SAS_10.20">__get_custom_date_format</a>(<a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'updated'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'date'</span>))
<a class="l" name="37" href="#37">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;37&nbsp;</a>        <span class="c"># doesn't have a last_modified_date tag.</span>
<a class="l" name="38" href="#38">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;38&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_last_modified_date'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'updated'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'date'</span>)
<a class="l" name="39" href="#39">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;39&nbsp;</a>
<a class="hl" name="40" href="#40">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;40&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_issue_date'</span>] = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_custom_date_format&amp;project=SAS_10.20">__get_custom_date_format</a>(<a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'issued'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'date'</span>))
<a class="l" name="41" href="#41">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;41&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_description'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'description'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="42" href="#42">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;42&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'packages'</span>] = []
<a class="l" name="43" href="#43">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;43&nbsp;</a>
<a class="l" name="44" href="#44">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;44&nbsp;</a>        <a href="/source/s?defs=erratum_type&amp;project=SAS_10.20">erratum_type</a> = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>[<span class="s">'type'</span>]
<a class="l" name="45" href="#45">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;45&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_advisory_type'</span>] = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_errata_advisory_type&amp;project=SAS_10.20">__get_errata_advisory_type</a>(<a href="/source/s?defs=erratum_type&amp;project=SAS_10.20">erratum_type</a>)
<a class="l" name="46" href="#46">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;46&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'copyright'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'rights'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="47" href="#47">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;47&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'solution'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'solution'</span>).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="48" href="#48">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;48&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'severity'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'severity'</span>, {}).<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'value'</span>)
<a class="l" name="49" href="#49">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;49&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'version'</span>] = <a href="/source/s?defs=erratum_dict&amp;project=SAS_10.20">erratum_dict</a>[<span class="s">'version'</span>]
<a class="hl" name="50" href="#50">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;50&nbsp;</a>
<a class="l" name="51" href="#51">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;51&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'errata_url'</span>] = <span class="s">"<a href="http://%s/errata/%s.html">http://%s/errata/%s.html</a>"</span> % (<a href="/source/s?defs=RHN_HOSTNAME&amp;project=SAS_10.20">RHN_HOSTNAME</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=errata_advisory&amp;project=SAS_10.20">errata_advisory</a>.<a href="/source/s?defs=replace&amp;project=SAS_10.20">replace</a>(<span class="s">':'</span>, <span class="s">'-'</span>))
<a class="l" name="52" href="#52">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;52&nbsp;</a>
<a class="l" name="53" href="#53">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;53&nbsp;</a>    <b>def</b> <a href="/source/s?defs=list_packages&amp;project=SAS_10.20">list_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=channel&amp;project=SAS_10.20">channel</a>):
<a class="l" name="54" href="#54">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;54&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<span class="s">'packages'</span>]
<a class="l" name="55" href="#55">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;55&nbsp;</a>
<a class="l" name="56" href="#56">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;56&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_details&amp;project=SAS_10.20">get_details</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="57" href="#57">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;57&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>
<a class="l" name="58" href="#58">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;58&nbsp;</a>
<a class="l" name="59" href="#59">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;59&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_policy_description&amp;project=SAS_10.20">get_policy_description</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="hl" name="60" href="#60">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;60&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = <span class="s">'''$errata_synopsis
<a class="l" name="61" href="#61">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;61&nbsp;</a>        $errata_url
<a class="l" name="62" href="#62">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;62&nbsp;</a>
<a class="l" name="63" href="#63">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;63&nbsp;</a>        Issued: $errata_issue_date
<a class="l" name="64" href="#64">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;64&nbsp;</a>        Updated: $errata_update_date
<a class="l" name="65" href="#65">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;65&nbsp;</a>
<a class="l" name="66" href="#66">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;66&nbsp;</a>        $errata_topic
<a class="l" name="67" href="#67">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;67&nbsp;</a>
<a class="l" name="68" href="#68">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;68&nbsp;</a>        $errata_description'''</span>
<a class="l" name="69" href="#69">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;69&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = <span class="s">'\n'</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>([<a href="/source/s?defs=line&amp;project=SAS_10.20">line</a>.<a href="/source/s?defs=strip&amp;project=SAS_10.20">strip</a>() <b>for</b> <a href="/source/s?defs=line&amp;project=SAS_10.20">line</a> <b>in</b> <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>.<a href="/source/s?defs=splitlines&amp;project=SAS_10.20">splitlines</a>()])
<a class="hl" name="70" href="#70">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;70&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = <a href="/source/s?defs=string&amp;project=SAS_10.20">string</a>.<a href="/source/s?defs=Template&amp;project=SAS_10.20">Template</a>(<a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>)
<a class="l" name="71" href="#71">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;71&nbsp;</a>        <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a> = {}
<a class="l" name="72" href="#72">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;72&nbsp;</a>
<a class="l" name="73" href="#73">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;73&nbsp;</a>        <b>for</b> <a href="/source/s?defs=key&amp;project=SAS_10.20">key</a> <b>in</b> [<span class="s">'errata_synopsis'</span>, <span class="s">'errata_url'</span>, <span class="s">'errata_issue_date'</span>, <span class="s">'errata_update_date'</span>, <span class="s">'errata_topic'</span>,
<a class="l" name="74" href="#74">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;74&nbsp;</a>                    <span class="s">'errata_description'</span>]:
<a class="l" name="75" href="#75">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;75&nbsp;</a>            <b>try</b>:
<a class="l" name="76" href="#76">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;76&nbsp;</a>                <b>if</b> <a href="/source/s?defs=key&amp;project=SAS_10.20">key</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>:
<a class="l" name="77" href="#77">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;77&nbsp;</a>                    <b>if</b> <a href="/source/s?defs=key&amp;project=SAS_10.20">key</a> <b>in</b> (<span class="s">'errata_topic'</span>, <span class="s">'errata_description'</span>):
<a class="l" name="78" href="#78">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;78&nbsp;</a>                        <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a> = <a href="/source/s?defs=unwrap&amp;project=SAS_10.20">unwrap</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>])
<a class="l" name="79" href="#79">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;79&nbsp;</a>                    <b>else</b>:
<a class="hl" name="80" href="#80">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;80&nbsp;</a>                        <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>]
<a class="l" name="81" href="#81">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;81&nbsp;</a>                    <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>[<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>] = <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a>
<a class="l" name="82" href="#82">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;82&nbsp;</a>                <b>else</b>:
<a class="l" name="83" href="#83">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;83&nbsp;</a>                    <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>[<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>] = <span class="s">"%s not found in Red Hat API results."</span> % <a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>
<a class="l" name="84" href="#84">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;84&nbsp;</a>            <b>except</b> <a href="/source/s?defs=KeyError&amp;project=SAS_10.20">KeyError</a>:
<a class="l" name="85" href="#85">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;85&nbsp;</a>                <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>[<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>] = <span class="s">"%s not found in rhn_import lookup table."</span> % <a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>
<a class="l" name="86" href="#86">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;86&nbsp;</a>        <b>return</b> <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>.<a href="/source/s?defs=safe_substitute&amp;project=SAS_10.20">safe_substitute</a>(<a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>)
<a class="l" name="87" href="#87">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;87&nbsp;</a>
<a class="l" name="88" href="#88">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;88&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="89" href="#89">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;89&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_custom_date_format&amp;project=SAS_10.20">__get_custom_date_format</a>(<a href="/source/s?defs=iso8601_date&amp;project=SAS_10.20">iso8601_date</a>):
<a class="hl" name="90" href="#90">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;90&nbsp;</a>        <span class="s">"""
<a class="l" name="91" href="#91">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;91&nbsp;</a>        Parses a date string in a custom ISO 8601 format (i.e: "%Y-%m-%d %H:%M:%S") and returns a string date
<a class="l" name="92" href="#92">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;92&nbsp;</a>        in simple format like: %d/%m/%y
<a class="l" name="93" href="#93">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;93&nbsp;</a>
<a class="l" name="94" href="#94">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;94&nbsp;</a>        :param iso8601_date: a string date like "%Y-%m-%d %H:%M:%S"
<a class="l" name="95" href="#95">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;95&nbsp;</a>        :return: a date string like %d/%m/%y where leading zeros from day and month are stripped. If input date
<a class="l" name="96" href="#96">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;96&nbsp;</a>        does not match the format "%Y-%m-%d %H:%M:%S" then the raw input is returned
<a class="l" name="97" href="#97">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;97&nbsp;</a>        """</span>
<a class="l" name="98" href="#98">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;98&nbsp;</a>        <b>if</b> <a href="/source/s?defs=CDNErratum&amp;project=SAS_10.20">CDNErratum</a>.<a href="/source/s?defs=__date_pattern&amp;project=SAS_10.20">__date_pattern</a>.<a href="/source/s?defs=match&amp;project=SAS_10.20">match</a>(<a href="/source/s?defs=iso8601_date&amp;project=SAS_10.20">iso8601_date</a>):
<a class="l" name="99" href="#99">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;99&nbsp;</a>            <a href="/source/s?defs=date_time&amp;project=SAS_10.20">date_time</a> = <a href="/source/s?defs=datetime&amp;project=SAS_10.20">datetime</a>.<a href="/source/s?defs=datetime&amp;project=SAS_10.20">datetime</a>(*<a href="/source/s?defs=time&amp;project=SAS_10.20">time</a>.<a href="/source/s?defs=strptime&amp;project=SAS_10.20">strptime</a>(<a href="/source/s?defs=iso8601_date&amp;project=SAS_10.20">iso8601_date</a>, <span class="s">"%Y-%m-%d %H:%M:%S"</span>)[:<span class="n">6</span>])
<a class="hl" name="100" href="#100">&nbsp;&nbsp;&nbsp;&nbsp;100&nbsp;</a>            <b>return</b> <span class="s">"%s/%s/%s"</span> % (<a href="/source/s?defs=date_time&amp;project=SAS_10.20">date_time</a>.<a href="/source/s?defs=day&amp;project=SAS_10.20">day</a>, <a href="/source/s?defs=date_time&amp;project=SAS_10.20">date_time</a>.<a href="/source/s?defs=month&amp;project=SAS_10.20">month</a>, <a href="/source/s?defs=date_time&amp;project=SAS_10.20">date_time</a>.<a href="/source/s?defs=strftime&amp;project=SAS_10.20">strftime</a>(<span class="s">"%y"</span>))
<a class="l" name="101" href="#101">&nbsp;&nbsp;&nbsp;&nbsp;101&nbsp;</a>        <b>return</b> <a href="/source/s?defs=iso8601_date&amp;project=SAS_10.20">iso8601_date</a>
<a class="l" name="102" href="#102">&nbsp;&nbsp;&nbsp;&nbsp;102&nbsp;</a>
<a class="l" name="103" href="#103">&nbsp;&nbsp;&nbsp;&nbsp;103&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="104" href="#104">&nbsp;&nbsp;&nbsp;&nbsp;104&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_errata_advisory_type&amp;project=SAS_10.20">__get_errata_advisory_type</a>(<a href="/source/s?defs=erratum_type&amp;project=SAS_10.20">erratum_type</a>):
<a class="l" name="105" href="#105">&nbsp;&nbsp;&nbsp;&nbsp;105&nbsp;</a>        <a href="/source/s?defs=lookup&amp;project=SAS_10.20">lookup</a> = {<span class="s">'security'</span>: <span class="s">'Security Advisory'</span>,
<a class="l" name="106" href="#106">&nbsp;&nbsp;&nbsp;&nbsp;106&nbsp;</a>                  <span class="s">'bugfix'</span>: <span class="s">'Bug Fix Advisory'</span>,
<a class="l" name="107" href="#107">&nbsp;&nbsp;&nbsp;&nbsp;107&nbsp;</a>                  <span class="s">'enhancement'</span>: <span class="s">'Product Enhancement Advisory'</span>}
<a class="l" name="108" href="#108">&nbsp;&nbsp;&nbsp;&nbsp;108&nbsp;</a>        <b>return</b> <a href="/source/s?defs=lookup&amp;project=SAS_10.20">lookup</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=erratum_type&amp;project=SAS_10.20">erratum_type</a>, <a href="/source/s?defs=erratum_type&amp;project=SAS_10.20">erratum_type</a>)
<a class="l" name="109" href="#109">&nbsp;&nbsp;&nbsp;&nbsp;109&nbsp;</a>
<a class="hl" name="110" href="#110">&nbsp;&nbsp;&nbsp;&nbsp;110&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__getattr__&amp;project=SAS_10.20">__getattr__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>):
<a class="l" name="111" href="#111">&nbsp;&nbsp;&nbsp;&nbsp;111&nbsp;</a>        <span class="c"># pass through access to dict items</span>
<a class="l" name="112" href="#112">&nbsp;&nbsp;&nbsp;&nbsp;112&nbsp;</a>        <b>try</b>:
<a class="l" name="113" href="#113">&nbsp;&nbsp;&nbsp;&nbsp;113&nbsp;</a>            <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>]
<a class="l" name="114" href="#114">&nbsp;&nbsp;&nbsp;&nbsp;114&nbsp;</a>        <b>except</b> <a href="/source/s?defs=KeyError&amp;project=SAS_10.20">KeyError</a>:
<a class="l" name="115" href="#115">&nbsp;&nbsp;&nbsp;&nbsp;115&nbsp;</a>            <b>raise</b> <a href="/source/s?defs=AttributeError&amp;project=SAS_10.20">AttributeError</a>(<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>)
<a class="l" name="116" href="#116">&nbsp;&nbsp;&nbsp;&nbsp;116&nbsp;</a>
<a class="l" name="117" href="#117">&nbsp;&nbsp;&nbsp;&nbsp;117&nbsp;</a>
<a class="l" name="118" href="#118">&nbsp;&nbsp;&nbsp;&nbsp;118&nbsp;</a><b>class</b> <a href="/source/s?defs=CDNPackage&amp;project=SAS_10.20">CDNPackage</a>(<a href="/source/s?defs=dict&amp;project=SAS_10.20">dict</a>):
<a class="l" name="119" href="#119">&nbsp;&nbsp;&nbsp;&nbsp;119&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>, <a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>):
<a class="hl" name="120" href="#120">&nbsp;&nbsp;&nbsp;&nbsp;120&nbsp;</a>        <span class="s">"""
<a class="l" name="121" href="#121">&nbsp;&nbsp;&nbsp;&nbsp;121&nbsp;</a>        Creates a package instance wrapper around &lt;package&gt; tags from <a href="/source/s?path=primary.xml&amp;project=SAS_10.20">primary.xml</a>
<a class="l" name="122" href="#122">&nbsp;&nbsp;&nbsp;&nbsp;122&nbsp;</a>        """</span>
<a class="l" name="123" href="#123">&nbsp;&nbsp;&nbsp;&nbsp;123&nbsp;</a>        <a href="/source/s?defs=super&amp;project=SAS_10.20">super</a>(<a href="/source/s?defs=CDNPackage&amp;project=SAS_10.20">CDNPackage</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>).<a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>()
<a class="l" name="124" href="#124">&nbsp;&nbsp;&nbsp;&nbsp;124&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"name"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"value"</span>)
<a class="l" name="125" href="#125">&nbsp;&nbsp;&nbsp;&nbsp;125&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=arch&amp;project=SAS_10.20">arch</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"arch"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"value"</span>)
<a class="l" name="126" href="#126">&nbsp;&nbsp;&nbsp;&nbsp;126&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=summary&amp;project=SAS_10.20">summary</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"summary"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"value"</span>)
<a class="l" name="127" href="#127">&nbsp;&nbsp;&nbsp;&nbsp;127&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=description&amp;project=SAS_10.20">description</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"description"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"value"</span>)
<a class="l" name="128" href="#128">&nbsp;&nbsp;&nbsp;&nbsp;128&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"version"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"ver"</span>)
<a class="l" name="129" href="#129">&nbsp;&nbsp;&nbsp;&nbsp;129&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"version"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"rel"</span>)
<a class="hl" name="130" href="#130">&nbsp;&nbsp;&nbsp;&nbsp;130&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=epoch&amp;project=SAS_10.20">epoch</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"version"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"epoch"</span>)
<a class="l" name="131" href="#131">&nbsp;&nbsp;&nbsp;&nbsp;131&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=checksum_type&amp;project=SAS_10.20">checksum_type</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"checksum"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"type"</span>)
<a class="l" name="132" href="#132">&nbsp;&nbsp;&nbsp;&nbsp;132&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=checksum&amp;project=SAS_10.20">checksum</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"checksum"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"value"</span>)
<a class="l" name="133" href="#133">&nbsp;&nbsp;&nbsp;&nbsp;133&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=location&amp;project=SAS_10.20">location</a> = <a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"location"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"href"</span>)
<a class="l" name="134" href="#134">&nbsp;&nbsp;&nbsp;&nbsp;134&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=package_size&amp;project=SAS_10.20">package_size</a> = <a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"size"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"package"</span>))
<a class="l" name="135" href="#135">&nbsp;&nbsp;&nbsp;&nbsp;135&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=installed_size&amp;project=SAS_10.20">installed_size</a> = <a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"size"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"installed"</span>))
<a class="l" name="136" href="#136">&nbsp;&nbsp;&nbsp;&nbsp;136&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=archive_size&amp;project=SAS_10.20">archive_size</a> = <a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=package_dict&amp;project=SAS_10.20">package_dict</a>[<span class="s">"size"</span>].<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"archive"</span>))
<a class="l" name="137" href="#137">&nbsp;&nbsp;&nbsp;&nbsp;137&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a> = <b>None</b>
<a class="l" name="138" href="#138">&nbsp;&nbsp;&nbsp;&nbsp;138&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a> = <a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>
<a class="l" name="139" href="#139">&nbsp;&nbsp;&nbsp;&nbsp;139&nbsp;</a>
<a class="hl" name="140" href="#140">&nbsp;&nbsp;&nbsp;&nbsp;140&nbsp;</a>        <span class="c"># the nevra format</span>
<a class="l" name="141" href="#141">&nbsp;&nbsp;&nbsp;&nbsp;141&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=uid&amp;project=SAS_10.20">uid</a> = <span class="s">"{0}{1}{2}{3}{4}{5}{6}{7}{8}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=epoch&amp;project=SAS_10.20">epoch</a>, <span class="s">':'</span>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <span class="s">'-'</span>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a>, <span class="s">'-'</span>,
<a class="l" name="142" href="#142">&nbsp;&nbsp;&nbsp;&nbsp;142&nbsp;</a>                                                        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a>, <span class="s">'.'</span>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=arch&amp;project=SAS_10.20">arch</a>)
<a class="l" name="143" href="#143">&nbsp;&nbsp;&nbsp;&nbsp;143&nbsp;</a>
<a class="l" name="144" href="#144">&nbsp;&nbsp;&nbsp;&nbsp;144&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="145" href="#145">&nbsp;&nbsp;&nbsp;&nbsp;145&nbsp;</a>    <b>def</b> <a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="146" href="#146">&nbsp;&nbsp;&nbsp;&nbsp;146&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a>
<a class="l" name="147" href="#147">&nbsp;&nbsp;&nbsp;&nbsp;147&nbsp;</a>
<a class="l" name="148" href="#148">&nbsp;&nbsp;&nbsp;&nbsp;148&nbsp;</a>    @<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>.<a href="/source/s?defs=setter&amp;project=SAS_10.20">setter</a>
<a class="l" name="149" href="#149">&nbsp;&nbsp;&nbsp;&nbsp;149&nbsp;</a>    <b>def</b> <a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a>):
<a class="hl" name="150" href="#150">&nbsp;&nbsp;&nbsp;&nbsp;150&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a> = <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a>
<a class="l" name="151" href="#151">&nbsp;&nbsp;&nbsp;&nbsp;151&nbsp;</a>
<a class="l" name="152" href="#152">&nbsp;&nbsp;&nbsp;&nbsp;152&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="153" href="#153">&nbsp;&nbsp;&nbsp;&nbsp;153&nbsp;</a>    <b>def</b> <a href="/source/s?defs=nevra&amp;project=SAS_10.20">nevra</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="154" href="#154">&nbsp;&nbsp;&nbsp;&nbsp;154&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=epoch&amp;project=SAS_10.20">epoch</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=arch&amp;project=SAS_10.20">arch</a>
<a class="l" name="155" href="#155">&nbsp;&nbsp;&nbsp;&nbsp;155&nbsp;</a>
<a class="l" name="156" href="#156">&nbsp;&nbsp;&nbsp;&nbsp;156&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_details&amp;project=SAS_10.20">get_details</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="157" href="#157">&nbsp;&nbsp;&nbsp;&nbsp;157&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>
<a class="l" name="158" href="#158">&nbsp;&nbsp;&nbsp;&nbsp;158&nbsp;</a>
<a class="l" name="159" href="#159">&nbsp;&nbsp;&nbsp;&nbsp;159&nbsp;</a>    <b>def</b> <a href="/source/s?defs=do_import&amp;project=SAS_10.20">do_import</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=folder_id&amp;project=SAS_10.20">folder_id</a>, <a href="/source/s?defs=platform_id&amp;project=SAS_10.20">platform_id</a>):
<a class="hl" name="160" href="#160">&nbsp;&nbsp;&nbsp;&nbsp;160&nbsp;</a>        <span class="s">"""
<a class="l" name="161" href="#161">&nbsp;&nbsp;&nbsp;&nbsp;161&nbsp;</a>        Downloads RPM package from CDN and uploads to HPSA library folder.
<a class="l" name="162" href="#162">&nbsp;&nbsp;&nbsp;&nbsp;162&nbsp;</a>        """</span>
<a class="l" name="163" href="#163">&nbsp;&nbsp;&nbsp;&nbsp;163&nbsp;</a>        <a href="/source/s?defs=progress_bar&amp;project=SAS_10.20">progress_bar</a> = <a href="/source/s?defs=ProgressBar&amp;project=SAS_10.20">ProgressBar</a>(<a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=package_size&amp;project=SAS_10.20">package_size</a>))
<a class="l" name="164" href="#164">&nbsp;&nbsp;&nbsp;&nbsp;164&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>.<a href="/source/s?defs=rhd&amp;project=SAS_10.20">rhd</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>
<a class="l" name="165" href="#165">&nbsp;&nbsp;&nbsp;&nbsp;165&nbsp;</a>
<a class="l" name="166" href="#166">&nbsp;&nbsp;&nbsp;&nbsp;166&nbsp;</a>        <b>def</b> <a href="/source/s?defs=retryfunc&amp;project=SAS_10.20">retryfunc</a>():
<a class="l" name="167" href="#167">&nbsp;&nbsp;&nbsp;&nbsp;167&nbsp;</a>            <b>try</b>:
<a class="l" name="168" href="#168">&nbsp;&nbsp;&nbsp;&nbsp;168&nbsp;</a>                <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>.<a href="/source/s?defs=rhd&amp;project=SAS_10.20">rhd</a>.<a href="/source/s?defs=get_package&amp;project=SAS_10.20">get_package</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=location&amp;project=SAS_10.20">location</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=location&amp;project=SAS_10.20">location</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=package_size&amp;project=SAS_10.20">package_size</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=checksum&amp;project=SAS_10.20">checksum</a>,
<a class="l" name="169" href="#169">&nbsp;&nbsp;&nbsp;&nbsp;169&nbsp;</a>                                                  <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=checksum_type&amp;project=SAS_10.20">checksum_type</a>,
<a class="hl" name="170" href="#170">&nbsp;&nbsp;&nbsp;&nbsp;170&nbsp;</a>                                                  <a href="/source/s?defs=progress_bar&amp;project=SAS_10.20">progress_bar</a>)
<a class="l" name="171" href="#171">&nbsp;&nbsp;&nbsp;&nbsp;171&nbsp;</a>            <b>except</b> <a href="/source/s?defs=RHNDownloadVerificationError&amp;project=SAS_10.20">RHNDownloadVerificationError</a>:
<a class="l" name="172" href="#172">&nbsp;&nbsp;&nbsp;&nbsp;172&nbsp;</a>                <a href="/source/s?defs=progress_bar&amp;project=SAS_10.20">progress_bar</a>.<a href="/source/s?defs=reset&amp;project=SAS_10.20">reset</a>()
<a class="l" name="173" href="#173">&nbsp;&nbsp;&nbsp;&nbsp;173&nbsp;</a>                <b>raise</b> <a href="/source/s?defs=Retry&amp;project=SAS_10.20">Retry</a>
<a class="l" name="174" href="#174">&nbsp;&nbsp;&nbsp;&nbsp;174&nbsp;</a>
<a class="l" name="175" href="#175">&nbsp;&nbsp;&nbsp;&nbsp;175&nbsp;</a>        <b>try</b>:
<a class="l" name="176" href="#176">&nbsp;&nbsp;&nbsp;&nbsp;176&nbsp;</a>            <a href="/source/s?defs=file_path&amp;project=SAS_10.20">file_path</a> = <a href="/source/s?defs=retry&amp;project=SAS_10.20">retry</a>(<a href="/source/s?defs=retryfunc&amp;project=SAS_10.20">retryfunc</a>)
<a class="l" name="177" href="#177">&nbsp;&nbsp;&nbsp;&nbsp;177&nbsp;</a>        <b>finally</b>:
<a class="l" name="178" href="#178">&nbsp;&nbsp;&nbsp;&nbsp;178&nbsp;</a>            <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>.<a href="/source/s?defs=rhd&amp;project=SAS_10.20">rhd</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a> = <b>None</b>
<a class="l" name="179" href="#179">&nbsp;&nbsp;&nbsp;&nbsp;179&nbsp;</a>        <a href="/source/s?defs=progress_bar&amp;project=SAS_10.20">progress_bar</a>.<a href="/source/s?defs=status&amp;project=SAS_10.20">status</a>(<span class="s">"Copying package to library..."</span>)
<a class="hl" name="180" href="#180">&nbsp;&nbsp;&nbsp;&nbsp;180&nbsp;</a>        <a href="/source/s?defs=unit_id&amp;project=SAS_10.20">unit_id</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>.<a href="/source/s?defs=word&amp;project=SAS_10.20">word</a>.<a href="/source/s?defs=upload&amp;project=SAS_10.20">upload</a>(<a href="/source/s?defs=file_path&amp;project=SAS_10.20">file_path</a>, <a href="/source/s?defs=folder_id&amp;project=SAS_10.20">folder_id</a>, <a href="/source/s?defs=platform_id&amp;project=SAS_10.20">platform_id</a>)
<a class="l" name="181" href="#181">&nbsp;&nbsp;&nbsp;&nbsp;181&nbsp;</a>        <a href="/source/s?defs=progress_bar&amp;project=SAS_10.20">progress_bar</a>.<a href="/source/s?defs=status&amp;project=SAS_10.20">status</a>()
<a class="l" name="182" href="#182">&nbsp;&nbsp;&nbsp;&nbsp;182&nbsp;</a>        <b>return</b> <a href="/source/s?defs=unit_id&amp;project=SAS_10.20">unit_id</a>
<a class="l" name="183" href="#183">&nbsp;&nbsp;&nbsp;&nbsp;183&nbsp;</a>
<a class="l" name="184" href="#184">&nbsp;&nbsp;&nbsp;&nbsp;184&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__str__&amp;project=SAS_10.20">__str__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="185" href="#185">&nbsp;&nbsp;&nbsp;&nbsp;185&nbsp;</a>        <a href="/source/s?defs=raw_string&amp;project=SAS_10.20">raw_string</a> = <span class="s">"{0}-{1}-{2}.{3}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=arch&amp;project=SAS_10.20">arch</a>)
<a class="l" name="186" href="#186">&nbsp;&nbsp;&nbsp;&nbsp;186&nbsp;</a>        <b>return</b> <a href="/source/s?defs=raw_string&amp;project=SAS_10.20">raw_string</a>.<a href="/source/s?defs=encode&amp;project=SAS_10.20">encode</a>(<span class="s">'utf-8'</span>).<a href="/source/s?defs=strip&amp;project=SAS_10.20">strip</a>()
<a class="l" name="187" href="#187">&nbsp;&nbsp;&nbsp;&nbsp;187&nbsp;</a>
<a class="l" name="188" href="#188">&nbsp;&nbsp;&nbsp;&nbsp;188&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__cmp__&amp;project=SAS_10.20">__cmp__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>):
<a class="l" name="189" href="#189">&nbsp;&nbsp;&nbsp;&nbsp;189&nbsp;</a>        <b>if</b> <a href="/source/s?defs=isinstance&amp;project=SAS_10.20">isinstance</a>(<a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>, <a href="/source/s?defs=CDNPackage&amp;project=SAS_10.20">CDNPackage</a>):
<a class="hl" name="190" href="#190">&nbsp;&nbsp;&nbsp;&nbsp;190&nbsp;</a>            <a href="/source/s?defs=epoch_tuple&amp;project=SAS_10.20">epoch_tuple</a> = (<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=epoch&amp;project=SAS_10.20">epoch</a>, <a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>.<a href="/source/s?defs=epoch&amp;project=SAS_10.20">epoch</a>)
<a class="l" name="191" href="#191">&nbsp;&nbsp;&nbsp;&nbsp;191&nbsp;</a>            <a href="/source/s?defs=version_tuple&amp;project=SAS_10.20">version_tuple</a> = (<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a>, <a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>.<a href="/source/s?defs=version&amp;project=SAS_10.20">version</a>)
<a class="l" name="192" href="#192">&nbsp;&nbsp;&nbsp;&nbsp;192&nbsp;</a>            <a href="/source/s?defs=release_tuple&amp;project=SAS_10.20">release_tuple</a> = (<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a>, <a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>.<a href="/source/s?defs=release&amp;project=SAS_10.20">release</a>)
<a class="l" name="193" href="#193">&nbsp;&nbsp;&nbsp;&nbsp;193&nbsp;</a>            <b>return</b> <a href="/source/s?defs=label_compare&amp;project=SAS_10.20">label_compare</a>(<a href="/source/s?defs=epoch_tuple&amp;project=SAS_10.20">epoch_tuple</a>, <a href="/source/s?defs=version_tuple&amp;project=SAS_10.20">version_tuple</a>, <a href="/source/s?defs=release_tuple&amp;project=SAS_10.20">release_tuple</a>)
<a class="l" name="194" href="#194">&nbsp;&nbsp;&nbsp;&nbsp;194&nbsp;</a>        <b>else</b>:
<a class="l" name="195" href="#195">&nbsp;&nbsp;&nbsp;&nbsp;195&nbsp;</a>            <b>return</b> <a href="/source/s?defs=cmp&amp;project=SAS_10.20">cmp</a>(<a href="/source/s?defs=id&amp;project=SAS_10.20">id</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>), <a href="/source/s?defs=id&amp;project=SAS_10.20">id</a>(<a href="/source/s?defs=other&amp;project=SAS_10.20">other</a>))
<a class="l" name="196" href="#196">&nbsp;&nbsp;&nbsp;&nbsp;196&nbsp;</a>
<a class="l" name="197" href="#197">&nbsp;&nbsp;&nbsp;&nbsp;197&nbsp;</a>
<a class="l" name="198" href="#198">&nbsp;&nbsp;&nbsp;&nbsp;198&nbsp;</a><b>class</b> <a href="/source/s?defs=CDNContent&amp;project=SAS_10.20">CDNContent</a>(<a href="/source/s?defs=MetaChannel&amp;project=SAS_10.20">MetaChannel</a>):
<a class="l" name="199" href="#199">&nbsp;&nbsp;&nbsp;&nbsp;199&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>, <a href="/source/s?defs=platform_id&amp;project=SAS_10.20">platform_id</a>, <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>, <a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>):
<a class="hl" name="200" href="#200">&nbsp;&nbsp;&nbsp;&nbsp;200&nbsp;</a>        <a href="/source/s?defs=super&amp;project=SAS_10.20">super</a>(<a href="/source/s?defs=CDNContent&amp;project=SAS_10.20">CDNContent</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>).<a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <a href="/source/s?defs=platform_id&amp;project=SAS_10.20">platform_id</a>, <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>)
<a class="l" name="201" href="#201">&nbsp;&nbsp;&nbsp;&nbsp;201&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content&amp;project=SAS_10.20">__content</a> = <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>
<a class="l" name="202" href="#202">&nbsp;&nbsp;&nbsp;&nbsp;202&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__guide&amp;project=SAS_10.20">__guide</a> = <a href="/source/s?defs=guide&amp;project=SAS_10.20">guide</a>
<a class="l" name="203" href="#203">&nbsp;&nbsp;&nbsp;&nbsp;203&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a> = <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>
<a class="l" name="204" href="#204">&nbsp;&nbsp;&nbsp;&nbsp;204&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a> = <b>None</b>
<a class="l" name="205" href="#205">&nbsp;&nbsp;&nbsp;&nbsp;205&nbsp;</a>
<a class="l" name="206" href="#206">&nbsp;&nbsp;&nbsp;&nbsp;206&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_policy_description&amp;project=SAS_10.20">get_policy_description</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="207" href="#207">&nbsp;&nbsp;&nbsp;&nbsp;207&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = \
<a class="l" name="208" href="#208">&nbsp;&nbsp;&nbsp;&nbsp;208&nbsp;</a>            <span class="s">'''Summary: $content_summary
<a class="l" name="209" href="#209">&nbsp;&nbsp;&nbsp;&nbsp;209&nbsp;</a>
<a class="hl" name="210" href="#210">&nbsp;&nbsp;&nbsp;&nbsp;210&nbsp;</a>            Label: $label'''</span>
<a class="l" name="211" href="#211">&nbsp;&nbsp;&nbsp;&nbsp;211&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = <span class="s">'\n'</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>([<a href="/source/s?defs=line&amp;project=SAS_10.20">line</a>.<a href="/source/s?defs=strip&amp;project=SAS_10.20">strip</a>() <b>for</b> <a href="/source/s?defs=line&amp;project=SAS_10.20">line</a> <b>in</b> <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>.<a href="/source/s?defs=splitlines&amp;project=SAS_10.20">splitlines</a>()])
<a class="l" name="212" href="#212">&nbsp;&nbsp;&nbsp;&nbsp;212&nbsp;</a>        <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a> = <a href="/source/s?defs=string&amp;project=SAS_10.20">string</a>.<a href="/source/s?defs=Template&amp;project=SAS_10.20">Template</a>(<a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>)
<a class="l" name="213" href="#213">&nbsp;&nbsp;&nbsp;&nbsp;213&nbsp;</a>        <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_details&amp;project=SAS_10.20">__get_details</a>()
<a class="l" name="214" href="#214">&nbsp;&nbsp;&nbsp;&nbsp;214&nbsp;</a>
<a class="l" name="215" href="#215">&nbsp;&nbsp;&nbsp;&nbsp;215&nbsp;</a>        <b>return</b> <a href="/source/s?defs=template&amp;project=SAS_10.20">template</a>.<a href="/source/s?defs=safe_substitute&amp;project=SAS_10.20">safe_substitute</a>(<a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>)
<a class="l" name="216" href="#216">&nbsp;&nbsp;&nbsp;&nbsp;216&nbsp;</a>
<a class="l" name="217" href="#217">&nbsp;&nbsp;&nbsp;&nbsp;217&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_path_dict&amp;project=SAS_10.20">get_path_dict</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="218" href="#218">&nbsp;&nbsp;&nbsp;&nbsp;218&nbsp;</a>        <b>return</b> <a href="/source/s?defs=PathDictionary&amp;project=SAS_10.20">PathDictionary</a>(
<a class="l" name="219" href="#219">&nbsp;&nbsp;&nbsp;&nbsp;219&nbsp;</a>            <a href="/source/s?defs=opsware_platform&amp;project=SAS_10.20">opsware_platform</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>,
<a class="hl" name="220" href="#220">&nbsp;&nbsp;&nbsp;&nbsp;220&nbsp;</a>            <a href="/source/s?defs=channel_name&amp;project=SAS_10.20">channel_name</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>,
<a class="l" name="221" href="#221">&nbsp;&nbsp;&nbsp;&nbsp;221&nbsp;</a>            <a href="/source/s?defs=channel_label&amp;project=SAS_10.20">channel_label</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>,
<a class="l" name="222" href="#222">&nbsp;&nbsp;&nbsp;&nbsp;222&nbsp;</a>            <a href="/source/s?defs=content_name&amp;project=SAS_10.20">content_name</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a> + <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_get_content_name_suffix&amp;project=SAS_10.20">_get_content_name_suffix</a>())
<a class="l" name="223" href="#223">&nbsp;&nbsp;&nbsp;&nbsp;223&nbsp;</a>
<a class="l" name="224" href="#224">&nbsp;&nbsp;&nbsp;&nbsp;224&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_details&amp;project=SAS_10.20">__get_details</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="225" href="#225">&nbsp;&nbsp;&nbsp;&nbsp;225&nbsp;</a>        <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a> = {<span class="s">"label"</span>: <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <span class="s">'content_summary'</span>: <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>}
<a class="l" name="226" href="#226">&nbsp;&nbsp;&nbsp;&nbsp;226&nbsp;</a>        <b>return</b> <a href="/source/s?defs=details&amp;project=SAS_10.20">details</a>
<a class="l" name="227" href="#227">&nbsp;&nbsp;&nbsp;&nbsp;227&nbsp;</a>
<a class="l" name="228" href="#228">&nbsp;&nbsp;&nbsp;&nbsp;228&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_get_content_name_suffix&amp;project=SAS_10.20">_get_content_name_suffix</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="229" href="#229">&nbsp;&nbsp;&nbsp;&nbsp;229&nbsp;</a>        <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> = <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>)
<a class="hl" name="230" href="#230">&nbsp;&nbsp;&nbsp;&nbsp;230&nbsp;</a>        <a href="/source/s?defs=url_vars&amp;project=SAS_10.20">url_vars</a> = <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_content_url_vars&amp;project=SAS_10.20">get_content_url_vars</a>()
<a class="l" name="231" href="#231">&nbsp;&nbsp;&nbsp;&nbsp;231&nbsp;</a>        <b>if</b> <a href="/source/s?defs=url_vars&amp;project=SAS_10.20">url_vars</a>:
<a class="l" name="232" href="#232">&nbsp;&nbsp;&nbsp;&nbsp;232&nbsp;</a>            <b>return</b> <span class="s">" (%s)"</span> % <span class="s">"-"</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>(<a href="/source/s?defs=url_vars&amp;project=SAS_10.20">url_vars</a>)
<a class="l" name="233" href="#233">&nbsp;&nbsp;&nbsp;&nbsp;233&nbsp;</a>        <b>else</b>:
<a class="l" name="234" href="#234">&nbsp;&nbsp;&nbsp;&nbsp;234&nbsp;</a>            <b>return</b> <span class="s">""</span>
<a class="l" name="235" href="#235">&nbsp;&nbsp;&nbsp;&nbsp;235&nbsp;</a>
<a class="l" name="236" href="#236">&nbsp;&nbsp;&nbsp;&nbsp;236&nbsp;</a>    <b>def</b> <a href="/source/s?defs=list_packages&amp;project=SAS_10.20">list_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="237" href="#237">&nbsp;&nbsp;&nbsp;&nbsp;237&nbsp;</a>        <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__guide&amp;project=SAS_10.20">__guide</a>.<a href="/source/s?defs=list_packages&amp;project=SAS_10.20">list_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <a href="/source/s?defs=which_packages&amp;project=SAS_10.20">which_packages</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a>[<span class="s">'which_packages'</span>])
<a class="l" name="238" href="#238">&nbsp;&nbsp;&nbsp;&nbsp;238&nbsp;</a>        <b>if</b> <a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>:
<a class="l" name="239" href="#239">&nbsp;&nbsp;&nbsp;&nbsp;239&nbsp;</a>            <b>return</b> <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>[:<a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>]
<a class="hl" name="240" href="#240">&nbsp;&nbsp;&nbsp;&nbsp;240&nbsp;</a>        <b>return</b> <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>
<a class="l" name="241" href="#241">&nbsp;&nbsp;&nbsp;&nbsp;241&nbsp;</a>
<a class="l" name="242" href="#242">&nbsp;&nbsp;&nbsp;&nbsp;242&nbsp;</a>    <b>def</b> <a href="/source/s?defs=list_errata&amp;project=SAS_10.20">list_errata</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>):
<a class="l" name="243" href="#243">&nbsp;&nbsp;&nbsp;&nbsp;243&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__guide&amp;project=SAS_10.20">__guide</a>.<a href="/source/s?defs=list_erratum&amp;project=SAS_10.20">list_erratum</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>)
<a class="l" name="244" href="#244">&nbsp;&nbsp;&nbsp;&nbsp;244&nbsp;</a>
<a class="l" name="245" href="#245">&nbsp;&nbsp;&nbsp;&nbsp;245&nbsp;</a>    <b>def</b> <a href="/source/s?defs=erratum_path&amp;project=SAS_10.20">erratum_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a>):
<a class="l" name="246" href="#246">&nbsp;&nbsp;&nbsp;&nbsp;246&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=resolve_path&amp;project=SAS_10.20">resolve_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a>[<span class="s">"erratum_policy_path"</span>], <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a>)
<a class="l" name="247" href="#247">&nbsp;&nbsp;&nbsp;&nbsp;247&nbsp;</a>
<a class="l" name="248" href="#248">&nbsp;&nbsp;&nbsp;&nbsp;248&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="249" href="#249">&nbsp;&nbsp;&nbsp;&nbsp;249&nbsp;</a>    <b>def</b> <a href="/source/s?defs=main_policy_path&amp;project=SAS_10.20">main_policy_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="hl" name="250" href="#250">&nbsp;&nbsp;&nbsp;&nbsp;250&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=resolve_path&amp;project=SAS_10.20">resolve_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a>[<span class="s">"content_policy_path"</span>])
<a class="l" name="251" href="#251">&nbsp;&nbsp;&nbsp;&nbsp;251&nbsp;</a>
<a class="l" name="252" href="#252">&nbsp;&nbsp;&nbsp;&nbsp;252&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="253" href="#253">&nbsp;&nbsp;&nbsp;&nbsp;253&nbsp;</a>    <b>def</b> <a href="/source/s?defs=errata_path&amp;project=SAS_10.20">errata_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="254" href="#254">&nbsp;&nbsp;&nbsp;&nbsp;254&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=resolve_path&amp;project=SAS_10.20">resolve_path</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a>[<span class="s">"errata_policy_path"</span>])
<a class="l" name="255" href="#255">&nbsp;&nbsp;&nbsp;&nbsp;255&nbsp;</a>
<a class="l" name="256" href="#256">&nbsp;&nbsp;&nbsp;&nbsp;256&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__str__&amp;project=SAS_10.20">__str__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="257" href="#257">&nbsp;&nbsp;&nbsp;&nbsp;257&nbsp;</a>        <a href="/source/s?defs=to_ret&amp;project=SAS_10.20">to_ret</a> = [<span class="s">"Content Name    : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <span class="s">"Content Mode    : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=mode&amp;project=SAS_10.20">mode</a>,
<a class="l" name="258" href="#258">&nbsp;&nbsp;&nbsp;&nbsp;258&nbsp;</a>                  <span class="s">"Content Packages: %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=which_packages&amp;project=SAS_10.20">which_packages</a>, <span class="s">"HPSA Platform: %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>,
<a class="l" name="259" href="#259">&nbsp;&nbsp;&nbsp;&nbsp;259&nbsp;</a>                  <span class="s">"Packages Only   : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=packages_only&amp;project=SAS_10.20">packages_only</a>, <span class="s">"Errata Path     : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=errata_path&amp;project=SAS_10.20">errata_path</a>,
<a class="hl" name="260" href="#260">&nbsp;&nbsp;&nbsp;&nbsp;260&nbsp;</a>                  <span class="s">"Content Path    : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=main_policy_path&amp;project=SAS_10.20">main_policy_path</a>, <span class="s">"Package Path    : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=package_path&amp;project=SAS_10.20">package_path</a>,
<a class="l" name="261" href="#261">&nbsp;&nbsp;&nbsp;&nbsp;261&nbsp;</a>                  <span class="s">"Keep Content policy in sync with CDN content    : %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=sync_channel&amp;project=SAS_10.20">sync_channel</a>, <span class="s">"Package Search Path:"</span>,
<a class="l" name="262" href="#262">&nbsp;&nbsp;&nbsp;&nbsp;262&nbsp;</a>                  <span class="s">"  %s"</span> % <span class="s">"\n  "</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=package_search_path&amp;project=SAS_10.20">package_search_path</a>), <span class="s">"Search Subfolders: %s"</span> % <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=pkg_search_subfolders&amp;project=SAS_10.20">pkg_search_subfolders</a>]
<a class="l" name="263" href="#263">&nbsp;&nbsp;&nbsp;&nbsp;263&nbsp;</a>        <b>return</b> <span class="s">"\n"</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>(<a href="/source/s?defs=to_ret&amp;project=SAS_10.20">to_ret</a>)
<a class="l" name="264" href="#264">&nbsp;&nbsp;&nbsp;&nbsp;264&nbsp;</a>
<a class="l" name="265" href="#265">&nbsp;&nbsp;&nbsp;&nbsp;265&nbsp;</a>
<a class="l" name="266" href="#266">&nbsp;&nbsp;&nbsp;&nbsp;266&nbsp;</a><b>class</b> <a href="/source/s?defs=CDNDownload&amp;project=SAS_10.20">CDNDownload</a>(<a href="/source/s?defs=AbstractRedHatDownload&amp;project=SAS_10.20">AbstractRedHatDownload</a>):
<a class="l" name="267" href="#267">&nbsp;&nbsp;&nbsp;&nbsp;267&nbsp;</a>    <span class="s">"""
<a class="l" name="268" href="#268">&nbsp;&nbsp;&nbsp;&nbsp;268&nbsp;</a>    Utility class to download packages from cdn.
<a class="l" name="269" href="#269">&nbsp;&nbsp;&nbsp;&nbsp;269&nbsp;</a>    """</span>
<a class="hl" name="270" href="#270">&nbsp;&nbsp;&nbsp;&nbsp;270&nbsp;</a>
<a class="l" name="271" href="#271">&nbsp;&nbsp;&nbsp;&nbsp;271&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=free_space_required&amp;project=SAS_10.20">free_space_required</a>, <a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>=<a href="/source/s?defs=False&amp;project=SAS_10.20">False</a>):
<a class="l" name="272" href="#272">&nbsp;&nbsp;&nbsp;&nbsp;272&nbsp;</a>        <a href="/source/s?defs=super&amp;project=SAS_10.20">super</a>(<a href="/source/s?defs=CDNDownload&amp;project=SAS_10.20">CDNDownload</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>).<a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=free_space_required&amp;project=SAS_10.20">free_space_required</a>, <a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>=<a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>)
<a class="l" name="273" href="#273">&nbsp;&nbsp;&nbsp;&nbsp;273&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a> = <b>None</b>
<a class="l" name="274" href="#274">&nbsp;&nbsp;&nbsp;&nbsp;274&nbsp;</a>
<a class="l" name="275" href="#275">&nbsp;&nbsp;&nbsp;&nbsp;275&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="276" href="#276">&nbsp;&nbsp;&nbsp;&nbsp;276&nbsp;</a>    <b>def</b> <a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="277" href="#277">&nbsp;&nbsp;&nbsp;&nbsp;277&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a>
<a class="l" name="278" href="#278">&nbsp;&nbsp;&nbsp;&nbsp;278&nbsp;</a>
<a class="l" name="279" href="#279">&nbsp;&nbsp;&nbsp;&nbsp;279&nbsp;</a>    @<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>.<a href="/source/s?defs=setter&amp;project=SAS_10.20">setter</a>
<a class="hl" name="280" href="#280">&nbsp;&nbsp;&nbsp;&nbsp;280&nbsp;</a>    <b>def</b> <a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a>):
<a class="l" name="281" href="#281">&nbsp;&nbsp;&nbsp;&nbsp;281&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_cdn_network&amp;project=SAS_10.20">_cdn_network</a> = <a href="/source/s?defs=value&amp;project=SAS_10.20">value</a>
<a class="l" name="282" href="#282">&nbsp;&nbsp;&nbsp;&nbsp;282&nbsp;</a>
<a class="l" name="283" href="#283">&nbsp;&nbsp;&nbsp;&nbsp;283&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_file_name&amp;project=SAS_10.20">get_file_name</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=package_file&amp;project=SAS_10.20">package_file</a>):
<a class="l" name="284" href="#284">&nbsp;&nbsp;&nbsp;&nbsp;284&nbsp;</a>        <a href="/source/s?defs=basename&amp;project=SAS_10.20">basename</a> = <a href="/source/s?defs=string&amp;project=SAS_10.20">string</a>.<a href="/source/s?defs=split&amp;project=SAS_10.20">split</a>(<a href="/source/s?defs=urllib&amp;project=SAS_10.20">urllib</a>.<a href="/source/s?defs=unquote&amp;project=SAS_10.20">unquote</a>(<a href="/source/s?defs=package_file&amp;project=SAS_10.20">package_file</a>), <span class="s">"/"</span>)[-<span class="n">1</span>]
<a class="l" name="285" href="#285">&nbsp;&nbsp;&nbsp;&nbsp;285&nbsp;</a>        <a href="/source/s?defs=filename&amp;project=SAS_10.20">filename</a> = <a href="/source/s?defs=os&amp;project=SAS_10.20">os</a>.<a href="/source/s?defs=path&amp;project=SAS_10.20">path</a>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=download_dir&amp;project=SAS_10.20">download_dir</a>, <a href="/source/s?defs=basename&amp;project=SAS_10.20">basename</a>)
<a class="l" name="286" href="#286">&nbsp;&nbsp;&nbsp;&nbsp;286&nbsp;</a>        <b>return</b> <a href="/source/s?defs=filename&amp;project=SAS_10.20">filename</a>
<a class="l" name="287" href="#287">&nbsp;&nbsp;&nbsp;&nbsp;287&nbsp;</a>
<a class="l" name="288" href="#288">&nbsp;&nbsp;&nbsp;&nbsp;288&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_package_url&amp;project=SAS_10.20">get_package_url</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=package_identifier&amp;project=SAS_10.20">package_identifier</a>):
<a class="l" name="289" href="#289">&nbsp;&nbsp;&nbsp;&nbsp;289&nbsp;</a>        <b>return</b> <a href="/source/s?defs=package_identifier&amp;project=SAS_10.20">package_identifier</a>
<a class="hl" name="290" href="#290">&nbsp;&nbsp;&nbsp;&nbsp;290&nbsp;</a>
<a class="l" name="291" href="#291">&nbsp;&nbsp;&nbsp;&nbsp;291&nbsp;</a>    <b>def</b> <a href="/source/s?defs=get_remote_file_handler&amp;project=SAS_10.20">get_remote_file_handler</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=url&amp;project=SAS_10.20">url</a>, <a href="/source/s?defs=data&amp;project=SAS_10.20">data</a>=<b>None</b>):
<a class="l" name="292" href="#292">&nbsp;&nbsp;&nbsp;&nbsp;292&nbsp;</a>        <b>if</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>:
<a class="l" name="293" href="#293">&nbsp;&nbsp;&nbsp;&nbsp;293&nbsp;</a>            <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a>.<a href="/source/s?defs=get_rpm&amp;project=SAS_10.20">get_rpm</a>(<a href="/source/s?defs=url&amp;project=SAS_10.20">url</a>)
<a class="l" name="294" href="#294">&nbsp;&nbsp;&nbsp;&nbsp;294&nbsp;</a>        <b>return</b> <b>None</b>
<a class="l" name="295" href="#295">&nbsp;&nbsp;&nbsp;&nbsp;295&nbsp;</a>
<a class="l" name="296" href="#296">&nbsp;&nbsp;&nbsp;&nbsp;296&nbsp;</a>
<a class="l" name="297" href="#297">&nbsp;&nbsp;&nbsp;&nbsp;297&nbsp;</a><b>class</b> <a href="/source/s?defs=EntitlementGuide&amp;project=SAS_10.20">EntitlementGuide</a>(<a href="/source/s?defs=dict&amp;project=SAS_10.20">dict</a>):
<a class="l" name="298" href="#298">&nbsp;&nbsp;&nbsp;&nbsp;298&nbsp;</a>    <span class="s">"""
<a class="l" name="299" href="#299">&nbsp;&nbsp;&nbsp;&nbsp;299&nbsp;</a>    Provider of details regarding the content that needs to be imported from CDN. Primarily this class
<a class="hl" name="300" href="#300">&nbsp;&nbsp;&nbsp;&nbsp;300&nbsp;</a>    provides the list of CDNChannel instances that need to be imported and some methods for retrieving
<a class="l" name="301" href="#301">&nbsp;&nbsp;&nbsp;&nbsp;301&nbsp;</a>    the packages and errata for CDN contents. This class is a dict of CDNChannel instances. The keys
<a class="l" name="302" href="#302">&nbsp;&nbsp;&nbsp;&nbsp;302&nbsp;</a>    in this dict are the content labels as they appear in the configuration file.
<a class="l" name="303" href="#303">&nbsp;&nbsp;&nbsp;&nbsp;303&nbsp;</a>    """</span>
<a class="l" name="304" href="#304">&nbsp;&nbsp;&nbsp;&nbsp;304&nbsp;</a>
<a class="l" name="305" href="#305">&nbsp;&nbsp;&nbsp;&nbsp;305&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=rhsm_config_section&amp;project=SAS_10.20">rhsm_config_section</a>, <a href="/source/s?defs=platform_guide&amp;project=SAS_10.20">platform_guide</a>, <a href="/source/s?defs=word&amp;project=SAS_10.20">word</a>=<b>None</b>, <a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>=<a href="/source/s?defs=False&amp;project=SAS_10.20">False</a>,
<a class="l" name="306" href="#306">&nbsp;&nbsp;&nbsp;&nbsp;306&nbsp;</a>                 <a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>=<b>None</b>):
<a class="l" name="307" href="#307">&nbsp;&nbsp;&nbsp;&nbsp;307&nbsp;</a>        <a href="/source/s?defs=super&amp;project=SAS_10.20">super</a>(<a href="/source/s?defs=EntitlementGuide&amp;project=SAS_10.20">EntitlementGuide</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>).<a href="/source/s?defs=__init__&amp;project=SAS_10.20">__init__</a>()
<a class="l" name="308" href="#308">&nbsp;&nbsp;&nbsp;&nbsp;308&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=word&amp;project=SAS_10.20">word</a> = <a href="/source/s?defs=word&amp;project=SAS_10.20">word</a>
<a class="l" name="309" href="#309">&nbsp;&nbsp;&nbsp;&nbsp;309&nbsp;</a>
<a class="hl" name="310" href="#310">&nbsp;&nbsp;&nbsp;&nbsp;310&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=rhd&amp;project=SAS_10.20">rhd</a> = <a href="/source/s?defs=CDNDownload&amp;project=SAS_10.20">CDNDownload</a>(<a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=rhsm_config_section&amp;project=SAS_10.20">rhsm_config_section</a>[<span class="s">"free_space_required"</span>]), <a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>=<a href="/source/s?defs=read_only&amp;project=SAS_10.20">read_only</a>)
<a class="l" name="311" href="#311">&nbsp;&nbsp;&nbsp;&nbsp;311&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__platform_guide&amp;project=SAS_10.20">__platform_guide</a> = <a href="/source/s?defs=platform_guide&amp;project=SAS_10.20">platform_guide</a>
<a class="l" name="312" href="#312">&nbsp;&nbsp;&nbsp;&nbsp;312&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a> = <a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>
<a class="l" name="313" href="#313">&nbsp;&nbsp;&nbsp;&nbsp;313&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a> = {}
<a class="l" name="314" href="#314">&nbsp;&nbsp;&nbsp;&nbsp;314&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__repomd_cache&amp;project=SAS_10.20">__repomd_cache</a> = {}
<a class="l" name="315" href="#315">&nbsp;&nbsp;&nbsp;&nbsp;315&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__all_packages&amp;project=SAS_10.20">__all_packages</a> = {}
<a class="l" name="316" href="#316">&nbsp;&nbsp;&nbsp;&nbsp;316&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__latest_packages&amp;project=SAS_10.20">__latest_packages</a> = {}
<a class="l" name="317" href="#317">&nbsp;&nbsp;&nbsp;&nbsp;317&nbsp;</a>
<a class="l" name="318" href="#318">&nbsp;&nbsp;&nbsp;&nbsp;318&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_rhsm_config_section&amp;project=SAS_10.20">_rhsm_config_section</a> = <a href="/source/s?defs=rhsm_config_section&amp;project=SAS_10.20">rhsm_config_section</a>
<a class="l" name="319" href="#319">&nbsp;&nbsp;&nbsp;&nbsp;319&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_load_available_content&amp;project=SAS_10.20">_load_available_content</a>()
<a class="hl" name="320" href="#320">&nbsp;&nbsp;&nbsp;&nbsp;320&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_init_content_to_import&amp;project=SAS_10.20">_init_content_to_import</a>(<a href="/source/s?defs=platform_guide&amp;project=SAS_10.20">platform_guide</a>)
<a class="l" name="321" href="#321">&nbsp;&nbsp;&nbsp;&nbsp;321&nbsp;</a>
<a class="l" name="322" href="#322">&nbsp;&nbsp;&nbsp;&nbsp;322&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__nonzero__&amp;project=SAS_10.20">__nonzero__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="323" href="#323">&nbsp;&nbsp;&nbsp;&nbsp;323&nbsp;</a>        <b>return</b> <a href="/source/s?defs=True&amp;project=SAS_10.20">True</a>
<a class="l" name="324" href="#324">&nbsp;&nbsp;&nbsp;&nbsp;324&nbsp;</a>
<a class="l" name="325" href="#325">&nbsp;&nbsp;&nbsp;&nbsp;325&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__enter__&amp;project=SAS_10.20">__enter__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="326" href="#326">&nbsp;&nbsp;&nbsp;&nbsp;326&nbsp;</a>        <b>return</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>
<a class="l" name="327" href="#327">&nbsp;&nbsp;&nbsp;&nbsp;327&nbsp;</a>
<a class="l" name="328" href="#328">&nbsp;&nbsp;&nbsp;&nbsp;328&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__exit__&amp;project=SAS_10.20">__exit__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=exc_type&amp;project=SAS_10.20">exc_type</a>, <a href="/source/s?defs=exc_val&amp;project=SAS_10.20">exc_val</a>, <a href="/source/s?defs=exc_tb&amp;project=SAS_10.20">exc_tb</a>):
<a class="l" name="329" href="#329">&nbsp;&nbsp;&nbsp;&nbsp;329&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=rhd&amp;project=SAS_10.20">rhd</a>.<a href="/source/s?defs=cleanup&amp;project=SAS_10.20">cleanup</a>()
<a class="hl" name="330" href="#330">&nbsp;&nbsp;&nbsp;&nbsp;330&nbsp;</a>
<a class="l" name="331" href="#331">&nbsp;&nbsp;&nbsp;&nbsp;331&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_init_content_to_import&amp;project=SAS_10.20">_init_content_to_import</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=platform_guide&amp;project=SAS_10.20">platform_guide</a>):
<a class="l" name="332" href="#332">&nbsp;&nbsp;&nbsp;&nbsp;332&nbsp;</a>        <span class="s">"""
<a class="l" name="333" href="#333">&nbsp;&nbsp;&nbsp;&nbsp;333&nbsp;</a>        Initializes the details of the content that needs to be imported. Basically this method tries to setup
<a class="l" name="334" href="#334">&nbsp;&nbsp;&nbsp;&nbsp;334&nbsp;</a>        a CDNChannel instance for each content section in the configuration. However if the entitlement content label
<a class="l" name="335" href="#335">&nbsp;&nbsp;&nbsp;&nbsp;335&nbsp;</a>        specified in the configuration is invalid or it is not possible to associate an SA platform with the content,
<a class="l" name="336" href="#336">&nbsp;&nbsp;&nbsp;&nbsp;336&nbsp;</a>        no CDNChannel is instantiated for the config section.
<a class="l" name="337" href="#337">&nbsp;&nbsp;&nbsp;&nbsp;337&nbsp;</a>        """</span>
<a class="l" name="338" href="#338">&nbsp;&nbsp;&nbsp;&nbsp;338&nbsp;</a>        <a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a> = <a href="/source/s?defs=platform_guide&amp;project=SAS_10.20">platform_guide</a>.<a href="/source/s?defs=sa_platforms&amp;project=SAS_10.20">sa_platforms</a>
<a class="l" name="339" href="#339">&nbsp;&nbsp;&nbsp;&nbsp;339&nbsp;</a>        <b>for</b> <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_rhsm_config_section&amp;project=SAS_10.20">_rhsm_config_section</a>.<a href="/source/s?defs=get_child_sections&amp;project=SAS_10.20">get_child_sections</a>():
<a class="hl" name="340" href="#340">&nbsp;&nbsp;&nbsp;&nbsp;340&nbsp;</a>            <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> = <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>(<a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>)
<a class="l" name="341" href="#341">&nbsp;&nbsp;&nbsp;&nbsp;341&nbsp;</a>            <a href="/source/s?defs=ent_content_label&amp;project=SAS_10.20">ent_content_label</a> = <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_ent_content_label&amp;project=SAS_10.20">get_ent_content_label</a>()
<a class="l" name="342" href="#342">&nbsp;&nbsp;&nbsp;&nbsp;342&nbsp;</a>            <b>if</b> <a href="/source/s?defs=ent_content_label&amp;project=SAS_10.20">ent_content_label</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>:
<a class="l" name="343" href="#343">&nbsp;&nbsp;&nbsp;&nbsp;343&nbsp;</a>                <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_init_content_instance&amp;project=SAS_10.20">_init_content_instance</a>(<a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>, <a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=ent_content_label&amp;project=SAS_10.20">ent_content_label</a>)
<a class="l" name="344" href="#344">&nbsp;&nbsp;&nbsp;&nbsp;344&nbsp;</a>            <b>else</b>:
<a class="l" name="345" href="#345">&nbsp;&nbsp;&nbsp;&nbsp;345&nbsp;</a>                <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=warning&amp;project=SAS_10.20">warning</a>(<span class="s">"Unable to process content label %s. This label is not available in any of the "</span>
<a class="l" name="346" href="#346">&nbsp;&nbsp;&nbsp;&nbsp;346&nbsp;</a>                            <span class="s">"entitlement certificates provided. This content label will be dropped."</span> %
<a class="l" name="347" href="#347">&nbsp;&nbsp;&nbsp;&nbsp;347&nbsp;</a>                            <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>)
<a class="l" name="348" href="#348">&nbsp;&nbsp;&nbsp;&nbsp;348&nbsp;</a>
<a class="l" name="349" href="#349">&nbsp;&nbsp;&nbsp;&nbsp;349&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_init_content_instance&amp;project=SAS_10.20">_init_content_instance</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>, <a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=ent_content_label&amp;project=SAS_10.20">ent_content_label</a>):
<a class="hl" name="350" href="#350">&nbsp;&nbsp;&nbsp;&nbsp;350&nbsp;</a>        <b>if</b> <span class="s">"platform"</span> <b>in</b> <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>:
<a class="l" name="351" href="#351">&nbsp;&nbsp;&nbsp;&nbsp;351&nbsp;</a>            <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a> = <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>[<span class="s">"platform"</span>]
<a class="l" name="352" href="#352">&nbsp;&nbsp;&nbsp;&nbsp;352&nbsp;</a>            <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_get_platform_by_name&amp;project=SAS_10.20">_get_platform_by_name</a>(<a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>)
<a class="l" name="353" href="#353">&nbsp;&nbsp;&nbsp;&nbsp;353&nbsp;</a>        <b>else</b>:
<a class="l" name="354" href="#354">&nbsp;&nbsp;&nbsp;&nbsp;354&nbsp;</a>            <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_get_platform_by_label&amp;project=SAS_10.20">_get_platform_by_label</a>(<a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>)
<a class="l" name="355" href="#355">&nbsp;&nbsp;&nbsp;&nbsp;355&nbsp;</a>
<a class="l" name="356" href="#356">&nbsp;&nbsp;&nbsp;&nbsp;356&nbsp;</a>            <b>if</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> <b>is</b> <b>None</b>:
<a class="l" name="357" href="#357">&nbsp;&nbsp;&nbsp;&nbsp;357&nbsp;</a>                <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=warning&amp;project=SAS_10.20">warning</a>(<span class="s">"Unable to process content label %s. No platform could be associated with this label. "</span>
<a class="l" name="358" href="#358">&nbsp;&nbsp;&nbsp;&nbsp;358&nbsp;</a>                            <span class="s">"This content label will be dropped. If you need to import this content, add the "</span>
<a class="l" name="359" href="#359">&nbsp;&nbsp;&nbsp;&nbsp;359&nbsp;</a>                            <span class="s">"'platform' option to the configuration file."</span> % <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>)
<a class="hl" name="360" href="#360">&nbsp;&nbsp;&nbsp;&nbsp;360&nbsp;</a>                <b>return</b>
<a class="l" name="361" href="#361">&nbsp;&nbsp;&nbsp;&nbsp;361&nbsp;</a>
<a class="l" name="362" href="#362">&nbsp;&nbsp;&nbsp;&nbsp;362&nbsp;</a>        <a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>[<a href="/source/s?defs=ent_content_label&amp;project=SAS_10.20">ent_content_label</a>]
<a class="l" name="363" href="#363">&nbsp;&nbsp;&nbsp;&nbsp;363&nbsp;</a>        <a href="/source/s?defs=cdn_channel&amp;project=SAS_10.20">cdn_channel</a> = <a href="/source/s?defs=CDNContent&amp;project=SAS_10.20">CDNContent</a>(<a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>, <a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a>,
<a class="l" name="364" href="#364">&nbsp;&nbsp;&nbsp;&nbsp;364&nbsp;</a>                                 <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=platform_id&amp;project=SAS_10.20">platform_id</a>, <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>)
<a class="l" name="365" href="#365">&nbsp;&nbsp;&nbsp;&nbsp;365&nbsp;</a>        <a href="/source/s?defs=cdn_channel&amp;project=SAS_10.20">cdn_channel</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a> = <a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>
<a class="l" name="366" href="#366">&nbsp;&nbsp;&nbsp;&nbsp;366&nbsp;</a>        <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>[<a href="/source/s?defs=content_section&amp;project=SAS_10.20">content_section</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>] = <a href="/source/s?defs=cdn_channel&amp;project=SAS_10.20">cdn_channel</a>
<a class="l" name="367" href="#367">&nbsp;&nbsp;&nbsp;&nbsp;367&nbsp;</a>
<a class="l" name="368" href="#368">&nbsp;&nbsp;&nbsp;&nbsp;368&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="369" href="#369">&nbsp;&nbsp;&nbsp;&nbsp;369&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_get_platform_by_name&amp;project=SAS_10.20">_get_platform_by_name</a>(<a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>):
<a class="hl" name="370" href="#370">&nbsp;&nbsp;&nbsp;&nbsp;370&nbsp;</a>        <b>for</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> <b>in</b> <a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>:
<a class="l" name="371" href="#371">&nbsp;&nbsp;&nbsp;&nbsp;371&nbsp;</a>            <b>if</b> <a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a> == <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>:
<a class="l" name="372" href="#372">&nbsp;&nbsp;&nbsp;&nbsp;372&nbsp;</a>                <b>return</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>
<a class="l" name="373" href="#373">&nbsp;&nbsp;&nbsp;&nbsp;373&nbsp;</a>        <b>return</b> <b>None</b>
<a class="l" name="374" href="#374">&nbsp;&nbsp;&nbsp;&nbsp;374&nbsp;</a>
<a class="l" name="375" href="#375">&nbsp;&nbsp;&nbsp;&nbsp;375&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="376" href="#376">&nbsp;&nbsp;&nbsp;&nbsp;376&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_get_platform_by_label&amp;project=SAS_10.20">_get_platform_by_label</a>(<a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>, <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>):
<a class="l" name="377" href="#377">&nbsp;&nbsp;&nbsp;&nbsp;377&nbsp;</a>        <b>for</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> <b>in</b> <a href="/source/s?defs=platforms&amp;project=SAS_10.20">platforms</a>:
<a class="l" name="378" href="#378">&nbsp;&nbsp;&nbsp;&nbsp;378&nbsp;</a>            <b>if</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> == <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>:
<a class="l" name="379" href="#379">&nbsp;&nbsp;&nbsp;&nbsp;379&nbsp;</a>                <b>return</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>
<a class="hl" name="380" href="#380">&nbsp;&nbsp;&nbsp;&nbsp;380&nbsp;</a>        <b>return</b> <b>None</b>
<a class="l" name="381" href="#381">&nbsp;&nbsp;&nbsp;&nbsp;381&nbsp;</a>
<a class="l" name="382" href="#382">&nbsp;&nbsp;&nbsp;&nbsp;382&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_load_available_content&amp;project=SAS_10.20">_load_available_content</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="383" href="#383">&nbsp;&nbsp;&nbsp;&nbsp;383&nbsp;</a>        <span class="s">"""
<a class="l" name="384" href="#384">&nbsp;&nbsp;&nbsp;&nbsp;384&nbsp;</a>        Parses entitlement certificates.
<a class="l" name="385" href="#385">&nbsp;&nbsp;&nbsp;&nbsp;385&nbsp;</a>
<a class="l" name="386" href="#386">&nbsp;&nbsp;&nbsp;&nbsp;386&nbsp;</a>        :return: a list of CDNContent instances
<a class="l" name="387" href="#387">&nbsp;&nbsp;&nbsp;&nbsp;387&nbsp;</a>        """</span>
<a class="l" name="388" href="#388">&nbsp;&nbsp;&nbsp;&nbsp;388&nbsp;</a>        <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=info&amp;project=SAS_10.20">info</a>(<span class="s">"Retrieving content labels from certificates"</span>)
<a class="l" name="389" href="#389">&nbsp;&nbsp;&nbsp;&nbsp;389&nbsp;</a>        <b>for</b> <a href="/source/s?defs=certificate_path&amp;project=SAS_10.20">certificate_path</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_rhsm_config_section&amp;project=SAS_10.20">_rhsm_config_section</a>.<a href="/source/s?defs=get_certificate_paths&amp;project=SAS_10.20">get_certificate_paths</a>():
<a class="hl" name="390" href="#390">&nbsp;&nbsp;&nbsp;&nbsp;390&nbsp;</a>            <a href="/source/s?defs=cdn_entitlement&amp;project=SAS_10.20">cdn_entitlement</a> = <a href="/source/s?defs=CDNEntitlement&amp;project=SAS_10.20">CDNEntitlement</a>(<a href="/source/s?defs=path_to_cert&amp;project=SAS_10.20">path_to_cert</a>=<a href="/source/s?defs=certificate_path&amp;project=SAS_10.20">certificate_path</a>)
<a class="l" name="391" href="#391">&nbsp;&nbsp;&nbsp;&nbsp;391&nbsp;</a>            <b>for</b> <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> <b>in</b> <a href="/source/s?defs=cdn_entitlement&amp;project=SAS_10.20">cdn_entitlement</a>.<a href="/source/s?defs=get_contents&amp;project=SAS_10.20">get_contents</a>():
<a class="l" name="392" href="#392">&nbsp;&nbsp;&nbsp;&nbsp;392&nbsp;</a>                <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>[<a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>] = <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>
<a class="l" name="393" href="#393">&nbsp;&nbsp;&nbsp;&nbsp;393&nbsp;</a>        <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=verbose&amp;project=SAS_10.20">verbose</a>(<span class="s">"Done retrieving content labels from certificates"</span>)
<a class="l" name="394" href="#394">&nbsp;&nbsp;&nbsp;&nbsp;394&nbsp;</a>
<a class="l" name="395" href="#395">&nbsp;&nbsp;&nbsp;&nbsp;395&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_get_latest_packages&amp;project=SAS_10.20">_get_latest_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=package_index&amp;project=SAS_10.20">package_index</a>):
<a class="l" name="396" href="#396">&nbsp;&nbsp;&nbsp;&nbsp;396&nbsp;</a>        <span class="s">"""
<a class="l" name="397" href="#397">&nbsp;&nbsp;&nbsp;&nbsp;397&nbsp;</a>        Returns a list of packages with the largest version (including release and epoch) from a given dict of
<a class="l" name="398" href="#398">&nbsp;&nbsp;&nbsp;&nbsp;398&nbsp;</a>        package name -&gt; list of CDNPackage(s).
<a class="l" name="399" href="#399">&nbsp;&nbsp;&nbsp;&nbsp;399&nbsp;</a>
<a class="hl" name="400" href="#400">&nbsp;&nbsp;&nbsp;&nbsp;400&nbsp;</a>        :param package_index: a map of package names to list of CDNPackage instances
<a class="l" name="401" href="#401">&nbsp;&nbsp;&nbsp;&nbsp;401&nbsp;</a>        :return: a list of packages with the largest version
<a class="l" name="402" href="#402">&nbsp;&nbsp;&nbsp;&nbsp;402&nbsp;</a>        """</span>
<a class="l" name="403" href="#403">&nbsp;&nbsp;&nbsp;&nbsp;403&nbsp;</a>        <a href="/source/s?defs=final_packages&amp;project=SAS_10.20">final_packages</a> = []
<a class="l" name="404" href="#404">&nbsp;&nbsp;&nbsp;&nbsp;404&nbsp;</a>        <b>for</b> <a href="/source/s?defs=indexed_packages&amp;project=SAS_10.20">indexed_packages</a> <b>in</b> <a href="/source/s?defs=package_index&amp;project=SAS_10.20">package_index</a>.<a href="/source/s?defs=itervalues&amp;project=SAS_10.20">itervalues</a>():
<a class="l" name="405" href="#405">&nbsp;&nbsp;&nbsp;&nbsp;405&nbsp;</a>            <b>if</b> <a href="/source/s?defs=len&amp;project=SAS_10.20">len</a>(<a href="/source/s?defs=indexed_packages&amp;project=SAS_10.20">indexed_packages</a>) &gt; <span class="n">1</span>:
<a class="l" name="406" href="#406">&nbsp;&nbsp;&nbsp;&nbsp;406&nbsp;</a>                <span class="c"># select package with highest version, release and epoch by building a list of custom</span>
<a class="l" name="407" href="#407">&nbsp;&nbsp;&nbsp;&nbsp;407&nbsp;</a>                <span class="c"># truncated nevra(s) with the following form: epoch-version-release</span>
<a class="l" name="408" href="#408">&nbsp;&nbsp;&nbsp;&nbsp;408&nbsp;</a>                <a href="/source/s?defs=indexed_packages&amp;project=SAS_10.20">indexed_packages</a>.<a href="/source/s?defs=sort&amp;project=SAS_10.20">sort</a>()
<a class="l" name="409" href="#409">&nbsp;&nbsp;&nbsp;&nbsp;409&nbsp;</a>                <a href="/source/s?defs=final_packages&amp;project=SAS_10.20">final_packages</a>.<a href="/source/s?defs=extend&amp;project=SAS_10.20">extend</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_extract_latest_packages&amp;project=SAS_10.20">_extract_latest_packages</a>(<a href="/source/s?defs=indexed_packages&amp;project=SAS_10.20">indexed_packages</a>))
<a class="hl" name="410" href="#410">&nbsp;&nbsp;&nbsp;&nbsp;410&nbsp;</a>            <b>else</b>:
<a class="l" name="411" href="#411">&nbsp;&nbsp;&nbsp;&nbsp;411&nbsp;</a>                <a href="/source/s?defs=final_packages&amp;project=SAS_10.20">final_packages</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=indexed_packages&amp;project=SAS_10.20">indexed_packages</a>[<span class="n">0</span>])
<a class="l" name="412" href="#412">&nbsp;&nbsp;&nbsp;&nbsp;412&nbsp;</a>        <b>return</b> <a href="/source/s?defs=final_packages&amp;project=SAS_10.20">final_packages</a>
<a class="l" name="413" href="#413">&nbsp;&nbsp;&nbsp;&nbsp;413&nbsp;</a>
<a class="l" name="414" href="#414">&nbsp;&nbsp;&nbsp;&nbsp;414&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="415" href="#415">&nbsp;&nbsp;&nbsp;&nbsp;415&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_extract_latest_packages&amp;project=SAS_10.20">_extract_latest_packages</a>(<a href="/source/s?defs=sorted_packages&amp;project=SAS_10.20">sorted_packages</a>):
<a class="l" name="416" href="#416">&nbsp;&nbsp;&nbsp;&nbsp;416&nbsp;</a>        <span class="s">"""
<a class="l" name="417" href="#417">&nbsp;&nbsp;&nbsp;&nbsp;417&nbsp;</a>        Extracts the latest packages from the given list of packages sorted by epoch, version and release.
<a class="l" name="418" href="#418">&nbsp;&nbsp;&nbsp;&nbsp;418&nbsp;</a>        This method returns all packages which have the same version (epoch, version, release) as the last
<a class="l" name="419" href="#419">&nbsp;&nbsp;&nbsp;&nbsp;419&nbsp;</a>        package in the given list. If there is a single package having the latest version, the returned list
<a class="hl" name="420" href="#420">&nbsp;&nbsp;&nbsp;&nbsp;420&nbsp;</a>        will contain a single element. Multiple elements will be returned in case the given list contains
<a class="l" name="421" href="#421">&nbsp;&nbsp;&nbsp;&nbsp;421&nbsp;</a>        the same package version but for different architectures (e.g. 389-ds-base-libs-1.2.11.15-22.el6_4.i686.rpm and
<a class="l" name="422" href="#422">&nbsp;&nbsp;&nbsp;&nbsp;422&nbsp;</a>        389-ds-base-libs-1.2.11.15-22.el6_4.x86_64.rpm)
<a class="l" name="423" href="#423">&nbsp;&nbsp;&nbsp;&nbsp;423&nbsp;</a>
<a class="l" name="424" href="#424">&nbsp;&nbsp;&nbsp;&nbsp;424&nbsp;</a>        :param sorted_packages a list of CDNPackage instances sorted by epoch, version and release
<a class="l" name="425" href="#425">&nbsp;&nbsp;&nbsp;&nbsp;425&nbsp;</a>        :return: a list of CDNPackage instances containing the packages with the latest version
<a class="l" name="426" href="#426">&nbsp;&nbsp;&nbsp;&nbsp;426&nbsp;</a>        """</span>
<a class="l" name="427" href="#427">&nbsp;&nbsp;&nbsp;&nbsp;427&nbsp;</a>        <a href="/source/s?defs=reference_package&amp;project=SAS_10.20">reference_package</a> = <a href="/source/s?defs=sorted_packages&amp;project=SAS_10.20">sorted_packages</a>[-<span class="n">1</span>]
<a class="l" name="428" href="#428">&nbsp;&nbsp;&nbsp;&nbsp;428&nbsp;</a>        <a href="/source/s?defs=latest_packages&amp;project=SAS_10.20">latest_packages</a> = [<a href="/source/s?defs=reference_package&amp;project=SAS_10.20">reference_package</a>]
<a class="l" name="429" href="#429">&nbsp;&nbsp;&nbsp;&nbsp;429&nbsp;</a>        <b>for</b> <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a> <b>in</b> <a href="/source/s?defs=reversed&amp;project=SAS_10.20">reversed</a>(<a href="/source/s?defs=sorted_packages&amp;project=SAS_10.20">sorted_packages</a>[:-<span class="n">1</span>]):
<a class="hl" name="430" href="#430">&nbsp;&nbsp;&nbsp;&nbsp;430&nbsp;</a>            <b>if</b> <a href="/source/s?defs=cmp&amp;project=SAS_10.20">cmp</a>(<a href="/source/s?defs=reference_package&amp;project=SAS_10.20">reference_package</a>, <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a>) == <span class="n">0</span>:
<a class="l" name="431" href="#431">&nbsp;&nbsp;&nbsp;&nbsp;431&nbsp;</a>                <a href="/source/s?defs=latest_packages&amp;project=SAS_10.20">latest_packages</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=package&amp;project=SAS_10.20">package</a>)
<a class="l" name="432" href="#432">&nbsp;&nbsp;&nbsp;&nbsp;432&nbsp;</a>            <b>else</b>:
<a class="l" name="433" href="#433">&nbsp;&nbsp;&nbsp;&nbsp;433&nbsp;</a>                <b>break</b>
<a class="l" name="434" href="#434">&nbsp;&nbsp;&nbsp;&nbsp;434&nbsp;</a>        <b>return</b> <a href="/source/s?defs=latest_packages&amp;project=SAS_10.20">latest_packages</a>
<a class="l" name="435" href="#435">&nbsp;&nbsp;&nbsp;&nbsp;435&nbsp;</a>
<a class="l" name="436" href="#436">&nbsp;&nbsp;&nbsp;&nbsp;436&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="437" href="#437">&nbsp;&nbsp;&nbsp;&nbsp;437&nbsp;</a>    <b>def</b> <a href="/source/s?defs=_index_packages&amp;project=SAS_10.20">_index_packages</a>(<a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>):
<a class="l" name="438" href="#438">&nbsp;&nbsp;&nbsp;&nbsp;438&nbsp;</a>        <span class="s">"""
<a class="l" name="439" href="#439">&nbsp;&nbsp;&nbsp;&nbsp;439&nbsp;</a>        Returns a map of package nevras and package values
<a class="hl" name="440" href="#440">&nbsp;&nbsp;&nbsp;&nbsp;440&nbsp;</a>        :param packages: a list of CDNPackage
<a class="l" name="441" href="#441">&nbsp;&nbsp;&nbsp;&nbsp;441&nbsp;</a>        :return: a dictionary of packages
<a class="l" name="442" href="#442">&nbsp;&nbsp;&nbsp;&nbsp;442&nbsp;</a>        """</span>
<a class="l" name="443" href="#443">&nbsp;&nbsp;&nbsp;&nbsp;443&nbsp;</a>        <a href="/source/s?defs=indexer&amp;project=SAS_10.20">indexer</a> = {}
<a class="l" name="444" href="#444">&nbsp;&nbsp;&nbsp;&nbsp;444&nbsp;</a>        <b>for</b> <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a> <b>in</b> <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>:
<a class="l" name="445" href="#445">&nbsp;&nbsp;&nbsp;&nbsp;445&nbsp;</a>            <a href="/source/s?defs=indexer&amp;project=SAS_10.20">indexer</a>[<a href="/source/s?defs=package&amp;project=SAS_10.20">package</a>.<a href="/source/s?defs=uid&amp;project=SAS_10.20">uid</a>] = <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a>
<a class="l" name="446" href="#446">&nbsp;&nbsp;&nbsp;&nbsp;446&nbsp;</a>        <b>return</b> <a href="/source/s?defs=indexer&amp;project=SAS_10.20">indexer</a>
<a class="l" name="447" href="#447">&nbsp;&nbsp;&nbsp;&nbsp;447&nbsp;</a>
<a class="l" name="448" href="#448">&nbsp;&nbsp;&nbsp;&nbsp;448&nbsp;</a>    <b>def</b> <a href="/source/s?defs=list_packages&amp;project=SAS_10.20">list_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>, <a href="/source/s?defs=which_packages&amp;project=SAS_10.20">which_packages</a>=<span class="s">'latest'</span>):
<a class="l" name="449" href="#449">&nbsp;&nbsp;&nbsp;&nbsp;449&nbsp;</a>        <span class="s">"""
<a class="hl" name="450" href="#450">&nbsp;&nbsp;&nbsp;&nbsp;450&nbsp;</a>        Returns a list of packages for the given content label.
<a class="l" name="451" href="#451">&nbsp;&nbsp;&nbsp;&nbsp;451&nbsp;</a>
<a class="l" name="452" href="#452">&nbsp;&nbsp;&nbsp;&nbsp;452&nbsp;</a>        :param conf_content_label: a string representing a content label.
<a class="l" name="453" href="#453">&nbsp;&nbsp;&nbsp;&nbsp;453&nbsp;</a>        :param which_packages: a string value specifying which packages to parse.
<a class="l" name="454" href="#454">&nbsp;&nbsp;&nbsp;&nbsp;454&nbsp;</a>                               There are two options here: 'all' packages and the 'latest' packages. By default 'latest'
<a class="l" name="455" href="#455">&nbsp;&nbsp;&nbsp;&nbsp;455&nbsp;</a>        :return: a list of CDNPackage(s)
<a class="l" name="456" href="#456">&nbsp;&nbsp;&nbsp;&nbsp;456&nbsp;</a>        """</span>
<a class="l" name="457" href="#457">&nbsp;&nbsp;&nbsp;&nbsp;457&nbsp;</a>        <span class="c"># search if the content_label exists in our local cache</span>
<a class="l" name="458" href="#458">&nbsp;&nbsp;&nbsp;&nbsp;458&nbsp;</a>        <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> = <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="l" name="459" href="#459">&nbsp;&nbsp;&nbsp;&nbsp;459&nbsp;</a>        <a href="/source/s?defs=all_packages_cache&amp;project=SAS_10.20">all_packages_cache</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__all_packages&amp;project=SAS_10.20">__all_packages</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>, [])
<a class="hl" name="460" href="#460">&nbsp;&nbsp;&nbsp;&nbsp;460&nbsp;</a>        <a href="/source/s?defs=latest_packages_cache&amp;project=SAS_10.20">latest_packages_cache</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__latest_packages&amp;project=SAS_10.20">__latest_packages</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>, [])
<a class="l" name="461" href="#461">&nbsp;&nbsp;&nbsp;&nbsp;461&nbsp;</a>
<a class="l" name="462" href="#462">&nbsp;&nbsp;&nbsp;&nbsp;462&nbsp;</a>        <a href="/source/s?defs=latest_packages&amp;project=SAS_10.20">latest_packages</a> = <a href="/source/s?defs=which_packages&amp;project=SAS_10.20">which_packages</a> != <span class="s">'all'</span>
<a class="l" name="463" href="#463">&nbsp;&nbsp;&nbsp;&nbsp;463&nbsp;</a>        <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_ent_content_label&amp;project=SAS_10.20">get_ent_content_label</a>(), <b>None</b>)
<a class="l" name="464" href="#464">&nbsp;&nbsp;&nbsp;&nbsp;464&nbsp;</a>
<a class="l" name="465" href="#465">&nbsp;&nbsp;&nbsp;&nbsp;465&nbsp;</a>        <b>if</b> <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> <b>is</b> <b>None</b>:
<a class="l" name="466" href="#466">&nbsp;&nbsp;&nbsp;&nbsp;466&nbsp;</a>            <b>raise</b> <a href="/source/s?defs=InvalidContentName&amp;project=SAS_10.20">InvalidContentName</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="l" name="467" href="#467">&nbsp;&nbsp;&nbsp;&nbsp;467&nbsp;</a>        <span class="c"># get the repomd xml and then start parsing primary xml but first look up the cache</span>
<a class="l" name="468" href="#468">&nbsp;&nbsp;&nbsp;&nbsp;468&nbsp;</a>        <b>if</b> <b>not</b> <a href="/source/s?defs=len&amp;project=SAS_10.20">len</a>(<a href="/source/s?defs=all_packages_cache&amp;project=SAS_10.20">all_packages_cache</a>) <b>or</b> <b>not</b> <a href="/source/s?defs=len&amp;project=SAS_10.20">len</a>(<a href="/source/s?defs=latest_packages_cache&amp;project=SAS_10.20">latest_packages_cache</a>):
<a class="l" name="469" href="#469">&nbsp;&nbsp;&nbsp;&nbsp;469&nbsp;</a>            <a href="/source/s?defs=final_path&amp;project=SAS_10.20">final_path</a> = <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=get_expanded_path&amp;project=SAS_10.20">get_expanded_path</a>(<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_content_url_vars&amp;project=SAS_10.20">get_content_url_vars</a>())
<a class="hl" name="470" href="#470">&nbsp;&nbsp;&nbsp;&nbsp;470&nbsp;</a>            <a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a> = <a href="/source/s?defs=RedHatCDNRepo&amp;project=SAS_10.20">RedHatCDNRepo</a>(<a href="/source/s?defs=final_path&amp;project=SAS_10.20">final_path</a>, <a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>, <a href="/source/s?defs=cert_file&amp;project=SAS_10.20">cert_file</a>=<a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=certificate_path&amp;project=SAS_10.20">certificate_path</a>)
<a class="l" name="471" href="#471">&nbsp;&nbsp;&nbsp;&nbsp;471&nbsp;</a>            <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_repomd&amp;project=SAS_10.20">__get_repomd</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="l" name="472" href="#472">&nbsp;&nbsp;&nbsp;&nbsp;472&nbsp;</a>            <span class="c"># we have the repomd file, let's look where <a href="/source/s?path=primary.xml&amp;project=SAS_10.20">primary.xml</a>.gz is located</span>
<a class="l" name="473" href="#473">&nbsp;&nbsp;&nbsp;&nbsp;473&nbsp;</a>            <a href="/source/s?defs=primary_href&amp;project=SAS_10.20">primary_href</a> = <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a>.<a href="/source/s?defs=get_attributes_for&amp;project=SAS_10.20">get_attributes_for</a>(<span class="s">'primary'</span>)[<span class="s">'location'</span>][<span class="s">'href'</span>]
<a class="l" name="474" href="#474">&nbsp;&nbsp;&nbsp;&nbsp;474&nbsp;</a>            <a href="/source/s?defs=primary_model&amp;project=SAS_10.20">primary_model</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_primary_model&amp;project=SAS_10.20">__get_primary_model</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=primary_href&amp;project=SAS_10.20">primary_href</a>)
<a class="l" name="475" href="#475">&nbsp;&nbsp;&nbsp;&nbsp;475&nbsp;</a>            <a href="/source/s?defs=package_index&amp;project=SAS_10.20">package_index</a> = <a href="/source/s?defs=collections&amp;project=SAS_10.20">collections</a>.<a href="/source/s?defs=OrderedDict&amp;project=SAS_10.20">OrderedDict</a>()
<a class="l" name="476" href="#476">&nbsp;&nbsp;&nbsp;&nbsp;476&nbsp;</a>            <b>for</b> <a href="/source/s?defs=rpm_dict&amp;project=SAS_10.20">rpm_dict</a> <b>in</b> <a href="/source/s?defs=primary_model&amp;project=SAS_10.20">primary_model</a>.<a href="/source/s?defs=get_packages&amp;project=SAS_10.20">get_packages</a>():
<a class="l" name="477" href="#477">&nbsp;&nbsp;&nbsp;&nbsp;477&nbsp;</a>                <a href="/source/s?defs=new_package&amp;project=SAS_10.20">new_package</a> = <a href="/source/s?defs=CDNPackage&amp;project=SAS_10.20">CDNPackage</a>(<a href="/source/s?defs=rpm_dict&amp;project=SAS_10.20">rpm_dict</a>, <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>)
<a class="l" name="478" href="#478">&nbsp;&nbsp;&nbsp;&nbsp;478&nbsp;</a>                <a href="/source/s?defs=new_package&amp;project=SAS_10.20">new_package</a>.<a href="/source/s?defs=cdn_network&amp;project=SAS_10.20">cdn_network</a> = <a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>
<a class="l" name="479" href="#479">&nbsp;&nbsp;&nbsp;&nbsp;479&nbsp;</a>                <a href="/source/s?defs=all_packages_cache&amp;project=SAS_10.20">all_packages_cache</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=new_package&amp;project=SAS_10.20">new_package</a>)
<a class="hl" name="480" href="#480">&nbsp;&nbsp;&nbsp;&nbsp;480&nbsp;</a>                <a href="/source/s?defs=package_index&amp;project=SAS_10.20">package_index</a>.<a href="/source/s?defs=setdefault&amp;project=SAS_10.20">setdefault</a>(<a href="/source/s?defs=new_package&amp;project=SAS_10.20">new_package</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, []).<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=new_package&amp;project=SAS_10.20">new_package</a>)
<a class="l" name="481" href="#481">&nbsp;&nbsp;&nbsp;&nbsp;481&nbsp;</a>
<a class="l" name="482" href="#482">&nbsp;&nbsp;&nbsp;&nbsp;482&nbsp;</a>            <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__all_packages&amp;project=SAS_10.20">__all_packages</a>[<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>] = <a href="/source/s?defs=all_packages_cache&amp;project=SAS_10.20">all_packages_cache</a>
<a class="l" name="483" href="#483">&nbsp;&nbsp;&nbsp;&nbsp;483&nbsp;</a>            <a href="/source/s?defs=latest_packages_cache&amp;project=SAS_10.20">latest_packages_cache</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_get_latest_packages&amp;project=SAS_10.20">_get_latest_packages</a>(<a href="/source/s?defs=package_index&amp;project=SAS_10.20">package_index</a>)
<a class="l" name="484" href="#484">&nbsp;&nbsp;&nbsp;&nbsp;484&nbsp;</a>            <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__latest_packages&amp;project=SAS_10.20">__latest_packages</a>[<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>] = <a href="/source/s?defs=latest_packages_cache&amp;project=SAS_10.20">latest_packages_cache</a>
<a class="l" name="485" href="#485">&nbsp;&nbsp;&nbsp;&nbsp;485&nbsp;</a>        <b>return</b> <a href="/source/s?defs=latest_packages_cache&amp;project=SAS_10.20">latest_packages_cache</a> <b>if</b> <a href="/source/s?defs=latest_packages&amp;project=SAS_10.20">latest_packages</a> <b>else</b> <a href="/source/s?defs=all_packages_cache&amp;project=SAS_10.20">all_packages_cache</a>
<a class="l" name="486" href="#486">&nbsp;&nbsp;&nbsp;&nbsp;486&nbsp;</a>
<a class="l" name="487" href="#487">&nbsp;&nbsp;&nbsp;&nbsp;487&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="488" href="#488">&nbsp;&nbsp;&nbsp;&nbsp;488&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__search_erratum_packages&amp;project=SAS_10.20">__search_erratum_packages</a>(<a href="/source/s?defs=primary_packages_dict&amp;project=SAS_10.20">primary_packages_dict</a>, <a href="/source/s?defs=raw_packages_to_find&amp;project=SAS_10.20">raw_packages_to_find</a>, <a href="/source/s?defs=erratum_id&amp;project=SAS_10.20">erratum_id</a>):
<a class="l" name="489" href="#489">&nbsp;&nbsp;&nbsp;&nbsp;489&nbsp;</a>        <span class="s">"""
<a class="hl" name="490" href="#490">&nbsp;&nbsp;&nbsp;&nbsp;490&nbsp;</a>        Searches raw_packages in primary_packages and returns a list of search result.
<a class="l" name="491" href="#491">&nbsp;&nbsp;&nbsp;&nbsp;491&nbsp;</a>
<a class="l" name="492" href="#492">&nbsp;&nbsp;&nbsp;&nbsp;492&nbsp;</a>        :param primary_packages_dict: a map of package nevra and CDNPackage instance, representing the cache where we
<a class="l" name="493" href="#493">&nbsp;&nbsp;&nbsp;&nbsp;493&nbsp;</a>                                    search
<a class="l" name="494" href="#494">&nbsp;&nbsp;&nbsp;&nbsp;494&nbsp;</a>        :param raw_packages_to_find: a list of raw dictionaries that contains nevra metadata about a package
<a class="l" name="495" href="#495">&nbsp;&nbsp;&nbsp;&nbsp;495&nbsp;</a>        :param erratum_id: the erratum id
<a class="l" name="496" href="#496">&nbsp;&nbsp;&nbsp;&nbsp;496&nbsp;</a>        :return: a list of CDNPackage's from a particular erratum
<a class="l" name="497" href="#497">&nbsp;&nbsp;&nbsp;&nbsp;497&nbsp;</a>        """</span>
<a class="l" name="498" href="#498">&nbsp;&nbsp;&nbsp;&nbsp;498&nbsp;</a>        <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a> = []
<a class="l" name="499" href="#499">&nbsp;&nbsp;&nbsp;&nbsp;499&nbsp;</a>        <b>for</b> <a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a> <b>in</b> <a href="/source/s?defs=raw_packages_to_find&amp;project=SAS_10.20">raw_packages_to_find</a>:
<a class="hl" name="500" href="#500">&nbsp;&nbsp;&nbsp;&nbsp;500&nbsp;</a>            <span class="c"># we do have a package_count : int_value so we don't want to mess up</span>
<a class="l" name="501" href="#501">&nbsp;&nbsp;&nbsp;&nbsp;501&nbsp;</a>            <b>if</b> <a href="/source/s?defs=isinstance&amp;project=SAS_10.20">isinstance</a>(<a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>, <a href="/source/s?defs=dict&amp;project=SAS_10.20">dict</a>):
<a class="l" name="502" href="#502">&nbsp;&nbsp;&nbsp;&nbsp;502&nbsp;</a>                <a href="/source/s?defs=uid&amp;project=SAS_10.20">uid</a> = <span class="s">"{0}:{1}-{2}-{3}.{4}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"epoch"</span>),
<a class="l" name="503" href="#503">&nbsp;&nbsp;&nbsp;&nbsp;503&nbsp;</a>                                                   <a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"name"</span>),
<a class="l" name="504" href="#504">&nbsp;&nbsp;&nbsp;&nbsp;504&nbsp;</a>                                                   <a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"version"</span>),
<a class="l" name="505" href="#505">&nbsp;&nbsp;&nbsp;&nbsp;505&nbsp;</a>                                                   <a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"release"</span>),
<a class="l" name="506" href="#506">&nbsp;&nbsp;&nbsp;&nbsp;506&nbsp;</a>                                                   <a href="/source/s?defs=raw_package&amp;project=SAS_10.20">raw_package</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">"arch"</span>))
<a class="l" name="507" href="#507">&nbsp;&nbsp;&nbsp;&nbsp;507&nbsp;</a>                <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a> = <a href="/source/s?defs=primary_packages_dict&amp;project=SAS_10.20">primary_packages_dict</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=uid&amp;project=SAS_10.20">uid</a>, <b>None</b>)
<a class="l" name="508" href="#508">&nbsp;&nbsp;&nbsp;&nbsp;508&nbsp;</a>                <b>if</b> <a href="/source/s?defs=package&amp;project=SAS_10.20">package</a> <b>is</b> <b>not</b> <b>None</b>:
<a class="l" name="509" href="#509">&nbsp;&nbsp;&nbsp;&nbsp;509&nbsp;</a>                    <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=package&amp;project=SAS_10.20">package</a>)
<a class="hl" name="510" href="#510">&nbsp;&nbsp;&nbsp;&nbsp;510&nbsp;</a>                <b>else</b>:
<a class="l" name="511" href="#511">&nbsp;&nbsp;&nbsp;&nbsp;511&nbsp;</a>                    <b>raise</b> <a href="/source/s?defs=Error&amp;project=SAS_10.20">Error</a>(<span class="s">"Erratum package with nevra %s was not found in the repository. The package "</span>
<a class="l" name="512" href="#512">&nbsp;&nbsp;&nbsp;&nbsp;512&nbsp;</a>                                <span class="s">"was referenced from erratum: %s"</span> % (<a href="/source/s?defs=uid&amp;project=SAS_10.20">uid</a>, <a href="/source/s?defs=erratum_id&amp;project=SAS_10.20">erratum_id</a>))
<a class="l" name="513" href="#513">&nbsp;&nbsp;&nbsp;&nbsp;513&nbsp;</a>
<a class="l" name="514" href="#514">&nbsp;&nbsp;&nbsp;&nbsp;514&nbsp;</a>        <b>if</b> <a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>:
<a class="l" name="515" href="#515">&nbsp;&nbsp;&nbsp;&nbsp;515&nbsp;</a>            <b>return</b> <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>[:<a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>]
<a class="l" name="516" href="#516">&nbsp;&nbsp;&nbsp;&nbsp;516&nbsp;</a>        <b>return</b> <a href="/source/s?defs=packages&amp;project=SAS_10.20">packages</a>
<a class="l" name="517" href="#517">&nbsp;&nbsp;&nbsp;&nbsp;517&nbsp;</a>
<a class="l" name="518" href="#518">&nbsp;&nbsp;&nbsp;&nbsp;518&nbsp;</a>    <b>def</b> <a href="/source/s?defs=list_erratum&amp;project=SAS_10.20">list_erratum</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>, <a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>):
<a class="l" name="519" href="#519">&nbsp;&nbsp;&nbsp;&nbsp;519&nbsp;</a>        <span class="s">"""
<a class="hl" name="520" href="#520">&nbsp;&nbsp;&nbsp;&nbsp;520&nbsp;</a>        Returns a list of CDNErratum instances
<a class="l" name="521" href="#521">&nbsp;&nbsp;&nbsp;&nbsp;521&nbsp;</a>
<a class="l" name="522" href="#522">&nbsp;&nbsp;&nbsp;&nbsp;522&nbsp;</a>        :param conf_content_label:
<a class="l" name="523" href="#523">&nbsp;&nbsp;&nbsp;&nbsp;523&nbsp;</a>        :param imported_erratum_list: a map with the already imported erratum name as key and their version
<a class="l" name="524" href="#524">&nbsp;&nbsp;&nbsp;&nbsp;524&nbsp;</a>        :return: a list of CDNErratum's from a particular erratum
<a class="l" name="525" href="#525">&nbsp;&nbsp;&nbsp;&nbsp;525&nbsp;</a>        """</span>
<a class="l" name="526" href="#526">&nbsp;&nbsp;&nbsp;&nbsp;526&nbsp;</a>        <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=info&amp;project=SAS_10.20">info</a>(<span class="s">"Retrieving errata"</span>)
<a class="l" name="527" href="#527">&nbsp;&nbsp;&nbsp;&nbsp;527&nbsp;</a>        <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> = <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="l" name="528" href="#528">&nbsp;&nbsp;&nbsp;&nbsp;528&nbsp;</a>        <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_ent_content_label&amp;project=SAS_10.20">get_ent_content_label</a>(), <b>None</b>)
<a class="l" name="529" href="#529">&nbsp;&nbsp;&nbsp;&nbsp;529&nbsp;</a>
<a class="hl" name="530" href="#530">&nbsp;&nbsp;&nbsp;&nbsp;530&nbsp;</a>        <a href="/source/s?defs=unchange_count&amp;project=SAS_10.20">unchange_count</a> = <span class="n">0</span>
<a class="l" name="531" href="#531">&nbsp;&nbsp;&nbsp;&nbsp;531&nbsp;</a>        <a href="/source/s?defs=change_count&amp;project=SAS_10.20">change_count</a> = <span class="n">0</span>
<a class="l" name="532" href="#532">&nbsp;&nbsp;&nbsp;&nbsp;532&nbsp;</a>        <a href="/source/s?defs=new_count&amp;project=SAS_10.20">new_count</a> = <span class="n">0</span>
<a class="l" name="533" href="#533">&nbsp;&nbsp;&nbsp;&nbsp;533&nbsp;</a>        <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a> = []
<a class="l" name="534" href="#534">&nbsp;&nbsp;&nbsp;&nbsp;534&nbsp;</a>        <b>if</b> <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> <b>is</b> <b>None</b>:
<a class="l" name="535" href="#535">&nbsp;&nbsp;&nbsp;&nbsp;535&nbsp;</a>            <b>raise</b> <a href="/source/s?defs=InvalidContentName&amp;project=SAS_10.20">InvalidContentName</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="l" name="536" href="#536">&nbsp;&nbsp;&nbsp;&nbsp;536&nbsp;</a>        <span class="c"># get the repomd xml and then start parsing updateinfo xml but first look up the cache</span>
<a class="l" name="537" href="#537">&nbsp;&nbsp;&nbsp;&nbsp;537&nbsp;</a>        <a href="/source/s?defs=final_path&amp;project=SAS_10.20">final_path</a> = <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=get_expanded_path&amp;project=SAS_10.20">get_expanded_path</a>(<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>.<a href="/source/s?defs=get_content_url_vars&amp;project=SAS_10.20">get_content_url_vars</a>())
<a class="l" name="538" href="#538">&nbsp;&nbsp;&nbsp;&nbsp;538&nbsp;</a>        <a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a> = <a href="/source/s?defs=RedHatCDNRepo&amp;project=SAS_10.20">RedHatCDNRepo</a>(<a href="/source/s?defs=final_path&amp;project=SAS_10.20">final_path</a>, <a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>=<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=proxy&amp;project=SAS_10.20">proxy</a>, <a href="/source/s?defs=cert_file&amp;project=SAS_10.20">cert_file</a>=<a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=certificate_path&amp;project=SAS_10.20">certificate_path</a>)
<a class="l" name="539" href="#539">&nbsp;&nbsp;&nbsp;&nbsp;539&nbsp;</a>        <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_repomd&amp;project=SAS_10.20">__get_repomd</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="hl" name="540" href="#540">&nbsp;&nbsp;&nbsp;&nbsp;540&nbsp;</a>        <span class="c"># check if model has erratum's - there are case like beta content where there is no update-info available</span>
<a class="l" name="541" href="#541">&nbsp;&nbsp;&nbsp;&nbsp;541&nbsp;</a>        <b>if</b> <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a>.<a href="/source/s?defs=get_attributes_for&amp;project=SAS_10.20">get_attributes_for</a>(<span class="s">'updateinfo'</span>) <b>is</b> <b>None</b>:
<a class="l" name="542" href="#542">&nbsp;&nbsp;&nbsp;&nbsp;542&nbsp;</a>            <b>return</b> []
<a class="l" name="543" href="#543">&nbsp;&nbsp;&nbsp;&nbsp;543&nbsp;</a>        <span class="c"># we have the repomd file, let's look where <a href="/source/s?path=updateinfo.xml&amp;project=SAS_10.20">updateinfo.xml</a>.gz is located</span>
<a class="l" name="544" href="#544">&nbsp;&nbsp;&nbsp;&nbsp;544&nbsp;</a>        <a href="/source/s?defs=updateinfo_href&amp;project=SAS_10.20">updateinfo_href</a> = <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a>.<a href="/source/s?defs=get_attributes_for&amp;project=SAS_10.20">get_attributes_for</a>(<span class="s">'updateinfo'</span>)[<span class="s">'location'</span>][<span class="s">'href'</span>]
<a class="l" name="545" href="#545">&nbsp;&nbsp;&nbsp;&nbsp;545&nbsp;</a>        <a href="/source/s?defs=updateinfo_model&amp;project=SAS_10.20">updateinfo_model</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_updateinfo_model&amp;project=SAS_10.20">__get_updateinfo_model</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=updateinfo_href&amp;project=SAS_10.20">updateinfo_href</a>)
<a class="l" name="546" href="#546">&nbsp;&nbsp;&nbsp;&nbsp;546&nbsp;</a>
<a class="l" name="547" href="#547">&nbsp;&nbsp;&nbsp;&nbsp;547&nbsp;</a>        <a href="/source/s?defs=primary_packages&amp;project=SAS_10.20">primary_packages</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=_index_packages&amp;project=SAS_10.20">_index_packages</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=list_packages&amp;project=SAS_10.20">list_packages</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>, <a href="/source/s?defs=which_packages&amp;project=SAS_10.20">which_packages</a>=<span class="s">'all'</span>))
<a class="l" name="548" href="#548">&nbsp;&nbsp;&nbsp;&nbsp;548&nbsp;</a>
<a class="l" name="549" href="#549">&nbsp;&nbsp;&nbsp;&nbsp;549&nbsp;</a>        <b>for</b> <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a> <b>in</b> <a href="/source/s?defs=updateinfo_model&amp;project=SAS_10.20">updateinfo_model</a>.<a href="/source/s?defs=itervalues&amp;project=SAS_10.20">itervalues</a>():
<a class="hl" name="550" href="#550">&nbsp;&nbsp;&nbsp;&nbsp;550&nbsp;</a>            <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a> = <a href="/source/s?defs=CDNErratum&amp;project=SAS_10.20">CDNErratum</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a>)
<a class="l" name="551" href="#551">&nbsp;&nbsp;&nbsp;&nbsp;551&nbsp;</a>            <b>if</b> <b>not</b> <a href="/source/s?defs=str&amp;project=SAS_10.20">str</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>]) <b>in</b> <a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>:
<a class="l" name="552" href="#552">&nbsp;&nbsp;&nbsp;&nbsp;552&nbsp;</a>                <a href="/source/s?defs=new_count&amp;project=SAS_10.20">new_count</a> += <span class="n">1</span>
<a class="l" name="553" href="#553">&nbsp;&nbsp;&nbsp;&nbsp;553&nbsp;</a>                <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'packages'</span>] = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__search_erratum_packages&amp;project=SAS_10.20">__search_erratum_packages</a>(<a href="/source/s?defs=primary_packages&amp;project=SAS_10.20">primary_packages</a>,
<a class="l" name="554" href="#554">&nbsp;&nbsp;&nbsp;&nbsp;554&nbsp;</a>                                                                         <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'pkglist'</span>, {}).<a href="/source/s?defs=values&amp;project=SAS_10.20">values</a>(),
<a class="l" name="555" href="#555">&nbsp;&nbsp;&nbsp;&nbsp;555&nbsp;</a>                                                                         <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>])
<a class="l" name="556" href="#556">&nbsp;&nbsp;&nbsp;&nbsp;556&nbsp;</a>                <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>)
<a class="l" name="557" href="#557">&nbsp;&nbsp;&nbsp;&nbsp;557&nbsp;</a>            <b>elif</b> <a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'version'</span>]) &gt; <a href="/source/s?defs=int&amp;project=SAS_10.20">int</a>(<a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>], <span class="n">0</span>)):
<a class="l" name="558" href="#558">&nbsp;&nbsp;&nbsp;&nbsp;558&nbsp;</a>                <a href="/source/s?defs=change_count&amp;project=SAS_10.20">change_count</a> += <span class="n">1</span>
<a class="l" name="559" href="#559">&nbsp;&nbsp;&nbsp;&nbsp;559&nbsp;</a>                <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'packages'</span>] = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__search_erratum_packages&amp;project=SAS_10.20">__search_erratum_packages</a>(<a href="/source/s?defs=primary_packages&amp;project=SAS_10.20">primary_packages</a>,
<a class="hl" name="560" href="#560">&nbsp;&nbsp;&nbsp;&nbsp;560&nbsp;</a>                                                                         <a href="/source/s?defs=erratum&amp;project=SAS_10.20">erratum</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<span class="s">'pkglist'</span>, {}).<a href="/source/s?defs=values&amp;project=SAS_10.20">values</a>(),
<a class="l" name="561" href="#561">&nbsp;&nbsp;&nbsp;&nbsp;561&nbsp;</a>                                                                         <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>])
<a class="l" name="562" href="#562">&nbsp;&nbsp;&nbsp;&nbsp;562&nbsp;</a>                <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a>.<a href="/source/s?defs=append&amp;project=SAS_10.20">append</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>)
<a class="l" name="563" href="#563">&nbsp;&nbsp;&nbsp;&nbsp;563&nbsp;</a>                <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=info&amp;project=SAS_10.20">info</a>(<span class="s">"Erratum updated since last redhat_import: [{0}]. Previous version = {1}. Current version: {2}"</span>
<a class="l" name="564" href="#564">&nbsp;&nbsp;&nbsp;&nbsp;564&nbsp;</a>                         .<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>],
<a class="l" name="565" href="#565">&nbsp;&nbsp;&nbsp;&nbsp;565&nbsp;</a>                                 <a href="/source/s?defs=imported_erratum_list&amp;project=SAS_10.20">imported_erratum_list</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>], <span class="n">0</span>), <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'version'</span>]))
<a class="l" name="566" href="#566">&nbsp;&nbsp;&nbsp;&nbsp;566&nbsp;</a>            <b>else</b>:
<a class="l" name="567" href="#567">&nbsp;&nbsp;&nbsp;&nbsp;567&nbsp;</a>                <a href="/source/s?defs=unchange_count&amp;project=SAS_10.20">unchange_count</a> += <span class="n">1</span>
<a class="l" name="568" href="#568">&nbsp;&nbsp;&nbsp;&nbsp;568&nbsp;</a>                <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=debug&amp;project=SAS_10.20">debug</a>(
<a class="l" name="569" href="#569">&nbsp;&nbsp;&nbsp;&nbsp;569&nbsp;</a>                    <span class="s">"Unchange count = {0}. No change since last redhat_import :  Erratum: [{1}] version: {2}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(
<a class="hl" name="570" href="#570">&nbsp;&nbsp;&nbsp;&nbsp;570&nbsp;</a>                        <a href="/source/s?defs=unchange_count&amp;project=SAS_10.20">unchange_count</a>, <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'errata_advisory'</span>], <a href="/source/s?defs=cdn_erratum&amp;project=SAS_10.20">cdn_erratum</a>[<span class="s">'version'</span>]))
<a class="l" name="571" href="#571">&nbsp;&nbsp;&nbsp;&nbsp;571&nbsp;</a>
<a class="l" name="572" href="#572">&nbsp;&nbsp;&nbsp;&nbsp;572&nbsp;</a>        <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a>.<a href="/source/s?defs=sort&amp;project=SAS_10.20">sort</a>(<a href="/source/s?defs=key&amp;project=SAS_10.20">key</a>=<b>lambda</b> <a href="/source/s?defs=er&amp;project=SAS_10.20">er</a>: <a href="/source/s?defs=er&amp;project=SAS_10.20">er</a>[<span class="s">'errata_update_date'</span>], <a href="/source/s?defs=reverse&amp;project=SAS_10.20">reverse</a>=<a href="/source/s?defs=True&amp;project=SAS_10.20">True</a>)
<a class="l" name="573" href="#573">&nbsp;&nbsp;&nbsp;&nbsp;573&nbsp;</a>        <a href="/source/s?defs=log&amp;project=SAS_10.20">log</a>.<a href="/source/s?defs=info&amp;project=SAS_10.20">info</a>(<span class="s">"Unchange count = {0}. Updated count = {1}. New count = {2} since last redhat_import"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(
<a class="l" name="574" href="#574">&nbsp;&nbsp;&nbsp;&nbsp;574&nbsp;</a>            <a href="/source/s?defs=unchange_count&amp;project=SAS_10.20">unchange_count</a>, <a href="/source/s?defs=change_count&amp;project=SAS_10.20">change_count</a>, <a href="/source/s?defs=new_count&amp;project=SAS_10.20">new_count</a>))
<a class="l" name="575" href="#575">&nbsp;&nbsp;&nbsp;&nbsp;575&nbsp;</a>        <b>if</b> <a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>:
<a class="l" name="576" href="#576">&nbsp;&nbsp;&nbsp;&nbsp;576&nbsp;</a>            <b>return</b> <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a>[:<a href="/source/s?defs=dbg_short_circuit&amp;project=SAS_10.20">dbg_short_circuit</a>.<a href="/source/s?defs=short_circuit&amp;project=SAS_10.20">short_circuit</a>]
<a class="l" name="577" href="#577">&nbsp;&nbsp;&nbsp;&nbsp;577&nbsp;</a>        <b>return</b> <a href="/source/s?defs=erratums&amp;project=SAS_10.20">erratums</a>
<a class="l" name="578" href="#578">&nbsp;&nbsp;&nbsp;&nbsp;578&nbsp;</a>
<a class="l" name="579" href="#579">&nbsp;&nbsp;&nbsp;&nbsp;579&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="hl" name="580" href="#580">&nbsp;&nbsp;&nbsp;&nbsp;580&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_updateinfo_model&amp;project=SAS_10.20">__get_updateinfo_model</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=updateinfo_href&amp;project=SAS_10.20">updateinfo_href</a>):
<a class="l" name="581" href="#581">&nbsp;&nbsp;&nbsp;&nbsp;581&nbsp;</a>        <span class="s">"""
<a class="l" name="582" href="#582">&nbsp;&nbsp;&nbsp;&nbsp;582&nbsp;</a>        Gets the raw model of the <a href="/source/s?path=updateinfo.xml&amp;project=SAS_10.20">updateinfo.xml</a>.gz file identified by the given updateinfo_href. The raw model
<a class="l" name="583" href="#583">&nbsp;&nbsp;&nbsp;&nbsp;583&nbsp;</a>        is obtained by downloading the file from CDN repository, expanding the archive and parsing it.
<a class="l" name="584" href="#584">&nbsp;&nbsp;&nbsp;&nbsp;584&nbsp;</a>
<a class="l" name="585" href="#585">&nbsp;&nbsp;&nbsp;&nbsp;585&nbsp;</a>        :param cdn: a RedHatCDNRepo instance
<a class="l" name="586" href="#586">&nbsp;&nbsp;&nbsp;&nbsp;586&nbsp;</a>        :param updateinfo_href: a remote path for <a href="/source/s?path=updateinfo.xml&amp;project=SAS_10.20">updateinfo.xml</a>.gz
<a class="l" name="587" href="#587">&nbsp;&nbsp;&nbsp;&nbsp;587&nbsp;</a>        :return: a UpdateInfoXMLCollector instance
<a class="l" name="588" href="#588">&nbsp;&nbsp;&nbsp;&nbsp;588&nbsp;</a>        """</span>
<a class="l" name="589" href="#589">&nbsp;&nbsp;&nbsp;&nbsp;589&nbsp;</a>
<a class="hl" name="590" href="#590">&nbsp;&nbsp;&nbsp;&nbsp;590&nbsp;</a>        <span class="c"># get updateinfo xml file, parse, digest and then get updateinfo model</span>
<a class="l" name="591" href="#591">&nbsp;&nbsp;&nbsp;&nbsp;591&nbsp;</a>        <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a> = <a href="/source/s?defs=UpdateInfoXMLParser&amp;project=SAS_10.20">UpdateInfoXMLParser</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>.<a href="/source/s?defs=get_cdn_xml&amp;project=SAS_10.20">get_cdn_xml</a>(<a href="/source/s?defs=updateinfo_href&amp;project=SAS_10.20">updateinfo_href</a>))
<a class="l" name="592" href="#592">&nbsp;&nbsp;&nbsp;&nbsp;592&nbsp;</a>        <b>return</b> <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a>.<a href="/source/s?defs=get_collector&amp;project=SAS_10.20">get_collector</a>()
<a class="l" name="593" href="#593">&nbsp;&nbsp;&nbsp;&nbsp;593&nbsp;</a>
<a class="l" name="594" href="#594">&nbsp;&nbsp;&nbsp;&nbsp;594&nbsp;</a>    @<a href="/source/s?defs=staticmethod&amp;project=SAS_10.20">staticmethod</a>
<a class="l" name="595" href="#595">&nbsp;&nbsp;&nbsp;&nbsp;595&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_primary_model&amp;project=SAS_10.20">__get_primary_model</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=primary_href&amp;project=SAS_10.20">primary_href</a>):
<a class="l" name="596" href="#596">&nbsp;&nbsp;&nbsp;&nbsp;596&nbsp;</a>        <span class="s">"""
<a class="l" name="597" href="#597">&nbsp;&nbsp;&nbsp;&nbsp;597&nbsp;</a>        Gets the raw model of the <a href="/source/s?path=primary.xml&amp;project=SAS_10.20">primary.xml</a>.gz file identified by the given primary_href. The raw model
<a class="l" name="598" href="#598">&nbsp;&nbsp;&nbsp;&nbsp;598&nbsp;</a>        is obtained by downloading the file from CDN repository, expanding the archive and parsing it.
<a class="l" name="599" href="#599">&nbsp;&nbsp;&nbsp;&nbsp;599&nbsp;</a>
<a class="hl" name="600" href="#600">&nbsp;&nbsp;&nbsp;&nbsp;600&nbsp;</a>        :param cdn: a RedHatCDNRepo instance
<a class="l" name="601" href="#601">&nbsp;&nbsp;&nbsp;&nbsp;601&nbsp;</a>        :param primary_href: a remote path for <a href="/source/s?path=primary.xml&amp;project=SAS_10.20">primary.xml</a>.gz
<a class="l" name="602" href="#602">&nbsp;&nbsp;&nbsp;&nbsp;602&nbsp;</a>        :return: a PrimaryXMLCollector instance
<a class="l" name="603" href="#603">&nbsp;&nbsp;&nbsp;&nbsp;603&nbsp;</a>        """</span>
<a class="l" name="604" href="#604">&nbsp;&nbsp;&nbsp;&nbsp;604&nbsp;</a>
<a class="l" name="605" href="#605">&nbsp;&nbsp;&nbsp;&nbsp;605&nbsp;</a>        <span class="c"># get primary xml file, parse, digest and then get primary model</span>
<a class="l" name="606" href="#606">&nbsp;&nbsp;&nbsp;&nbsp;606&nbsp;</a>        <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a> = <a href="/source/s?defs=PrimaryXMLParser&amp;project=SAS_10.20">PrimaryXMLParser</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>.<a href="/source/s?defs=get_cdn_xml&amp;project=SAS_10.20">get_cdn_xml</a>(<a href="/source/s?defs=primary_href&amp;project=SAS_10.20">primary_href</a>))
<a class="l" name="607" href="#607">&nbsp;&nbsp;&nbsp;&nbsp;607&nbsp;</a>        <b>return</b> <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a>.<a href="/source/s?defs=get_collector&amp;project=SAS_10.20">get_collector</a>()
<a class="l" name="608" href="#608">&nbsp;&nbsp;&nbsp;&nbsp;608&nbsp;</a>
<a class="l" name="609" href="#609">&nbsp;&nbsp;&nbsp;&nbsp;609&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_repomd&amp;project=SAS_10.20">__get_repomd</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>, <a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>):
<a class="hl" name="610" href="#610">&nbsp;&nbsp;&nbsp;&nbsp;610&nbsp;</a>        <span class="s">"""
<a class="l" name="611" href="#611">&nbsp;&nbsp;&nbsp;&nbsp;611&nbsp;</a>        Searches internal cache for the repomd model. If not found the <a href="/source/s?path=repomd.xml&amp;project=SAS_10.20">repomd.xml</a>
<a class="l" name="612" href="#612">&nbsp;&nbsp;&nbsp;&nbsp;612&nbsp;</a>        file that corresponds to content label is parsed and a model is returned.
<a class="l" name="613" href="#613">&nbsp;&nbsp;&nbsp;&nbsp;613&nbsp;</a>
<a class="l" name="614" href="#614">&nbsp;&nbsp;&nbsp;&nbsp;614&nbsp;</a>        :param cdn: a RedHatCDNRepo instance
<a class="l" name="615" href="#615">&nbsp;&nbsp;&nbsp;&nbsp;615&nbsp;</a>        :param conf_content_label: a string content label
<a class="l" name="616" href="#616">&nbsp;&nbsp;&nbsp;&nbsp;616&nbsp;</a>        :return: a RepomdXMLCollector instance
<a class="l" name="617" href="#617">&nbsp;&nbsp;&nbsp;&nbsp;617&nbsp;</a>        """</span>
<a class="l" name="618" href="#618">&nbsp;&nbsp;&nbsp;&nbsp;618&nbsp;</a>        <b>if</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__repomd_cache&amp;project=SAS_10.20">__repomd_cache</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>):
<a class="l" name="619" href="#619">&nbsp;&nbsp;&nbsp;&nbsp;619&nbsp;</a>            <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__repomd_cache&amp;project=SAS_10.20">__repomd_cache</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>)
<a class="hl" name="620" href="#620">&nbsp;&nbsp;&nbsp;&nbsp;620&nbsp;</a>        <b>else</b>:
<a class="l" name="621" href="#621">&nbsp;&nbsp;&nbsp;&nbsp;621&nbsp;</a>            <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a> = <a href="/source/s?defs=RepomdXMLParser&amp;project=SAS_10.20">RepomdXMLParser</a>(<a href="/source/s?defs=cdn&amp;project=SAS_10.20">cdn</a>.<a href="/source/s?defs=get_cdn_repomd&amp;project=SAS_10.20">get_cdn_repomd</a>())
<a class="l" name="622" href="#622">&nbsp;&nbsp;&nbsp;&nbsp;622&nbsp;</a>            <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a> = <a href="/source/s?defs=parser&amp;project=SAS_10.20">parser</a>.<a href="/source/s?defs=get_collector&amp;project=SAS_10.20">get_collector</a>()
<a class="l" name="623" href="#623">&nbsp;&nbsp;&nbsp;&nbsp;623&nbsp;</a>            <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__repomd_cache&amp;project=SAS_10.20">__repomd_cache</a>[<a href="/source/s?defs=conf_content_label&amp;project=SAS_10.20">conf_content_label</a>] = <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a>
<a class="l" name="624" href="#624">&nbsp;&nbsp;&nbsp;&nbsp;624&nbsp;</a>
<a class="l" name="625" href="#625">&nbsp;&nbsp;&nbsp;&nbsp;625&nbsp;</a>        <b>return</b> <a href="/source/s?defs=repomd_model&amp;project=SAS_10.20">repomd_model</a>
<a class="l" name="626" href="#626">&nbsp;&nbsp;&nbsp;&nbsp;626&nbsp;</a>
<a class="l" name="627" href="#627">&nbsp;&nbsp;&nbsp;&nbsp;627&nbsp;</a>    @<a href="/source/s?defs=property&amp;project=SAS_10.20">property</a>
<a class="l" name="628" href="#628">&nbsp;&nbsp;&nbsp;&nbsp;628&nbsp;</a>    <b>def</b> <a href="/source/s?defs=enabled_channels&amp;project=SAS_10.20">enabled_channels</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="629" href="#629">&nbsp;&nbsp;&nbsp;&nbsp;629&nbsp;</a>        <b>return</b> [<a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> <b>for</b> <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=itervalues&amp;project=SAS_10.20">itervalues</a>() <b>if</b> <a href="/source/s?defs=content&amp;project=SAS_10.20">content</a>.<a href="/source/s?defs=conf&amp;project=SAS_10.20">conf</a>[<span class="s">"enabled"</span>]]
<a class="hl" name="630" href="#630">&nbsp;&nbsp;&nbsp;&nbsp;630&nbsp;</a>
<a class="l" name="631" href="#631">&nbsp;&nbsp;&nbsp;&nbsp;631&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__get_content_info&amp;project=SAS_10.20">__get_content_info</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>, <a href="/source/s?defs=content_name&amp;project=SAS_10.20">content_name</a>, <a href="/source/s?defs=content_platform&amp;project=SAS_10.20">content_platform</a>, <a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>):
<a class="l" name="632" href="#632">&nbsp;&nbsp;&nbsp;&nbsp;632&nbsp;</a>        <b>return</b> [<span class="s">" * {0}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=content_name&amp;project=SAS_10.20">content_name</a>), <span class="s">"   HPSA Platform: {0}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=content_platform&amp;project=SAS_10.20">content_platform</a>),
<a class="l" name="633" href="#633">&nbsp;&nbsp;&nbsp;&nbsp;633&nbsp;</a>                <span class="s">"   Label: {0}"</span>.<a href="/source/s?defs=format&amp;project=SAS_10.20">format</a>(<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>)]
<a class="l" name="634" href="#634">&nbsp;&nbsp;&nbsp;&nbsp;634&nbsp;</a>
<a class="l" name="635" href="#635">&nbsp;&nbsp;&nbsp;&nbsp;635&nbsp;</a>    <b>def</b> <a href="/source/s?defs=__str__&amp;project=SAS_10.20">__str__</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>):
<a class="l" name="636" href="#636">&nbsp;&nbsp;&nbsp;&nbsp;636&nbsp;</a>        s = []
<a class="l" name="637" href="#637">&nbsp;&nbsp;&nbsp;&nbsp;637&nbsp;</a>        <b>for</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__platform_guide&amp;project=SAS_10.20">__platform_guide</a>.<a href="/source/s?defs=sa_platforms&amp;project=SAS_10.20">sa_platforms</a>:
<a class="l" name="638" href="#638">&nbsp;&nbsp;&nbsp;&nbsp;638&nbsp;</a>            <span class="c"># if it is configured in the conf we are going to print it later.</span>
<a class="l" name="639" href="#639">&nbsp;&nbsp;&nbsp;&nbsp;639&nbsp;</a>            <b>if</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> <b>is</b> <b>not</b> <b>None</b> <b>and</b> <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a> <b>not</b> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>:
<a class="hl" name="640" href="#640">&nbsp;&nbsp;&nbsp;&nbsp;640&nbsp;</a>                <a href="/source/s?defs=cdn_content_descriptor&amp;project=SAS_10.20">cdn_content_descriptor</a> = <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__content_cache&amp;project=SAS_10.20">__content_cache</a>.<a href="/source/s?defs=get&amp;project=SAS_10.20">get</a>(
<a class="l" name="641" href="#641">&nbsp;&nbsp;&nbsp;&nbsp;641&nbsp;</a>                    <a href="/source/s?defs=ContentLabel&amp;project=SAS_10.20">ContentLabel</a>(<a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>).<a href="/source/s?defs=get_ent_content_label&amp;project=SAS_10.20">get_ent_content_label</a>())
<a class="l" name="642" href="#642">&nbsp;&nbsp;&nbsp;&nbsp;642&nbsp;</a>                <b>if</b> <a href="/source/s?defs=cdn_content_descriptor&amp;project=SAS_10.20">cdn_content_descriptor</a> <b>is</b> <b>not</b> <b>None</b>:
<a class="l" name="643" href="#643">&nbsp;&nbsp;&nbsp;&nbsp;643&nbsp;</a>                    s.<a href="/source/s?defs=extend&amp;project=SAS_10.20">extend</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_content_info&amp;project=SAS_10.20">__get_content_info</a>(<a href="/source/s?defs=cdn_content_descriptor&amp;project=SAS_10.20">cdn_content_descriptor</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>,
<a class="l" name="644" href="#644">&nbsp;&nbsp;&nbsp;&nbsp;644&nbsp;</a>                                                     <a href="/source/s?defs=platform&amp;project=SAS_10.20">platform</a>.<a href="/source/s?defs=content_label&amp;project=SAS_10.20">content_label</a>))
<a class="l" name="645" href="#645">&nbsp;&nbsp;&nbsp;&nbsp;645&nbsp;</a>
<a class="l" name="646" href="#646">&nbsp;&nbsp;&nbsp;&nbsp;646&nbsp;</a>        <b>for</b> <a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a> <b>in</b> <a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=values&amp;project=SAS_10.20">values</a>():
<a class="l" name="647" href="#647">&nbsp;&nbsp;&nbsp;&nbsp;647&nbsp;</a>            s.<a href="/source/s?defs=extend&amp;project=SAS_10.20">extend</a>(<a href="/source/s?defs=self&amp;project=SAS_10.20">self</a>.<a href="/source/s?defs=__get_content_info&amp;project=SAS_10.20">__get_content_info</a>(<a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a>.<a href="/source/s?defs=name&amp;project=SAS_10.20">name</a>, <a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a>.<a href="/source/s?defs=platform_name&amp;project=SAS_10.20">platform_name</a>, <a href="/source/s?defs=cdn_content&amp;project=SAS_10.20">cdn_content</a>.<a href="/source/s?defs=label&amp;project=SAS_10.20">label</a>))
<a class="l" name="648" href="#648">&nbsp;&nbsp;&nbsp;&nbsp;648&nbsp;</a>
<a class="l" name="649" href="#649">&nbsp;&nbsp;&nbsp;&nbsp;649&nbsp;</a>        <b>return</b> <span class="s">"\n"</span>.<a href="/source/s?defs=join&amp;project=SAS_10.20">join</a>(s)
<a class="hl" name="650" href="#650">&nbsp;&nbsp;&nbsp;&nbsp;650&nbsp;</a></pre></div>

<div id="Footer">
    <p class="Center">
        <a href="http://www.opensolaris.org/os/project/opengrok/"><img src="/source/default/img/servedby.png" alt="Served by OpenGrok" title="Served by OpenGrok"/></a>
    </p>
    <p class="Center">Indexes created Sat Apr 11 05:37:35 UTC 2015
    </p>
</div>
</div>
</div>

</body>
</html>

