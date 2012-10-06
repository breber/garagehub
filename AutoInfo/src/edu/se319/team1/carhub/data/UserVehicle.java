package edu.se319.team1.carhub.data;

import java.util.Date;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Entity;

@PersistenceCapable
public class UserVehicle implements Comparable<UserVehicle> {

	/**
	 * Column names for the database
	 */
	public static class Columns {
		public static final String IDENTIFIER = "identifier";
		public static final String LAST_MODIFIED = "dateLastModified";
		public static final String OWNER = "owner";
		public static final String MAKE = "make";
		public static final String MODEL = "model";
		public static final String YEAR = "year";
	}

	/**
	 * The primary key in the database
	 */
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long identifier;

	/**
	 * The date this record was last updated
	 */
	private Date dateLastModified;

	/**
	 * The owner's ID
	 */
	private String owner;

	/**
	 * The make of the vehicle
	 */
	private String make;

	/**
	 * The model of the vehicle
	 */
	private String model;

	/**
	 * The year of the vehicle
	 */
	private String year;

	// TODO: add color
	// TODO: add license plate
	// TODO: add VIN?

	/**
	 * @param owner
	 * @param make
	 * @param model
	 * @param year
	 */
	public UserVehicle(String owner, String make, String model, String year) {
		this.owner = owner;
		this.make = make;
		this.model = model;
		this.year = year;
		this.dateLastModified = new Date();
	}

	/**
	 * @param e
	 */
	public UserVehicle(Entity e) {
		this.owner = (String) e.getProperty(Columns.OWNER);
		this.make = (String) e.getProperty(Columns.MAKE);
		this.model = (String) e.getProperty(Columns.MODEL);
		this.year = (String) e.getProperty(Columns.YEAR);
		this.dateLastModified = (Date) e.getProperty(Columns.LAST_MODIFIED);
	}

	/**
	 * @return the identifier
	 */
	public Long getIdentifier() {
		return identifier;
	}

	/**
	 * @return the date
	 */
	public Date getDate() {
		return dateLastModified;
	}

	/**
	 * @return the make
	 */
	public String getMake() {
		return make;
	}

	/**
	 * @return the model
	 */
	public String getModel() {
		return model;
	}

	/**
	 * @return the owner
	 */
	public String getOwner() {
		return owner;
	}

	/**
	 * @return the year
	 */
	public String getYear() {
		return year;
	}

	@Override
	public int compareTo(UserVehicle arg0) {
		// If the makes are the same compare the models
		if (make.compareTo(arg0.make) == 0) {
			// If the models are the same, return the year comparison
			if (model.compareTo(arg0.model) == 0) {
				return year.compareTo(arg0.year);
			} else {
				// Otherwise return the modle comparison
				return model.compareTo(arg0.model);
			}
		} else {
			// Otherwise just compare the make
			return make.compareTo(arg0.make);
		}
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return year + " " + make + " " + model;
	}
}
