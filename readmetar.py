import requests
import json

url = "https://www.aviationweather.gov/cgi-bin/json/MetarJSON.php?"
args = "bbox=-93,29,-91,31&density=all&jsonp="
station_wx_dict = {}
# uncomment one and comment the other to see another station's data!
STATION_ID = "KIYA"
#STATION_ID = "KLFT"



def get_json(site, arguments):
    '''Takes the site url, and url arguments and retrieves METAR JSON data'''
    response = requests.get(url + args)
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type' , ''):
        return response.json()


# puts full JSON into "data" dictionary
data = get_json(url, args)
# gives me a variable to use later that hops down a level to get to the data
data_items = data['features']


def get_wxstation_to_dict():
    ''' Uses the full JSON data to iterate through each station and find the index number for the station that matches the STATION_ID. It then takes the dictionary data for that station and saves it into "station_wx_dict" '''
    # lets me write to the global variable station_wx_dict inside this function
    global station_wx_dict
    station_index = 0

    for index in range(len(data_items)):
        # print(f"Now working on index ', {index}")
        for x in data_items[index]['properties']:
            if data_items[index]['properties'][x] == STATION_ID:
                station_index = int(index)
                # print(f"The station index is: {station_index}")
    
    # station_keys must go here after the index is grabbed by the for loop above.
    station_keys = data_items[station_index]['properties']

    station_wx_dict = station_keys


# This runs the get_wxstation_to_dict function to get just the one station into a dictionary.
get_wxstation_to_dict()

# This is just something pretty I worked up to display the data.
print(f"FORMATTED METAR DATA FOR {STATION_ID}")
print("======================================")
print(f"            Data: {station_wx_dict['data']}")
print(f"      Station ID: {station_wx_dict['id']}")
print(f"        Location: {station_wx_dict['site']}")
print(f"           prior: {station_wx_dict['prior']}")
print(f"Observation Time: {station_wx_dict['obsTime']}")
print(f"            Temp: {station_wx_dict['temp']} C")
print(f"       Dew Point: {station_wx_dict['dewp']} C")
print(f"      Wind Speed: {station_wx_dict['wspd']} kn")
print(f"  Wind Direction: {station_wx_dict['wdir']} deg")
print(f" Max Cloud Cover: {station_wx_dict['cover']}")
print(f"         cldCvg1: {station_wx_dict['cldCvg1']}")
print(f"      Visibility: {station_wx_dict['visib']} mi")
print(f" Flight Category: {station_wx_dict['fltcat']}")
print(f"       Altimeter: {station_wx_dict['altim']} hPa")
print(f"  Raw METAR text: {station_wx_dict['rawOb']}")
print("")
print("")
# printing just the raw dictionary data for the STATION_ID we chose
print(f"Raw METAR dictionary data from JSON. Dict variable is: 'station_wx_dict'")
print("========================================================================")
print("")
print(f"{station_wx_dict}")


     
# THIS BELOW IS JUST SAMPLE DATA FOR ME TO COMPARE WITH

'''
{
    "features": [
        {
            "properties": {
                "bbox": "-93.0000,29.0000,-91.0000,31.0000",
                "beg_time": "1629940701",
                "data": "METAR",
                "end_time": "1629947901",
                "wrap": ""
            },
            "type": "Feature"
        },
        {
            "geometry": {
                "coordinates": [
                    -92.083,
                    29.976
                ],
                "type": "Point"
            },
            "id": "608389884",
            "properties": {
                "altim": 1016.0,
                "cldCvg1": "CLR",
                "cover": "CLR",
                "data": "METAR",
                "dewp": 23.3,
                "fltcat": "VFR",
                "id": "KIYA",
                "obsTime": "2021-08-26T03:15:00Z",
                "prior": 6,
                "rawOb": "KIYA 260315Z AUTO 07003KT 7SM CLR 25/23 A3000 RMK AO2 LTG DSNT W T02510233",
                "site": "Abbeville/Crusta Mem",
                "temp": 25.1,
                "visib": 7.0,
                "wdir": 70,
                "wspd": 3
            },
            "type": "Feature"
        },


{'data': 'METAR', 'id': 'KIYA', 'site': 'Abbeville/Crusta Mem', 'prior': 6, 'obsTime': '2021-08-26T04:55:00Z', 'temp': 25.0, 'dewp': 23.0, 'wspd': 3, 'wdir': 10, 'cover': 'CLR', 'cldCvg1': 'CLR', 'visib': 7.0, 'fltcat': 'VFR', 'altim': 1016.7, 'rawOb': 'KIYA 260455Z AUTO 01003KT 7SM CLR 25/23 A3002 RMK AO2 T02500230'}

'''