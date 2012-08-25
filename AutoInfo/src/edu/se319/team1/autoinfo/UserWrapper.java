package edu.se319.team1.autoinfo;

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
	 * The MD5 of the user's email address
	 */
	private String md5 = "";

	/**
	 * The user's nickname
	 */
	private String nickname;

	/**
	 * Get the UserWrapper for the current logged in user
	 * 
	 * @return the UserWrapper for the current user
	 */
	public static UserWrapper getInstance() {
		UserWrapper toRet = new UserWrapper();
		UserService service = UserServiceFactory.getUserService();
		User user = service.getCurrentUser();

		toRet.isLoggedIn = service.isUserLoggedIn();
		toRet.isAdmin = toRet.isLoggedIn && service.isUserAdmin();
		toRet.nickname = (toRet.isLoggedIn) ? user.getNickname() : "";
		toRet.md5 = (toRet.isLoggedIn) ? MD5Util.md5Hex(user.getEmail()) : "00000000000000000000000000000000";

		return toRet;
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
	};
}
