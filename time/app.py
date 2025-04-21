from flask import Flask, request, jsonify
import requests
import os
import time
from datetime import datetime
import pytz

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json"

@app.route("/api/v1/time", methods=["GET"])
def capital_time():
    capital = request.args.get("capital", "Washington, D.C.")
    secret = request.args.get("secret", "secret")
    
    if secret != "secret":
        return jsonify({"error": "Invalid secret"}), 403

    try:
        geocoding_params = {
            "address": capital,
            "key": GOOGLE_API_KEY
        }
        geocoding_response = requests.get(GEOCODING_API_URL, params=geocoding_params).json()
        if geocoding_response["status"] != "OK":
            return jsonify({"error": "Failed to get coordinates for the capital"}), 500
        
        location = geocoding_response["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]

        timezone_params = {
            "location": f"{latitude},{longitude}",
            "timestamp": int(time.time()),
            "key": GOOGLE_API_KEY
        }
        timezone_response = requests.get(TIMEZONE_API_URL, params=timezone_params).json()
        if timezone_response["status"] != "OK":
            return jsonify({"error": "Failed to get timezone information"}), 500

        timezone_info = timezone_response["timeZoneId"]
        
        time_dict = time_at_location(timezone_info)
        
        return jsonify({"capital": capital, "timezone": timezone_info, "local_time": time_dict["time"],
                        "utc_offset":time_dict["utc_offset"]}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def time_at_location(timezone_str):
    try:
        est = pytz.timezone("America/New_York")
        timezone = pytz.timezone(timezone_str)
        loc_dt = est.localize(datetime.now())
        print("loc_dt:", loc_dt)
        timezone_dt = loc_dt.astimezone(timezone)
        print("timezone_dt:", timezone_dt)
        
        return {
            "time": timezone_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": timezone_dt.strftime("%z"),
        }
    except Exception as e:
        return str(e)

app.run(debug=True)