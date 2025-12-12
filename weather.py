import requests

def fetch_weather(city="Delhi"):
    city = city.replace(" ", "%20")  # URL encode
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            speak(f"Sorry, I couldn't fetch weather info for {city}. Error {response.status_code}")
            return
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temp}°C with {desc}.")
    except Exception as e:
        print(f"Weather API error: {e}")
        speak("Sorry, I couldn't fetch the weather right now.")
