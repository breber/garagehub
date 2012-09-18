<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance();
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
			<div class="well well-small span9">
				<h2>Settings</h2>

				<div class="control-group">
	                <label class="control-label" for="username"><b>Username</b></label>
	                <div class="controls">
	                	<input type="text" id="username" name="username" disabled="disabled" value="<%= user.getNickname() %>"/>
                	</div>
            	</div>
            	
				<div class="control-group">
	                <label class="control-label" for="avatar"><b>Avatar</b></label>
	                <div class="controls">
	                	<img src="http://www.gravatar.com/avatar/<%=user.getMd5() %>?s=40" />
	                	<a href="http://gravatar.com">Chage your avatar at Gravatar.com</a>
                	</div>
            	</div>
			</div>
		</div>
	</div>
</body>
</html>