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
	
	<script type="text/javascript">
		
		$().ready(function() {
			// When the user chooses a new make, get the models
			// for the updated make
			$("#makes").change(function() {
				if ($("#makes").prop("selectedIndex") !== 0) {
					$.get('/cars/raw/' + $("#makes").val(), function(data) {
						var optionString = [];
						
						optionString.push("<option>Select a model</option>");
						
						$.each(data, function(i) {
							optionString.push("<option>" + data[i] + "</option>");
						});
						
						$("#models").html(optionString.join(""));
						$("#years").html("<option>Select a year</option>");
					});
				} else {
					$("#models").html("<option>Select a model</option>");
					$("#years").html("<option>Select a year</option>");
				}
			});
			
			$("#models").change(function() {
				if ($("#models").prop("selectedIndex") !== 0) {
					$.get('/cars/raw/' + $("#makes").val() + '/' + $("#models").val(), function(data) {
						var optionString = [];
						
						optionString.push("<option>Select a year</option>");
						
						$.each(data, function(i) {
							optionString.push("<option>" + data[i] + "</option>");
						});
						
						$("#years").html(optionString.join(""));
					});
				} else {
					$("#years").html("<option>Select a year</option>");
				}
			});
		});
	
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
					<jsp:include page="/navbar.jsp" />
					
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container-fluid center-block">
		<div class="well well-small">
			<h2>Add Vehicle</h2>

			<p>Make</p>
			<select id="makes">
				<option>Select a make</option>
				<% for (String s : DatastoreUtils.getListOfMakes()) { %>
					<option><%= s %></option>
				<% } %>
			</select>

			<p>Model</p>
			<select id="models">
				<option>Select a model</option>
			</select>
			
			<p>Year</p>
			<select id="years">
				<option>Select a year</option>
			</select>
		</div>
	</div>
</body>
</html>