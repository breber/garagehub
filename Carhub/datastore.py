'''
Created on Oct 17, 2012

@author: breber
'''
import models

def getUserVehicle(vehicleId):
    return models.UserVehicle.get_by_id(long(vehicleId))


def getListOfMakes():
    query = models.BaseVehicle().query()
    result = query.fetch(1000)

    toRet = []
    for v in result:
        if not v.make in toRet:
            toRet.append(v.make)
    
    toRet.sort()
    
    return toRet

def getListOfModels(make):
    query = models.BaseVehicle().query(models.BaseVehicle.make == make)
    result = query.fetch(1000)

    toRet = []
    for v in result:
        if not v.model in toRet:
            toRet.append(v.model)
    
    toRet.sort()
    
    return toRet

def getListOfYears(make, model):
    query = models.BaseVehicle().query(models.BaseVehicle.make == make, models.BaseVehicle.model == model)
    result = query.get()
    
    toRet = result.years.split(",")
    toRet.sort()
    
    return toRet
        