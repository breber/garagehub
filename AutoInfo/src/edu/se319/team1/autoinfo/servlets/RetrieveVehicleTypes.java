package edu.se319.team1.autoinfo.servlets;

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

import edu.se319.team1.autoinfo.PMF;
import edu.se319.team1.autoinfo.Utilities;
import edu.se319.team1.autoinfo.data.CarResponseString;
import edu.se319.team1.autoinfo.data.DatastoreUtils;
import edu.se319.team1.autoinfo.data.Vehicle;

/**
 * Fetch list of make/model/years from cars.com
 */
@SuppressWarnings("serial")
public class RetrieveVehicleTypes extends HttpServlet {

	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(RetrieveVehicleTypes.class.getSimpleName());

	@Override
	public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Date currentTime = new Date();
		List<Vehicle> vehicleList = new ArrayList<Vehicle>();
		Entity carResponseStringEntity = null;
		boolean skip = false;

		// Get the Datastore Service
		DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();

		// Grab the data from cars.com
		URL url = new URL("http://www.cars.com/js/mmyCrp.js");
		InputStream stream = url.openStream();

		// Convert the result into a string
		String serverResponse = Utilities.convertStreamToString(stream);

		// Just get the data part (the JSONArray)
		serverResponse = serverResponse.substring(serverResponse.indexOf('['), serverResponse.lastIndexOf(']') + 1);

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
					String years = obj1.getString("yrs");

					// TODO: check to see if prevArray contains this make, model and year combination
					if (prevArray == null) {

					}

					// Years is a comma-delimited string of years
					Vehicle vehicle = new Vehicle(makeString, model, years);
					vehicleList.add(vehicle);
				}
			}
		} catch (JSONException e) {
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
			e.printStackTrace();
		}

		// Keep track of how many entities were added, and how
		// many were updated
		int numAdded = 0;
		int numUpdated = 0;
		MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();

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
					} else {
						// If the result is null, we want to add the vehicle to the database
						pm.makePersistent(v);
						numAdded++;
					}
				} catch (TooManyResultsException ex) {
					log.log(Level.SEVERE, "More than one result...");
					log.log(Level.SEVERE, v.toString());
				} finally {
					if (txn.isActive()) {
						txn.commit();
					}
				}
			}

			// Update the car response string
			if (carResponseStringEntity != null) {
				carResponseStringEntity.setProperty(CarResponseString.Columns.RESPONSE, new Text(serverResponse));
			} else {
				pm.makePersistent(new CarResponseString(serverResponse));
			}
		} catch (Exception e) {
			log.log(Level.SEVERE, "Error modifiying database");
			log.log(Level.SEVERE, e.getMessage());
			log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
		} finally {
			pm.close();
		}

		// Invalidate the current memcache string if we updated anything
		if (!vehicleList.isEmpty()) {
			syncCache.delete(DatastoreUtils.KEY_VEHICLE_MAKE);
		}

		// Print out status report
		log.log(Level.INFO, "Finished " + RetrieveVehicleTypes.class.getSimpleName());
		log.log(Level.INFO, "Num Updated:  " + numUpdated);
		log.log(Level.INFO, "Num Added:  " + numAdded);
	}
}
