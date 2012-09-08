package edu.se319.team1.carhub.servlets;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.se319.team1.carhub.data.DatastoreUtils;

/**
 * Delete all Vehicles
 */
@SuppressWarnings("serial")
public class DeleteAllVehicles extends HttpServlet {

	@Override
	public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		DatastoreUtils.deleteAllVehicles();

		resp.sendRedirect("/admin/admin.jsp");
	}
}
