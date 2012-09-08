package edu.se319.team1.carhub;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Utilities used for URL paths
 */
public class PathUtils {

	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(PathUtils.class.getSimpleName());

	private PathUtils() {}

	/**
	 * Parse a URL path into substrings
	 * 
	 * @param aInPath the path ("/cars/Audi/R8")
	 * @return a List of path parts (["cars, "Audi", "R8"])
	 */
	public static List<String> parsePath(String aInPath) {
		List<String> toRet = new ArrayList<String>();

		log.log(Level.FINE, "Path: " + aInPath);

		if (aInPath != null) {
			if (aInPath.startsWith("/")) {
				aInPath = aInPath.substring(1);
			}
			toRet.addAll(Arrays.asList(aInPath.split("/")));
		}

		log.log(Level.FINE, "Result: " + toRet);

		return toRet;
	}

}
