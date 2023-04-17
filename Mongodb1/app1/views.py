from django.shortcuts import render
from datetime import datetime, timedelta
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.http import HttpResponse
import csv


connection = MongoClient()
db = connection.querydata





def common(data, name):
    print(data)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=" + name + ".csv"},
    )
    fieldnames = data[0].keys()
    writer = csv.DictWriter(response, fieldnames)
    print(writer)
    writer.writeheader()
    print("bye")
    writer.writerows(data)
    return response


def home(request):
    trip_data=db.tripdata.aggregate(
        [
            {"$project": {"_id": 0}},
        ]
    )
    data = trip_data
    trip_id=None
    sensor_name=None
    from_time=None
    to_time=None
    sensor_data=""
    sensor_data1=""
    sensor_sum=""
    sensor_avg=""
    boatsensor_data=""
    time1=""
    time2=""
    
    if request.GET.get("tripId"):
        trip_id=request.GET.get("tripId")

    if request.GET.get("sensorName"):
        sensor_name = request.GET.get("sensorName")
    
    if request.GET.get("from"):
        from_time = request.GET.get("from")
        format = "%Y-%m-%d"
        time1 = datetime.strptime(from_time, format)
        print(type(time1))
    
    if request.GET.get("to"):
        to_time = request.GET.get("to")
        format = "%Y-%m-%d"
        time2 = datetime.strptime(to_time, format)
        print(type(time1))
    
    if trip_id:
        sensor_data=db.vesseltripdata.aggregate(
            [
                {"$match": {"tripId": trip_id}},
                {"$group": {"_id": 0, "sensors": {"$addToSet": "$sensorName"}}},
                {"$project": {"_id": 0}},
            ]
        )
    data1=list(sensor_data)
    

    if trip_id:
        sensor_data1 = db.vesseltripdata.aggregate(
                [
                    {"$match": {"tripId": trip_id,}},
                    {"$project": {"_id": 0}},
                ]
            )

    if trip_id and sensor_name:
        sensor_data1 = db.vesseltripdata.aggregate(
                [
                    {"$match": {"tripId": trip_id,
                                "sensorName": sensor_name,}},
                    {"$project": {"_id": 0}},
                ]
            )
    
    

    if time1 and time2:
        # format = "%Y-%m-%d"
        # time1 = datetime.strptime(from_time, format)
        # print(type(time1))
        # time2 = datetime.strptime(to_time, format)
        # print(type(time2))
        sensor_data1 = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": time1, "$lte": time2},
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )  

    if sensor_name and time1 and time2:
        
        sensor_data1 = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": time1, "$lte": time2},
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )
    if trip_id and time1 and time2:
        
        sensor_data1 = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": time1, "$lte": time2},
                        "tripId": trip_id,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )
    if trip_id and sensor_name and time1 and time2:
        
        sensor_data1 = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": time1, "$lte": time2},
                        "tripId": trip_id,
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )
    data2=list(sensor_data1)
    if request.GET.get("export", None) == "True":
        name = "get_all_data"
        result = common(data2, name)
        return result
    
    

    if request.GET.get("Details") == "get_sum" and trip_id and sensor_name:
        sensor_sum = db.vesseltripdata.aggregate(
                [
                    {"$match": {"tripId": trip_id, "sensorName": sensor_name}},
                    {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
                    {
                        "$group": {
                            "_id":{"sensorname":"$sensorName"},
                            "index0_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 0]}},
                            "index1_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 1]}},
                            "index2_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 2]}},
                        }
                    },
                ]
            )
    
    data3 = list(sensor_sum)
    
    if request.GET.get("export1", None) == "True":
        name = "get_sum"
        result = common(data3, name)
        return result
    

    if request.GET.get("Details") == "get_average" and trip_id and sensor_name:
        sensor_avg = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id, "sensorName": sensor_name}},
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    
                    "_id": "$sensorName",
                    "index0_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    
    
    data4 = list(sensor_avg)
    if request.GET.get("export2", None) == "True":
        name = "get_sensor_avg"
        result = common(data4, name)
        return result
    
    if request.GET.get("Details") == "get_boat_sensor_average" and trip_id and sensor_name and time1 and time2:
        
        print(trip_id,sensor_name,time1,time2)
        boatsensor_data = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": time1, "$lte": time2},
                        "sensorName": sensor_name,
                    }
                },
                {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
                {
                    "$group": {
                        "_id": {
                            "day": {"$dayOfMonth": "$datetime"},
                            "month": {"$month": "$datetime"},
                            "year": {"$year": "$datetime"},
                        },
                        "index0_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 0]}},
                        "index1_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 1]}},
                        "index2_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 2]}},
                    }
                },
            ]
        )
    
    # print(boatsensor_data)
    # print(type(boatsensor_data))
    data5 = list(boatsensor_data)
    print(data5)
    if request.GET.get("export3", None) == "True":
        name = "get_boatsenor_data"
        result = common(data5, name)
        return result
     



    return render(request, "home.html",{"data": data, "data1":data1, "data2":data2,"data3":data3, "data4":data4, "data5":data5, "time1":time1, "time2":time2})

