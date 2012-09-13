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
	    google.load("search", "1");
	
	    // Call this function when the page has been loaded
	    function initialize() {
	      var searchControl = new google.search.SearchControl();
	      searchControl.addSearcher(new google.search.WebSearch());
	      searchControl.addSearcher(new google.search.NewsSearch());
	      searchControl.draw(document.getElementById("searchresults"));
	    }
	    google.setOnLoadCallback(initialize);
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