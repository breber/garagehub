package edu.se319.team1.autoinfo.data;

import java.util.List;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.FetchOptions;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;

/**
 * Utility methods for interacting with the Datastore
 */
public class DatastoreUtils {

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
