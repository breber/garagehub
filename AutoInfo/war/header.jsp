<div class="navbar navbar-fixed-top">
	<div class="navbar-inner">
		<div class="container">
			<a class="brand" href="/">Auto Info</a>
			
			<ul class="nav pull-right">
			<%
			if (Boolean.parseBoolean(request.getParameter("showAdminLink"))) {
			%>
			<li><a href="/admin/admin.jsp">Admin</a></li>
			<%
			}
			%>
			</ul>
		</div>
	</div>
</div>

