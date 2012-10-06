<%@ page language="java" contentType="text/html"%>

<%
	String carName = request.getParameter("carName");
	String carId = request.getParameter("carId");
%>

<div class="well span3" style="padding: 8px 0;">
	<ul class="nav nav-list">
		<li class="nav-header">Navigate</li>
		<li><a href="/user/car.jsp?carId=<%=carId %>"><%=carName %></a></li>
		<li>
			<ul>
				<li><a href="/user/expenseTracker.jsp?carId=<%=carId %>">Expense Manager</a></li>
				<li><a href="/user/maintenance.jsp?carId=<%=carId %>">Maintenance Records</a></li>
				<li><a href="/user/gasMileage.jsp?carId=<%=carId %>">Gas Mileage Tracking</a></li>
				<li><a href="/user/charts.jsp?carId=<%=carId %>">Charts</a></li>
				<li><a href="/user/news.jsp?carId=<%=carId %>">News</a></li>
			</ul>
		</li>
	</ul>
</div>