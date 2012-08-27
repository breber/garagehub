package edu.se319.team1.autoinfo.servlets;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.se319.team1.autoinfo.data.DatastoreUtils;

/**
 * Delete all CarResponseString
 */
@SuppressWarnings("serial")
public class DeleteAllCarResponseString extends HttpServlet {

	@Override
	public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		DatastoreUtils.deleteAllCarResponseStrings();

		resp.sendRedirect("/admin/admin.jsp");
	}
}
