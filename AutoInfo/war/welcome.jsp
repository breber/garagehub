<%@page import="com.google.appengine.api.users.UserService"%>
<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page language="java" contentType="text/html"%>

<%
	UserService user = UserServiceFactory.getUserService();
%>

<div class="container-fluid center-block">
	<div>
		<h2>Please log in...</h2>
		
		<table class="table">
			<tr>
				<td><a href="<%=user.createLoginURL("/index.jsp", null, "https://www.google.com/accounts/o8/id", null)%>" title="Google"><img src="/img/google.png"></img></a></td>
				<td><a href="<%=user.createLoginURL("/index.jsp", null, "https://me.yahoo.com", null)%>" title="Yahoo"><img src="/img/yahoo.png"></img></a></td>
			</tr>
			<tr>
				<td><a href="" title="Blogger"><img src="/img/blogger.png"></img></a></td>
				<td><a href="" title="Flickr"><img src="/img/flickr.png"></img></a></td>
			</tr>
			<tr>
				<td><a href="" title="LiveJournal"><img src="/img/livejournal.png"></img></a></td>
				<td><a href="<%=user.createLoginURL("/index.jsp", null, "http://www.myspace.com/openid", null)%>" title="MySpace"><img src="/img/myspace.gif"></img></a></td>
			</tr>
			<tr>
				<td colspan="2">
					<a href="" title="Wordpress" class="center-block"><img src="/img/wordpress.png"></img></a>
				</td>
			</tr>
		</table>
	</div>
</div>