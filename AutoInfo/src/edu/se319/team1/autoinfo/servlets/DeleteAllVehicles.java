package edu.se319.team1.autoinfo.servlets;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.se319.team1.autoinfo.data.DatastoreUtils;

/**
 * Delete all Vehicles
 */
@SuppressWarnings("serial")
public class DeleteAllVehicles extends HttpServlet {

	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(DeleteAllVehicles.class.getSimpleName());

	@Override
	public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		log.log(Level.FINE, DeleteAllVehicles.class.getSimpleName());

		DatastoreUtils.deleteAllVehicles();

		log.log(Level.FINE, DeleteAllVehicles.class.getSimpleName() + " : finished");
	}
}
