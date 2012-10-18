'''
Created on Oct 17, 2012

@author: breber
'''
from google.appengine.api import memcache
import logging
import models

def getUserVehicle(vehicleId):
    result = models.UserVehicle.get_by_id(long(vehicleId))
    
    # TODO: cache this?
    
    return result

def getListOfMakes():
    cacheResult = memcache.Client().get("vehicleMakeList")
    
    # If it was in the cache, use that
    if cacheResult:
        return str(cacheResult).split("~~")
    else:
        # Otherwise query for the data, and add to the cache
        logging.warn("Retrieved make list from datastore")
        
        query = models.BaseVehicle().all()
        result = query.fetch(1000)

        toRet = []
        for v in result:
            if not v.make in toRet:
                toRet.append(v.make)
        
        toRet.sort()
        memcache.Client().add("vehicleMakeList", "~~".join(toRet))
        
        return toRet

def getListOfModels(make):
    memcacheKey = "vehicleModelList_%s" % make
    cacheResult = memcache.Client().get(memcacheKey)
    
    # If it was in the cache, use that
    if cacheResult:
        return str(cacheResult).split("~~")
    else:
        # Otherwise query for the data, and add to the cache
        logging.warn("Retrieved model list from datastore")
        
        query = models.BaseVehicle().all()
        query.filter("make =", make)
        result = query.fetch(1000)

        toRet = []
        for v in result:
            if not v.model in toRet:
                toRet.append(v.model)
        
        toRet.sort()
        memcache.Client().add(memcacheKey, "~~".join(toRet))
        
        return toRet

def getListOfYears(make, model):
    memcacheKey = "vehicleModelList_%s_%s" % (make, model)
    cacheResult = memcache.Client().get(memcacheKey)
    
    # If it was in the cache, use that
    if cacheResult:
        return str(cacheResult).split("~~")
    else:
        # Otherwise query for the data, and add to the cache
        logging.warn("Retrieved year list from datastore")
        
        query = models.BaseVehicle().all()
        query.filter("make =", make)
        query.filter("model =", model)
        result = query.get()
        
        toRet = result.years.split(",")

        toRet.sort()
        memcache.Client().add(memcacheKey, "~~".join(toRet))
        
        return toRet
        