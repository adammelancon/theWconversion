# Code is supposed to be circuitpython ready.  THIS WON'T RUN IN REPLIT.  
# I need to get a circuitpython board with wifi to test it out.

# import ssl     # not used yet
import wifi
# import socketpool      # not used yet
import board
import neopixel as strip
import time
import adafruit_requests as requests
# from board import SCL, SDA     # not used yet
import busio
import adafruit_ssd1306

# Input a station id.
STATION_ID = "KIYA"  

url = "https://www.aviationweather.gov/cgi-bin/json/MetarJSON.php?"
arguments = "bbox=-93,29,-91,31&density=all&jsonp="

# Main dictionary to hold station JSON data.
station_wx_dict = {}

UTC_OFFSET = 5
conditions = ""

# Create the I2C interface SCL-4 SDA-5 and initalize display.
i2c = busio.I2C(4, 5)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x31)

# Setup neopixels
pixel_pin = board.D18
pixel_color = ""
LEDOFF = (0, 0, 0)
SUPERCOLD = (0, 0, 100)
COLD = (0, 100, 100)
COOL = (0, 100, 50)
NORMAL = (0, 100, 0)
WARM = (100,0,50)
HOT = (100, 0, 0)
ERROR = (255, 255, 255)  # error state wifi



def wifi_setup():
    # Get wifi details and more from a secrets.py file to hide passwords
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    print("Connecting to %s" % secrets["ssid"])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to %s!" % secrets["ssid"])
    print("My IP address is", wifi.radio.ipv4_address)

    # socket = socketpool.SocketPool(wifi.radio)
    # https = requests.Session(socket, ssl.create_default_context())



def get_json(site, args):
    # TODO - elif not 200 response turn LEDs red
    '''Takes the site url, and url arguments and retrieves bulk METAR JSON data'''
    response = requests.get(site + args)
    if response.status_code == 200 and 'application/json' in response.headers.get(
            'Content-Type', ''):
        return response.json()
    



def get_wxstation_to_dict(stn_id):
    ''' 
    Takes SATION_ID as input.  Finds JSON index id for matching STATION_ID. 
    Then takes the dictionary at that index and saves it into "station_wx_dict" 
    '''
    global station_wx_dict
    station_id_index = 0

    for index in range(len(data_items)):
        for x in data_items[index]['properties']:
            if data_items[index]['properties'][x] == stn_id:
                station_id_index = int(index)

    
    station_wx_dict = data_items[station_id_index]['properties']




# Setup and enable wifi.
wifi_setup()

# Puts all JSON in a dictionary.
data = get_json(url, arguments)
# Where key:value data for all METAR stations will live.
data_items = data['features']

# Main script to get STATION_ID key:value pairs into 'station_wx_dict'.
get_wxstation_to_dict(STATION_ID)




def led_brightness_time():
    # TODO - figure out actual circpy code for neopixels
    ''' Sets LED brightness based on the time of day'''

    time_of_day = int(station_wx_dict['obsTime'][-9:-7]) - UTC_OFFSET

    if time_of_day <= 9:
        #strip.setBrightness(5)
        pass
    else:
        #strip.setBrightness(64)
        pass    



led_brightness_time()


def set_color_based_on_temp():
    '''
    Gets tmep from JSON and uses to assign LED color.
    '''
    global pixel_color
    temp = int(station_wx_dict['temp'])
    if temp < 4:
        pixel_color =  SUPERCOLD
    elif temp < 15:
        pixel_color = COLD
    elif temp < 18:
        pixel_color = COOL
    elif temp < 29:
        pixel_color = NORMAL
    elif temp <= 32:
        pixel_color = WARM
    elif temp > 32:
        pixel_color = HOT

set_color_based_on_temp()




def get_conditions():
    '''
    Gets conditions from JSON and assigns the 'conditions' global variable.
    '''
    global conditions
    current_cond = station_wx_dict['cover']
    if current_cond == "RA":
        conditions = "RAIN"
    elif current_cond == "DZ":
        conditions = "DRIZZLE"
    elif current_cond == "CLR":
        conditions = "CLEAR"
    elif current_cond == "FG":
        conditions = "FOGGY"
    elif current_cond == "OVC":
        conditions = "OVERCAST"
    elif current_cond == "SCT":
        conditions = "SCATTERED"
    # Added this line because I see it today in the METAR but it wasn't in your code.
    elif current_cond == "BKN":
        conditions = "SCATTERED"

get_conditions()




def rain_pattern(raterain):
    # TODO - figure out actual circpy code for neopixels
    '''
    Accepts the rate of the rain pattern and makes the LEDs display a rain like pattern
    '''
    phys_rain_pattern_layout = [7, 8, 15, 16, 5, 11, 12, 17, 6, 9, 14, 16, 6, 10, 13, 17]
    for x in range(0, 6):
        strip.setPixelColor(x, COOL)
        pass
    for x in range(0, 450):
        for i in range(0,7):
            if i == 0:
                strip.setPixelColor(phys_rain_pattern_layout[14], LEDOFF)
                strip.setPixelColor(phys_rain_pattern_layout[15], LEDOFF)
                strip.setPixelColor(phys_rain_pattern_layout[i], pixel_color);
                strip.setPixelColor(phys_rain_pattern_layout[i-1], 0)
                strip.show()
                time.sleep(raterain)
                pass


# TODO - finish these functions
def overcast_day():
    pass

def foggy_day():
    pass

def scattered_day():
    pass

def clear_day():
    pass





def led_based_on_wx(cond): 
    # TODO - Finish the other functions.
    '''
    Takes in global coditions variable and sets the LED pattern/color. Examples:
    RAIN, DRIZZLE, OVERCAST, FOGGY, SCATTERED, CLEAR, UNSET 
    ''' 
    if cond == "RAIN":
      rain_pattern(200)
    elif(cond == "DRIZZLE"):
      rain_pattern(400)
    elif(cond == "OVERCAST"):
        overcast_day()
    elif(cond == "FOGGY"):
        foggy_day()
    elif(cond == "SCATTERED"):
        scattered_day()
    elif(cond == "CLEAR"):
        clear_day()
    elif(cond == "UNSET"):
        clear_day()
        

led_based_on_wx(conditions)


  


''''
TESTING AREA, NOT CODE
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
print("")
print("AREA TO TEST PRINT VARIABLES")
print(
    f"Time of day test: {int(station_wx_dict['obsTime'][-9:-7]) - UTC_OFFSET}")
print("")
print("")
# printing just the raw dictionary data for the STATION_ID we chose
print(
    f"Raw METAR dictionary data from JSON. Dict variable is: 'station_wx_dict'"
)
print(
    "========================================================================")
print("")
print(json.dumps(station_wx_dict, indent=2))
'''