#!/usr/bin/python3

'''
Spring 2024 CTS-233-400 Social Coding Project
 _______          __ __________        __          
 \      \   _____/  |\______   _____ _/  |_________
 /   |   \_/ __ \   __|       _\__  \\   __\___   /
/    |    \  ___/|  | |    |   \/ __ \|  |  /    / 
\____|__  /\___  |__| |____|_  (____  |__| /_____ \
        \/     \/            \/     \/           \/
Josh B., Josh K., Clover L., Drew P., & Evan Y.
Enhancement of graphhopper lab 4.9.2

Change log:
02 Apr 2024:
    included choice between miles/kilometers
    included round trip time/distance
04 Apr 2024
    changed input confirmation to only match first character
    added exit (quit) options to location and distance unit selections
    commented out some of the diagnostic api data
'''

import requests
import urllib.parse

# Global constants
route_url = "https://graphhopper.com/api/1/route?"
key = "7d0c4840-367b-47d5-bf27-748914da9f7d"  # Replace with your Graphhopper API key

# Geocoding API function
def geocoding(location, key):
    while location =="":
        location = input("Enter location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) !=0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        # uncomment for api debugging
        # print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng,new_loc

# Script Start
while True:
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot or quit")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle.lower()[0] == "q":
        print("Quitting... ")
        break
    elif vehicle.lower()[0] == "c":
        vehicle = "car"
    elif vehicle.lower()[0] == "b":
        vehicle = "bike"
    elif vehicle.lower()[0] == "f":
        vehicle = "foot"
    else:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")
    
    loc1 = input("Starting Location: ")
    if loc1.lower == "quit" or loc1.lower == "q":
        print("Quitting... ")
        exit
    
    orig = geocoding(loc1, key)
    loc2 = input("Destination: ")
    
    if loc2.lower == "quit" or loc2.lower =="q":
        print("Quitting... ")
        exit
    
    dest = geocoding(loc2, key)
    print("=================================================")
    
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        # uncomment for API debugging
        #print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            # ask user for distance unit
            distance_choice = input("Display distance in miles or kilometers? (miles/kilometers): ")
            # compare lowercase first letter
            if distance_choice.lower()[0] == "m":
                distance_choice == "miles"
                print("Distance Traveled: {0:.1f} miles".format(miles))
                print("Round Trip Distance: {0:.1f} miles".format(miles * 2))
            elif distance_choice.lower()[0] == "q":
                print("Quitting... ")
                break
            else:
                print("Distance Traveled: {0:.1f} kilometers".format(km))
                print("Round Trip Distance: {0:.1f} kilometers".format(km * 2))

            # Calculate Trip Duration
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            # Calculate Round Trip Duration (duration x 2)
            r_sec = int(paths_data["paths"][0]["time"] / 500 % 60)
            r_min = int(paths_data["paths"][0]["time"] / 500 / 60 % 60)
            r_hr = int(paths_data["paths"][0]["time"] / 500 / 60 / 60)
            print("Round Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(r_hr, r_min, r_sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                if distance_choice == "miles":
                    distance_display = distance / 1000 / 1.61
                    distance_unit = "miles"
                else:
                    distance_display = distance / 1000
                    distance_unit = "kilometers"
                print("{0} ( {1:.1f} {2} )".format(path, distance_display, distance_unit))
            print("=============================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")
         
