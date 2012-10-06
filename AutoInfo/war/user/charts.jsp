<%@page import="edu.se319.team1.carhub.PathUtils"%>
<%@page import="java.util.List"%>
<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	List<String> parsedPath = PathUtils.parsePath(request.getPathInfo());
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
	String carId = parsedPath.get(parsedPath.size() - 1);
	UserVehicle vehicle = DatastoreUtils.getUserVehicle(user, carId);
	String carName = vehicle.toString();
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
	<jsp:include page="/user/navbar.jsp" />
	
	<div class="container-fluid center-block">
		<div class="row-fluid">
			<jsp:include page="/sideNav.jsp">
				<jsp:param value='<%=carName %>' name="carName"/>
				<jsp:param value='<%=carId %>' name="carId"/>
			</jsp:include>

			<div class="well span9">
				<div id="chart_div"></div>
			</div>
		</div>
	</div>
</body>
</html>