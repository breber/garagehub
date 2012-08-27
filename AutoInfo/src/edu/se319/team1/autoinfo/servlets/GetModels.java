package edu.se319.team1.autoinfo.servlets;

import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;

import edu.se319.team1.autoinfo.data.DatastoreUtils;

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
		String pathInfo = req.getPathInfo();
		log.log(Level.FINE, GetModels.class.getSimpleName());

		if (!"".equals(pathInfo)) {
			if (pathInfo.startsWith("/")) {
				pathInfo = pathInfo.substring(1);
			}

			List<String> models = DatastoreUtils.getListOfModels(pathInfo);
			JSONArray values = new JSONArray(models);

			resp.setContentType("application/json");
			resp.getWriter().print(values.toString());
		}
	}
}
