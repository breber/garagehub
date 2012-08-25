<%@page import="edu.se319.team1.autoinfo.UserWrapper"%>
<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@ page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance();
%>

<% if (user.isLoggedIn()) { %>
<li>
	<a href="http://gravatar.com/emails" style="padding:0 0 0;" rel="tooltip" title="Change your avatar at gravatar.com" data-placement="bottom">
		<img src="http://www.gravatar.com/avatar/<%=user.getMd5() %>?s=40" />
	</a>
</li>
<li>
	<a href="javascript:void(0);"><%=user.getNickname() %></a>
</li>
<% } else { %>
<li>
	<a href="<%= UserServiceFactory.getUserService().createLoginURL("/") %>">Login</a>
</li>
<% } %>