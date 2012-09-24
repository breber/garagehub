package edu.se319.team1.carhub.servlets;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.google.appengine.labs.repackaged.org.json.JSONException;
import com.google.appengine.labs.repackaged.org.json.JSONObject;

@SuppressWarnings("serial")
public class FBLoginServlet extends HttpServlet {
	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(FBLoginServlet.class.getSimpleName());

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		String code = req.getParameter("code");
		if (code == null || code.equals("")) {
			log.log(Level.SEVERE, "code is unavailable...");
		}

		String token = null;
		try {
			String g = "https://graph.facebook.com/oauth/access_token?client_id=176948449109248&redirect_uri=" + URLEncoder.encode("http://carhub.us/login_fb.do", "UTF-8") + "&client_secret=de669797f7bd27a88319f7574e212808&code=" + code;
			URL u = new URL(g);
			URLConnection c = u.openConnection();
			BufferedReader in = new BufferedReader(new InputStreamReader(c.getInputStream()));
			String inputLine;
			StringBuffer b = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				b.append(inputLine + "\n");
			}
			in.close();
			token = b.toString();
			if (token.startsWith("{")) {
				throw new Exception("error on requesting token: " + token + " with code: " + code);
			}
		} catch (Exception e) {
			log.log(Level.SEVERE, "Problem retrieving access token");
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
		}

		String graph = null;
		try {
			String g = "https://graph.facebook.com/me?" + token;
			URL u = new URL(g);
			URLConnection c = u.openConnection();
			BufferedReader in = new BufferedReader(new InputStreamReader(c.getInputStream()));
			String inputLine;
			StringBuffer b = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				b.append(inputLine + "\n");
			}
			in.close();
			graph = b.toString();
		} catch (Exception e) {
			log.log(Level.SEVERE, "Problem getting user data from facebook");
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
		}

		String facebookId = null;
		String username = null;
		String name = null;
		String email = null;
		try {
			JSONObject json = new JSONObject(graph);
			facebookId = json.getString("id");
			name = json.getString("name");
			username = json.getString("username");
			email = json.getString("email");
		} catch (JSONException e) {
			log.log(Level.SEVERE, "Problem parsing user data");
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
		}

		log.log(Level.WARNING, "Facebook ID: " + facebookId);
		log.log(Level.WARNING, "Name: " + name);
		log.log(Level.WARNING, "Email: " + email);

		HttpSession session = req.getSession(true);
		if (session != null) {
			session.setAttribute("logged_in", facebookId);
			session.setAttribute("username", username);
			session.setAttribute("name", name);
		}

		resp.sendRedirect("/");
	}
}
