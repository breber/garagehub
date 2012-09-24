package edu.se319.team1.carhub.servlets;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.jdo.PersistenceManager;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.PreparedQuery.TooManyResultsException;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.CompositeFilterOperator;
import com.google.appengine.api.datastore.Query.FilterPredicate;
import com.google.appengine.api.datastore.Text;
import com.google.appengine.api.datastore.Transaction;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

import edu.se319.team1.carhub.Email;
import edu.se319.team1.carhub.PMF;
import edu.se319.team1.carhub.Utilities;
import edu.se319.team1.carhub.data.CarResponseString;
import edu.se319.team1.carhub.data.DatastoreUtils;
import edu.se319.team1.carhub.data.Vehicle;

/**
 * Fetch list of make/model/years from cars.com
 */
@SuppressWarnings("serial")
public class RetrieveVehicleTypes extends HttpServlet {

	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(RetrieveVehicleTypes.class.getSimpleName());

	/**
	 * The list of Vehicles to add to the database
	 */
	private List<Vehicle> vehicleList = new ArrayList<Vehicle>();

	/**
	 * The instance used to access the memcache service
	 */
	private MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();

	/**
	 * Get the Datastore Service
	 */
	private DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();

	/**
	 * The PersistenceManager used to write to the database
	 */
	private PersistenceManager pm = PMF.get().getPersistenceManager();

	/**
	 * Represents the number of records added to the database
	 */
	private int numAdded = 0;

	/**
	 * Represents the number of records that were updated
	 */
	private int numUpdated = 0;

	/**
	 * The number that were skipped
	 */
	private int numSkipped = 0;

	@Override
	public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		// Grab the data from cars.com
		URL url = new URL("http://www.cars.com/js/mmyCrp.js");
		InputStream stream = url.openStream();

		// Convert the result into a string
		String serverResponse = Utilities.convertStreamToString(stream);

		// Just get the data part (the JSONArray)
		serverResponse = serverResponse.substring(serverResponse.indexOf('['), serverResponse.lastIndexOf(']') + 1);

		// Figure out which records have been updated/added
		getUpdatedRecords(serverResponse);

		// Perform the update in the database
		updateDatabase();

		// Close the persistence manager
		pm.close();

		// Invalidate the current memcache string if we updated anything
		if (!vehicleList.isEmpty()) {
			syncCache.delete(DatastoreUtils.KEY_VEHICLE_MAKE);
		}

		// Print out status report
		log.log(Level.INFO, "Finished " + RetrieveVehicleTypes.class.getSimpleName());
		log.log(Level.INFO, "Num Updated:  " + numUpdated);
		log.log(Level.INFO, "Num Added:  " + numAdded);
		log.log(Level.INFO, "Num Skipped:  " + numSkipped);

		// TODO: don't email this, but store results in datastore somewhere
		Email.sendEmailToBrian("RetrieveVehicleTypes Update: " + new Date(), "Updated at " + new Date() + "<br /><br />Updated: " + numUpdated
				+ "<br />Added: " + numAdded + "<br />Skipped: " + numSkipped + "<br /><br />" + vehicleList.toString());

