<%@ page language="java" contentType="text/html"%>

<%
	String carName = request.getParameter("carName");
%>

<div class="well span3" style="padding: 8px 0;">
	<ul class="nav nav-list">
		<li class="nav-header">Navigate</li>
		<li><a href="/user/car.jsp?carName=<%=carName %>"><%=carName %></a></li>
		<li>
			<ul>
			<li><a href="/user/expenseTracker.jsp?carName=<%=carName %>">Expense Manager</a></li>
			<li><a href="/user/maintenance.jsp?carName=<%=carName %>">Maintenance Records</a></li>
			<li><a href="/user/gasMileage.jsp?carName=<%=carName %>">Gas Mileage Tracking</a></li>
			<li><a href="/user/news.jsp?carName=<%=carName %>">News</a></li>
			</ul>
		</li>
	</ul>
</div>