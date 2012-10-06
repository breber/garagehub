<%@page language="java" contentType="text/html"%>
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
				<jsp:param value='<%=request.getParameter("carName") %>' name="carName"/>
			</jsp:include>

			<div class="well span9">
				<h2><%=request.getParameter("carName") %></h2>

				<p>Some info about <%=request.getParameter("carName") %></p>
			</div>
		</div>
	</div>
</body>
</html>