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
		google.load("visualization", "1", {packages:["corechart"]});
		google.setOnLoadCallback(drawChart);
	
		function drawChart() {
			var data = new google.visualization.DataTable();
			data.addColumn('string', '');
			data.addColumn('number', '');

			var currentDate = new Date();
			var arr = [];
			for (var i = 10; i >= 0; i--) {
				var rand = Math.random();
				var result = 35;
				if (rand > .5) {
					result += (rand * 5); 
				} else {
					result -= (rand * 5);
				}
				
				var tmp = [];
				var tmpDate = new Date(currentDate.getTime() - (i * 604800000));
				tmp.push((tmpDate.getMonth() + 1) + "/" + tmpDate.getDate());
				tmp.push(result);
				
				arr.push(tmp);
			}
			
			data.addRows(arr);

			var options = { title: 'Average Gas Milage' };
	        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	        chart.draw(data, options);
		}
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
		<div class="well well-small">
			<div id="chart_div"></div>
		</div>
	</div>
</body>
</html>