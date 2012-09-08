package edu.se319.team1.carhub.data;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.FetchOptions;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.PropertyProjection;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.FilterPredicate;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

/**
 * Utility methods for interacting with the Datastore
 */
public class DatastoreUtils {
	/**
	 * The logger for AppEngine
	 */
	private static final Logger log = Logger.getLogger(DatastoreUtils.class.getSimpleName());

	/**
	 * String used to separate list items in a memcache string
	 */
	public static final String SEPARATOR = "~~";

	/**
	 * Memcache key containing Vehicle Make information
	 */
	public static final String KEY_VEHICLE_MAKE = "vehicleMakeList";

	/**
	 * Memcache key containing Vehicle Model information
	 */
	public static final String KEY_VEHICLE_MODEL = "vehicleModelList";

	/**
	 * Get a list of Vehicle Makes
	 * 
	 * @return a list of Vehicle Makes
	 */
	public static List<String> getListOfMakes() {
		// Using the synchronous cache
		MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();
		List<String> toRet = new ArrayList<String>();
		Object memcacheResult = syncCache.get(KEY_VEHICLE_MAKE);

		// If the value is in memcache, parse it
		if (memcacheResult != null) {
			String stringified = String.valueOf(memcacheResult);
			toRet.addAll(Arrays.asList(stringified.split(SEPARATOR)));
		} else {
			// The value isn't in memcache, so fall back to datastore,
			// and add the result to memcache so we don't need to go back
			// to the datastore for a while
			log.log(Level.WARNING, "Retrieved make list from datastore");

			// Get the Datastore Service
			DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
			Query q = new Query(Vehicle.class.getSimpleName());
			q.addProjection(new PropertyProjection(Vehicle.VehicleColumns.MAKE, String.class));
			PreparedQuery pq = datastore.prepare(q);
			StringBuilder memcachedResult = new StringBuilder();

			for (Entity e : pq.asIterable()) {
				String make = String.valueOf(e.getProperty(Vehicle.VehicleColumns.MAKE));
				if (!toRet.contains(make)) {
					toRet.add(make);
					memcachedResult.append(make).append(SEPARATOR);
				}
			}

			// Put string into memcache
			syncCache.put(KEY_VEHICLE_MAKE, memcachedResult.toString());
		}

		return toRet;
	}

	/**
	 * Get a list of Vehicle Models for the given make
	 * 
	 * @return a list of Vehicle Models
	 */
	public static List<String> getListOfModels(String make) {
		// Using the synchronous cache
		MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();
		List<String> toRet = new ArrayList<String>();
		Object memcacheResult = syncCache.get(KEY_VEHICLE_MODEL + "_" + make);

		// If the value is in memcache, parse it
		if (memcacheResult != null) {
			String stringified = String.valueOf(memcacheResult);
			toRet.addAll(Arrays.asList(stringified.split(SEPARATOR)));
		} else {
			// The value isn't in memcache, so fall back to datastore,
			// and add the result to memcache so we don't need to go back
			// to the datastore for a while
			log.log(Level.WARNING, "Retrieved model list from datastore");

			// Get the Datastore Service
			DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
			Query q = new Query(Vehicle.class.getSimpleName());
			q.setFilter(new FilterPredicate(Vehicle.VehicleColumns.MAKE, Query.FilterOperator.EQUAL, make));
			q.addProjection(new PropertyProjection(Vehicle.VehicleColumns.MODEL, String.class));
			PreparedQuery pq = datastore.prepare(q);
			StringBuilder memcachedResult = new StringBuilder();

			for (Entity e : pq.asIterable()) {
				String model = String.valueOf(e.getProperty(Vehicle.VehicleColumns.MODEL));
				if (!toRet.contains(model)) {
					toRet.add(model);
					memcachedResult.append(model).append(SEPARATOR);
				}
			}

			// Put string into memcache
			syncCache.put(KEY_VEHICLE_MODEL + "_" + make, memcachedResult.toString());
		}

		return toRet;
	}

	/**
	 * Get a list of Years for the given make and model
	 * 
	 * @return a list of years
	 */
	public static List<String> getListOfYears(String make, String model) {
		// Using the synchronous cache
		MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();
		List<String> toRet = new ArrayList<String>();
		Object memcacheResult = syncCache.get(KEY_VEHICLE_MODEL + "_" + make + "_" + model);

		// If the value is in memcache, parse it
		if (memcacheResult != null) {
			String stringified = String.valueOf(memcacheResult);
			toRet.addAll(Arrays.asList(stringified.split(SEPARATOR)));
		} else {
			// The value isn't in memcache, so fall back to datastore,
			// and add the result to memcache so we don't need to go back
			// to the datastore for a while
			log.log(Level.WARNING, "Retrieved year list from datastore");

			// Get the Datastore Service
			DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
			Query q = new Query(Vehicle.class.getSimpleName());
			q.setFilter(new FilterPredicate(Vehicle.VehicleColumns.MAKE, Query.FilterOperator.EQUAL, make));
			q.setFilter(new FilterPredicate(Vehicle.VehicleColumns.MODEL, Query.FilterOperator.EQUAL, model));
			q.addProjection(new PropertyProjection(Vehicle.VehicleColumns.YEARS, String.class));
			PreparedQuery pq = datastore.prepare(q);
			StringBuilder memcachedResult = new StringBuilder();

			try {
				Entity result = pq.asSingleEntity();

				if (result != null) {
					String years = String.valueOf(result.getProperty(Vehicle.VehicleColumns.YEARS));
					String[] split = years.split(",");

					for (String s : split) {
						toRet.add(s);
						memcachedResult.append(s).append(SEPARATOR);
					}
				}
			} catch (Exception e) {
				log.log(Level.SEVERE, e.getMessage());
				log.log(Level.SEVERE, Arrays.toString(e.getStackTrace()));
			}

			// Put string into memcache
			syncCache.put(KEY_VEHICLE_MODEL + "_" + make + "_" + model, memcachedResult.toString());
		}

		return toRet;
	}


	/**
	 * Delete all CarResponseString
	 */
	public static void deleteAllCarResponseStrings() {
		// Get the Datastore Service
		DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
		Query q = new Query(CarResponseString.class.getSimpleName());

		while (true) {
			PreparedQuery pq = datastore.prepare(q);
			List<Entity> resultList = pq.asList(FetchOptions.Builder.withDefaults());
			if (resultList != null && !resultList.isEmpty()) {
				for (Entity entity : resultList) {
					datastore.delete(entity.getKey());
				}
			} else {
				break;
			}
		}
	}

	/**
	 * Delete all vehicles
	 */
	public static void deleteAllVehicles() {
		// Get the Datastore Service
		DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
		Query q = new Query(Vehicle.class.getSimpleName());

		while (true) {
			PreparedQuery pq = datastore.prepare(q);
			List<Entity> resultList = pq.asList(FetchOptions.Builder.withDefaults());
			if (resultList != null && !resultList.isEmpty()) {
				for (Entity entity : resultList) {
					datastore.delete(entity.getKey());
				}
			} else {
				break;
			}
		}
	}

}
