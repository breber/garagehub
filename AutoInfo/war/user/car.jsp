<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
	String carId = request.getParameter("carId");
	UserVehicle vehicle = DatastoreUtils.getUserVehicle(user, carId);
	String carName = vehicle.toString();
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />
	
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
				<h2><%=carName %></h2>

				<p>Some info about <%=carName %></p>
			</div>
		</div>
	</div>
</body>
</html>