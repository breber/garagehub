<%@page import="java.util.ArrayList"%>
<%@page import="edu.se319.team1.autoinfo.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.autoinfo.UserWrapper"%>
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
					$.get('/cars/models/' + $("#makes").val(), function(data) {
						var optionString = [];
						
						optionString.push("<option>Select a model</option>");
						
						$.each(data, function(i) {
							optionString.push("<option>" + data[i] + "</option>");
						});
						
						$("#models").html(optionString.join(""));
					});
				} else {
					$("#models").html("<option>Select a model</option>");
				}
			});
		});
	
	</script>
	
	<title>Automotive Info</title>
</head>
<body>
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="brand" href="/">Automotive Info</a>
				<ul class="nav">
					<li><a href="/">Home</a></li>
				</ul>
				
				<ul class="nav pull-right">
					<jsp:include page="/username.jsp" />
				</ul>
			</div>
		</div>
	</div>

	<div class="container">
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
		</div>
	</div>
</body>
</html>