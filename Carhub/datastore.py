'''
Created on Oct 17, 2012

@author: breber
'''
from google.appengine.ext import ndb
import models

def getUserVehicle(vehicleId):
    return models.UserVehicle.get_by_id(long(vehicleId))


def getListOfMakes():
    query = models.BaseVehicle().query()
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    for v in results:
        if not v.make in toRet:
            toRet.append(v.make)
    
    toRet.sort()
    
    return toRet

def getListOfModels(make):
    query = models.BaseVehicle().query(models.BaseVehicle.make == make)
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    for v in results:
        if not v.model in toRet:
            toRet.append(v.model)
    
    toRet.sort()
    
    return toRet

def getListOfYears(make, model):
    query = models.BaseVehicle().query(models.BaseVehicle.make == make, 
                                       models.BaseVehicle.model == model)
    result = query.get()
    
    toRet = result.years.split(",")
    toRet.sort()
    
    return toRet
        