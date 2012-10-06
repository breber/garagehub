package edu.se319.team1.carhub;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

import javax.servlet.http.HttpSession;

import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

/**
 * Wrapper for the Google User API
 */
public class UserWrapper {

	/**
	 * Is a user logged in?
	 */
	private boolean isLoggedIn;

	/**
	 * Is the logged in user an administrator?
	 */
	private boolean isAdmin;

	/**
	 * The ID of this user
	 */
	private String userId = "";

	/**
	 * The MD5 of the user's email address
	 */
	private String md5 = "";

	/**
	 * The user's nickname
	 */
	private String nickname;

	/**
	 * The user's profile picture URL
	 */
	private String profilePictureUrl;

	/**
	 * Get the UserWrapper for the current logged in user
	 *
	 * @return the UserWrapper for the current user
	 */
	public static UserWrapper getInstance() {
		UserWrapper toRet = new UserWrapper();
		UserService service = UserServiceFactory.getUserService();
		User user = service.getCurrentUser();

		if (user != null) {
			toRet.isLoggedIn = service.isUserLoggedIn();
			toRet.isAdmin = toRet.isLoggedIn && service.isUserAdmin();
			toRet.nickname = (toRet.isLoggedIn) ? user.getNickname() : "";
			toRet.md5 = (toRet.isLoggedIn) ? MD5Util.md5Hex(user.getEmail()) : "00000000000000000000000000000000";
			toRet.userId = (toRet.isLoggedIn) ? user.getUserId() : "";

			return toRet;
		} else {
			return null;
		}
	}

	/**
	 * Get the UserWrapper for the current logged in user
	 * 
	 * @return the UserWrapper for the current user
	 */
	public static UserWrapper getInstance(HttpSession session) {
		// Check if we have a user logged in using Google Login
		UserWrapper toRetGoogle = getInstance();

		if (toRetGoogle != null) {
			return toRetGoogle;
		}

		if (session != null) {
			UserWrapper toRet = new UserWrapper();

			toRet.isLoggedIn = (session.getAttribute("logged_in") != null);
			toRet.nickname = (toRet.isLoggedIn) ? (String) session.getAttribute("username") : "";
			toRet.isAdmin = toRet.isLoggedIn &&
					("breber".equals(toRet.nickname) ||
							"josh.peters.33".equals(toRet.nickname) ||
							"jgkujawa".equals(toRet.nickname) ||
							"fantashley".equals(toRet.nickname));
			toRet.md5 = null;
			toRet.profilePictureUrl = "https://graph.facebook.com/" + toRet.nickname + "/picture";
			toRet.userId = (String) ((toRet.isLoggedIn) ? session.getAttribute("logged_in") : "");

			return toRet;
		} else {
			return null;
		}
	}

	/**
	 * Get a Google Login URL
	 * 
	 * @return the URL to login with
	 */
	public static String getGoogleLoginURL() {
		UserService service = UserServiceFactory.getUserService();
		return service.createLoginURL("/");
	}

	/**
	 * Get a URL to login using Facebook
	 * 
	 * @return the Facebook Login URL
	 */
	public static String getFacebookLoginURL() {
		try {
			return "http://www.facebook.com/dialog/oauth?client_id=176948449109248&redirect_uri=" + URLEncoder.encode("http://carhub.us/login_fb.do", "UTF-8") + "&scope=email";
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
			return "";
		}
	}

	/**
	 * Private constructor
	 */
	private UserWrapper() { }

	/**
	 * @return the isLoggedIn
	 */
	public boolean isLoggedIn() {
		return isLoggedIn;
	}

	/**
	 * @return the isAdmin
	 */
	public boolean isAdmin() {
		return isAdmin;
	}

	/**
	 * @return the md5
	 */
	public String getMd5() {
		return md5;
	}

	/**
	 * @return the nickname
	 */
	public String getNickname() {
		return nickname;
	}

	/**
	 * @return the profilePictureUrl
	 */
	public String getProfilePictureUrl() {
		return profilePictureUrl;
	}

	/**
	 * @return the userId
	 */
	public String getUserId() {
		return userId;
	};
}
