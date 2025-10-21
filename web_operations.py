import requests
import os
from dotenv import load_dotenv

load_dotenv()

def weather_call(city: str = "Casablanca") -> str: 
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "API key for weather not found"
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q":city, 
        "appid": api_key, 
        "units":"metric",
        # "lang": "ar"
    }
    try :
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            result = {
                "city": data["name"], 
                "weather": data["weather"][0]["description"],
                "temperature" : data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "winds" : data["wind"]["speed"]
            }
            return result
        else :
            return f"Error {response.status_code} - i couldn't get the {city} weather"
    except Exception as e:
        return f"Api failed - Error : {str(e)}"

def Adhan_call(city: str, country: str):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
    response = requests.get(url)
    try : 
        if response.status_code == 200:
            data = response.json()
            return data["data"]["timings"]
        else :
            return f"Error {response.status_code} - {response.text}"
    except Exception as e:
        return f"Api Failed : {str(e)}"

def wikipedia_call(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts", 
        "titles": query,
        "exintro": True,
        "explaintext": True
    }
    headers = {
        "User-Agent": "LangGraphBot/1.0 (contact@example.com)"  
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        for _, v in pages.items():
            return v.get("extract", "No extract found for this topic.")
    else:
        return f"Error {response.status_code} : {response.text}"
