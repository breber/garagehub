<%@page import="java.util.ArrayList"%>
<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance();
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />
	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<script type="text/javascript">
	// This code generates a "Raw Searcher" to handle search queries. The Raw 
    // Searcher requires you to handle and draw the search results manually.
    google.load('search', '1');

    var newsSearch;

    function searchComplete() {

      // Check that we got results
      document.getElementById('searchresults').innerHTML = '';
      if (newsSearch.results && newsSearch.results.length > 0) {
        for (var i = 0; i < newsSearch.results.length; i++) {

          // Create HTML elements for search results
          var p = document.createElement('p');
          var a = document.createElement('a');
          a.href = newsSearch.results[i].unescapedUrl;
          a.innerHTML = newsSearch.results[i].title;

          // Append search results to the HTML nodes
          p.appendChild(a);
          document.getElementById('searchresults').appendChild(p);
        }
      }
    }

    function onLoad() {

      // Create a News Search instance.
      newsSearch = new google.search.NewsSearch();

      // Set searchComplete as the callback function when a search is 
      // complete.  The newsSearch object will have results in it.
      newsSearch.setSearchCompleteCallback(this, searchComplete, null);

      // Specify search quer(ies)
      newsSearch.execute('Honda CRV');

      // Include the required Google branding
      google.search.Search.getBranding('branding');
    }

    // Set a callback to call your code when the page loads
    google.setOnLoadCallback(onLoad);
	</script>
	
	<title>CarHub</title>
</head>
<body>
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</a>
			
				<a class="brand" href="/">CarHub</a>
				
				<div class="nav-collapse collapse">
					<jsp:include page="/user/navbar.jsp" />
					
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

<div class="container-fluid center-block">
		<div class="row-fluid">
			<jsp:include page="/sideNav.jsp" />

			<div class="well well-small span9">
				<h2>News</h2>

				<div class="well well-small">
					<div id="searchresults"></div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>