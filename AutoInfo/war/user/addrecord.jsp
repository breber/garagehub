<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
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
			<jsp:include page="/sideNav.jsp" />

			<div class="well span9">
				<h2>Add Record</h2>

				<form id="maintenanceForm" class="form-horizontal">
				  <div class="control-group">
				    <label class="control-label" for="categorySelect">Select Category</label>
				    <div class="controls">
				      <select id="categorySelect" onchange="populateForm()">
				      	<option>Oil Change</option>
				      	<option>Car Wash</option>
				      	<option>Miscellaneous</option>
				      </select>
				    </div>
				  </div>
				  <div class="control-group">
				    <label class="control-label" for="inputPassword">Password</label>
				    <div class="controls">
				      <input type="password" id="inputPassword" placeholder="Password">
				    </div>
				  </div>
				  <div class="form-actions">
					<button type="submit" class="btn btn-primary">Save</button>
					<button type="button" class="btn">Cancel</button>
				  </div>
				</form>
			</div>
		</div>
	</div>
	
	<script type="text/javascript">
	
	function populateForm() {
		var dateDiv = document.createElement('div');
		dateDiv.setAttribute("class", "control-group");
		var dateLabel = document.createElement('label');
		dateLabel.setAttribute("class", "control-label");
		dateLabel.setAttribute("for", "dateField");
		dateLabel.innerHTML = "Date";
		dateDiv.appendChild(dateLabel);
		var dateField = document.createElement('input');
		dateField.setAttribute("type", "text");
		dateField.setAttribute("id", "dateField");
		var dateFieldDiv = document.createElement('div');
		dateFieldDiv.setAttribute("class", "controls");
		dateFieldDiv.appendChild(dateField);
		dateDiv.appendChild(dateFieldDiv);
		document.getElementById('maintenanceForm').appendChild(dateDiv);
	}
	
	</script>
</body>
</html>