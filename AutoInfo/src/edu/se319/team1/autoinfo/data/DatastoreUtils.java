package edu.se319.team1.autoinfo.data;

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
	 * Get a list of Vehicle Makes
	 * 
	 * @return a list of Vehicle Makes
	 */
	public static List<String> getListOfMakes() {
		final String MEMCACHE_KEY = "vehicleMakeList";
		final String SEPARATOR = "~~";

		// Using the synchronous cache
		MemcacheService syncCache = MemcacheServiceFactory.getMemcacheService();
		List<String> toRet = new ArrayList<String>();
		Object memcacheResult = syncCache.get(MEMCACHE_KEY);

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
			syncCache.put(MEMCACHE_KEY, memcachedResult.toString());
		}

		return toRet;
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
