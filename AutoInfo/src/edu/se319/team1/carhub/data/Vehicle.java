package edu.se319.team1.carhub.data;

import java.util.Date;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

@PersistenceCapable
public class Vehicle implements Comparable<Vehicle> {

	/**
	 * Column names for the database
	 */
	public static class Columns {
		public static final String IDENTIFIER = "identifier";
		public static final String LAST_MODIFIED = "dateLastModified";
		public static final String MAKE = "make";
		public static final String MODEL = "model";
		public static final String YEARS = "years";
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
	private String years;

	/**
	 * @param make
	 * @param model
	 * @param years
	 */
	public Vehicle(String make, String model, String years) {
		this.make = make;
		this.model = model;
		this.years = years;
		this.dateLastModified = new Date();
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
	 * @return the year
	 */
	public String getYear() {
		return years;
	}

	@Override
	public int compareTo(Vehicle arg0) {
		// If the makes are the same compare the models
		if (make.compareTo(arg0.make) == 0) {
			// If the models are the same, return the year comparison
			if (model.compareTo(arg0.model) == 0) {
				return years.compareTo(arg0.years);
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
		StringBuilder builder = new StringBuilder();
		builder.append("Vehicle [identifier=");
		builder.append(identifier);
		builder.append(", dateLastModified=");
		builder.append(dateLastModified);
		builder.append(", make=");
		builder.append(make);
		builder.append(", model=");
		builder.append(model);
		builder.append(", year=");
		builder.append(years);
		builder.append("]");
		return builder.toString();
	}
}
