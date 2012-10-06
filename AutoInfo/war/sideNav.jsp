<%@ page language="java" contentType="text/html"%>

<%
	String carName = request.getParameter("carName");
	String carId = request.getParameter("carId");
%>
<div class="well span3" style="padding: 8px 0;">
	<ul class="nav nav-list">
		<li class="nav-header">Navigate</li>
		<li><a href="/vehicle/<%=carId %>"><%=carName %></a></li>
		<li>
			<ul>
				<li><a href="/vehicle/expenses/<%=carId %>">Expense Manager</a></li>
				<li><a href="/vehicle/maintenance/<%=carId %>">Maintenance Records</a></li>
				<li><a href="/vehicle/gasmileage/<%=carId %>">Gas Mileage Tracking</a></li>
				<li><a href="/vehicle/charts/<%=carId %>">Charts</a></li>
				<li><a href="/vehicle/news/<%=carId %>">News</a></li>
			</ul>
		</li>
	</ul>
</div>