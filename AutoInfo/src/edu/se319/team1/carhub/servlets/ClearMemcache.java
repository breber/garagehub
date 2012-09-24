package edu.se319.team1.carhub.servlets;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

import edu.se319.team1.carhub.UserWrapper;

/**
 * Clear all of Memcache
 */
@SuppressWarnings("serial")
public class ClearMemcache extends HttpServlet {

	@Override
	public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		UserWrapper user = UserWrapper.getInstance(req.getSession(false));

		if (user != null && user.isAdmin()) {
			MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();
			syncCache.clearAll();

			resp.sendRedirect("/admin/admin.jsp");
		} else {
			resp.sendRedirect("/");
		}
	}
}
