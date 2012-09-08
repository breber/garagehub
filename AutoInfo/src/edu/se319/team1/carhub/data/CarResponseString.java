package edu.se319.team1.carhub.data;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Text;

/**
 * The response from the server where we get the car information.
 * 
 * Can be used to check and see if what we currently have in the
 * database matches up with what the remote server knows about.
 */
@PersistenceCapable
public class CarResponseString {

	/**
	 * Column names for the database
	 */
	public static class Columns {
		public static final String IDENTIFIER = "identifier";
		public static final String RESPONSE = "response";
	}

	/**
	 * The primary key in the database
	 */
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long identifier;

	/**
	 * The JSON string response
	 */
	private Text response;

	/**
	 * @param response
	 */
	public CarResponseString(String response) {
		this.response = new Text(response);
	}

	/**
	 * @return the identifier
	 */
	public Long getIdentifier() {
		return identifier;
	}

	/**
	 * @return the response
	 */
	public String getResponse() {
		return response.getValue();
	}
}