		// Send the user to the admin page
		resp.sendRedirect("/admin/admin.jsp");
	}

	/**
	 * Take the data from the remote server and compare it against
	 * what we received previously. Update the vehicleList with records
	 * that need to be added/modified.
	 * 
	 * @param serverResponse the string from the server
	 */
	private void getUpdatedRecords(String serverResponse) {
		Entity carResponseStringEntity = null;
		boolean skip = false;

		try {
			// Get the wrapping JSONArray
			JSONArray arr = new JSONArray(serverResponse);

			// The array of results from the previous CarResponseStringEntity
			JSONArray prevArray = null;

			// Query the database for a previous response string
			Query q = new Query(CarResponseString.class.getSimpleName());
			PreparedQuery pq = datastore.prepare(q);

			try {
				carResponseStringEntity = pq.asSingleEntity();

				if (carResponseStringEntity != null) {
					Text entityData = (Text) carResponseStringEntity.getProperty(CarResponseString.Columns.RESPONSE);

					if (entityData != null) {
						prevArray = new JSONArray(entityData.getValue());

						// If we have a matching string comparison, no need to do anything
						if (entityData.getValue().equals(serverResponse)) {
							skip = true;
							log.log(Level.INFO, "string match...skipping the rest of the steps");
						}
					}
				}
			} catch (TooManyResultsException ex) {
				carResponseStringEntity = null;
				DatastoreUtils.deleteAllCarResponseStrings();
				log.log(Level.WARNING, "more than one previous car response entity");
			}

			// For each entry in the JSONArray (each make is an entry)
			for (int i = 0; i < arr.length() && !skip; i++) {
				JSONObject obj = (JSONObject) arr.get(i);
				JSONObject make = (JSONObject) obj.get("mk");
				JSONArray models = (JSONArray) obj.get("mds");

				String makeString = make.getString("n");

				for (int j = 0; j < models.length(); j++) {
					JSONObject obj1 = (JSONObject) models.get(j);
					String model = obj1.getString("dn");
					String years = obj1.getString("yrs"); // Years is a comma-delimited string of years

					// Get the list of years we previously knew about
					String prevYears = getYears(prevArray, makeString, model);

					// If we couldn't find the previous years, or what we
					// previously had doesn't match what we have now, add
					// it to the list to update
					if (prevYears == null || !prevYears.equals(years)) {
						Vehicle vehicle = new Vehicle(makeString, model, years);
						vehicleList.add(vehicle);

						log.log(Level.INFO, "the years DO NOT match, so no need to update (" + makeString + " " + model + ")");
					} else {
						numSkipped++;
						log.log(Level.INFO, "the years match, so no need to update (" + makeString + " " + model + ")");
					}
				}
			}

			// Update the car response string
			if (carResponseStringEntity != null) {
				carResponseStringEntity.setProperty(CarResponseString.Columns.RESPONSE, new Text(serverResponse));
				datastore.put(carResponseStringEntity);
			} else {
				pm.makePersistent(new CarResponseString(serverResponse));
			}
		} catch (JSONException e) {
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
			e.printStackTrace();
		}
	}

	/**
	 * Get the years available for the given make and model
	 * 
	 * @param prevArray the JSONArray to search
	 * @param make the make of the vehicle to search for
	 * @param model the model of the vehicle to search for
	 * 
	 * @return the years of the vehicle in the JSONArray
	 */
	private String getYears(JSONArray prevArray, String make, String model) {
		if (prevArray == null) {
			return null;
		}

		try {
			// For each entry in the JSONArray (each make is an entry)
			for (int i = 0; i < prevArray.length(); i++) {
				JSONObject obj = (JSONObject) prevArray.get(i);
				JSONObject makeObj = (JSONObject) obj.get("mk");
				JSONArray models = (JSONArray) obj.get("mds");

				String makeString = makeObj.getString("n");

				if (make.equals(makeString)) {
					for (int j = 0; j < models.length(); j++) {
						JSONObject obj1 = (JSONObject) models.get(j);
						String modelStr = obj1.getString("dn");

						// We found a match for make and model
						if (model.equals(modelStr)) {
							return obj1.getString("yrs");
						}
					}
				}
			}
		} catch (JSONException ex) {
			log.log(Level.SEVERE, ex.getMessage());
			log.log(Level.SEVERE, Arrays.toString(ex.getStackTrace()));
		}
		return null;
	}

	/**
	 * Perform the update of the database using the records found in vehicleList
	 */
	private void updateDatabase() {
		Date currentTime = new Date();

		// Go through the list and add new entries, and update times
		// of pre-exisiting entries
		try {
			for (Vehicle v : vehicleList) {
				Query q = new Query(Vehicle.class.getSimpleName());
				FilterPredicate make = new FilterPredicate(Vehicle.VehicleColumns.MAKE, Query.FilterOperator.EQUAL, v.getMake());
				FilterPredicate model = new FilterPredicate(Vehicle.VehicleColumns.MODEL, Query.FilterOperator.EQUAL, v.getModel());

				q.setFilter(CompositeFilterOperator.and(make, model));

				Transaction txn = datastore.beginTransaction();
				try {
					// Prepare the query. Try and get the result as a single entity.
					//  - If the result is null, we don't have a record, so we want to add it
					//  - If the pq.asSingleEntity method throws a TooManyResultsException, just log an error
					PreparedQuery pq = datastore.prepare(q);
					Entity result = pq.asSingleEntity();

					// If result isn't null, update the last modified time to the current time
					if (result != null) {
						numUpdated++;
						result.setProperty(Vehicle.VehicleColumns.LAST_MODIFIED, currentTime);
						result.setProperty(Vehicle.VehicleColumns.YEARS, v.getYear());
						datastore.put(result);
					} else {
						// If the result is null, we want to add the vehicle to the database
						pm.makePersistent(v);
						// TODO: create entity instead of pm.makePersistent
						numAdded++;
					}

					// TODO: remove the Vehicle Model list from cache if we updated it
				} catch (TooManyResultsException ex) {
					log.log(Level.SEVERE, "More than one result...");
					log.log(Level.SEVERE, v.toString());
				} finally {
					if (txn != null) {
						txn.commit();
					}
				}
			}
		} catch (Exception e) {
			log.log(Level.SEVERE, "Error modifiying database");
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
		}
	}
}
