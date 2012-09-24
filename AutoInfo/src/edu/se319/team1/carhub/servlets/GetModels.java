package edu.se319.team1.carhub.servlets;

import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;

import edu.se319.team1.carhub.PathUtils;
import edu.se319.team1.carhub.UserWrapper;
import edu.se319.team1.carhub.data.DatastoreUtils;

/**
 * Delete all Vehicles
 */
@SuppressWarnings("serial")
public class GetModels extends HttpServlet {

	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(GetModels.class.getSimpleName());

	@Override
	public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		log.log(Level.FINE, GetModels.class.getSimpleName());
		UserWrapper user = UserWrapper.getInstance(req.getSession(false));

		if (user != null && user.isLoggedIn()) {
			List<String> parsedPath = PathUtils.parsePath(req.getPathInfo());
			JSONArray values = new JSONArray();

			// If there are no entries, return a list of Makes
			// If there is one entry, treat is as a Make, so return the Models for that make
			if (parsedPath.isEmpty()) {
				List<String> makes = DatastoreUtils.getListOfMakes();
				values = new JSONArray(makes);
			}

			// If there is one entry, treat is as a Make, so return the Models for that make
			if (parsedPath.size() == 1) {
				List<String> models = DatastoreUtils.getListOfModels(parsedPath.get(0));
				values = new JSONArray(models);
			}

			// If there are two entries, treat them as Make and Model, so return years
			if (parsedPath.size() == 2) {
				List<String> years = DatastoreUtils.getListOfYears(parsedPath.get(0), parsedPath.get(1));
				values = new JSONArray(years);
			}

			resp.addHeader("Cache-Control", "max-age=600");
			resp.setContentType("application/json");
			resp.getWriter().print(values.toString());
		} else {
			resp.sendRedirect("/");
		}
	}
}
