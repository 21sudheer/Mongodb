from django.shortcuts import render
from datetime import datetime, timedelta
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.http import HttpResponse
import csv
import datetime

connection = MongoClient()
db = connection.querydata

# Create your views here.


def home(request):
    return render(request, template_name="home.html")


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


# 1] From a given trip, give me all the data for "Sensor X" over time
def get_all_data(request):
    print("hello")
    sensor_data = db.vesseltripdata.aggregate(
        [
            {"$project": {"_id": 0}},
        ]
    )
    sensor_name = None
    from_time = None
    to_time = None

    if request.GET.get("sensorName"):
        sensor_name = request.GET.get("sensorName")

        sensor_data = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )
    if request.GET.get("from"):
        from_time = request.GET.get("from")

    if request.GET.get("to"):
        to_time = request.GET.get("to")

    print(sensor_name, from_time, to_time)
    if sensor_name and from_time and to_time:
        format = "%Y-%m-%d"
        from_time = datetime.datetime.strptime(from_time, format)
        to_time = datetime.datetime.strptime(to_time, format)
        sensor_data = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": from_time, "$lte": to_time},
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )

    data = list(sensor_data)

    if request.GET.get("export", None) == "True":
        name = "get_all_data"
        res = common(data, name)
        return res
    return render(request, "index.html", {"data": data})


# 2] From a given timespan, give me all the data for "Sensor X" over time
def timespan(request):
    sensor_data = db.vesseltripdata.aggregate(
        [
            {"$project": {"_id": 0}},
        ]
    )
    sensor_name = None
    from_time = None
    to_time = None

    if request.GET.get("sensorName"):
        sensor_name = request.GET.get("sensorName")

        sensor_data = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )
    if request.GET.get("from"):
        from_time = request.GET.get("from")

    if request.GET.get("to"):
        to_time = request.GET.get("to")

    print(sensor_name, from_time, to_time)

    if sensor_name and from_time and to_time:
        format = "%Y-%m-%d"
        from_time = datetime.datetime.strptime(from_time, format)
        to_time = datetime.datetime.strptime(to_time, format)
        sensor_data = db.vesseltripdata.aggregate(
            [
                {
                    "$match": {
                        "dateTime": {"$gte": from_time, "$lte": to_time},
                        "sensorName": sensor_name,
                    }
                },
                {"$project": {"_id": 0}},
            ]
        )

    data = list(sensor_data)
    if request.GET.get("done", None) == "True":
        name = "timespan"
        res = common(data, name)
        return res
    return render(request, "info.html", {"data": data})


# 3] From a given trip, give the sum of "Sensor X" throughout the entire trip
def get_sum(request):

    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
    sensor_sum = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id, "sensorName": sensor_name}},
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    "_id": "$sensorName",
                    "index0_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    print(sensor_sum)
    print(type(sensor_sum))
    data = list(sensor_sum)
    print(data)
    if request.GET.get("done", None) == "False":
        name = "get_sum"
        result = common(data, name)
        return result
    return render(request, "get_sum.html", {"data": data})


# 4] From a given trip, give the average of "Sensor X" throughout the entire trip</h2>
def get_avg(request):

    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
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
    print(sensor_avg)
    print(type(sensor_avg))
    data = list(sensor_avg)
    print(data)
    if request.GET.get("done", None) == "True":
        name = "get_avg"
        result = common(data, name)
        return result
    return render(request, "get_avg.html", {"data": data})


# 5] From a given boat, give the average of “Sensor X” for each day between these dates
def get_bs_avg(request):
    sensor_name = "GPS"
    from_time = datetime.now() - timedelta(days=90)
    to_time = datetime.now()
    boatsensor_data = db.vesseltripdata.aggregate(
        [
            {
                "$match": {
                    "dateTime": {"$gte": from_time, "$lte": to_time},
                    "sensorName": sensor_name,
                }
            },
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    "_id": {
                        "day": {"$dayOfMonth": "$dateTime"},
                        "month": {"$month": "$dateTime"},
                        "year": {"$year": "$dateTime"},
                    },
                    "index0_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    print(boatsensor_data)
    print(type(boatsensor_data))
    data = list(boatsensor_data)
    print(data)
    if request.GET.get("export", None) == "True":
        name = "get_bs_avg"
        res = common(data, name)
        return res
    return render(request, "get_bs_avg.html", {"data": data})


# 6] For a given trip, tell me which sensors were available
def get_sensors(request):
    trip_id = "63d4228e01afc1d6b6813e38"
    trip_data = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id}},
            {"$group": {"_id": "$tripId", "sensors": {"$addToSet": "$sensorName"}}},
        ]
    )
    print(trip_data)
    print(type(trip_data))
    data = list(trip_data)
    print(data)
    if request.GET.get("export", None) == "True":
        name = "get_sensors"
        result = common(data, name)
        return result
    # return HttpResponse("hi")
    return render(request, "get_sensors.html", {"data": data})
